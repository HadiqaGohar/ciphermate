"""Permission management service for handling service scopes and templates"""

from typing import Dict, List, Any, Optional
from app.models.permission_template import PermissionTemplate
from app.core.database import AsyncSessionLocal
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


class PermissionService:
    """Service for managing permission templates and scope definitions"""
    
    def __init__(self):
        # Define comprehensive scope templates for each service
        self.service_scopes = {
            "google": {
                "calendar": {
                    "scope": "https://www.googleapis.com/auth/calendar",
                    "description": "Full access to Google Calendar",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "calendar_readonly": {
                    "scope": "https://www.googleapis.com/auth/calendar.readonly",
                    "description": "Read-only access to Google Calendar",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "gmail_readonly": {
                    "scope": "https://www.googleapis.com/auth/gmail.readonly",
                    "description": "Read-only access to Gmail",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "gmail_send": {
                    "scope": "https://www.googleapis.com/auth/gmail.send",
                    "description": "Send emails via Gmail",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "drive_readonly": {
                    "scope": "https://www.googleapis.com/auth/drive.readonly",
                    "description": "Read-only access to Google Drive",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "drive": {
                    "scope": "https://www.googleapis.com/auth/drive",
                    "description": "Full access to Google Drive",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "userinfo_email": {
                    "scope": "https://www.googleapis.com/auth/userinfo.email",
                    "description": "Access to user email address",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "userinfo_profile": {
                    "scope": "https://www.googleapis.com/auth/userinfo.profile",
                    "description": "Access to user profile information",
                    "risk_level": "low",
                    "requires_step_up": False
                }
            },
            "github": {
                "repo": {
                    "scope": "repo",
                    "description": "Full access to repositories",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "repo_status": {
                    "scope": "repo:status",
                    "description": "Access to commit status",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "public_repo": {
                    "scope": "public_repo",
                    "description": "Access to public repositories",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "user": {
                    "scope": "user",
                    "description": "Full access to user profile",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "user_email": {
                    "scope": "user:email",
                    "description": "Access to user email addresses",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "read_user": {
                    "scope": "read:user",
                    "description": "Read-only access to user profile",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "gist": {
                    "scope": "gist",
                    "description": "Access to gists",
                    "risk_level": "medium",
                    "requires_step_up": False
                }
            },
            "slack": {
                "channels_read": {
                    "scope": "channels:read",
                    "description": "View basic information about public channels",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "channels_write": {
                    "scope": "channels:write",
                    "description": "Manage public channels",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "chat_write": {
                    "scope": "chat:write",
                    "description": "Send messages as the user",
                    "risk_level": "high",
                    "requires_step_up": True
                },
                "chat_write_public": {
                    "scope": "chat:write.public",
                    "description": "Send messages to public channels",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "users_read": {
                    "scope": "users:read",
                    "description": "View people in the workspace",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "users_read_email": {
                    "scope": "users:read.email",
                    "description": "View email addresses of people in the workspace",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "files_read": {
                    "scope": "files:read",
                    "description": "View files shared in channels and conversations",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "files_write": {
                    "scope": "files:write",
                    "description": "Upload, edit, and delete files",
                    "risk_level": "high",
                    "requires_step_up": True
                }
            }
        }
    
    async def initialize_permission_templates(self) -> None:
        """Initialize permission templates in the database"""
        try:
            async with AsyncSessionLocal() as db:
                # Check if templates already exist
                result = await db.execute(select(PermissionTemplate).limit(1))
                if result.scalar_one_or_none():
                    logger.info("Permission templates already initialized")
                    return
                
                # Insert all permission templates
                templates = []
                for service_name, scopes in self.service_scopes.items():
                    for scope_key, scope_data in scopes.items():
                        template = PermissionTemplate(
                            service_name=service_name,
                            scope_name=scope_data["scope"],
                            description=scope_data["description"],
                            risk_level=scope_data["risk_level"],
                            requires_step_up=scope_data["requires_step_up"]
                        )
                        templates.append(template)
                
                db.add_all(templates)
                await db.commit()
                
                logger.info(f"Initialized {len(templates)} permission templates")
                
        except Exception as e:
            logger.error(f"Failed to initialize permission templates: {e}")
            raise
    
    async def get_service_scopes(self, service_name: str) -> Dict[str, Any]:
        """Get available scopes for a service"""
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(PermissionTemplate).where(
                        PermissionTemplate.service_name == service_name.lower()
                    )
                )
                templates = result.scalars().all()
                
                scopes = {}
                for template in templates:
                    scopes[template.scope_name] = {
                        "description": template.description,
                        "risk_level": template.risk_level,
                        "requires_step_up": template.requires_step_up
                    }
                
                return scopes
                
        except Exception as e:
            logger.error(f"Failed to get service scopes: {e}")
            return {}
    
    async def get_scope_info(self, service_name: str, scope: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific scope"""
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(PermissionTemplate).where(
                        PermissionTemplate.service_name == service_name.lower(),
                        PermissionTemplate.scope_name == scope
                    )
                )
                template = result.scalar_one_or_none()
                
                if not template:
                    return None
                
                return {
                    "scope": template.scope_name,
                    "description": template.description,
                    "risk_level": template.risk_level,
                    "requires_step_up": template.requires_step_up
                }
                
        except Exception as e:
            logger.error(f"Failed to get scope info: {e}")
            return None
    
    def get_default_scopes_for_service(self, service_name: str) -> List[str]:
        """Get default scopes for a service (safe, commonly used scopes)"""
        default_scopes = {
            "google": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/calendar.readonly",
                "https://www.googleapis.com/auth/gmail.readonly"
            ],
            "github": [
                "user:email",
                "read:user",
                "public_repo"
            ],
            "slack": [
                "channels:read",
                "users:read",
                "chat:write.public"
            ]
        }
        
        return default_scopes.get(service_name.lower(), [])
    
    def get_high_risk_scopes_for_service(self, service_name: str) -> List[str]:
        """Get high-risk scopes that require step-up authentication"""
        high_risk_scopes = []
        
        service_data = self.service_scopes.get(service_name.lower(), {})
        for scope_data in service_data.values():
            if scope_data.get("requires_step_up", False):
                high_risk_scopes.append(scope_data["scope"])
        
        return high_risk_scopes
    
    async def validate_scopes(self, service_name: str, requested_scopes: List[str]) -> Dict[str, Any]:
        """Validate requested scopes and return validation results"""
        try:
            available_scopes = await self.get_service_scopes(service_name)
            
            valid_scopes = []
            invalid_scopes = []
            high_risk_scopes = []
            
            for scope in requested_scopes:
                if scope in available_scopes:
                    valid_scopes.append(scope)
                    if available_scopes[scope].get("requires_step_up", False):
                        high_risk_scopes.append(scope)
                else:
                    invalid_scopes.append(scope)
            
            return {
                "valid_scopes": valid_scopes,
                "invalid_scopes": invalid_scopes,
                "high_risk_scopes": high_risk_scopes,
                "requires_step_up": len(high_risk_scopes) > 0,
                "validation_passed": len(invalid_scopes) == 0
            }
            
        except Exception as e:
            logger.error(f"Failed to validate scopes: {e}")
            return {
                "valid_scopes": [],
                "invalid_scopes": requested_scopes,
                "high_risk_scopes": [],
                "requires_step_up": False,
                "validation_passed": False,
                "error": str(e)
            }
    
    async def get_permission_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive permission summary for a user"""
        try:
            from app.core.oauth_handlers import oauth_service
            
            permissions = await oauth_service.get_user_permissions(user_id)
            
            summary = {
                "total_services": len(permissions),
                "active_services": len([p for p in permissions if p["status"] == "active"]),
                "expired_services": len([p for p in permissions if p["status"] == "expired"]),
                "revoked_services": len([p for p in permissions if p["status"] == "revoked"]),
                "services": {},
                "risk_analysis": {
                    "low_risk_scopes": 0,
                    "medium_risk_scopes": 0,
                    "high_risk_scopes": 0,
                    "total_scopes": 0
                }
            }
            
            for permission in permissions:
                service_name = permission["service"]
                scopes = permission["scopes"]
                
                # Analyze risk levels
                for scope in scopes:
                    scope_info = await self.get_scope_info(service_name, scope)
                    if scope_info:
                        risk_level = scope_info["risk_level"]
                        summary["risk_analysis"][f"{risk_level}_risk_scopes"] += 1
                        summary["risk_analysis"]["total_scopes"] += 1
                
                summary["services"][service_name] = {
                    "status": permission["status"],
                    "scopes": scopes,
                    "scope_count": len(scopes),
                    "created_at": permission["created_at"],
                    "last_used_at": permission["last_used_at"],
                    "expires_at": permission["expires_at"]
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get permission summary: {e}")
            return {
                "total_services": 0,
                "active_services": 0,
                "expired_services": 0,
                "revoked_services": 0,
                "services": {},
                "risk_analysis": {
                    "low_risk_scopes": 0,
                    "medium_risk_scopes": 0,
                    "high_risk_scopes": 0,
                    "total_scopes": 0
                },
                "error": str(e)
            }
    
    async def cleanup_expired_permissions(self, days_old: int = 30) -> int:
        """Clean up expired permission records"""
        try:
            from datetime import datetime, timedelta
            from app.models.service_connection import ServiceConnection
            
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            async with AsyncSessionLocal() as db:
                # Find expired connections
                result = await db.execute(
                    select(ServiceConnection).where(
                        ServiceConnection.is_active == False,
                        ServiceConnection.created_at < cutoff_date
                    )
                )
                expired_connections = result.scalars().all()
                
                # Delete expired connections
                for connection in expired_connections:
                    await db.delete(connection)
                
                await db.commit()
                
                logger.info(f"Cleaned up {len(expired_connections)} expired permission records")
                return len(expired_connections)
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired permissions: {e}")
            return 0


# Global permission service instance
permission_service = PermissionService()