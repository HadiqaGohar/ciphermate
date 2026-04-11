"""Permission management API endpoints"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from app.core.auth import get_current_user
from app.core.oauth_handlers import (
    oauth_service, 
    OAuthError, 
    InvalidStateError, 
    AuthorizationError, 
    TokenExchangeError
)
from app.core.token_vault import TokenVaultError
from app.core.audit_service import audit_service
from app.models.audit_log import AuditLog
from app.core.database import AsyncSessionLocal
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/permissions", tags=["permissions"])

    # // done hadiqa

class PermissionGrantRequest(BaseModel):
    service: str = Field(..., description="Service name (google, github, slack)")
    scopes: Optional[List[str]] = Field(None, description="Custom scopes (optional, uses defaults if not provided)")


class PermissionRevokeRequest(BaseModel):
    service: str = Field(..., description="Service name to revoke permissions for")


class PermissionResponse(BaseModel):
    service: str
    scopes: List[str]
    status: str
    created_at: Optional[str] = None
    last_used_at: Optional[str] = None
    expires_at: Optional[str] = None


class AuthorizationUrlResponse(BaseModel):
    authorization_url: str
    state: str
    service: str
    scopes: List[str]
    expires_in: int = 300  # State expires in 5 minutes


class CallbackResponse(BaseModel):
    success: bool
    service: str
    user_info: Dict[str, Any]
    scopes: List[str]
    message: str
    granted_at: str


@router.get("/services")
async def get_supported_services():
    """Get list of supported services and their default scopes"""
    try:
        # Return demo services for hackathon
        services = {
            "google_calendar": {
                "name": "Google Calendar",
                "default_scopes": ["calendar:read", "calendar:write"],
                "description": "Access Google Calendar events and scheduling"
            },
            "gmail": {
                "name": "Gmail",
                "default_scopes": ["email:read", "email:send"],
                "description": "Access Gmail messages and sending capabilities"
            },
            "github": {
                "name": "GitHub",
                "default_scopes": ["repo:read", "issues:write"],
                "description": "Access GitHub repositories and issues"
            },
            "slack": {
                "name": "Slack",
                "default_scopes": ["channels:read", "messages:send"],
                "description": "Access Slack channels and messaging"
            }
        }
        
        return {
            "services": services,
            "total_services": len(services)
        }
        
    except Exception as e:
        logger.error(f"Error getting supported services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get supported services"
        )
        
    except Exception as e:
        logger.error(f"Error getting supported services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get supported services"
        )


@router.post("/grant", response_model=AuthorizationUrlResponse)
async def initiate_permission_grant(
    request: PermissionGrantRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Initiate OAuth flow to grant permissions for a service"""
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        # Validate service
        if request.service.lower() not in oauth_service.handlers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported service: {request.service}"
            )
        
        # Get scopes (use custom or default)
        scopes = request.scopes or oauth_service.get_default_scopes(request.service)
        if not scopes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No scopes available for service: {request.service}"
            )
        
        # Initiate OAuth flow
        auth_url, state = await oauth_service.initiate_oauth_flow(
            user_id=user_id,
            service_name=request.service,
            custom_scopes=scopes
        )
        
        # Log the permission grant initiation
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_grant_initiated",
            service_name=request.service,
            details={
                "scopes": scopes,
                "state": state[:10] + "..."  # Log partial state for debugging
            },
            request=request
        )
        
        return AuthorizationUrlResponse(
            authorization_url=auth_url,
            state=state,
            service=request.service,
            scopes=scopes
        )
        
    except OAuthError as e:
        logger.error(f"OAuth error initiating permission grant: {e}")
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
        logger.error(f"Unexpected error initiating permission grant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate permission grant"
        )


