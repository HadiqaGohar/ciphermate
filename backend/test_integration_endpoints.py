"""
Integration tests for the API integration endpoints.
Tests the FastAPI endpoints with mocked external services.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from main import app
from app.core.api_integration import APIResponse


class TestIntegrationEndpoints:
    """Test the integration API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user"""
        return {
            "auth0_id": "test_user_123",
            "email": "test@example.com",
            "name": "Test User"
        }
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        with patch('app.core.api_integration.api_integration_service.health_check') as mock_health:
            mock_health.return_value = {
                "status": "healthy",
                "services_configured": ["google_calendar", "gmail", "github", "slack"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            response = client.get("/api/v1/integrations/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "services_configured" in data
    
    def test_rate_limit_endpoint(self, client, mock_user):
        """Test the rate limit status endpoint"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.api_integration.api_integration_service.get_rate_limit_status') as mock_rate_limit:
            
            mock_rate_limit.return_value = {
                "service": "github",
                "remaining": 100,
                "reset_at": datetime.now(timezone.utc).isoformat()
            }
            
            response = client.get("/api/v1/integrations/rate-limits/github")
            assert response.status_code == 200
            data = response.json()
            assert data["service"] == "github"
            assert "remaining" in data
    
    def test_generic_api_call_endpoint(self, client, mock_user):
        """Test the generic API call endpoint"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.api_integration.api_integration_service.make_api_call') as mock_api_call:
            
            mock_response = APIResponse(
                success=True,
                data={"login": "testuser", "id": 12345},
                status_code=200,
                service="github"
            )
            mock_api_call.return_value = mock_response
            
            request_data = {
                "service": "github",
                "method": "GET",
                "endpoint": "/user"
            }
            
            response = client.post("/api/v1/integrations/call", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["login"] == "testuser"
    
    def test_google_calendar_endpoints(self, client, mock_user):
        """Test Google Calendar specific endpoints"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.service_clients.service_client_factory.get_google_calendar_client') as mock_client:
            
            # Mock calendar client
            mock_calendar_client = AsyncMock()
            mock_client.return_value = mock_calendar_client
            
            # Test list calendars
            mock_calendar_client.list_calendars.return_value = APIResponse(
                success=True,
                data={"items": [{"id": "primary", "summary": "Primary Calendar"}]},
                service="google_calendar"
            )
            
            response = client.get("/api/v1/integrations/google-calendar/calendars")
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
    
    def test_github_endpoints(self, client, mock_user):
        """Test GitHub specific endpoints"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.service_clients.service_client_factory.get_github_client') as mock_client:
            
            # Mock GitHub client
            mock_github_client = AsyncMock()
            mock_client.return_value = mock_github_client
            
            # Test get user
            mock_github_client.get_user.return_value = APIResponse(
                success=True,
                data={"login": "testuser", "id": 12345},
                service="github"
            )
            
            response = client.get("/api/v1/integrations/github/user")
            assert response.status_code == 200
            data = response.json()
            assert data["login"] == "testuser"
    
    def test_slack_endpoints(self, client, mock_user):
        """Test Slack specific endpoints"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.service_clients.service_client_factory.get_slack_client') as mock_client:
            
            # Mock Slack client
            mock_slack_client = AsyncMock()
            mock_client.return_value = mock_slack_client
            
            # Test get user info
            mock_slack_client.get_user_info.return_value = APIResponse(
                success=True,
                data={"ok": True, "user": "testuser"},
                service="slack"
            )
            
            response = client.get("/api/v1/integrations/slack/user")
            assert response.status_code == 200
            data = response.json()
            assert data["ok"] is True
    
    def test_error_handling(self, client, mock_user):
        """Test error handling in endpoints"""
        with patch('app.core.auth.get_current_user', return_value=mock_user), \
             patch('app.core.api_integration.api_integration_service.make_api_call') as mock_api_call:
            
            # Test authorization error
            from app.core.api_integration import AuthorizationError
            mock_api_call.side_effect = AuthorizationError("No token found")
            
            request_data = {
                "service": "github",
                "method": "GET",
                "endpoint": "/user"
            }
            
            response = client.post("/api/v1/integrations/call", json=request_data)
            assert response.status_code == 401
            assert "No token found" in response.json()["detail"]
    
    def test_unsupported_service(self, client, mock_user):
        """Test unsupported service handling"""
        with patch('app.core.auth.get_current_user', return_value=mock_user):
            
            request_data = {
                "service": "unsupported_service",
                "method": "GET",
                "endpoint": "/test"
            }
            
            response = client.post("/api/v1/integrations/call", json=request_data)
            assert response.status_code == 400
            assert "Unsupported service" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])