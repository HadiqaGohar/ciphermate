"""End-to-end tests for complete user workflows"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from fastapi import status

from app.main import app


class TestCompleteUserWorkflows:
    """End-to-end tests for complete user workflows"""

    @pytest.fixture
    def mock_auth0_user(self):
        """Mock authenticated user"""
        return {
            "sub": "auth0|e2e_test_user",
            "email": "e2e@example.com",
            "name": "E2E Test User",
            "aud": "test_audience",
            "iss": "https://test-domain.auth0.com/",
            "exp": 9999999999,
            "iat": 1000000000,
            "scope": "openid profile email"
        }

    @pytest.fixture
    def auth_headers(self):
        """Authentication headers for requests"""
        return {"Authorization": "Bearer mock.jwt.token"}

    @pytest.mark.asyncio
    async def test_complete_google_calendar_workflow(self, mock_auth0_user, auth_headers):
        """Test complete workflow: authenticate -> grant permissions -> create calendar event"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            # Mock authentication
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Check initial permissions (should be empty)
                response = await client.get("/api/v1/permissions/list", headers=auth_headers)
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert len(data["permissions"]) == 0
                
                # Step 2: Initiate OAuth flow for Google Calendar
                with patch('app.core.oauth_handlers.GoogleOAuthHandler.initiate_flow') as mock_oauth:
                    mock_oauth.return_value = {
                        "authorization_url": "https://accounts.google.com/oauth/authorize?...",
                        "state": "random_state_123"
                    }
                    
                    response = await client.post(
                        "/api/v1/permissions/grant",
                        json={
                            "service": "google",
                            "scopes": ["calendar.events"]
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    oauth_data = response.json()
                    assert "authorization_url" in oauth_data
                
                # Step 3: Simulate OAuth callback (token exchange)
                with patch('app.core.token_vault.TokenVaultService.store_token') as mock_store_token:
                    mock_store_token.return_value = {
                        "success": True,
                        "token_vault_id": "vault_google_123"
                    }
                    
                    with patch('app.core.oauth_handlers.GoogleOAuthHandler.exchange_code') as mock_exchange:
                        mock_exchange.return_value = {
                            "access_token": "google_access_token",
                            "refresh_token": "google_refresh_token",
                            "expires_in": 3600,
                            "scope": "https://www.googleapis.com/auth/calendar"
                        }
                        
                        response = await client.post(
                            "/api/v1/auth/callback/google",
                            json={
                                "code": "oauth_authorization_code",
                                "state": "random_state_123"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                
                # Step 4: Verify permissions were granted
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {
                        "google": ["calendar.events"]
                    }
                    
                    response = await client.get("/api/v1/permissions/list", headers=auth_headers)
                    assert response.status_code == status.HTTP_200_OK
                    data = response.json()
                    assert len(data["permissions"]) == 1
                    assert data["permissions"][0]["service_name"] == "google"
                
                # Step 5: Send AI request to create calendar event
                with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                    mock_ai.return_value = {
                        "success": True,
                        "response": "I've created your meeting for tomorrow at 10am.",
                        "intent": "calendar_create_event",
                        "action_result": {
                            "event_id": "google_event_123",
                            "title": "Team Meeting",
                            "start_time": "2024-01-02T10:00:00Z"
                        }
                    }
                    
                    response = await client.post(
                        "/api/v1/chat",
                        json={
                            "message": "Create a team meeting tomorrow at 10am"
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    chat_data = response.json()
                    assert chat_data["success"] is True
                    assert "created your meeting" in chat_data["response"].lower()
                
                # Step 6: Verify audit log was created
                response = await client.get("/api/v1/audit/logs", headers=auth_headers)
                assert response.status_code == status.HTTP_200_OK
                audit_data = response.json()
                assert len(audit_data["logs"]) > 0
                assert any(log["action_type"] == "calendar_create_event" for log in audit_data["logs"])

    @pytest.mark.asyncio
    async def test_complete_github_workflow(self, mock_auth0_user, auth_headers):
        """Test complete workflow: authenticate -> grant GitHub permissions -> create issue"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Grant GitHub permissions
                with patch('app.core.oauth_handlers.GitHubOAuthHandler.initiate_flow') as mock_oauth:
                    mock_oauth.return_value = {
                        "authorization_url": "https://github.com/login/oauth/authorize?...",
                        "state": "github_state_123"
                    }
                    
                    response = await client.post(
                        "/api/v1/permissions/grant",
                        json={
                            "service": "github",
                            "scopes": ["repo"]
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                
                # Step 2: Complete OAuth flow
                with patch('app.core.token_vault.TokenVaultService.store_token') as mock_store_token:
                    mock_store_token.return_value = {
                        "success": True,
                        "token_vault_id": "vault_github_123"
                    }
                    
                    with patch('app.core.oauth_handlers.GitHubOAuthHandler.exchange_code') as mock_exchange:
                        mock_exchange.return_value = {
                            "access_token": "github_access_token",
                            "token_type": "bearer",
                            "scope": "repo"
                        }
                        
                        response = await client.post(
                            "/api/v1/auth/callback/github",
                            json={
                                "code": "github_oauth_code",
                                "state": "github_state_123"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                
                # Step 3: Create GitHub issue via AI
                with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                    mock_ai.return_value = {
                        "success": True,
                        "response": "I've created the bug report issue in your repository.",
                        "intent": "github_create_issue",
                        "action_result": {
                            "issue_id": 123,
                            "title": "Bug Report",
                            "url": "https://github.com/user/repo/issues/123"
                        }
                    }
                    
                    response = await client.post(
                        "/api/v1/chat",
                        json={
                            "message": "Create a GitHub issue for the bug I found in the login system"
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    chat_data = response.json()
                    assert chat_data["success"] is True
                    assert "created the bug report" in chat_data["response"].lower()

    @pytest.mark.asyncio
    async def test_permission_revocation_workflow(self, mock_auth0_user, auth_headers):
        """Test complete workflow: grant permissions -> use service -> revoke permissions"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Grant permissions (simulate existing permission)
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {
                        "slack": ["chat:write"]
                    }
                    
                    response = await client.get("/api/v1/permissions/list", headers=auth_headers)
                    assert response.status_code == status.HTTP_200_OK
                    data = response.json()
                    assert len(data["permissions"]) == 1
                
                # Step 2: Use the service successfully
                with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                    mock_ai.return_value = {
                        "success": True,
                        "response": "Message sent to #general channel.",
                        "intent": "slack_send_message"
                    }
                    
                    response = await client.post(
                        "/api/v1/chat",
                        json={
                            "message": "Send a message to the general channel saying hello"
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    assert response.json()["success"] is True
                
                # Step 3: Revoke permissions
                with patch('app.core.token_vault.TokenVaultService.revoke_token') as mock_revoke:
                    mock_revoke.return_value = {"success": True}
                    
                    response = await client.post(
                        "/api/v1/permissions/revoke",
                        json={"service": "slack"},
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    assert response.json()["success"] is True
                
                # Step 4: Verify service is no longer accessible
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {}  # No permissions
                    
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": False,
                            "error_type": "permission_required",
                            "missing_permissions": {"slack": ["chat:write"]},
                            "message": "Permission required for Slack"
                        }
                        
                        response = await client.post(
                            "/api/v1/chat",
                            json={
                                "message": "Send another message to Slack"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                        chat_data = response.json()
                        assert chat_data["success"] is False
                        assert chat_data["error_type"] == "permission_required"

    @pytest.mark.asyncio
    async def test_security_event_workflow(self, mock_auth0_user, auth_headers):
        """Test workflow with security events and resolution"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Trigger security event (failed authentication)
                with patch('app.core.security_monitor.SecurityMonitor.log_event') as mock_log_event:
                    mock_log_event.return_value = {
                        "event_id": "security_event_123",
                        "event_type": "failed_authentication",
                        "severity": "high"
                    }
                    
                    # Simulate failed authentication attempt
                    response = await client.post(
                        "/api/v1/auth/login",
                        json={"token": "invalid_token"}
                    )
                    
                    # This should fail and create a security event
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED
                
                # Step 2: Check security events
                response = await client.get("/api/v1/audit/security-events", headers=auth_headers)
                assert response.status_code == status.HTTP_200_OK
                events_data = response.json()
                assert len(events_data["events"]) > 0
                
                # Step 3: Resolve security event
                event_id = events_data["events"][0]["id"]
                response = await client.post(
                    f"/api/v1/audit/security-events/{event_id}/resolve",
                    headers=auth_headers
                )
                
                assert response.status_code == status.HTTP_200_OK
                assert response.json()["success"] is True

    @pytest.mark.asyncio
    async def test_multi_service_workflow(self, mock_auth0_user, auth_headers):
        """Test workflow using multiple services in sequence"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Mock user has permissions for multiple services
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {
                        "google": ["calendar.events", "gmail.send"],
                        "github": ["repo"],
                        "slack": ["chat:write"]
                    }
                    
                    # Step 1: Create calendar event
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": True,
                            "response": "Created meeting and sent email notification.",
                            "intent": "calendar_create_event",
                            "action_result": {"event_id": "event_123"}
                        }
                        
                        response = await client.post(
                            "/api/v1/chat",
                            json={
                                "message": "Create a project review meeting tomorrow and send email invites"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                        assert response.json()["success"] is True
                    
                    # Step 2: Create GitHub issue
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": True,
                            "response": "Created GitHub issue for meeting action items.",
                            "intent": "github_create_issue",
                            "action_result": {"issue_id": 456}
                        }
                        
                        response = await client.post(
                            "/api/v1/chat",
                            json={
                                "message": "Create a GitHub issue to track the action items from the meeting"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                        assert response.json()["success"] is True
                    
                    # Step 3: Send Slack notification
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": True,
                            "response": "Sent notification to team channel.",
                            "intent": "slack_send_message",
                            "action_result": {"message_ts": "1234567890.123456"}
                        }
                        
                        response = await client.post(
                            "/api/v1/chat",
                            json={
                                "message": "Notify the team in Slack about the new GitHub issue"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                        assert response.json()["success"] is True
                
                # Step 4: Verify all actions were logged
                response = await client.get("/api/v1/audit/logs", headers=auth_headers)
                assert response.status_code == status.HTTP_200_OK
                audit_data = response.json()
                
                action_types = [log["action_type"] for log in audit_data["logs"]]
                assert "calendar_create_event" in action_types
                assert "github_create_issue" in action_types
                assert "slack_send_message" in action_types

    @pytest.mark.asyncio
    async def test_token_refresh_workflow(self, mock_auth0_user, auth_headers):
        """Test workflow with automatic token refresh"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Mock expired token scenario
                with patch('app.core.token_vault.TokenVaultService.retrieve_token') as mock_retrieve:
                    # First call returns expired token, second call returns refreshed token
                    mock_retrieve.side_effect = [
                        {
                            "access_token": "expired_token",
                            "refresh_token": "valid_refresh_token",
                            "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                        },
                        {
                            "access_token": "new_access_token",
                            "refresh_token": "new_refresh_token",
                            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
                        }
                    ]
                    
                    with patch('app.core.database.get_user_permissions') as mock_get_perms:
                        mock_get_perms.return_value = {"google": ["calendar.events"]}
                        
                        with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                            mock_ai.return_value = {
                                "success": True,
                                "response": "Event created with refreshed token.",
                                "intent": "calendar_create_event"
                            }
                            
                            response = await client.post(
                                "/api/v1/chat",
                                json={
                                    "message": "Create a meeting for next week"
                                },
                                headers=auth_headers
                            )
                            
                            assert response.status_code == status.HTTP_200_OK
                            assert response.json()["success"] is True
                            
                            # Verify token refresh was attempted
                            assert mock_retrieve.call_count == 2

    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, mock_auth0_user, auth_headers):
        """Test workflow with error conditions and recovery"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Attempt action that fails due to API error
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {"google": ["calendar.events"]}
                    
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": False,
                            "error_type": "api_error",
                            "message": "Google Calendar API is temporarily unavailable",
                            "retry_after": 60
                        }
                        
                        response = await client.post(
                            "/api/v1/chat",
                            json={
                                "message": "Create a meeting for tomorrow"
                            },
                            headers=auth_headers
                        )
                        
                        assert response.status_code == status.HTTP_200_OK
                        chat_data = response.json()
                        assert chat_data["success"] is False
                        assert "temporarily unavailable" in chat_data["message"]
                
                # Step 2: Retry the same action (should succeed)
                with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                    mock_ai.return_value = {
                        "success": True,
                        "response": "Meeting created successfully after retry.",
                        "intent": "calendar_create_event"
                    }
                    
                    response = await client.post(
                        "/api/v1/chat",
                        json={
                            "message": "Try creating that meeting again"
                        },
                        headers=auth_headers
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    assert response.json()["success"] is True

    @pytest.mark.asyncio
    async def test_audit_export_workflow(self, mock_auth0_user, auth_headers):
        """Test complete audit data export workflow"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = mock_auth0_user
                
                # Step 1: Generate some audit data
                with patch('app.core.database.get_user_permissions') as mock_get_perms:
                    mock_get_perms.return_value = {"google": ["calendar.events"]}
                    
                    with patch('app.core.ai_agent.AIAgentEngine.process_user_message') as mock_ai:
                        mock_ai.return_value = {
                            "success": True,
                            "response": "Actions completed.",
                            "intent": "calendar_create_event"
                        }
                        
                        # Perform several actions to generate audit data
                        for i in range(3):
                            response = await client.post(
                                "/api/v1/chat",
                                json={
                                    "message": f"Create meeting {i+1}"
                                },
                                headers=auth_headers
                            )
                            assert response.status_code == status.HTTP_200_OK
                
                # Step 2: Export audit data
                with patch('app.core.audit_service.AuditService.export_user_data') as mock_export:
                    mock_export.return_value = b"user_id,action_type,timestamp\nauth0|e2e_test_user,calendar_create_event,2024-01-01T10:00:00Z"
                    
                    response = await client.get("/api/v1/audit/export", headers=auth_headers)
                    
                    assert response.status_code == status.HTTP_200_OK
                    assert response.headers["content-type"] == "text/csv"
                    assert b"calendar_create_event" in response.content