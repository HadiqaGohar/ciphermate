from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.core.auth import get_current_user, get_optional_user
from app.core.session import session_manager
from app.core.token_vault import token_vault_service
from app.core.database import get_db
from app.core.audit_service import audit_service
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

class UserProfile(BaseModel):
    """User profile response model"""
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = False
    permissions: list[str] = []
    scope: list[str] = []

class SessionInfo(BaseModel):
    """Session information response model"""
    session_id: str
    user_id: str
    created_at: str
    last_accessed: str

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user profile"""
    try:
        # Log profile access
        await audit_service.log_action(
            user_id=current_user["sub"],
            action_type="profile_access",
            details={"accessed_fields": ["sub", "email", "name", "nickname", "picture"]},
            request=request
        )
        
        return UserProfile(**current_user)
    except Exception as e:
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="profile_access_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise

@router.get("/session")
async def get_session_info(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current session information"""
    try:
        user_id = current_user["sub"]
        session_data = await session_manager.get_user_session(user_id)
        
        if not session_data:
            # Create a new session for the authenticated user
            session_id = await session_manager.create_session(
                user_id=user_id,
                user_data=current_user
            )
            session_data = await session_manager.get_session(session_id)
        
        # Log session access
        await audit_service.log_action(
            user_id=user_id,
            action_type="session_access",
            details={"session_id": session_data.get("session_id", "unknown")[:10] + "..."},
            request=request
        )
        
        return {
            "session_id": session_data.get("session_id", "unknown"),
            "user_id": session_data.get("user_id"),
            "created_at": session_data.get("created_at"),
            "last_accessed": session_data.get("last_accessed"),
            "user_data": session_data.get("user_data", {})
        }
        
    except Exception as e:
        logger.error(f"Failed to get session info: {e}")
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="session_access_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session information"
        )

@router.post("/session/refresh")
async def refresh_session(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Refresh current user session"""
    try:
        user_id = current_user["sub"]
        
        # Update session with latest user data
        session_data = await session_manager.get_user_session(user_id)
        if session_data:
            await session_manager.update_session(
                session_id=session_data.get("session_id", ""),
                updates={"user_data": current_user}
            )
        else:
            # Create new session if none exists
            await session_manager.create_session(
                user_id=user_id,
                user_data=current_user
            )
        
        # Log session refresh
        await audit_service.log_action(
            user_id=user_id,
            action_type="session_refresh",
            details={"refreshed_at": session_data.get("last_accessed") if session_data else None},
            request=request
        )
        
        return {"message": "Session refreshed successfully"}
        
    except Exception as e:
        logger.error(f"Failed to refresh session: {e}")
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="session_refresh_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh session"
        )

@router.delete("/session")
async def logout_session(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Logout and delete current session"""
    try:
        user_id = current_user["sub"]
        session_data = await session_manager.get_user_session(user_id)
        
        if session_data:
            session_id = session_data.get("session_id", "")
            await session_manager.delete_session(session_id)
        
        # Log logout
        await audit_service.log_action(
            user_id=user_id,
            action_type="logout",
            details={"session_terminated": True},
            request=request
        )
        
        return {"message": "Session terminated successfully"}
        
    except Exception as e:
        logger.error(f"Failed to logout session: {e}")
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="logout_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to terminate session"
        )

@router.get("/tokens")
async def list_user_tokens(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List all tokens stored in Token Vault for current user"""
    try:
        user_id = current_user["sub"]
        tokens = await token_vault_service.list_tokens(user_id)
        
        # Log token list access
        await audit_service.log_action(
            user_id=user_id,
            action_type="token_list_access",
            details={"token_count": len(tokens)},
            request=request
        )
        
        return {"tokens": tokens}
        
    except Exception as e:
        logger.error(f"Failed to list user tokens: {e}")
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="token_list_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tokens"
        )

@router.delete("/tokens/{service_name}")
async def revoke_service_token(
    service_name: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke a token for a specific service from Token Vault"""
    try:
        user_id = current_user["sub"]
        
        success = await token_vault_service.revoke_token(
            user_id=user_id,
            service_name=service_name
        )
        
        if not success:
            await audit_service.log_security_event(
                user_id=user_id,
                event_type="token_revoke_failed",
                severity="warning",
                details={"service": service_name, "reason": "token_not_found"},
                request=request
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No token found for service: {service_name}"
            )
        
        # Log successful token revocation
        await audit_service.log_action(
            user_id=user_id,
            action_type="token_revoked",
            service_name=service_name,
            details={"revoked_service": service_name},
            request=request
        )
        
        return {"message": f"Token for {service_name} revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to revoke token: {e}")
        await audit_service.log_security_event(
            user_id=current_user["sub"],
            event_type="token_revoke_error",
            severity="error",
            details={"error": str(e), "service": service_name},
            request=request
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke token"
        )

@router.get("/health")
async def auth_health_check(
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """Health check endpoint that shows auth status"""
    return {
        "status": "healthy",
        "authenticated": current_user is not None,
        "user_id": current_user.get("sub") if current_user else None,
        "timestamp": session_manager.redis_client is not None
    }

        # // done hadiqa
