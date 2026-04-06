"""Integration tests for AI Agent API endpoints"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.models.user import User
from app.models.service_connection import ServiceConnection
from app.models.agent_action import AgentAction
from main import app

# Test database URL (use in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """Override database dependency for testing"""
    async with TestSessionLocal() as session:
        yield session


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def setup_database():
    """Set up test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user():
    """Create a test user"""
    async with TestSessionLocal() as session:
        user = User(
            auth0_id="test_auth0_id",
            email="test@example.com",
            name="Test User"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.fixture
def mock_auth():
    """Mock authentication dependency"""
    with patch('app.api.v1.agent.get_current_user') as mock_get_user:
        mock_user = Mock()
        mock_user.id = 1
        mock_user.auth0_id = "test_auth0_id"
        mock_user.email = "test@example.com"
        mock_get_user.return_value = mock_user
        yield mock_get_user


class TestAgentAPIIntegration:
    """Integration tests for Agent API endpoints"""
    
    @pytest.mark.asyncio
    async def test_analyze_intent_endpoint(self, setup_database, test_user, mock_auth):
        """Test the analyze intent endpoint"""
        with TestClient(app) as client:
            # Mock the AI agent
            with patch('app.api.v1.agent.ai_agent') as mock_agent:
                # Mock intent analysis result
                from app.core.ai_agent import IntentAnalysisResult, IntentType, ConfidenceLevel
                
                mock_result = IntentAnalysisResult(
                    intent_type=IntentType.CALENDAR_CREATE_EVENT,
                    confidence=ConfidenceLevel.HIGH,
                    parameters={"title": "Test Meeting"},
                    required_permissions=["https://www.googleapis.com/auth/calendar"],
                    service_name="google",
                    clarification_needed=False
                )
                
                mock_agent.analyze_intent.return_value = mock_result
                mock_agent.check_user_permissions.return_value = (True, [])
                
                # Make request
                response = client.post(
                    "/api/v1/agent/analyze-intent",
                    json={
                        "message": "Schedule a meeting tomorrow at 2pm",
                        "context": {}
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                
                assert data["intent_type"] == "calendar_create_event"
                assert data["confidence"] == "high"
                assert data["service_name"] == "google"
                assert data["has_permissions"] is True
    
    @pytest.mark.asyncio
    async def test_chat_endpoint(self, setup_database, test_user, mock_auth):
        """Test the chat endpoint"""
        with TestClient(app) as client:
            # Mock the AI agent
            with patch('app.api.v1.agent.ai_agent') as mock_agent:
                from app.core.ai_agent import IntentAnalysisResult, IntentType, ConfidenceLevel
                
                mock_result = IntentAnalysisResult(
                    intent_type=IntentType.CALENDAR_CREATE_EVENT,
                    confidence=ConfidenceLevel.HIGH,
                    parameters={"title": "Test Meeting"},
                    required_permissions=["https://www.googleapis.com/auth/calendar"],
                    service_name="google",
                    clarification_needed=False
                )
                
                mock_agent.analyze_intent.return_value = mock_result
                mock_agent.check_user_permissions.return_value = (False, ["https://www.googleapis.com/auth/calendar"])
                mock_agent.generate_response.return_value = "I need permission to access your Google Calendar to create this event."
                
                # Make request
                response = client.post(
                    "/api/v1/agent/chat",
                    json={
                        "message": "Schedule a meeting tomorrow at 2pm"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                
                assert "message" in data
                assert data["requires_permission"] is True
                assert data["permission_grant_url"] is not None
                assert data["action_id"] is not None
    
    @pytest.mark.asyncio
    async def test_get_permission_requirements_endpoint(self, setup_database, mock_auth):
        """Test the permission requirements endpoint"""
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/agent/permissions/requirements/calendar_create_event",
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["intent_type"] == "calendar_create_event"
            assert data["requires_permissions"] is True
            assert data["service"] == "google"
            assert "https://www.googleapis.com/auth/calendar" in data["scopes"]
    
    @pytest.mark.asyncio
    async def test_get_permission_requirements_unknown_intent(self, setup_database, mock_auth):
        """Test permission requirements for unknown intent"""
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/agent/permissions/requirements/unknown_intent",
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400
            data = response.json()
            assert "Invalid intent type" in data["detail"]


if __name__ == "__main__":
    # Run a simple test
    async def run_simple_test():
        print("Testing AI Agent API integration...")
        
        # Test that the endpoints are properly registered
        from fastapi.testclient import TestClient
        
        with TestClient(app) as client:
            # Test root endpoint
            response = client.get("/")
            print(f"Root endpoint: {response.status_code}")
            
            # Test API status
            response = client.get("/api/v1/status")
            print(f"API status: {response.status_code}")
            
            # Test that agent endpoints exist (will fail auth but that's expected)
            response = client.post("/api/v1/agent/chat", json={"message": "test"})
            print(f"Chat endpoint (no auth): {response.status_code}")  # Should be 401 or 422
            
        print("Basic API integration test completed!")
    
    asyncio.run(run_simple_test())