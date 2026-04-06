"""Permission template model for defining service permissions"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base


class PermissionTemplate(Base):
    """Model for defining permission templates for different services"""
    
    __tablename__ = "permission_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(50), nullable=False, index=True)
    scope_name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    risk_level = Column(String(20), default="medium", index=True)  # low, medium, high, critical
    requires_step_up = Column(Boolean, default=False, index=True)
    
    def __repr__(self) -> str:
        return f"<PermissionTemplate(id={self.id}, service='{self.service_name}', scope='{self.scope_name}', risk='{self.risk_level}')>"
    
    @property
    def is_high_risk(self) -> bool:
        """Check if this permission is considered high risk"""
        return self.risk_level in ["high", "critical"]
    
    @property
    def is_critical(self) -> bool:
        """Check if this permission is critical and requires special handling"""
        return self.risk_level == "critical"