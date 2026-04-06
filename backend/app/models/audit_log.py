"""Audit log model for comprehensive activity tracking"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuditLog(Base):
    """Model for comprehensive audit logging of all user actions"""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True)
    service_name = Column(String(50), index=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String(255), index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action='{self.action_type}', service='{self.service_name}')>"
    
    @classmethod
    def create_log(
        cls,
        user_id: int,
        action_type: str,
        service_name: str = None,
        details: dict = None,
        ip_address: str = None,
        user_agent: str = None,
        session_id: str = None
    ) -> "AuditLog":
        """Factory method to create audit log entries"""
        return cls(
            user_id=user_id,
            action_type=action_type,
            service_name=service_name,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )