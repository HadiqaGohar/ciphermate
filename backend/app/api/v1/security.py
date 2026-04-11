"""
Security monitoring and management endpoints
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from ...core.auth import get_current_user
from ...core.security_monitor import security_monitor, security_metrics
from ...core.audit_service import audit_service
from ...core.exceptions import CipherMateException

router = APIRouter(prefix="/security", tags=["security"])
    # // done hadiqa


class SecurityStatusResponse(BaseModel):
    """Security monitoring status response"""
    blocked_ips: int
    suspicious_ips: int
    monitored_ips: Dict[str, int]
    thresholds: Dict[str, Any]
    metrics: Dict[str, Any]


class SecurityEventResponse(BaseModel):
    """Security event response"""
    id: int
    event_type: str
    severity: str
    details: Dict[str, Any]
    ip_address: Optional[str]
    timestamp: datetime
    resolved: bool


class SecurityMetricsResponse(BaseModel):
    """Security metrics response"""
    requests_blocked: int
    threats_detected: int
    ips_blocked: int
    security_events: Dict[str, int]
    attack_types: Dict[str, int]


@router.get("/status", response_model=SecurityStatusResponse)
async def get_security_status(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current security monitoring status
    Requires admin privileges
    """
    # Check if user has admin privileges (you may need to implement role checking)
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        status_data = security_monitor.get_security_status()
        metrics_data = security_metrics.get_metrics()
        
        return SecurityStatusResponse(
            blocked_ips=status_data["blocked_ips"],
            suspicious_ips=status_data["suspicious_ips"],
            monitored_ips=status_data["monitored_ips"],
            thresholds=status_data["thresholds"],
            metrics=metrics_data
        )
    except Exception as e:
        raise CipherMateException(
            message="Failed to retrieve security status",
            details={"error": str(e)}
        )


@router.get("/events", response_model=List[SecurityEventResponse])
async def get_security_events(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    severity: Optional[str] = Query(None, pattern="^(info|warning|high|critical)$"),
    event_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """
    Get security events with filtering
    Requires admin privileges
    """
    # Check if user has admin privileges
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        if not audit_service:
            raise CipherMateException(
                message="Audit service not available",
                details={"service": "audit_service"}
            )
        
        # Get security events from audit service
        events = await audit_service.get_security_events(
            limit=limit,
            offset=offset,
            severity=severity,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date
        )
        
        return [
            SecurityEventResponse(
                id=event.id,
                event_type=event.event_type,
                severity=event.severity,
                details=event.details or {},
                ip_address=event.ip_address,
                timestamp=event.timestamp,
                resolved=event.resolved
            )
            for event in events
        ]
    except Exception as e:
        raise CipherMateException(
            message="Failed to retrieve security events",
            details={"error": str(e)}
        )


@router.get("/metrics", response_model=SecurityMetricsResponse)
async def get_security_metrics(
    current_user: dict = Depends(get_current_user)
):
    """
    Get security metrics
    Requires admin privileges
    """
    # Check if user has admin privileges
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        metrics = security_metrics.get_metrics()
        
        return SecurityMetricsResponse(
            requests_blocked=metrics["requests_blocked"],
            threats_detected=metrics["threats_detected"],
            ips_blocked=metrics["ips_blocked"],
            security_events=metrics["security_events"],
            attack_types=metrics["attack_types"]
        )
    except Exception as e:
        raise CipherMateException(
            message="Failed to retrieve security metrics",
            details={"error": str(e)}
        )


@router.post("/events/{event_id}/resolve")
async def resolve_security_event(
    event_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark a security event as resolved
    Requires admin privileges
    """
    # Check if user has admin privileges
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        if not audit_service:
            raise CipherMateException(
                message="Audit service not available",
                details={"service": "audit_service"}
            )
        
        # Resolve the security event
        success = await audit_service.resolve_security_event(event_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Security event not found"
            )
        
        # Log the resolution action
        await audit_service.log_action(
            user_id=int(current_user.get("sub", 0)),
            action="resolve_security_event",
            details={"event_id": event_id},
            ip_address=None  # Will be filled by middleware
        )
        
        return {"message": "Security event resolved successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise CipherMateException(
            message="Failed to resolve security event",
            details={"error": str(e), "event_id": event_id}
        )


@router.post("/ip/{ip_address}/unblock")
async def unblock_ip_address(
    ip_address: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Manually unblock an IP address
    Requires admin privileges
    """
    # Check if user has admin privileges
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        # Validate IP address format
        import ipaddress
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid IP address format"
            )
        
        # Remove from blocked and suspicious lists
        security_monitor.blocked_ips.discard(ip_address)
        security_monitor.suspicious_ips.discard(ip_address)
        
        # Log the unblock action
        if audit_service:
            await audit_service.log_security_event(
                user_id=int(current_user.get("sub", 0)),
                event_type="manual_ip_unblock",
                severity="info",
                details={
                    "ip_address": ip_address,
                    "admin_user": current_user.get("email", "unknown")
                },
                ip_address=ip_address
            )
        
        return {"message": f"IP address {ip_address} has been unblocked"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise CipherMateException(
            message="Failed to unblock IP address",
            details={"error": str(e), "ip_address": ip_address}
        )


@router.post("/metrics/reset")
async def reset_security_metrics(
    current_user: dict = Depends(get_current_user)
):
    """
    Reset security metrics counters
    Requires admin privileges
    """
    # Check if user has admin privileges
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    try:
        # Reset metrics
        security_metrics.reset_metrics()
        
        # Log the reset action
        if audit_service:
            await audit_service.log_action(
                user_id=int(current_user.get("sub", 0)),
                action="reset_security_metrics",
                details={"admin_user": current_user.get("email", "unknown")},
                ip_address=None  # Will be filled by middleware
            )
        
        return {"message": "Security metrics have been reset"}
    
    except Exception as e:
        raise CipherMateException(
            message="Failed to reset security metrics",
            details={"error": str(e)}
        )


@router.get("/health")
async def security_health_check():
    """
    Security service health check
    Public endpoint for monitoring
    """
    try:
        # Check if security monitor is running
        status_data = security_monitor.get_security_status()
        
        # Check if audit service is available
        audit_available = audit_service is not None
        
        return {
            "status": "healthy",
            "security_monitor": "active",
            "audit_service": "active" if audit_available else "unavailable",
            "blocked_ips": status_data["blocked_ips"],
            "suspicious_ips": status_data["suspicious_ips"]
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }