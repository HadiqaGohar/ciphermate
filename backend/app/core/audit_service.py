"""Comprehensive audit logging service for CipherMate platform"""

import asyncio
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from fastapi import Request
import logging

from app.models.audit_log import AuditLog
from app.models.security_event import SecurityEvent
from app.models.agent_action import AgentAction
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class AuditService:
    """Centralized audit logging service"""
    
    # Action types for consistent logging
    ACTION_TYPES = {
        # Authentication actions
        "LOGIN": "login",
        "LOGOUT": "logout",
        "TOKEN_REFRESH": "token_refresh",
        "AUTH_FAILURE": "auth_failure",
        
        # Permission actions
        "PERMISSION_GRANTED": "permission_granted",
        "PERMISSION_REVOKED": "permission_revoked",
        "PERMISSION_REQUEST": "permission_request",
        "PERMISSION_DENIED": "permission_denied",
        
        # API actions
        "API_CALL": "api_call",
        "API_ERROR": "api_error",
        "API_RATE_LIMITED": "api_rate_limited",
        
        # Agent actions
        "AGENT_REQUEST": "agent_request",
        "AGENT_ACTION": "agent_action",
        "AGENT_ERROR": "agent_error",
        
        # Security actions
        "SECURITY_VIOLATION": "security_violation",
        "SUSPICIOUS_ACTIVITY": "suspicious_activity",
        "DATA_ACCESS": "data_access",
        "DATA_EXPORT": "data_export",
        
        # System actions
        "SYSTEM_ERROR": "system_error",
        "PERFORMANCE_ISSUE": "performance_issue",
    }
    
    # Security event types
    SECURITY_EVENT_TYPES = {
        "FAILED_LOGIN": "failed_login",
        "MULTIPLE_FAILED_LOGINS": "multiple_failed_logins",
        "SUSPICIOUS_IP": "suspicious_ip",
        "TOKEN_THEFT_ATTEMPT": "token_theft_attempt",
        "UNAUTHORIZED_ACCESS": "unauthorized_access",
        "PERMISSION_ESCALATION": "permission_escalation",
        "DATA_BREACH_ATTEMPT": "data_breach_attempt",
        "RATE_LIMIT_EXCEEDED": "rate_limit_exceeded",
    }
    
    def __init__(self):
        self._performance_metrics = {}
        self._failed_login_attempts = {}
    
    async def log_action(
        self,
        user_id: int,
        action_type: str,
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        request: Optional[Request] = None
    ) -> Optional[AuditLog]:
        """Log a user action with comprehensive details"""
        try:
            # Extract request information if provided
            if request:
                ip_address = ip_address or self._get_client_ip(request)
                user_agent = user_agent or request.headers.get("user-agent")
                session_id = session_id or request.headers.get("x-session-id")
            
            async with AsyncSessionLocal() as db:
                audit_log = AuditLog.create_log(
                    user_id=user_id,
                    action_type=action_type,
                    service_name=service_name,
                    details=details or {},
                    ip_address=ip_address,
                    user_agent=user_agent,
                    session_id=session_id
                )
                
                db.add(audit_log)
                await db.commit()
                await db.refresh(audit_log)
                
                logger.info(f"Audit log created: {audit_log.id} - {action_type} by user {user_id}")
                return audit_log
                
        except Exception as e:
            logger.error(f"Failed to create audit log: {e}")
            return None
    
    async def log_security_event(
        self,
        user_id: int,
        event_type: str,
        severity: str = "info",
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        request: Optional[Request] = None
    ) -> Optional[SecurityEvent]:
        """Log a security event"""
        try:
            if request:
                ip_address = ip_address or self._get_client_ip(request)
            
            async with AsyncSessionLocal() as db:
                security_event = SecurityEvent.create_event(
                    user_id=user_id,
                    event_type=event_type,
                    severity=severity,
                    details=details or {},
                    ip_address=ip_address
                )
                
                db.add(security_event)
                await db.commit()
                await db.refresh(security_event)
                
                logger.warning(f"Security event logged: {security_event.id} - {event_type} (severity: {severity})")
                
                # Handle critical security events
                if severity == "critical":
                    await self._handle_critical_security_event(security_event)
                
                return security_event
                
        except Exception as e:
            logger.error(f"Failed to create security event log: {e}")
            return None
    
    async def log_performance_metric(
        self,
        user_id: int,
        operation: str,
        duration_ms: float,
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log performance metrics for operations"""
        try:
            metric_details = {
                "operation": operation,
                "duration_ms": duration_ms,
                "service_name": service_name,
                **(details or {})
            }
            
            await self.log_action(
                user_id=user_id,
                action_type="performance_metric",
                service_name=service_name,
                details=metric_details
            )
            
            # Store in memory for real-time monitoring
            key = f"{operation}:{service_name or 'system'}"
            if key not in self._performance_metrics:
                self._performance_metrics[key] = []
            
            self._performance_metrics[key].append({
                "timestamp": datetime.now(timezone.utc),
                "duration_ms": duration_ms,
                "user_id": user_id
            })
            
            # Keep only last 100 metrics per operation
            self._performance_metrics[key] = self._performance_metrics[key][-100:]
            
        except Exception as e:
            logger.error(f"Failed to log performance metric: {e}")
    
    async def get_audit_logs(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        action_type: Optional[str] = None,
        service_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AuditLog]:
        """Retrieve audit logs with filtering"""
        try:
            async with AsyncSessionLocal() as db:
                query = select(AuditLog).where(AuditLog.user_id == user_id)
                
                if action_type:
                    query = query.where(AuditLog.action_type == action_type)
                
                if service_name:
                    query = query.where(AuditLog.service_name == service_name)
                
                if start_date:
                    query = query.where(AuditLog.timestamp >= start_date)
                
                if end_date:
                    query = query.where(AuditLog.timestamp <= end_date)
                
                query = query.order_by(desc(AuditLog.timestamp)).offset(offset).limit(limit)
                
                result = await db.execute(query)
                return result.scalars().all()
                
        except Exception as e:
            logger.error(f"Failed to retrieve audit logs: {e}")
            return []
    
    async def get_security_events(
        self,
        limit: int = 50,
        offset: int = 0,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[SecurityEvent]:
        """Retrieve security events with filtering (admin method)"""
        try:
            async with AsyncSessionLocal() as db:
                query = select(SecurityEvent)
                
                if event_type:
                    query = query.where(SecurityEvent.event_type == event_type)
                
                if severity:
                    query = query.where(SecurityEvent.severity == severity)
                
                if start_date:
                    query = query.where(SecurityEvent.timestamp >= start_date)
                
                if end_date:
                    query = query.where(SecurityEvent.timestamp <= end_date)
                
                query = query.order_by(desc(SecurityEvent.timestamp)).offset(offset).limit(limit)
                
                result = await db.execute(query)
                return result.scalars().all()
                
        except Exception as e:
            logger.error(f"Failed to retrieve security events: {e}")
            return []
    
    async def resolve_security_event(self, event_id: int) -> bool:
        """Mark a security event as resolved"""
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(SecurityEvent).where(SecurityEvent.id == event_id)
                )
                event = result.scalar_one_or_none()
                
                if event:
                    event.resolved = True
                    await db.commit()
                    logger.info(f"Security event {event_id} marked as resolved")
                    return True
                else:
                    logger.warning(f"Security event {event_id} not found")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to resolve security event {event_id}: {e}")
            return False
    
    async def get_audit_summary(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get audit summary for the specified number of days"""
        try:
            start_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            async with AsyncSessionLocal() as db:
                # Get action counts by type
                action_counts = await db.execute(
                    select(
                        AuditLog.action_type,
                        func.count(AuditLog.id).label('count')
                    )
                    .where(
                        and_(
                            AuditLog.user_id == user_id,
                            AuditLog.timestamp >= start_date
                        )
                    )
                    .group_by(AuditLog.action_type)
                )
                
                # Get service usage counts
                service_counts = await db.execute(
                    select(
                        AuditLog.service_name,
                        func.count(AuditLog.id).label('count')
                    )
                    .where(
                        and_(
                            AuditLog.user_id == user_id,
                            AuditLog.timestamp >= start_date,
                            AuditLog.service_name.isnot(None)
                        )
                    )
                    .group_by(AuditLog.service_name)
                )
                
                # Get security event counts
                security_counts = await db.execute(
                    select(
                        SecurityEvent.event_type,
                        SecurityEvent.severity,
                        func.count(SecurityEvent.id).label('count')
                    )
                    .where(
                        and_(
                            SecurityEvent.user_id == user_id,
                            SecurityEvent.timestamp >= start_date
                        )
                    )
                    .group_by(SecurityEvent.event_type, SecurityEvent.severity)
                )
                
                return {
                    "period_days": days,
                    "start_date": start_date.isoformat(),
                    "action_counts": {row.action_type: row.count for row in action_counts},
                    "service_usage": {row.service_name: row.count for row in service_counts},
                    "security_events": [
                        {
                            "event_type": row.event_type,
                            "severity": row.severity,
                            "count": row.count
                        }
                        for row in security_counts
                    ]
                }
                
        except Exception as e:
            logger.error(f"Failed to get audit summary: {e}")
            return {}
    
    async def track_failed_login(self, ip_address: str, user_identifier: str) -> None:
        """Track failed login attempts for security monitoring"""
        key = f"{ip_address}:{user_identifier}"
        current_time = datetime.now(timezone.utc)
        
        if key not in self._failed_login_attempts:
            self._failed_login_attempts[key] = []
        
        # Add current attempt
        self._failed_login_attempts[key].append(current_time)
        
        # Remove attempts older than 1 hour
        one_hour_ago = current_time - timedelta(hours=1)
        self._failed_login_attempts[key] = [
            attempt for attempt in self._failed_login_attempts[key]
            if attempt > one_hour_ago
        ]
        
        # Check for suspicious activity
        recent_attempts = len(self._failed_login_attempts[key])
        if recent_attempts >= 5:
            # Log security event for multiple failed logins
            await self.log_security_event(
                user_id=0,  # System user for security events
                event_type=self.SECURITY_EVENT_TYPES["MULTIPLE_FAILED_LOGINS"],
                severity="warning",
                details={
                    "ip_address": ip_address,
                    "user_identifier": user_identifier,
                    "attempt_count": recent_attempts,
                    "time_window": "1 hour"
                },
                ip_address=ip_address
            )
    
    def get_performance_metrics(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """Get current performance metrics"""
        if operation:
            metrics = {k: v for k, v in self._performance_metrics.items() if k.startswith(operation)}
        else:
            metrics = self._performance_metrics
        
        # Calculate averages and statistics
        result = {}
        for key, values in metrics.items():
            if values:
                durations = [v["duration_ms"] for v in values]
                result[key] = {
                    "count": len(durations),
                    "avg_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "recent_count": len([v for v in values if v["timestamp"] > datetime.now(timezone.utc) - timedelta(minutes=5)])
                }
        
        return result
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    async def _handle_critical_security_event(self, event: SecurityEvent) -> None:
        """Handle critical security events with immediate actions"""
        logger.critical(f"Critical security event detected: {event.event_type} for user {event.user_id}")
        
        # Here you could implement additional actions like:
        # - Send alerts to administrators
        # - Temporarily lock user accounts
        # - Trigger additional security measures
        # - Send notifications to security monitoring systems
        
        # For now, just log the critical event
        pass


# Global audit service instance
audit_service = AuditService()


class PerformanceTracker:
    """Context manager for tracking operation performance"""
    
    def __init__(
        self,
        user_id: int,
        operation: str,
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.operation = operation
        self.service_name = service_name
        self.details = details
        self.start_time = None
    
    async def __aenter__(self):
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            await audit_service.log_performance_metric(
                user_id=self.user_id,
                operation=self.operation,
                duration_ms=duration_ms,
                service_name=self.service_name,
                details=self.details
            )