@router.get("/callback/{service}")
async def handle_oauth_callback(
    service: str,
    code: str = Query(..., description="Authorization code from OAuth provider"),
    state: str = Query(..., description="State parameter for security"),
    error: Optional[str] = Query(None, description="Error from OAuth provider"),
    error_description: Optional[str] = Query(None, description="Error description from OAuth provider"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Handle OAuth callback and complete permission grant"""
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        # Check for OAuth errors
        if error:
            error_msg = error_description or error
            logger.warning(f"OAuth error for user {user_id}, service {service}: {error_msg}")
            
            await audit_service.log_action(
                user_id=user_id,
                action_type="permission_grant_failed",
                service_name=service,
                details={
                    "error": error,
                    "error_description": error_description
                },
                request=request
            )
            
            # Redirect to frontend with error
            return RedirectResponse(
                url=f"{_get_frontend_url()}/permissions?error={error}&service={service}",
                status_code=status.HTTP_302_FOUND
            )
        
        # Handle successful callback
        result = await oauth_service.handle_oauth_callback(
            service_name=service,
            code=code,
            state=state,
            expected_user_id=user_id
        )
        
        # Log successful permission grant
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_granted",
            service_name=service,
            details={
                "scopes": result["scopes"],
                "vault_id": result["vault_id"],
                "user_info": {
                    "id": result["user_info"].get("id"),
                    "email": result["user_info"].get("email"),
                    "name": result["user_info"].get("name")
                }
            },
            request=request
        )
        
        # Redirect to frontend with success
        return RedirectResponse(
            url=f"{_get_frontend_url()}/permissions?success=true&service={service}",
            status_code=status.HTTP_302_FOUND
        )
        
    except InvalidStateError as e:
        logger.error(f"Invalid state error: {e}")
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_grant_failed",
            service_name=service,
            details={"error": "invalid_state", "message": str(e)},
            request=request
        )
        return RedirectResponse(
            url=f"{_get_frontend_url()}/permissions?error=invalid_state&service={service}",
            status_code=status.HTTP_302_FOUND
        )
    except (TokenExchangeError, AuthorizationError) as e:
        logger.error(f"OAuth flow error: {e}")
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_grant_failed",
            service_name=service,
            details={"error": "oauth_error", "message": str(e)},
            request=request
        )
        return RedirectResponse(
            url=f"{_get_frontend_url()}/permissions?error=oauth_failed&service={service}",
            status_code=status.HTTP_302_FOUND
        )
    except TokenVaultError as e:
        logger.error(f"Token vault error: {e}")
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_grant_failed",
            service_name=service,
            details={"error": "token_vault_error", "message": str(e)},
            request=request
        )
        return RedirectResponse(
            url=f"{_get_frontend_url()}/permissions?error=storage_failed&service={service}",
            status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        logger.error(f"Unexpected error in OAuth callback: {e}")
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_grant_failed",
            service_name=service,
            details={"error": "unexpected_error", "message": str(e)},
            request=request
        )
        return RedirectResponse(
            url=f"{_get_frontend_url()}/permissions?error=unexpected&service={service}",
            status_code=status.HTTP_302_FOUND
        )


@router.get("/list", response_model=List[PermissionResponse])
async def list_user_permissions(
    include_inactive: bool = Query(False, description="Include revoked/inactive permissions")
):
    """List all permissions granted by the user"""
    try:
        # Return demo permissions for hackathon
        demo_permissions = [
            {
                "service": "google_calendar",
                "scopes": ["calendar:read", "calendar:write"],
                "status": "active",
                "created_at": "2026-04-05T10:00:00Z",
                "last_used_at": "2026-04-05T11:30:00Z",
                "expires_at": "2026-05-05T10:00:00Z"
            },
            {
                "service": "gmail",
                "scopes": ["email:read"],
                "status": "active",
                "created_at": "2026-04-05T09:00:00Z",
                "last_used_at": "2026-04-05T12:00:00Z",
                "expires_at": "2026-05-05T09:00:00Z"
            },
            {
                "service": "github",
                "scopes": ["repo:read", "issues:write"],
                "status": "active",
                "created_at": "2026-04-04T15:00:00Z",
                "last_used_at": "2026-04-05T08:00:00Z",
                "expires_at": "2026-05-04T15:00:00Z"
            },
            {
                "service": "slack",
                "scopes": ["channels:read"],
                "status": "inactive",
                "created_at": "2026-04-03T12:00:00Z",
                "last_used_at": "2026-04-03T14:00:00Z",
                "expires_at": "2026-05-03T12:00:00Z"
            }
        ]
        
        # Filter based on include_inactive
        if not include_inactive:
            demo_permissions = [p for p in demo_permissions if p["status"] == "active"]
        
        # Convert to response format
        permission_responses = []
        for perm in demo_permissions:
            permission_responses.append(PermissionResponse(
                service=perm["service"],
                scopes=perm["scopes"],
                status=perm["status"],
                created_at=perm["created_at"],
                last_used_at=perm["last_used_at"],
                expires_at=perm["expires_at"]
            ))
        
        return permission_responses
        
    except Exception as e:
        logger.error(f"Unexpected error listing permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list permissions"
        )
        
    except OAuthError as e:
        logger.error(f"OAuth error listing permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error listing permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list permissions"
        )


@router.delete("/revoke")
async def revoke_permission(
    request: PermissionRevokeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke permission for a specific service"""
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        # Validate service
        if request.service.lower() not in oauth_service.handlers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported service: {request.service}"
            )
        
        # Revoke permission
        success = await oauth_service.revoke_service_permission(user_id, request.service)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No active permission found for service: {request.service}"
            )
        
        # Log the revocation
        await audit_service.log_action(
            user_id=user_id,
            action_type="permission_revoked",
            service_name=request.service,
            details={"revoked_at": datetime.utcnow().isoformat()},
            request=request
        )
        
        return {
            "success": True,
            "service": request.service,
            "message": f"Permission revoked successfully for {request.service}",
            "revoked_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except OAuthError as e:
        logger.error(f"OAuth error revoking permission: {e}")
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
        logger.error(f"Unexpected error revoking permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke permission"
        )


@router.delete("/revoke-all")
async def revoke_all_permissions(
    confirm: bool = Query(False, description="Confirmation flag to prevent accidental revocation"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke all permissions for the user"""
    try:
        if not confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Confirmation required. Set confirm=true to revoke all permissions."
            )
        
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        # Get current permissions
        permissions = await oauth_service.get_user_permissions(user_id)
        active_services = [p["service"] for p in permissions if p["status"] == "active"]
        
        if not active_services:
            return {
                "success": True,
                "message": "No active permissions to revoke",
                "revoked_services": [],
                "revoked_at": datetime.utcnow().isoformat() + "Z"
            }
        
        # Revoke all permissions
        revoked_services = []
        failed_services = []
        
        for service in active_services:
            try:
                success = await oauth_service.revoke_service_permission(user_id, service)
                if success:
                    revoked_services.append(service)
                else:
                    failed_services.append(service)
            except Exception as e:
                logger.error(f"Failed to revoke permission for {service}: {e}")
                failed_services.append(service)
        
        # Log the bulk revocation
        await audit_service.log_action(
            user_id=user_id,
            action_type="bulk_permission_revoked",
            service_name="all",
            details={
                "revoked_services": revoked_services,
                "failed_services": failed_services,
                "total_attempted": len(active_services)
            },
            request=request
        )
        
        return {
            "success": len(failed_services) == 0,
            "message": f"Revoked permissions for {len(revoked_services)} services",
            "revoked_services": revoked_services,
            "failed_services": failed_services,
            "revoked_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Unexpected error revoking all permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke all permissions"
        )


@router.get("/status/{service}")
async def get_permission_status(
    service: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed status for a specific service permission"""
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        # Validate service
        if service.lower() not in oauth_service.handlers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported service: {service}"
            )
        
        # Get user permissions
        permissions = await oauth_service.get_user_permissions(user_id)
        service_permission = next((p for p in permissions if p["service"] == service), None)
        
        if not service_permission:
            return {
                "service": service,
                "status": "not_granted",
                "has_permission": False,
                "message": f"No permission granted for {service}",
                "available_scopes": oauth_service.get_default_scopes(service)
            }
        
        return {
            "service": service,
            "status": service_permission["status"],
            "has_permission": service_permission["status"] == "active",
            "scopes": service_permission["scopes"],
            "created_at": service_permission["created_at"],
            "last_used_at": service_permission["last_used_at"],
            "expires_at": service_permission["expires_at"],
            "message": f"Permission status: {service_permission['status']}"
        }
        
    except Exception as e:
        logger.error(f"Error getting permission status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get permission status"
        )


@router.get("/scopes/{service}")
async def get_service_scopes(
    service: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get available scopes for a service with detailed information"""
    try:
        # Validate service
        if service.lower() not in oauth_service.handlers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported service: {service}"
            )
        
        from app.core.permission_service import permission_service
        
        scopes = await permission_service.get_service_scopes(service)
        default_scopes = permission_service.get_default_scopes_for_service(service)
        high_risk_scopes = permission_service.get_high_risk_scopes_for_service(service)
        
        return {
            "service": service,
            "available_scopes": scopes,
            "default_scopes": default_scopes,
            "high_risk_scopes": high_risk_scopes,
            "total_scopes": len(scopes)
        }
        
    except Exception as e:
        logger.error(f"Error getting service scopes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get service scopes"
        )


@router.post("/validate-scopes/{service}")
async def validate_scopes_endpoint(
    service: str,
    request_body: Dict[str, List[str]],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Validate requested scopes for a service"""
    try:
        # Validate service
        if service.lower() not in oauth_service.handlers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported service: {service}"
            )
        
        scopes = request_body.get("scopes", [])
        if not scopes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scopes list is required"
            )
        
        from app.core.permission_service import permission_service
        
        validation_result = await permission_service.validate_scopes(service, scopes)
        
        return {
            "service": service,
            "requested_scopes": scopes,
            "validation": validation_result
        }
        
    except Exception as e:
        logger.error(f"Error validating scopes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate scopes"
        )


@router.get("/summary")
async def get_permission_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive permission summary for the user"""
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user authentication"
            )
        
        from app.core.permission_service import permission_service
        
        summary = await permission_service.get_permission_summary(user_id)
        
        return {
            "user_id": user_id,
            "summary": summary,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting permission summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get permission summary"
        )


# Helper functions

def _get_service_description(service_name: str) -> str:
    """Get human-readable description for a service"""
    descriptions = {
        "google": "Access Google services like Calendar, Gmail, and Drive",
        "github": "Access GitHub repositories, issues, and user information",
        "slack": "Access Slack channels, messages, and workspace information"
    }
    return descriptions.get(service_name.lower(), f"Access {service_name.title()} services")


def _get_frontend_url() -> str:
    """Get frontend URL for redirects"""
    from app.core.config import settings
    # In production, this would be the actual frontend URL
    return "http://localhost:3000"