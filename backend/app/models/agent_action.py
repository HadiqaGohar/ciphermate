"""Agent action model for tracking AI agent operations"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class AgentAction(Base):
    """Model for tracking AI agent actions and their execution status"""

    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    parameters = Column(JSON, default=dict)
    status = Column(String(20), default="pending", index=True)  # pending, executing, completed, failed
    result = Column(Text)
    requires_step_up = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    executed_at = Column(DateTime(timezone=True))
    execution_time_ms = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="agent_actions")
    
    def __repr__(self) -> str:
        return f"<AgentAction(id={self.id}, user_id={self.user_id}, action='{self.action}', status='{self.status}')>"
    
    def mark_executing(self) -> None:
        """Mark the action as currently executing"""
        self.status = "executing"
        self.executed_at = func.now()
    
    def mark_completed(self, result: str = None, execution_time_ms: int = None) -> None:
        """Mark the action as completed with optional result and timing"""
        self.status = "completed"
        if result:
            self.result = result
        if execution_time_ms:
            self.execution_time_ms = execution_time_ms
    
    def mark_failed(self, error_message: str) -> None:
        """Mark the action as failed with error message"""
        self.status = "failed"
        self.result = error_message
    
    @property
    def is_pending(self) -> bool:
        """Check if the action is still pending"""
        return self.status == "pending"
    
    @property
    def is_completed(self) -> bool:
        """Check if the action has completed successfully"""
        return self.status == "completed"
    
    @property
    def is_failed(self) -> bool:
        """Check if the action has failed"""
        return self.status == "failed"