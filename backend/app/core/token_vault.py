from typing import Optional, List, Dict, Any, Union
import httpx
import json
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.models.service_connection import ServiceConnection
from app.core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)


class TokenVaultError(Exception):
    """Base exception for Token Vault operations"""
    pass


class TokenNotFoundError(TokenVaultError):
    """Raised when a token is not found in the vault"""
    pass


class TokenExpiredError(TokenVaultError):
    """Raised when a token has expired and cannot be refreshed"""
    pass


class AuthenticationError(TokenVaultError):
    """Raised when Auth0 authentication fails"""
    pass


class ServiceError(TokenVaultError):
    """Raised when external service operations fail"""
    pass


class TokenStatus(Enum):
    """Token status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    REFRESH_FAILED = "refresh_failed"


class TokenVaultService:
    """Auth0 Token Vault integration service with comprehensive error handling"""
    
    def __init__(self):
        self.management_api_url = f"https://{settings.AUTH0_DOMAIN}/api/v2"
        self.token_vault_url = f"{self.management_api_url}/users"
        self._management_token_cache = None
        self._management_token_expires = None
        self._max_retries = 3
        self._retry_delay = 1.0  # seconds
    
    async def _get_management_token_with_retry(self) -> str:
        """Get Auth0 Management API token with retry logic"""
        for attempt in range(self._max_retries):
            try:
                return await self._get_management_token()
            except Exception as e:
                if attempt == self._max_retries - 1:
                    logger.error(f"Failed to get management token after {self._max_retries} attempts: {e}")
                    raise AuthenticationError(f"Unable to authenticate with Auth0: {str(e)}")
                
                logger.warning(f"Management token attempt {attempt + 1} failed: {e}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))  # Exponential backoff
        
        raise AuthenticationError("Maximum retry attempts exceeded")
    
    async def _get_management_token(self) -> str:
        """Get Auth0 Management API token with caching"""
        # Check if cached token is still valid
        if (self._management_token_cache and 
            self._management_token_expires and 
            datetime.now(timezone.utc) < self._management_token_expires):
            return self._management_token_cache
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://{settings.AUTH0_DOMAIN}/oauth/token",
                    json={
                        "client_id": settings.AUTH0_CLIENT_ID,
                        "client_secret": settings.AUTH0_CLIENT_SECRET,
                        "audience": f"https://{settings.AUTH0_DOMAIN}/api/v2/",
                        "grant_type": "client_credentials"
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Invalid Auth0 credentials")
                elif response.status_code == 403:
                    raise AuthenticationError("Insufficient permissions for Auth0 Management API")
                
                response.raise_for_status()
                data = response.json()
                
                # Cache the token with expiration
                self._management_token_cache = data["access_token"]
                expires_in = data.get("expires_in", 3600)  # Default 1 hour
                self._management_token_expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 300)  # 5 min buffer
                
                return self._management_token_cache
                
        except httpx.TimeoutException:
            raise AuthenticationError("Auth0 authentication request timed out")
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(f"Auth0 authentication failed: HTTP {e.response.status_code}")
        except Exception as e:
            raise AuthenticationError(f"Auth0 authentication error: {str(e)}")
    
    async def get_management_token(self) -> str:
        """Public method to get management token (for backward compatibility)"""
        return await self._get_management_token_with_retry()
    
    async def store_token(
        self,
        user_id: str,
        service_name: str,
        token_data: Dict[str, Any],
        scopes: List[str],
        expires_at: Optional[datetime] = None
    ) -> str:
        """Store token in Auth0 Token Vault with comprehensive error handling"""
        if not user_id or not service_name or not token_data:
            raise ValueError("user_id, service_name, and token_data are required")
        
        try:
            management_token = await self._get_management_token_with_retry()
            
            # Prepare vault data with enhanced metadata
            vault_data = {
                "service": service_name,
                "token": token_data,
                "scopes": scopes,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": expires_at.isoformat() if expires_at else None,
                "metadata": {
                    "user_id": user_id,
                    "service_name": service_name,
                    "token_type": token_data.get("token_type", "Bearer"),
                    "scope_count": len(scopes)
                }
            }
            
            # Store in Auth0 Token Vault with retry logic
            vault_id = await self._store_in_vault_with_retry(
                user_id, vault_data, management_token
            )
            
            # Store reference in local database
            await self._store_local_reference(
                user_id, service_name, vault_id, scopes, expires_at, vault_data
            )
            
            logger.info(f"Token stored successfully for user {user_id}, service {service_name}")
            return vault_id
                
        except TokenVaultError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error storing token: {e}")
            raise TokenVaultError(f"Token storage failed: {str(e)}")
    
    async def _store_in_vault_with_retry(
        self, user_id: str, vault_data: Dict[str, Any], management_token: str
    ) -> str:
        """Store token in Auth0 vault with retry logic"""
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.token_vault_url}/{user_id}/token-vault",
                        headers={
                            "Authorization": f"Bearer {management_token}",
                            "Content-Type": "application/json"
                        },
                        json=vault_data
                    )
                    
                    if response.status_code == 401:
                        # Token might be expired, refresh and retry
                        self._management_token_cache = None
                        management_token = await self._get_management_token_with_retry()
                        continue
                    elif response.status_code == 404:
                        raise TokenVaultError(f"User {user_id} not found in Auth0")
                    elif response.status_code == 409:
                        raise TokenVaultError(f"Token already exists for service {vault_data['service']}")
                    
                    response.raise_for_status()
                    result = response.json()
                    return result.get("id", "")
                    
            except httpx.TimeoutException:
                if attempt == self._max_retries - 1:
                    raise TokenVaultError("Token Vault request timed out")
                logger.warning(f"Vault storage timeout, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
            except httpx.HTTPStatusError as e:
                if attempt == self._max_retries - 1:
                    raise TokenVaultError(f"Token Vault HTTP error: {e.response.status_code}")
                logger.warning(f"Vault storage HTTP error, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
        
        raise TokenVaultError("Maximum retry attempts exceeded for vault storage")
    
    async def _store_local_reference(
        self, user_id: str, service_name: str, vault_id: str, 
        scopes: List[str], expires_at: Optional[datetime], vault_data: Dict[str, Any]
    ) -> None:
        """Store local database reference"""
        try:
            async with AsyncSessionLocal() as db:
                # Check if connection already exists and deactivate it
                existing = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.user_id == user_id,
                        ServiceConnection.service_name == service_name,
                        ServiceConnection.is_active == True
                    )
                )
                existing_conn = existing.scalar_one_or_none()
                if existing_conn:
                    existing_conn.is_active = False
                
                # Create new connection
                connection = ServiceConnection(
                    user_id=user_id,
                    service_name=service_name,
                    token_vault_id=vault_id,
                    scopes=scopes,
                    is_active=True,
                    created_at=datetime.now(timezone.utc),
                    expires_at=expires_at,
                    metadata_json={"vault_data": vault_data}
                )
                db.add(connection)
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to store local reference: {e}")
            # Don't raise here as the token is already in the vault
            # This is a non-critical failure
    
    async def retrieve_token(
        self,
        user_id: str,
        service_name: str,
        auto_refresh: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Retrieve token from Auth0 Token Vault with automatic refresh"""
        if not user_id or not service_name:
            raise ValueError("user_id and service_name are required")
        
        try:
            # Get token vault ID from local database
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.user_id == user_id,
                        ServiceConnection.service_name == service_name,
                        ServiceConnection.is_active == True
                    )
                )
                connection = result.scalar_one_or_none()
                
                if not connection:
                    logger.info(f"No active connection found for user {user_id}, service {service_name}")
                    return None
                
                # Check if token is expired
                if connection.expires_at and connection.expires_at <= datetime.now(timezone.utc):
                    if auto_refresh:
                        logger.info(f"Token expired for {service_name}, attempting refresh...")
                        refreshed_token = await self._attempt_token_refresh(connection)
                        if refreshed_token:
                            return refreshed_token
                    
                    logger.warning(f"Token expired and refresh failed for {service_name}")
                    raise TokenExpiredError(f"Token expired for service {service_name}")
                
                # Retrieve from vault
                token_data = await self._retrieve_from_vault_with_retry(
                    user_id, connection.token_vault_id
                )
                
                if token_data:
                    # Update last used timestamp
                    connection.last_used_at = datetime.now(timezone.utc)
                    await db.commit()
                    
                    logger.info(f"Token retrieved successfully for user {user_id}, service {service_name}")
                    return token_data
                else:
                    # Token not found in vault, mark as inactive
                    connection.is_active = False
                    await db.commit()
                    raise TokenNotFoundError(f"Token not found in vault for service {service_name}")
                    
        except (TokenVaultError, ValueError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving token: {e}")
            raise TokenVaultError(f"Token retrieval failed: {str(e)}")
    
    async def _retrieve_from_vault_with_retry(
        self, user_id: str, vault_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve token from Auth0 vault with retry logic"""
        management_token = await self._get_management_token_with_retry()
        
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(
                        f"{self.token_vault_url}/{user_id}/token-vault/{vault_id}",
                        headers={
                            "Authorization": f"Bearer {management_token}"
                        }
                    )
                    
                    if response.status_code == 401:
                        # Token might be expired, refresh and retry
                        self._management_token_cache = None
                        management_token = await self._get_management_token_with_retry()
                        continue
                    elif response.status_code == 404:
                        return None  # Token not found
                    
                    response.raise_for_status()
                    vault_data = response.json()
                    return vault_data.get("token")
                    
            except httpx.TimeoutException:
                if attempt == self._max_retries - 1:
                    raise TokenVaultError("Token Vault retrieval timed out")
                logger.warning(f"Vault retrieval timeout, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                if attempt == self._max_retries - 1:
                    raise TokenVaultError(f"Token Vault HTTP error: {e.response.status_code}")
                logger.warning(f"Vault retrieval HTTP error, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
        
        raise TokenVaultError("Maximum retry attempts exceeded for vault retrieval")
    
    async def revoke_token(
        self,
        user_id: str,
        service_name: str
    ) -> bool:
        """Revoke token from Auth0 Token Vault with comprehensive cleanup"""
        if not user_id or not service_name:
            raise ValueError("user_id and service_name are required")
        
        try:
            # Get token vault ID from local database
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.user_id == user_id,
                        ServiceConnection.service_name == service_name,
                        ServiceConnection.is_active == True
                    )
                )
                connection = result.scalar_one_or_none()
                
                if not connection:
                    logger.info(f"No active connection found for user {user_id}, service {service_name}")
                    return False
                
                # Revoke from Auth0 Token Vault
                vault_success = await self._revoke_from_vault_with_retry(
                    user_id, connection.token_vault_id
                )
                
                # Mark as inactive in local database regardless of vault response
                connection.is_active = False
                connection.last_used_at = datetime.now(timezone.utc)
                await db.commit()
                
                logger.info(f"Token revoked for user {user_id}, service {service_name}")
                return vault_success
                    
        except (TokenVaultError, ValueError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error revoking token: {e}")
            raise TokenVaultError(f"Token revocation failed: {str(e)}")
    
    async def _revoke_from_vault_with_retry(
        self, user_id: str, vault_id: str
    ) -> bool:
        """Revoke token from Auth0 vault with retry logic"""
        management_token = await self._get_management_token_with_retry()
        
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.delete(
                        f"{self.token_vault_url}/{user_id}/token-vault/{vault_id}",
                        headers={
                            "Authorization": f"Bearer {management_token}"
                        }
                    )
                    
                    if response.status_code == 401:
                        # Token might be expired, refresh and retry
                        self._management_token_cache = None
                        management_token = await self._get_management_token_with_retry()
                        continue
                    
                    # Consider success if 200, 204, or 404 (already deleted)
                    return response.status_code in [200, 204, 404]
                    
            except httpx.TimeoutException:
                if attempt == self._max_retries - 1:
                    logger.warning("Token Vault revocation timed out, but local cleanup completed")
                    return False
                logger.warning(f"Vault revocation timeout, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code in [404, 410]:  # Not found or gone
                    return True
                if attempt == self._max_retries - 1:
                    logger.warning(f"Token Vault revocation failed: HTTP {e.response.status_code}")
                    return False
                logger.warning(f"Vault revocation HTTP error, attempt {attempt + 1}, retrying...")
                await asyncio.sleep(self._retry_delay * (2 ** attempt))
        
        logger.warning("Maximum retry attempts exceeded for vault revocation")
        return False
    
    async def list_tokens(
        self,
        user_id: str,
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """List all tokens for a user with enhanced metadata"""
        if not user_id:
            raise ValueError("user_id is required")
        
        try:
            async with AsyncSessionLocal() as db:
                query = select(ServiceConnection).where(
                    ServiceConnection.user_id == user_id
                )
                
                if not include_inactive:
                    query = query.where(ServiceConnection.is_active == True)
                
                result = await db.execute(query)
                connections = result.scalars().all()
                
                token_list = []
                for conn in connections:
                    token_info = {
                        "service": conn.service_name,
                        "scopes": conn.scopes or [],
                        "created_at": conn.created_at.isoformat() if conn.created_at else None,
                        "last_used_at": conn.last_used_at.isoformat() if conn.last_used_at else None,
                        "expires_at": conn.expires_at.isoformat() if conn.expires_at else None,
                        "token_vault_id": conn.token_vault_id,
                        "is_active": conn.is_active,
                        "status": self._get_token_status(conn)
                    }
                    token_list.append(token_info)
                
                logger.info(f"Listed {len(token_list)} tokens for user {user_id}")
                return token_list
                
        except Exception as e:
            logger.error(f"Failed to list tokens: {e}")
            raise TokenVaultError(f"Token listing failed: {str(e)}")
    
    def _get_token_status(self, connection: ServiceConnection) -> str:
        """Determine token status based on connection data"""
        if not connection.is_active:
            return TokenStatus.REVOKED.value
        
        if connection.expires_at and connection.expires_at <= datetime.now(timezone.utc):
            return TokenStatus.EXPIRED.value
        
        return TokenStatus.ACTIVE.value
    
    async def refresh_token(
        self,
        user_id: str,
        service_name: str,
        refresh_token: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Refresh an expired token with enhanced service-specific logic"""
        if not user_id or not service_name:
            raise ValueError("user_id and service_name are required")
        
        try:
            # Get current token data if refresh_token not provided
            if not refresh_token:
                current_token = await self.retrieve_token(user_id, service_name, auto_refresh=False)
                if not current_token:
                    raise TokenNotFoundError(f"No token found for service {service_name}")
                refresh_token = current_token.get("refresh_token")
            
            if not refresh_token:
                logger.warning(f"No refresh token available for {service_name}")
                return None
            
            # Service-specific refresh logic
            new_token_data = await self._refresh_service_token(service_name, refresh_token)
            
            if new_token_data:
                # Calculate expiration time
                expires_at = None
                if "expires_in" in new_token_data:
                    expires_at = datetime.now(timezone.utc) + timedelta(seconds=new_token_data["expires_in"])
                
                # Store the refreshed token
                await self._update_stored_token(user_id, service_name, new_token_data, expires_at)
                
                logger.info(f"Token refreshed successfully for user {user_id}, service {service_name}")
                return new_token_data
            
            return None
            
        except (TokenVaultError, ValueError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error refreshing token: {e}")
            raise TokenVaultError(f"Token refresh failed: {str(e)}")
    
    async def _attempt_token_refresh(self, connection: ServiceConnection) -> Optional[Dict[str, Any]]:
        """Attempt to refresh a token for an expired connection"""
        try:
            # Get current token data to extract refresh token
            current_token = await self._retrieve_from_vault_with_retry(
                connection.user_id, connection.token_vault_id
            )
            
            if not current_token or not current_token.get("refresh_token"):
                return None
            
            return await self.refresh_token(
                connection.user_id,
                connection.service_name,
                current_token["refresh_token"]
            )
        except Exception as e:
            logger.error(f"Token refresh attempt failed: {e}")
            return None
    
    async def _refresh_service_token(self, service_name: str, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh token using service-specific logic"""
        service_lower = service_name.lower()
        
        if service_lower.startswith("google"):
            return await self._refresh_google_token(refresh_token)
        elif service_lower.startswith("github"):
            return await self._refresh_github_token(refresh_token)
        elif service_lower.startswith("slack"):
            return await self._refresh_slack_token(refresh_token)
        else:
            logger.warning(f"No refresh logic implemented for service: {service_name}")
            return None
    
    async def _update_stored_token(
        self, user_id: str, service_name: str, token_data: Dict[str, Any], expires_at: Optional[datetime]
    ) -> None:
        """Update stored token with new data"""
        # Get current scopes from database
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ServiceConnection).where(
                    ServiceConnection.user_id == user_id,
                    ServiceConnection.service_name == service_name,
                    ServiceConnection.is_active == True
                )
            )
            connection = result.scalar_one_or_none()
            
            if connection:
                scopes = connection.scopes or []
                # Store new token (this will deactivate the old one)
                await self.store_token(user_id, service_name, token_data, scopes, expires_at)
    
    async def _refresh_google_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh Google OAuth token with enhanced error handling"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token"
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code == 400:
                    error_data = response.json()
                    if error_data.get("error") == "invalid_grant":
                        raise TokenExpiredError("Google refresh token is invalid or expired")
                
                response.raise_for_status()
                token_data = response.json()
                
                # Google doesn't always return a new refresh token
                if "refresh_token" not in token_data:
                    token_data["refresh_token"] = refresh_token
                
                return token_data
                
        except TokenExpiredError:
            raise
        except httpx.TimeoutException:
            raise ServiceError("Google token refresh timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(f"Google token refresh failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Google token refresh failed: {e}")
            raise ServiceError(f"Google token refresh error: {str(e)}")
    
    async def _refresh_github_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Validate GitHub token (GitHub tokens don't typically expire)"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
                
                if response.status_code == 401:
                    raise TokenExpiredError("GitHub token is invalid or revoked")
                
                response.raise_for_status()
                
                # Return the same token if valid
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "scope": "repo,user"  # Default scopes, should be stored properly
                }
                
        except TokenExpiredError:
            raise
        except httpx.TimeoutException:
            raise ServiceError("GitHub token validation timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(f"GitHub token validation failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"GitHub token validation failed: {e}")
            raise ServiceError(f"GitHub token validation error: {str(e)}")
    
    async def _refresh_slack_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh Slack OAuth token with enhanced error handling"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://slack.com/api/oauth.v2.access",
                    data={
                        "client_id": settings.SLACK_CLIENT_ID,
                        "client_secret": settings.SLACK_CLIENT_SECRET,
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token"
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                response.raise_for_status()
                data = response.json()
                
                if not data.get("ok"):
                    error = data.get("error", "unknown_error")
                    if error == "invalid_refresh_token":
                        raise TokenExpiredError("Slack refresh token is invalid or expired")
                    raise ServiceError(f"Slack API error: {error}")
                
                return {
                    "access_token": data.get("access_token"),
                    "refresh_token": data.get("refresh_token", refresh_token),
                    "token_type": "bearer",
                    "scope": data.get("scope", ""),
                    "expires_in": data.get("expires_in")
                }
                
        except TokenExpiredError:
            raise
        except httpx.TimeoutException:
            raise ServiceError("Slack token refresh timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(f"Slack token refresh failed: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Slack token refresh failed: {e}")
            raise ServiceError(f"Slack token refresh error: {str(e)}")
    
    async def get_token_status(self, user_id: str, service_name: str) -> Dict[str, Any]:
        """Get comprehensive token status information"""
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.user_id == user_id,
                        ServiceConnection.service_name == service_name,
                        ServiceConnection.is_active == True
                    )
                )
                connection = result.scalar_one_or_none()
                
                if not connection:
                    return {
                        "exists": False,
                        "status": "not_found",
                        "message": "No token found for this service"
                    }
                
                status = self._get_token_status(connection)
                
                return {
                    "exists": True,
                    "status": status,
                    "service": service_name,
                    "scopes": connection.scopes or [],
                    "created_at": connection.created_at.isoformat() if connection.created_at else None,
                    "expires_at": connection.expires_at.isoformat() if connection.expires_at else None,
                    "last_used_at": connection.last_used_at.isoformat() if connection.last_used_at else None,
                    "can_refresh": status == TokenStatus.EXPIRED.value
                }
                
        except Exception as e:
            logger.error(f"Failed to get token status: {e}")
            return {
                "exists": False,
                "status": "error",
                "message": f"Error checking token status: {str(e)}"
            }
    
    async def cleanup_expired_tokens(self, days_old: int = 30) -> int:
        """Clean up expired and inactive tokens older than specified days"""
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
            
            async with AsyncSessionLocal() as db:
                # Find expired connections to clean up
                result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.is_active == False,
                        ServiceConnection.created_at < cutoff_date
                    )
                )
                expired_connections = result.scalars().all()
                
                cleaned_count = 0
                for connection in expired_connections:
                    try:
                        # Try to remove from vault (best effort)
                        await self._revoke_from_vault_with_retry(
                            connection.user_id, connection.token_vault_id
                        )
                        
                        # Remove from local database
                        await db.delete(connection)
                        cleaned_count += 1
                        
                    except Exception as e:
                        logger.warning(f"Failed to cleanup connection {connection.id}: {e}")
                
                await db.commit()
                logger.info(f"Cleaned up {cleaned_count} expired token connections")
                return cleaned_count
                
        except Exception as e:
            logger.error(f"Token cleanup failed: {e}")
            return 0

    async def bulk_revoke_tokens(self, user_id: str, service_names: List[str] = None) -> Dict[str, bool]:
        """Revoke multiple tokens for a user"""
        if not user_id:
            raise ValueError("user_id is required")
        
        try:
            async with AsyncSessionLocal() as db:
                query = select(ServiceConnection).where(
                    ServiceConnection.user_id == user_id,
                    ServiceConnection.is_active == True
                )
                
                if service_names:
                    query = query.where(ServiceConnection.service_name.in_(service_names))
                
                result = await db.execute(query)
                connections = result.scalars().all()
                
                revocation_results = {}
                for connection in connections:
                    try:
                        success = await self.revoke_token(user_id, connection.service_name)
                        revocation_results[connection.service_name] = success
                    except Exception as e:
                        logger.error(f"Failed to revoke {connection.service_name}: {e}")
                        revocation_results[connection.service_name] = False
                
                logger.info(f"Bulk revocation completed for user {user_id}: {revocation_results}")
                return revocation_results
                
        except Exception as e:
            logger.error(f"Bulk revocation failed: {e}")
            raise TokenVaultError(f"Bulk revocation failed: {str(e)}")

    async def validate_token_health(self, user_id: str, service_name: str) -> Dict[str, Any]:
        """Validate token health by making a test API call"""
        if not user_id or not service_name:
            raise ValueError("user_id and service_name are required")
        
        try:
            token_data = await self.retrieve_token(user_id, service_name, auto_refresh=True)
            if not token_data:
                return {
                    "healthy": False,
                    "status": "not_found",
                    "message": "Token not found"
                }
            
            # Service-specific health checks
            health_result = await self._perform_health_check(service_name, token_data)
            
            # Update last used timestamp if healthy
            if health_result.get("healthy"):
                async with AsyncSessionLocal() as db:
                    await db.execute(
                        update(ServiceConnection)
                        .where(
                            ServiceConnection.user_id == user_id,
                            ServiceConnection.service_name == service_name,
                            ServiceConnection.is_active == True
                        )
                        .values(last_used_at=datetime.now(timezone.utc))
                    )
                    await db.commit()
            
            return health_result
            
        except Exception as e:
            logger.error(f"Token health validation failed: {e}")
            return {
                "healthy": False,
                "status": "error",
                "message": f"Health check failed: {str(e)}"
            }

    async def _perform_health_check(self, service_name: str, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform service-specific health checks"""
        service_lower = service_name.lower()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return {
                "healthy": False,
                "status": "invalid_token",
                "message": "No access token found"
            }
        
        try:
            if service_lower.startswith("google"):
                return await self._check_google_token_health(access_token)
            elif service_lower.startswith("github"):
                return await self._check_github_token_health(access_token)
            elif service_lower.startswith("slack"):
                return await self._check_slack_token_health(access_token)
            else:
                return {
                    "healthy": True,
                    "status": "unknown_service",
                    "message": f"No health check implemented for {service_name}"
                }
        except Exception as e:
            return {
                "healthy": False,
                "status": "health_check_failed",
                "message": f"Health check error: {str(e)}"
            }

    async def _check_google_token_health(self, access_token: str) -> Dict[str, Any]:
        """Check Google token health"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v1/tokeninfo",
                    params={"access_token": access_token}
                )
                
                if response.status_code == 200:
                    token_info = response.json()
                    return {
                        "healthy": True,
                        "status": "active",
                        "expires_in": token_info.get("expires_in"),
                        "scope": token_info.get("scope")
                    }
                else:
                    return {
                        "healthy": False,
                        "status": "invalid",
                        "message": f"Token validation failed: {response.status_code}"
                    }
        except Exception as e:
            return {
                "healthy": False,
                "status": "error",
                "message": f"Google health check failed: {str(e)}"
            }

    async def _check_github_token_health(self, access_token: str) -> Dict[str, Any]:
        """Check GitHub token health"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
                
                if response.status_code == 200:
                    user_info = response.json()
                    return {
                        "healthy": True,
                        "status": "active",
                        "user": user_info.get("login"),
                        "scopes": response.headers.get("X-OAuth-Scopes", "").split(", ")
                    }
                else:
                    return {
                        "healthy": False,
                        "status": "invalid",
                        "message": f"Token validation failed: {response.status_code}"
                    }
        except Exception as e:
            return {
                "healthy": False,
                "status": "error",
                "message": f"GitHub health check failed: {str(e)}"
            }

    async def _check_slack_token_health(self, access_token: str) -> Dict[str, Any]:
        """Check Slack token health"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://slack.com/api/auth.test",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        return {
                            "healthy": True,
                            "status": "active",
                            "user": data.get("user"),
                            "team": data.get("team"),
                            "url": data.get("url")
                        }
                    else:
                        return {
                            "healthy": False,
                            "status": "invalid",
                            "message": f"Slack API error: {data.get('error')}"
                        }
                else:
                    return {
                        "healthy": False,
                        "status": "invalid",
                        "message": f"Token validation failed: {response.status_code}"
                    }
        except Exception as e:
            return {
                "healthy": False,
                "status": "error",
                "message": f"Slack health check failed: {str(e)}"
            }

    async def get_vault_statistics(self) -> Dict[str, Any]:
        """Get comprehensive Token Vault statistics"""
        try:
            async with AsyncSessionLocal() as db:
                # Total connections
                total_result = await db.execute(select(ServiceConnection))
                total_connections = len(total_result.scalars().all())
                
                # Active connections
                active_result = await db.execute(
                    select(ServiceConnection).where(ServiceConnection.is_active == True)
                )
                active_connections = len(active_result.scalars().all())
                
                # Expired connections
                expired_result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.expires_at <= datetime.now(timezone.utc),
                        ServiceConnection.is_active == True
                    )
                )
                expired_connections = len(expired_result.scalars().all())
                
                # Service breakdown
                service_result = await db.execute(
                    select(ServiceConnection.service_name, ServiceConnection.is_active)
                )
                service_data = service_result.fetchall()
                
                service_stats = {}
                for service_name, is_active in service_data:
                    if service_name not in service_stats:
                        service_stats[service_name] = {"total": 0, "active": 0}
                    service_stats[service_name]["total"] += 1
                    if is_active:
                        service_stats[service_name]["active"] += 1
                
                return {
                    "total_connections": total_connections,
                    "active_connections": active_connections,
                    "expired_connections": expired_connections,
                    "inactive_connections": total_connections - active_connections,
                    "service_breakdown": service_stats,
                    "health_percentage": (active_connections / total_connections * 100) if total_connections > 0 else 0,
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get vault statistics: {e}")
            return {
                "error": f"Statistics generation failed: {str(e)}",
                "generated_at": datetime.now(timezone.utc).isoformat()
            }


# Global instance
token_vault_service = TokenVaultService()