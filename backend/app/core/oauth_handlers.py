"""OAuth flow handlers for third-party services"""

from typing import Dict, Any, List, Optional, Tuple
import httpx
import secrets
import urllib.parse
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.core.token_vault import token_vault_service, TokenVaultError
from app.models.service_connection import ServiceConnection
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


class OAuthError(Exception):
    """Base exception for OAuth operations"""
    pass

    # // done hadiqa

class InvalidStateError(OAuthError):
    """Raised when OAuth state parameter is invalid"""
    pass


class AuthorizationError(OAuthError):
    """Raised when OAuth authorization fails"""
    pass


class TokenExchangeError(OAuthError):
    """Raised when OAuth token exchange fails"""
    pass


class OAuthHandler:
    """Base OAuth handler with common functionality"""
    
    def __init__(self, service_name: str, client_id: str, client_secret: str):
        self.service_name = service_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = f"{settings.APP_BASE_URL}/api/v1/permissions/callback/{service_name}"
    
    def generate_state(self, user_id: str) -> str:
        """Generate secure state parameter for OAuth flow"""
        random_part = secrets.token_urlsafe(32)
        return f"{user_id}:{random_part}"
    
    def validate_state(self, state: str, expected_user_id: str) -> bool:
        """Validate OAuth state parameter"""
        try:
            user_id, _ = state.split(":", 1)
            return user_id == expected_user_id
        except ValueError:
            return False
    
    async def get_authorization_url(self, user_id: str, scopes: List[str]) -> Tuple[str, str]:
        """Get authorization URL and state for OAuth flow"""
        raise NotImplementedError("Subclasses must implement get_authorization_url")
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        raise NotImplementedError("Subclasses must implement exchange_code_for_token")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information using access token"""
        raise NotImplementedError("Subclasses must implement get_user_info")


class GoogleOAuthHandler(OAuthHandler):
    """Google OAuth 2.0 handler"""
    
    def __init__(self):
        super().__init__(
            service_name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET
        )
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    async def get_authorization_url(self, user_id: str, scopes: List[str]) -> Tuple[str, str]:
        """Get Google OAuth authorization URL"""
        state = self.generate_state(user_id)
        scope_string = " ".join(scopes)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope_string,
            "response_type": "code",
            "state": state,
            "access_type": "offline",  # Request refresh token
            "prompt": "consent"  # Force consent screen to get refresh token
        }
        
        auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
        return auth_url, state
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange Google authorization code for tokens"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": self.redirect_uri
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code == 400:
                    error_data = response.json()
                    raise TokenExchangeError(f"Google token exchange failed: {error_data.get('error_description', 'Invalid request')}")
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise TokenExchangeError("Google token exchange timed out")
        except httpx.HTTPStatusError as e:
            raise TokenExchangeError(f"Google token exchange failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Google token exchange error: {e}")
            raise TokenExchangeError(f"Google token exchange error: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Google user information"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise OAuthError("Google user info request timed out")
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"Google user info request failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Google user info error: {e}")
            raise OAuthError(f"Google user info error: {str(e)}")


class GitHubOAuthHandler(OAuthHandler):
    """GitHub OAuth handler"""
    
    def __init__(self):
        super().__init__(
            service_name="github",
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET
        )
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_info_url = "https://api.github.com/user"
    
    async def get_authorization_url(self, user_id: str, scopes: List[str]) -> Tuple[str, str]:
        """Get GitHub OAuth authorization URL"""
        state = self.generate_state(user_id)
        scope_string = " ".join(scopes)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope_string,
            "state": state,
            "allow_signup": "true"
        }
        
        auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
        return auth_url, state
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange GitHub authorization code for token"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                        "state": state
                    },
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code == 400:
                    error_data = response.json()
                    raise TokenExchangeError(f"GitHub token exchange failed: {error_data.get('error_description', 'Invalid request')}")
                
                response.raise_for_status()
                token_data = response.json()
                
                # GitHub returns different error format
                if "error" in token_data:
                    raise TokenExchangeError(f"GitHub token exchange failed: {token_data['error_description']}")
                
                return token_data
                
        except httpx.TimeoutException:
            raise TokenExchangeError("GitHub token exchange timed out")
        except httpx.HTTPStatusError as e:
            raise TokenExchangeError(f"GitHub token exchange failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"GitHub token exchange error: {e}")
            raise TokenExchangeError(f"GitHub token exchange error: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get GitHub user information"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.user_info_url,
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise OAuthError("GitHub user info request timed out")
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"GitHub user info request failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"GitHub user info error: {e}")
            raise OAuthError(f"GitHub user info error: {str(e)}")


class SlackOAuthHandler(OAuthHandler):
    """Slack OAuth handler"""
    
    def __init__(self):
        super().__init__(
            service_name="slack",
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET
        )
        self.auth_url = "https://slack.com/oauth/v2/authorize"
        self.token_url = "https://slack.com/api/oauth.v2.access"
        self.user_info_url = "https://slack.com/api/users.identity"
    
    async def get_authorization_url(self, user_id: str, scopes: List[str]) -> Tuple[str, str]:
        """Get Slack OAuth authorization URL"""
        state = self.generate_state(user_id)
        scope_string = ",".join(scopes)  # Slack uses comma-separated scopes
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope_string,
            "state": state,
            "user_scope": "identity.basic,identity.email"  # Basic user scopes
        }
        
        auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
        return auth_url, state
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange Slack authorization code for token"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                response.raise_for_status()
                token_data = response.json()
                
                # Slack returns ok: false on error
                if not token_data.get("ok", False):
                    raise TokenExchangeError(f"Slack token exchange failed: {token_data.get('error', 'Unknown error')}")
                
                return token_data
                
        except httpx.TimeoutException:
            raise TokenExchangeError("Slack token exchange timed out")
        except httpx.HTTPStatusError as e:
            raise TokenExchangeError(f"Slack token exchange failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Slack token exchange error: {e}")
            raise TokenExchangeError(f"Slack token exchange error: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Slack user information"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                response.raise_for_status()
                user_data = response.json()
                
                if not user_data.get("ok", False):
                    raise OAuthError(f"Slack user info failed: {user_data.get('error', 'Unknown error')}")
                
                return user_data.get("user", {})
                
        except httpx.TimeoutException:
            raise OAuthError("Slack user info request timed out")
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"Slack user info request failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Slack user info error: {e}")
            raise OAuthError(f"Slack user info error: {str(e)}")


class OAuthService:
    """Service for managing OAuth flows across different providers"""
    
    def __init__(self):
        self.handlers = {
            "google": GoogleOAuthHandler(),
            "github": GitHubOAuthHandler(),
            "slack": SlackOAuthHandler()
        }
        
        # Default scopes for each service
        self.default_scopes = {
            "google": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/calendar",
                "https://www.googleapis.com/auth/gmail.readonly"
            ],
            "github": [
                "user:email",
                "repo",
                "read:user"
            ],
            "slack": [
                "channels:read",
                "chat:write",
                "users:read"
            ]
        }
    
    def get_handler(self, service_name: str) -> OAuthHandler:
        """Get OAuth handler for service"""
        handler = self.handlers.get(service_name.lower())
        if not handler:
            raise ValueError(f"Unsupported service: {service_name}")
        return handler
    
    def get_default_scopes(self, service_name: str) -> List[str]:
        """Get default scopes for service"""
        return self.default_scopes.get(service_name.lower(), [])
    
    async def initiate_oauth_flow(
        self, 
        user_id: str, 
        service_name: str, 
        custom_scopes: Optional[List[str]] = None
    ) -> Tuple[str, str]:
        """Initiate OAuth flow for a service"""
        handler = self.get_handler(service_name)
        scopes = custom_scopes or self.default_scopes.get(service_name.lower(), [])
        
        if not scopes:
            raise ValueError(f"No scopes defined for service: {service_name}")
        
        auth_url, state = await handler.get_authorization_url(user_id, scopes)
        
        logger.info(f"OAuth flow initiated for user {user_id}, service {service_name}")
        return auth_url, state
    
    async def handle_oauth_callback(
        self, 
        service_name: str, 
        code: str, 
        state: str, 
        expected_user_id: str
    ) -> Dict[str, Any]:
        """Handle OAuth callback and complete token exchange"""
        handler = self.get_handler(service_name)
        
        # Validate state parameter
        if not handler.validate_state(state, expected_user_id):
            raise InvalidStateError("Invalid state parameter")
        
        # Exchange code for token
        token_data = await handler.exchange_code_for_token(code, state)
        
        # Get user info to verify the connection
        access_token = token_data.get("access_token")
        if not access_token:
            raise TokenExchangeError("No access token received")
        
        user_info = await handler.get_user_info(access_token)
        
        # Calculate token expiration
        expires_at = None
        if "expires_in" in token_data:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"])
        
        # Store token in Token Vault
        scopes = self._extract_scopes_from_token(service_name, token_data)
        vault_id = await token_vault_service.store_token(
            user_id=expected_user_id,
            service_name=service_name,
            token_data=token_data,
            scopes=scopes,
            expires_at=expires_at
        )
        
        logger.info(f"OAuth flow completed for user {expected_user_id}, service {service_name}")
        
        return {
            "service": service_name,
            "user_info": user_info,
            "scopes": scopes,
            "vault_id": vault_id,
            "expires_at": expires_at.isoformat() if expires_at else None
        }
    
    def _extract_scopes_from_token(self, service_name: str, token_data: Dict[str, Any]) -> List[str]:
        """Extract scopes from token response"""
        scope_string = token_data.get("scope", "")
        
        if service_name.lower() == "slack":
            # Slack returns comma-separated scopes
            return [s.strip() for s in scope_string.split(",") if s.strip()]
        else:
            # Google and GitHub return space-separated scopes
            return [s.strip() for s in scope_string.split(" ") if s.strip()]
    
    async def revoke_service_permission(self, user_id: str, service_name: str) -> bool:
        """Revoke permission for a service"""
        try:
            # Revoke token from Token Vault
            success = await token_vault_service.revoke_token(user_id, service_name)
            
            if success:
                logger.info(f"Permission revoked for user {user_id}, service {service_name}")
            else:
                logger.warning(f"Failed to revoke permission for user {user_id}, service {service_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error revoking permission: {e}")
            raise OAuthError(f"Failed to revoke permission: {str(e)}")
    
    async def get_user_permissions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all permissions for a user"""
        try:
            tokens = await token_vault_service.list_tokens(user_id, include_inactive=False)
            
            permissions = []
            for token in tokens:
                permissions.append({
                    "service": token["service"],
                    "scopes": token["scopes"],
                    "status": token["status"],
                    "created_at": token["created_at"],
                    "last_used_at": token["last_used_at"],
                    "expires_at": token["expires_at"]
                })
            
            return permissions
            
        except Exception as e:
            logger.error(f"Error getting user permissions: {e}")
            raise OAuthError(f"Failed to get user permissions: {str(e)}")


# Global OAuth service instance
oauth_service = OAuthService()