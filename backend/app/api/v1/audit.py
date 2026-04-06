"""Audit log API endpoints"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from ...core.database import get_db
from ...models.audit_log import AuditLog
from ...models.security_event import SecurityEvent
from ...core.auth import get_current_user

router = APIRouter(prefix="/audit", tags=["audit"])
logger = logging.getLogger(__name__)

@router.get("/logs")
async def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action_type: Optional[str] = None,
    service_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get audit logs for the current user"""
    try:
        # Build query
        query = select(AuditLog).where(AuditLog.user_id == current_user.id)
        
        # Apply filters
        if action_type:
            query = query.where(AuditLog.action_type == action_type)
        if service_name:
            query = query.where(AuditLog.service_name == service_name)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(AuditLog.timestamp.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        logs = result.scalars().all()
        
        # Convert to dict format
        logs_data = []
        for log in logs:
            logs_data.append({
                "id": log.id,
                "user_id": log.user_id,
                "action_type": log.action_type,
                "service_name": log.service_name,
                "details": log.details,
                "timestamp": log.timestamp.isoformat() + "Z",
                "ip_address": log.ip_address,
                "user_agent": log.user_agent
            })
        
        return {
            "logs": logs_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_audit_summary(
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get audit statistics summary for the current user"""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        # Get action counts
        action_query = select(
            AuditLog.action_type,
            func.count(AuditLog.id).label('count')
        ).where(
            and_(
                AuditLog.user_id == current_user.id,
                AuditLog.timestamp >= start_date
            )
        ).group_by(AuditLog.action_type)
        
        action_result = await db.execute(action_query)
        action_counts = {row.action_type.lower(): row.count for row in action_result}
        
        # Get service usage
        service_query = select(
            AuditLog.service_name,
            func.count(AuditLog.id).label('count')
        ).where(
            and_(
                AuditLog.user_id == current_user.id,
                AuditLog.timestamp >= start_date
            )
        ).group_by(AuditLog.service_name)
        
        service_result = await db.execute(service_query)
        service_usage = {row.service_name: row.count for row in service_result}
        
        # Get security events
        security_query = select(
            SecurityEvent.event_type,
            SecurityEvent.severity,
            func.count(SecurityEvent.id).label('count'),
            func.sum(func.case((SecurityEvent.resolved == True, 1), else_=0)).label('resolved_count')
        ).where(
            and_(
                SecurityEvent.user_id == current_user.id,
                SecurityEvent.timestamp >= start_date
            )
        ).group_by(SecurityEvent.event_type, SecurityEvent.severity)
        
        security_result = await db.execute(security_query)
        security_events = []
        for row in security_result:
            security_events.append({
                "event_type": row.event_type,
                "severity": row.severity,
                "count": row.count,
                "resolved_count": row.resolved_count or 0
            })
        
        return {
            "period_days": days,
            "start_date": start_date.date().isoformat(),
            "action_counts": action_counts,
            "service_usage": service_usage,
            "security_events": security_events
        }
    except Exception as e:
        logger.error(f"Error getting audit summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_audit_logs(
    format: str = Query("csv", pattern="^(csv|json)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Export audit logs in CSV or JSON format"""
    try:
        # Build query for user's logs
        query = select(AuditLog).where(AuditLog.user_id == current_user.id)
        
        # Apply date filters if provided
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.where(AuditLog.timestamp >= start_dt)
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.where(AuditLog.timestamp <= end_dt)
        
        # Get count
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total_records = count_result.scalar()
        
        return {
            "message": f"Audit logs exported in {format} format",
            "download_url": f"/api/v1/audit/download/{format}",
            "total_records": total_records,
            "generated_at": datetime.now().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error exporting audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/security-events")
async def get_security_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get security-related audit events for the current user"""
    try:
        # Build query
        query = select(SecurityEvent).where(SecurityEvent.user_id == current_user.id)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(SecurityEvent.timestamp.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        events = result.scalars().all()
        
        # Convert to dict format
        events_data = []
        for event in events:
            events_data.append({
                "id": event.id,
                "event_type": event.event_type,
                "severity": event.severity,
                "user_id": event.user_id,
                "description": event.description,
                "timestamp": event.timestamp.isoformat() + "Z",
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "details": event.details,
                "resolved": event.resolved
            })
        
        return {
            "events": events_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "total_count": total,
            "has_next": (page * page_size) < total
        }
    except Exception as e:
        logger.error(f"Error getting security events: {e}")
        raise HTTPException(status_code=500, detail=str(e))