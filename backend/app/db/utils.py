"""Database utility functions for common operations"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

from app.models.user import User
from app.models.service_connection import ServiceConnection
from app.models.audit_log import AuditLog
from app.models.agent_action import AgentAction
from app.models.permission_template import PermissionTemplate
from app.models.security_event import SecurityEvent


async def get_user_by_auth0_id(session: AsyncSession, auth0_id: str) -> Optional[User]:
    """Get user by Auth0 ID"""
    result = await session.execute(
        select(User).where(User.auth0_id == auth0_id)
    )
    return result.scalar_one_or_none()


async def get_user_with_connections(session: AsyncSession, user_id: int) -> Optional[User]:
    """Get user with all service connections loaded"""
    result = await session.execute(
        select(User)
        .options(selectinload(User.service_connections))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_active_service_connections(
    session: AsyncSession, 
    user_id: int, 
    service_name: Optional[str] = None
) -> List[ServiceConnection]:
    """Get active service connections for a user, optionally filtered by service"""
    query = select(ServiceConnection).where(
        and_(
            ServiceConnection.user_id == user_id,
            ServiceConnection.is_active == True
        )
    )
    
    if service_name:
        query = query.where(ServiceConnection.service_name == service_name)
    
    result = await session.execute(query)
    return result.scalars().all()


async def get_service_connection_by_vault_id(
    session: AsyncSession, 
    token_vault_id: str
) -> Optional[ServiceConnection]:
    """Get service connection by Token Vault ID"""
    result = await session.execute(
        select(ServiceConnection).where(
            and_(
                ServiceConnection.token_vault_id == token_vault_id,
                ServiceConnection.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()


async def create_audit_log(
    session: AsyncSession,
    user_id: int,
    action_type: str,
    service_name: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    session_id: Optional[str] = None
) -> AuditLog:
    """Create and save an audit log entry"""
    audit_log = AuditLog.create_log(
        user_id=user_id,
        action_type=action_type,
        service_name=service_name,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        session_id=session_id
    )
    
    session.add(audit_log)
    await session.flush()  # Get the ID without committing
    return audit_log


async def get_recent_audit_logs(
    session: AsyncSession,
    user_id: int,
    limit: int = 50,
    service_name: Optional[str] = None,
    action_type: Optional[str] = None
) -> List[AuditLog]:
    """Get recent audit logs for a user with optional filtering"""
    query = select(AuditLog).where(AuditLog.user_id == user_id)
    
    if service_name:
        query = query.where(AuditLog.service_name == service_name)
    
    if action_type:
        query = query.where(AuditLog.action_type == action_type)
    
    query = query.order_by(AuditLog.timestamp.desc()).limit(limit)
    
    result = await session.execute(query)
    return result.scalars().all()


async def get_pending_agent_actions(
    session: AsyncSession, 
    user_id: int
) -> List[AgentAction]:
    """Get pending agent actions for a user"""
    result = await session.execute(
        select(AgentAction).where(
            and_(
                AgentAction.user_id == user_id,
                AgentAction.status == "pending"
            )
        ).order_by(AgentAction.created_at.asc())
    )
    return result.scalars().all()


async def get_permission_templates_by_service(
    session: AsyncSession, 
    service_name: str
) -> List[PermissionTemplate]:
    """Get all permission templates for a specific service"""
    result = await session.execute(
        select(PermissionTemplate)
        .where(PermissionTemplate.service_name == service_name)
        .order_by(PermissionTemplate.risk_level, PermissionTemplate.scope_name)
    )
    return result.scalars().all()


async def get_high_risk_permissions(session: AsyncSession) -> List[PermissionTemplate]:
    """Get all high-risk permission templates"""
    result = await session.execute(
        select(PermissionTemplate).where(
            PermissionTemplate.risk_level.in_(["high", "critical"])
        )
    )
    return result.scalars().all()


async def create_security_event(
    session: AsyncSession,
    user_id: int,
    event_type: str,
    severity: str = "info",
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
) -> SecurityEvent:
    """Create and save a security event"""
    security_event = SecurityEvent.create_event(
        user_id=user_id,
        event_type=event_type,
        severity=severity,
        details=details,
        ip_address=ip_address
    )
    
    session.add(security_event)
    await session.flush()
    return security_event


async def get_unresolved_security_events(
    session: AsyncSession,
    user_id: Optional[int] = None,
    severity: Optional[str] = None
) -> List[SecurityEvent]:
    """Get unresolved security events with optional filtering"""
    query = select(SecurityEvent).where(SecurityEvent.resolved == False)
    
    if user_id:
        query = query.where(SecurityEvent.user_id == user_id)
    
    if severity:
        query = query.where(SecurityEvent.severity == severity)
    
    query = query.order_by(SecurityEvent.timestamp.desc())
    
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_statistics(session: AsyncSession, user_id: int) -> Dict[str, Any]:
    """Get comprehensive statistics for a user"""
    
    # Count active connections
    active_connections = await session.execute(
        select(func.count(ServiceConnection.id)).where(
            and_(
                ServiceConnection.user_id == user_id,
                ServiceConnection.is_active == True
            )
        )
    )
    
    # Count total actions
    total_actions = await session.execute(
        select(func.count(AgentAction.id)).where(AgentAction.user_id == user_id)
    )
    
    # Count recent audit logs (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_logs = await session.execute(
        select(func.count(AuditLog.id)).where(
            and_(
                AuditLog.user_id == user_id,
                AuditLog.timestamp >= thirty_days_ago
            )
        )
    )
    
    # Count unresolved security events
    security_events = await session.execute(
        select(func.count(SecurityEvent.id)).where(
            and_(
                SecurityEvent.user_id == user_id,
                SecurityEvent.resolved == False
            )
        )
    )
    
    return {
        "active_connections": active_connections.scalar() or 0,
        "total_actions": total_actions.scalar() or 0,
        "recent_activity_count": recent_logs.scalar() or 0,
        "unresolved_security_events": security_events.scalar() or 0,
    }


async def cleanup_expired_connections(session: AsyncSession) -> int:
    """Clean up expired service connections and return count of cleaned up connections"""
    from sqlalchemy import update
    
    # Mark expired connections as inactive
    result = await session.execute(
        update(ServiceConnection)
        .where(
            and_(
                ServiceConnection.expires_at < func.now(),
                ServiceConnection.is_active == True
            )
        )
        .values(is_active=False)
    )
    
    return result.rowcount