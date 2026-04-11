"""Security event model for tracking security-related incidents"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SecurityEvent(Base):
    """Model for tracking security events and incidents"""

    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Nullable for system-level events
    event_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), default="info", index=True)  # info, warning, error, critical
    description = Column(Text, nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45))
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved = Column(Boolean, default=False, index=True)

    # Relationships
    user = relationship("User", back_populates="security_events")

    def __repr__(self) -> str:
        return f"<SecurityEvent(id={self.id}, user_id={self.user_id}, type='{self.event_type}', severity='{self.severity}')>"

    def mark_resolved(self) -> None:
        """Mark the security event as resolved"""
        self.resolved = True

    @property
    def is_critical(self) -> bool:
        """Check if this is a critical security event"""
        return self.severity == "critical"

    @property
    def requires_attention(self) -> bool:
        """Check if this event requires immediate attention"""
        return self.severity in ["error", "critical"] and not self.resolved

    @classmethod
    def create_event(
        cls,
        user_id: int,
        event_type: str,
        severity: str = "info",
        details: dict = None,
        ip_address: str = None,
        user_agent: str = None,
        description: str = None
    ) -> "SecurityEvent":
        """Factory method to create security event entries"""
        return cls(
            user_id=user_id,
            event_type=event_type,
            severity=severity,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            description=description or f"{event_type} - {severity} severity"
        )