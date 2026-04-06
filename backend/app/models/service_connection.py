"""Service connection model for managing third-party service integrations"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ServiceConnection(Base):
    """Model for tracking user connections to third-party services"""

    __tablename__ = "service_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    service_name = Column(String(50), nullable=False, index=True)
    token_vault_id = Column(String(255), nullable=False, index=True)  # Auth0 Token Vault reference
    scopes = Column(JSON, default=list)  # Array of granted permissions
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    last_used_at = Column(DateTime(timezone=True))
    metadata_json = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="service_connections")
    
    def __repr__(self) -> str:
        return f"<ServiceConnection(id={self.id}, user_id={self.user_id}, service='{self.service_name}', active={self.is_active})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if the service connection has expired"""
        if not self.expires_at:
            return False
        return self.expires_at < func.now()
    
    def update_last_used(self) -> None:
        """Update the last used timestamp"""
        self.last_used_at = func.now()