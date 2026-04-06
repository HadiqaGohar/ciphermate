from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.core.session import session_manager
from app.core.token_vault import token_vault_service
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Security scheme for Bearer token
security = HTTPBearer()

class Auth0JWTBearer:
    """Auth0 JWT Bearer token validator with session management"""
    
    def __init__(self):
        self.jwks_client = None
        self._jwks_cache: Optional[Dict[str, Any]] = None
    
    async def get_jwks(self) -> Dict[str, Any]:
        """Get JWKS from Auth0"""
        if self._jwks_cache is None:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(settings.auth0_jwks_url)
                    response.raise_for_status()
                    self._jwks_cache = response.json()
            except Exception as e:
                logger.error(f"Failed to fetch JWKS: {e}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Unable to verify token"
                )
        return self._jwks_cache
    
    def get_rsa_key(self, jwks: Dict[str, Any], kid: str) -> Optional[Dict[str, Any]]:
        """Get RSA key from JWKS"""
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return {
                    "kty": key.get("kty"),
                    "kid": key.get("kid"),
                    "use": key.get("use"),
                    "n": key.get("n"),
                    "e": key.get("e")
                }
        return None
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            # Get unverified header to extract kid
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing kid in header"
                )
            
            # Get JWKS and find the right key
            jwks = await self.get_jwks()
            rsa_key = self.get_rsa_key(jwks, kid)
            
            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find appropriate key"
                )
            
            # Verify and decode the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=settings.AUTH0_ALGORITHMS,
                audience=settings.AUTH0_AUDIENCE,
                issuer=settings.auth0_issuer_url,
            )
            
            return payload
            
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed"
            )
    
    async def refresh_token_if_needed(self, user_id: str, token_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Check if token needs refresh and handle it"""
        try:
            # Check token expiration
            exp = token_payload.get("exp")
            if exp:
                exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)
                now = datetime.now(timezone.utc)
                
                # If token expires in less than 5 minutes, try to refresh
                if (exp_time - now).total_seconds() < 300:
                    logger.info(f"Token for user {user_id} expires soon, attempting refresh")
                    
                    # Try to get refresh token from session or Token Vault
                    session_data = await session_manager.get_user_session(user_id)
                    if session_data and "refresh_token" in session_data.get("user_data", {}):
                        refresh_token = session_data["user_data"]["refresh_token"]
                        
                        # Attempt to refresh the token
                        new_token_data = await self._refresh_auth0_token(refresh_token)
                        if new_token_data:
                            # Update session with new token data
                            await session_manager.update_session(
                                session_data.get("session_id", ""),
                                {"user_data": {**session_data.get("user_data", {}), **new_token_data}}
                            )
                            
                            # Verify the new token and return updated payload
                            new_payload = await self.verify_token(new_token_data["access_token"])
                            return new_payload
            
            return token_payload
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            # Return original payload if refresh fails
            return token_payload
    
    async def _refresh_auth0_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh Auth0 token using refresh token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{settings.AUTH0_DOMAIN}/oauth/token",
                    json={
                        "grant_type": "refresh_token",
                        "client_id": settings.AUTH0_CLIENT_ID,
                        "client_secret": settings.AUTH0_CLIENT_SECRET,
                        "refresh_token": refresh_token
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Token refresh failed with status {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Auth0 token refresh error: {e}")
            return None

# Global instance
auth0_jwt_bearer = Auth0JWTBearer()

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user from JWT token with session management
    """
    token = credentials.credentials
    payload = await auth0_jwt_bearer.verify_token(token)
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    
    # Check for token refresh if needed
    payload = await auth0_jwt_bearer.refresh_token_if_needed(user_id, payload)
    
    # Extract user information from token
    user_info = {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "nickname": payload.get("nickname"),
        "picture": payload.get("picture"),
        "email_verified": payload.get("email_verified", False),
        "permissions": payload.get("permissions", []),
        "scope": payload.get("scope", "").split() if payload.get("scope") else [],
        "exp": payload.get("exp"),
        "iat": payload.get("iat")
    }
    
    # Update or create session
    try:
        session_data = await session_manager.get_user_session(user_id)
        if session_data:
            # Update existing session
            await session_manager.update_session(
                session_data.get("session_id", ""),
                {
                    "user_data": user_info,
                    "ip_address": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent", "")
                }
            )
        else:
            # Create new session
            await session_manager.create_session(
                user_id=user_id,
                user_data={
                    **user_info,
                    "ip_address": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent", "")
                }
            )
    except Exception as e:
        logger.error(f"Session management error: {e}")
        # Continue without session if it fails
    
    return user_info

async def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """
    Optional dependency to get current user (doesn't raise if no token)
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None

class RequirePermissions:
    """Dependency class to require specific permissions"""
    
    def __init__(self, *permissions: str):
        self.required_permissions = set(permissions)
    
    def __call__(self, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_permissions = set(user.get("permissions", []))
        
        if not self.required_permissions.issubset(user_permissions):
            missing_permissions = self.required_permissions - user_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        
        return user

class RequireScope:
    """Dependency class to require specific OAuth scopes"""
    
    def __init__(self, *scopes: str):
        self.required_scopes = set(scopes)
    
    def __call__(self, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_scopes = set(user.get("scope", []))
        
        if not self.required_scopes.issubset(user_scopes):
            missing_scopes = self.required_scopes - user_scopes
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scopes: {', '.join(missing_scopes)}"
            )
        
        return user

# Session management endpoints
async def logout_user(user_id: str) -> bool:
    """Logout user by clearing their session"""
    try:
        session_data = await session_manager.get_user_session(user_id)
        if session_data:
            session_id = session_data.get("session_id", "")
            return await session_manager.delete_session(session_id)
        return True
    except Exception as e:
        logger.error(f"Logout error for user {user_id}: {e}")
        return False

async def get_user_session_info(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user session information"""
    try:
        return await session_manager.get_user_session(user_id)
    except Exception as e:
        logger.error(f"Get session info error for user {user_id}: {e}")
        return None

# Common permission dependencies
require_read = RequirePermissions("read:profile")
require_write = RequirePermissions("write:profile")
require_admin = RequirePermissions("admin:all")

# Common scope dependencies  
require_openid = RequireScope("openid")
require_profile = RequireScope("openid", "profile")
require_email = RequireScope("openid", "profile", "email")