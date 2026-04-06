"""Unit tests for database operations"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.service_connection import ServiceConnection
from app.models.audit_log import AuditLog
from app.models.agent_action import AgentAction
from app.models.security_event import SecurityEvent
from app.models.permission_template import PermissionTemplate


class TestUserModel:
    """Test cases for User model operations"""

    @pytest.mark.asyncio
    async def test_create_user(self, test_db: AsyncSession):
        """Test user creation"""
        user = User(
            auth0_id="auth0|test123",
            email="test@example.com",
            name="Test User",
            preferences={"theme": "dark", "notifications": True}
        )
        
        test_db.add(user)
        await test_db.commit()
        await test_db.refresh(user)
        
        assert user.id is not None
        assert user.auth0_id == "auth0|test123"
        assert user.email == "test@example.com"
        assert user.preferences["theme"] == "dark"

    @pytest.mark.asyncio
    async def test_find_user_by_auth0_id(self, test_db: AsyncSession):
        """Test finding user by Auth0 ID"""
        # Create user
        user = User(
            auth0_id="auth0|findme123",
            email="findme@example.com",
            name="Find Me User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Find user
        result = await test_db.execute(
            select(User).where(User.auth0_id == "auth0|findme123")
        )
        found_user = result.scalar_one_or_none()
        
        assert found_user is not None
        assert found_user.email == "findme@example.com"

    @pytest.mark.asyncio
    async def test_update_user_preferences(self, test_db: AsyncSession):
        """Test updating user preferences"""
        user = User(
            auth0_id="auth0|update123",
            email="update@example.com",
            name="Update User",
            preferences={"theme": "light"}
        )
        test_db.add(user)
        await test_db.commit()
        
        # Update preferences
        user.preferences = {"theme": "dark", "language": "en"}
        await test_db.commit()
        await test_db.refresh(user)
        
        assert user.preferences["theme"] == "dark"
        assert user.preferences["language"] == "en"

    @pytest.mark.asyncio
    async def test_update_last_login(self, test_db: AsyncSession):
        """Test updating user last login timestamp"""
        user = User(
            auth0_id="auth0|login123",
            email="login@example.com",
            name="Login User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Update last login
        login_time = datetime.now(timezone.utc)
        user.last_login = login_time
        await test_db.commit()
        await test_db.refresh(user)
        
        assert user.last_login == login_time


class TestServiceConnectionModel:
    """Test cases for ServiceConnection model operations"""

    @pytest.mark.asyncio
    async def test_create_service_connection(self, test_db: AsyncSession):
        """Test service connection creation"""
        # Create user first
        user = User(
            auth0_id="auth0|service123",
            email="service@example.com",
            name="Service User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create service connection
        connection = ServiceConnection(
            user_id=user.id,
            service_name="google",
            token_vault_id="vault_123",
            scopes=["calendar.events", "calendar.readonly"],
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            metadata={"client_id": "google_client_123"}
        )
        
        test_db.add(connection)
        await test_db.commit()
        await test_db.refresh(connection)
        
        assert connection.id is not None
        assert connection.service_name == "google"
        assert "calendar.events" in connection.scopes
        assert connection.is_active is True

    @pytest.mark.asyncio
    async def test_find_user_connections(self, test_db: AsyncSession):
        """Test finding all connections for a user"""
        # Create user
        user = User(
            auth0_id="auth0|multi123",
            email="multi@example.com",
            name="Multi User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create multiple connections
        google_conn = ServiceConnection(
            user_id=user.id,
            service_name="google",
            token_vault_id="vault_google",
            scopes=["calendar.events"]
        )
        
        github_conn = ServiceConnection(
            user_id=user.id,
            service_name="github",
            token_vault_id="vault_github",
            scopes=["repo", "user"]
        )
        
        test_db.add_all([google_conn, github_conn])
        await test_db.commit()
        
        # Find all connections
        result = await test_db.execute(
            select(ServiceConnection).where(ServiceConnection.user_id == user.id)
        )
        connections = result.scalars().all()
        
        assert len(connections) == 2
        service_names = [conn.service_name for conn in connections]
        assert "google" in service_names
        assert "github" in service_names

    @pytest.mark.asyncio
    async def test_deactivate_connection(self, test_db: AsyncSession):
        """Test deactivating a service connection"""
        user = User(
            auth0_id="auth0|deactivate123",
            email="deactivate@example.com",
            name="Deactivate User"
        )
        test_db.add(user)
        await test_db.commit()
        
        connection = ServiceConnection(
            user_id=user.id,
            service_name="slack",
            token_vault_id="vault_slack",
            scopes=["chat:write"]
        )
        test_db.add(connection)
        await test_db.commit()
        
        # Deactivate connection
        connection.is_active = False
        await test_db.commit()
        await test_db.refresh(connection)
        
        assert connection.is_active is False

    @pytest.mark.asyncio
    async def test_update_last_used(self, test_db: AsyncSession):
        """Test updating connection last used timestamp"""
        user = User(
            auth0_id="auth0|lastused123",
            email="lastused@example.com",
            name="Last Used User"
        )
        test_db.add(user)
        await test_db.commit()
        
        connection = ServiceConnection(
            user_id=user.id,
            service_name="google",
            token_vault_id="vault_google",
            scopes=["calendar.events"]
        )
        test_db.add(connection)
        await test_db.commit()
        
        # Update last used
        used_time = datetime.now(timezone.utc)
        connection.last_used_at = used_time
        await test_db.commit()
        await test_db.refresh(connection)
        
        assert connection.last_used_at == used_time


class TestAuditLogModel:
    """Test cases for AuditLog model operations"""

    @pytest.mark.asyncio
    async def test_create_audit_log(self, test_db: AsyncSession):
        """Test audit log creation"""
        user = User(
            auth0_id="auth0|audit123",
            email="audit@example.com",
            name="Audit User"
        )
        test_db.add(user)
        await test_db.commit()
        
        audit_log = AuditLog(
            user_id=user.id,
            action_type="calendar_create_event",
            service_name="google",
            details={
                "event_title": "Test Meeting",
                "start_time": "2024-01-01T10:00:00Z"
            },
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0...",
            session_id="session_123"
        )
        
        test_db.add(audit_log)
        await test_db.commit()
        await test_db.refresh(audit_log)
        
        assert audit_log.id is not None
        assert audit_log.action_type == "calendar_create_event"
        assert audit_log.details["event_title"] == "Test Meeting"

    @pytest.mark.asyncio
    async def test_find_user_audit_logs(self, test_db: AsyncSession):
        """Test finding audit logs for a user"""
        user = User(
            auth0_id="auth0|auditfind123",
            email="auditfind@example.com",
            name="Audit Find User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create multiple audit logs
        logs = [
            AuditLog(
                user_id=user.id,
                action_type="calendar_create_event",
                service_name="google",
                details={"event_id": "event1"}
            ),
            AuditLog(
                user_id=user.id,
                action_type="email_send",
                service_name="google",
                details={"to": "test@example.com"}
            )
        ]
        
        test_db.add_all(logs)
        await test_db.commit()
        
        # Find logs
        result = await test_db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user.id)
            .order_by(AuditLog.timestamp.desc())
        )
        found_logs = result.scalars().all()
        
        assert len(found_logs) == 2
        assert found_logs[0].action_type in ["calendar_create_event", "email_send"]

    @pytest.mark.asyncio
    async def test_filter_audit_logs_by_service(self, test_db: AsyncSession):
        """Test filtering audit logs by service"""
        user = User(
            auth0_id="auth0|auditfilter123",
            email="auditfilter@example.com",
            name="Audit Filter User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create logs for different services
        google_log = AuditLog(
            user_id=user.id,
            action_type="calendar_create_event",
            service_name="google",
            details={"event_id": "google_event"}
        )
        
        github_log = AuditLog(
            user_id=user.id,
            action_type="github_create_issue",
            service_name="github",
            details={"issue_id": "123"}
        )
        
        test_db.add_all([google_log, github_log])
        await test_db.commit()
        
        # Filter by Google service
        result = await test_db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user.id)
            .where(AuditLog.service_name == "google")
        )
        google_logs = result.scalars().all()
        
        assert len(google_logs) == 1
        assert google_logs[0].service_name == "google"


class TestAgentActionModel:
    """Test cases for AgentAction model operations"""

    @pytest.mark.asyncio
    async def test_create_agent_action(self, test_db: AsyncSession):
        """Test agent action creation"""
        user = User(
            auth0_id="auth0|action123",
            email="action@example.com",
            name="Action User"
        )
        test_db.add(user)
        await test_db.commit()
        
        action = AgentAction(
            user_id=user.id,
            action="calendar_create_event",
            parameters={
                "title": "AI Created Meeting",
                "start_time": "2024-01-01T10:00:00Z"
            },
            status="pending"
        )
        
        test_db.add(action)
        await test_db.commit()
        await test_db.refresh(action)
        
        assert action.id is not None
        assert action.action == "calendar_create_event"
        assert action.status == "pending"

    @pytest.mark.asyncio
    async def test_update_action_status(self, test_db: AsyncSession):
        """Test updating agent action status"""
        user = User(
            auth0_id="auth0|actionupdate123",
            email="actionupdate@example.com",
            name="Action Update User"
        )
        test_db.add(user)
        await test_db.commit()
        
        action = AgentAction(
            user_id=user.id,
            action="email_send",
            parameters={"to": "test@example.com"},
            status="pending"
        )
        test_db.add(action)
        await test_db.commit()
        
        # Update to completed
        action.status = "completed"
        action.result = "Email sent successfully"
        action.executed_at = datetime.now(timezone.utc)
        action.execution_time_ms = 1500
        
        await test_db.commit()
        await test_db.refresh(action)
        
        assert action.status == "completed"
        assert action.result == "Email sent successfully"
        assert action.executed_at is not None
        assert action.execution_time_ms == 1500

    @pytest.mark.asyncio
    async def test_find_pending_actions(self, test_db: AsyncSession):
        """Test finding pending agent actions"""
        user = User(
            auth0_id="auth0|pending123",
            email="pending@example.com",
            name="Pending User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create actions with different statuses
        pending_action = AgentAction(
            user_id=user.id,
            action="calendar_create_event",
            parameters={"title": "Pending Event"},
            status="pending"
        )
        
        completed_action = AgentAction(
            user_id=user.id,
            action="email_send",
            parameters={"to": "test@example.com"},
            status="completed"
        )
        
        test_db.add_all([pending_action, completed_action])
        await test_db.commit()
        
        # Find pending actions
        result = await test_db.execute(
            select(AgentAction)
            .where(AgentAction.user_id == user.id)
            .where(AgentAction.status == "pending")
        )
        pending_actions = result.scalars().all()
        
        assert len(pending_actions) == 1
        assert pending_actions[0].action == "calendar_create_event"


class TestSecurityEventModel:
    """Test cases for SecurityEvent model operations"""

    @pytest.mark.asyncio
    async def test_create_security_event(self, test_db: AsyncSession):
        """Test security event creation"""
        user = User(
            auth0_id="auth0|security123",
            email="security@example.com",
            name="Security User"
        )
        test_db.add(user)
        await test_db.commit()
        
        security_event = SecurityEvent(
            user_id=user.id,
            event_type="failed_authentication",
            severity="high",
            details={
                "reason": "invalid_token",
                "attempts": 3
            },
            ip_address="192.168.1.100"
        )
        
        test_db.add(security_event)
        await test_db.commit()
        await test_db.refresh(security_event)
        
        assert security_event.id is not None
        assert security_event.event_type == "failed_authentication"
        assert security_event.severity == "high"
        assert security_event.resolved is False

    @pytest.mark.asyncio
    async def test_resolve_security_event(self, test_db: AsyncSession):
        """Test resolving a security event"""
        user = User(
            auth0_id="auth0|resolve123",
            email="resolve@example.com",
            name="Resolve User"
        )
        test_db.add(user)
        await test_db.commit()
        
        security_event = SecurityEvent(
            user_id=user.id,
            event_type="suspicious_activity",
            severity="medium",
            details={"activity": "unusual_login_location"}
        )
        test_db.add(security_event)
        await test_db.commit()
        
        # Resolve the event
        security_event.resolved = True
        await test_db.commit()
        await test_db.refresh(security_event)
        
        assert security_event.resolved is True

    @pytest.mark.asyncio
    async def test_find_unresolved_events(self, test_db: AsyncSession):
        """Test finding unresolved security events"""
        user = User(
            auth0_id="auth0|unresolved123",
            email="unresolved@example.com",
            name="Unresolved User"
        )
        test_db.add(user)
        await test_db.commit()
        
        # Create resolved and unresolved events
        resolved_event = SecurityEvent(
            user_id=user.id,
            event_type="resolved_issue",
            severity="low",
            resolved=True
        )
        
        unresolved_event = SecurityEvent(
            user_id=user.id,
            event_type="unresolved_issue",
            severity="high",
            resolved=False
        )
        
        test_db.add_all([resolved_event, unresolved_event])
        await test_db.commit()
        
        # Find unresolved events
        result = await test_db.execute(
            select(SecurityEvent)
            .where(SecurityEvent.user_id == user.id)
            .where(SecurityEvent.resolved == False)
        )
        unresolved_events = result.scalars().all()
        
        assert len(unresolved_events) == 1
        assert unresolved_events[0].event_type == "unresolved_issue"


class TestPermissionTemplateModel:
    """Test cases for PermissionTemplate model operations"""

    @pytest.mark.asyncio
    async def test_create_permission_template(self, test_db: AsyncSession):
        """Test permission template creation"""
        template = PermissionTemplate(
            service_name="google",
            scope_name="calendar.events",
            description="Create and modify calendar events",
            risk_level="medium",
            requires_step_up=False
        )
        
        test_db.add(template)
        await test_db.commit()
        await test_db.refresh(template)
        
        assert template.id is not None
        assert template.service_name == "google"
        assert template.scope_name == "calendar.events"
        assert template.risk_level == "medium"

    @pytest.mark.asyncio
    async def test_find_templates_by_service(self, test_db: AsyncSession):
        """Test finding permission templates by service"""
        # Create templates for different services
        google_template = PermissionTemplate(
            service_name="google",
            scope_name="calendar.readonly",
            description="Read calendar events",
            risk_level="low"
        )
        
        github_template = PermissionTemplate(
            service_name="github",
            scope_name="repo",
            description="Access repositories",
            risk_level="high",
            requires_step_up=True
        )
        
        test_db.add_all([google_template, github_template])
        await test_db.commit()
        
        # Find Google templates
        result = await test_db.execute(
            select(PermissionTemplate)
            .where(PermissionTemplate.service_name == "google")
        )
        google_templates = result.scalars().all()
        
        assert len(google_templates) == 1
        assert google_templates[0].scope_name == "calendar.readonly"

    @pytest.mark.asyncio
    async def test_find_high_risk_templates(self, test_db: AsyncSession):
        """Test finding high-risk permission templates"""
        # Create templates with different risk levels
        low_risk = PermissionTemplate(
            service_name="google",
            scope_name="profile.readonly",
            description="Read user profile",
            risk_level="low"
        )
        
        high_risk = PermissionTemplate(
            service_name="github",
            scope_name="admin:org",
            description="Organization administration",
            risk_level="high",
            requires_step_up=True
        )
        
        test_db.add_all([low_risk, high_risk])
        await test_db.commit()
        
        # Find high-risk templates
        result = await test_db.execute(
            select(PermissionTemplate)
            .where(PermissionTemplate.risk_level == "high")
        )
        high_risk_templates = result.scalars().all()
        
        assert len(high_risk_templates) == 1
        assert high_risk_templates[0].requires_step_up is True