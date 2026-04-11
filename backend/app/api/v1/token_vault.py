from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.core.auth import get_current_user
from app.core.token_vault import (
    token_vault_service, 
    TokenVaultError, 
    TokenNotFoundError, 
    TokenExpiredError,
    AuthenticationError,
    ServiceError
)
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/token-vault", tags=["token-vault"])


class TokenStoreRequest(BaseModel):
    service: str = Field(..., description="Service name (e.g., 'google_calendar', 'github')")
    token: Dict[str, Any] = Field(..., description="Token data including access_token, refresh_token, etc.")
    scopes: List[str] = Field(..., description="List of OAuth scopes granted")
    user_id: str = Field(..., description="User ID (must match authenticated user)")
    expires_at: Optional[str] = Field(None, description="Token expiration timestamp (ISO format)")


class TokenRevokeRequest(BaseModel):
    user_id: str = Field(..., description="User ID (must match authenticated user)")


class TokenRefreshRequest(BaseModel):
    user_id: str = Field(..., description="User ID (must match authenticated user)")
    refresh_token: Optional[str] = Field(None, description="Refresh token (optional if stored)")


class TokenStatusResponse(BaseModel):
    exists: bool
    status: str
    service: Optional[str] = None
    scopes: Optional[List[str]] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    last_used_at: Optional[str] = None
    can_refresh: Optional[bool] = None
    message: Optional[str] = None


@router.post("/store")
async def store_token(
    request: TokenStoreRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Store a token in Auth0 Token Vault with enhanced error handling"""
    try:
        # Verify user can only store tokens for themselves
        if request.user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot store tokens for other users"
            )
        
        # Parse expiration date if provided
        expires_at = None
        if request.expires_at:
            try:
                expires_at = datetime.fromisoformat(request.expires_at.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid expires_at format. Use ISO format (e.g., '2024-01-01T12:00:00Z')"
                )
        
        vault_id = await token_vault_service.store_token(
            user_id=request.user_id,
            service_name=request.service,
            token_data=request.token,
            scopes=request.scopes,
            expires_at=expires_at
        )
        
        return {
            "success": True,
            "vault_id": vault_id,
            "service": request.service,
            "message": f"Token stored successfully for {request.service}",
            "expires_at": request.expires_at
        }
        
    except AuthenticationError as e:
        logger.error(f"Auth0 authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Authentication service error: {str(e)}"
        )
    except TokenVaultError as e:
        logger.error(f"Token vault error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error storing token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while storing the token"
        )


@router.get("/retrieve/{service}")
async def retrieve_token(
    service: str,
    user_id: str,
    auto_refresh: bool = True,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Retrieve a token from Auth0 Token Vault with automatic refresh"""
    try:
        # Verify user can only retrieve their own tokens
        if user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot retrieve tokens for other users"
            )
        
        token_data = await token_vault_service.retrieve_token(
            user_id=user_id,
            service_name=service,
            auto_refresh=auto_refresh
        )
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No token found for service: {service}"
            )
        
        return {
            "token": token_data,
            "service": service,
            "retrieved_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except TokenNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=f"{str(e)}. Please re-authenticate with the service."
        )
    except AuthenticationError as e:
        logger.error(f"Auth0 authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Authentication service error: {str(e)}"
        )
    except TokenVaultError as e:
        logger.error(f"Token vault error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the token"
        )


@router.delete("/revoke/{service}")
async def revoke_token(
    service: str,
    request: TokenRevokeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke a token from Auth0 Token Vault with comprehensive cleanup"""
    try:
        # Verify user can only revoke their own tokens
        if request.user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot revoke tokens for other users"
            )
        
        success = await token_vault_service.revoke_token(
            user_id=request.user_id,
            service_name=service
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No active token found for service: {service}"
            )
        
        return {
            "success": True,
            "service": service,
            "message": f"Token revoked successfully for {service}",
            "revoked_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except TokenNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except AuthenticationError as e:
        logger.error(f"Auth0 authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Authentication service error: {str(e)}"
        )
    except TokenVaultError as e:
        logger.error(f"Token vault error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error revoking token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while revoking the token"
        )


@router.get("/list")
async def list_tokens(
    user_id: Optional[str] = None,
    include_inactive: bool = False,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List all tokens for a user with enhanced metadata"""
    try:
        # Use the user_id from the authenticated user if not provided
        if not user_id:
            user_id = current_user.get("sub")
        
        # Get tokens from token vault service
        tokens = await token_vault_service.list_user_tokens(user_id, include_inactive)

        return {
            "tokens": tokens,
            "total": len(tokens),
            "count": len(tokens),
            "user_id": user_id,
            "include_inactive": include_inactive,
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_tokens": len(tokens),
                "active_tokens": sum(1 for t in tokens if t.get("status") == "active"),
                "expiring_soon": sum(1 for t in tokens if t.get("status") == "expiring_soon"),
                "expired": sum(1 for t in tokens if t.get("status") == "expired")
            }
        }

    except Exception as e:
        logger.error(f"Unexpected error listing tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while listing tokens"
        )


