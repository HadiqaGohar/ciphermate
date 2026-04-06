#!/usr/bin/env python3
"""Simple test script to verify database models work correctly"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.service_connection import ServiceConnection
from app.models.audit_log import AuditLog
from app.models.agent_action import AgentAction
from app.models.permission_template import PermissionTemplate
from app.models.security_event import SecurityEvent
from app.db.utils import (
    get_user_by_auth0_id,
    create_audit_log,
    create_security_event,
    get_user_statistics
)


async def test_models():
    """Test basic model operations"""
    print("🧪 Testing database models...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Test User model
            print("  ✓ Testing User model...")
            user = User(
                auth0_id="test|123456789",
                email="test@example.com",
                name="Test User",
                preferences={"theme": "dark", "notifications": True}
            )
            session.add(user)
            await session.flush()
            
            # Test ServiceConnection model
            print("  ✓ Testing ServiceConnection model...")
            connection = ServiceConnection(
                user_id=user.id,
                service_name="google",
                token_vault_id="vault_123",
                scopes=["calendar.read", "calendar.write"],
                metadata={"client_id": "test_client"}
            )
            session.add(connection)
            await session.flush()
            
            # Test AuditLog model
            print("  ✓ Testing AuditLog model...")
            audit_log = await create_audit_log(
                session=session,
                user_id=user.id,
                action_type="service_connected",
                service_name="google",
                details={"scopes": ["calendar.read"]},
                ip_address="192.168.1.1"
            )
            
            # Test AgentAction model
            print("  ✓ Testing AgentAction model...")
            action = AgentAction(
                user_id=user.id,
                action="create_calendar_event",
                parameters={"title": "Test Event", "date": "2024-03-26"},
                status="pending"
            )
            session.add(action)
            await session.flush()
            
            # Test PermissionTemplate model
            print("  ✓ Testing PermissionTemplate model...")
            template = PermissionTemplate(
                service_name="google",
                scope_name="calendar.read",
                description="Read calendar events",
                risk_level="low",
                requires_step_up=False
            )
            session.add(template)
            await session.flush()
            
            # Test SecurityEvent model
            print("  ✓ Testing SecurityEvent model...")
            security_event = await create_security_event(
                session=session,
                user_id=user.id,
                event_type="login_attempt",
                severity="info",
                details={"success": True},
                ip_address="192.168.1.1"
            )
            
            # Test utility functions
            print("  ✓ Testing utility functions...")
            found_user = await get_user_by_auth0_id(session, "test|123456789")
            assert found_user is not None
            assert found_user.email == "test@example.com"
            
            stats = await get_user_statistics(session, user.id)
            assert isinstance(stats, dict)
            assert "active_connections" in stats
            
            # Test model methods
            print("  ✓ Testing model methods...")
            action.mark_executing()
            assert action.status == "executing"
            
            action.mark_completed("Event created successfully", 150)
            assert action.status == "completed"
            assert action.result == "Event created successfully"
            
            security_event.mark_resolved()
            assert security_event.resolved == True
            
            # Test relationships
            print("  ✓ Testing relationships...")
            await session.refresh(user, ["service_connections", "audit_logs", "agent_actions"])
            assert len(user.service_connections) == 1
            assert len(user.audit_logs) == 1
            assert len(user.agent_actions) == 1
            
            print("✅ All model tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise
        finally:
            # Clean up - rollback the transaction
            await session.rollback()


async def main():
    """Main test function"""
    try:
        await test_models()
        print("\n🎉 Database models are working correctly!")
    except Exception as e:
        print(f"\n💥 Tests failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())