@router.post("/refresh/{service}")
async def refresh_token(
    service: str,
    request: TokenRefreshRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Refresh an expired token with enhanced error handling"""
    try:
        # Verify user can only refresh their own tokens
        if request.user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot refresh tokens for other users"
            )
        
        new_token = await token_vault_service.refresh_token(
            user_id=request.user_id,
            service_name=service,
            refresh_token=request.refresh_token
        )
        
        if not new_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to refresh token for service: {service}. The refresh token may be invalid or expired."
            )
        
        return {
            "success": True,
            "service": service,
            "message": f"Token refreshed successfully for {service}",
            "token": new_token,
            "refreshed_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except TokenNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=f"{str(e)}. Please re-authenticate with the service."
        )
    except ServiceError as e:
        logger.error(f"Service error during token refresh: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External service error: {str(e)}"
        )
    except AuthenticationError as e:
        logger.error(f"Auth0 authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Authentication service error: {str(e)}"
        )
    except TokenVaultError as e:
        logger.error(f"Token vault error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error refreshing token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while refreshing the token"
        )


@router.get("/status/{service}", response_model=TokenStatusResponse)
async def get_token_status(
    service: str,
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive token status information"""
    try:
        # Verify user can only check their own token status
        if user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot check token status for other users"
            )
        
        status_info = await token_vault_service.get_token_status(user_id, service)
        
        return TokenStatusResponse(**status_info)
        
    except Exception as e:
        logger.error(f"Error getting token status: {e}")
        return TokenStatusResponse(
            exists=False,
            status="error",
            message=f"Error checking token status: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup_expired_tokens(
    days_old: int = 30,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Clean up expired tokens (admin operation)"""
    try:
        # This could be restricted to admin users in a real implementation
        # For now, we'll allow any authenticated user to clean their own tokens
        
        cleaned_count = await token_vault_service.cleanup_expired_tokens(days_old)
        
        return {
            "success": True,
            "cleaned_count": cleaned_count,
            "days_old": days_old,
            "message": f"Cleaned up {cleaned_count} expired token connections",
            "cleaned_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Token cleanup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token cleanup failed: {str(e)}"
        )


@router.post("/bulk-revoke")
async def bulk_revoke_tokens(
    user_id: str,
    service_names: Optional[List[str]] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke multiple tokens for a user"""
    try:
        # Verify user can only revoke their own tokens
        if user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot revoke tokens for other users"
            )
        
        results = await token_vault_service.bulk_revoke_tokens(user_id, service_names)
        
        return {
            "success": True,
            "user_id": user_id,
            "revocation_results": results,
            "total_services": len(results),
            "successful_revocations": sum(1 for success in results.values() if success),
            "revoked_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except TokenVaultError as e:
        logger.error(f"Bulk revocation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during bulk revocation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during bulk revocation"
        )


@router.get("/health/{service}")
async def validate_token_health(
    service: str,
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Validate token health by making a test API call"""
    try:
        # Verify user can only check their own token health
        if user_id != current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot check token health for other users"
            )
        
        health_result = await token_vault_service.validate_token_health(user_id, service)
        
        return {
            "service": service,
            "user_id": user_id,
            "health_check": health_result,
            "checked_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Token health validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token health validation failed: {str(e)}"
        )


@router.get("/statistics")
async def get_vault_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive Token Vault statistics"""
    try:
        stats = await token_vault_service.get_vault_statistics()
        
        return {
            "statistics": stats,
            "requested_by": current_user.get("sub"),
            "requested_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Statistics generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Statistics generation failed: {str(e)}"
        )