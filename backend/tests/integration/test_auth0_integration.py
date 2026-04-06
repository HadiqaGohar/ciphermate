"""Integration tests for Auth0 and Token Vault operations"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from fastapi import status

from app.core.token_vault import TokenVaultService
from app.core.auth import Auth0JWTBearer
from app.main import app


class TestAuth0Integration:
    """Integration tests for Auth0 authentication and Token Vault"""

    @pytest.fixture
    def mock_auth0_config(self):
        """Mock Auth0 configuration"""
        return {
            "domain": "test-domain.auth0.com",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "audience": "test_audience"
        }

    @pytest.fixture
    def mock_management_api_response(self):
        """Mock Auth0 Management API response"""
        return {
            "access_token": "mgmt_token_123",
            "token_type": "Bearer",
            "expires_in": 3600
        }

    @pytest.fixture
    def mock_token_vault_store_response(self):
        """Mock Token Vault store response"""
        return {
            "id": "token_vault_id_123",
            "user_id": "auth0|test123",
            "service": "google",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        }

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_google(self, mock_auth0_config, mock_management_api_response, mock_token_vault_store_response):
        """Test complete OAuth flow for Google Calendar"""
        # Mock OAuth token exchange
        oauth_token_response = {
            "access_token": "google_access_token",
            "refresh_token": "google_refresh_token",
            "expires_in": 3600,
            "scope": "https://www.googleapis.com/auth/calendar",
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            
            # Mock different responses for different endpoints
            def mock_json_response(*args, **kwargs):
                url = args[0] if args else kwargs.get('url', '')
                if 'oauth/token' in str(url):
                    return mock_management_api_response
                elif 'token-vault' in str(url):
                    return mock_token_vault_store_response
                else:
                    return oauth_token_response
            
            mock_response.json.side_effect = mock_json_response
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            # Test the OAuth flow
            token_vault_service = TokenVaultService()
            
            # Step 1: Exchange authorization code for tokens
            result = await token_vault_service.store_token(
                user_id="auth0|test123",
                service="google",
                token_data=oauth_token_response
            )
            
            assert result["success"] is True
            assert result["token_vault_id"] == "token_vault_id_123"

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_github(self, mock_management_api_response, mock_token_vault_store_response):
        """Test complete OAuth flow for GitHub"""
        oauth_token_response = {
            "access_token": "github_access_token",
            "refresh_token": "github_refresh_token",
            "expires_in": 28800,
            "scope": "repo,user",
            "token_type": "bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            
            def mock_json_response(*args, **kwargs):
                url = args[0] if args else kwargs.get('url', '')
                if 'oauth/token' in str(url):
                    return mock_management_api_response
                elif 'token-vault' in str(url):
                    return mock_token_vault_store_response
                else:
                    return oauth_token_response
            
            mock_response.json.side_effect = mock_json_response
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            token_vault_service = TokenVaultService()
            
            result = await token_vault_service.store_token(
                user_id="auth0|test123",
                service="github",
                token_data=oauth_token_response
            )
            
            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_slack(self, mock_management_api_response, mock_token_vault_store_response):
        """Test complete OAuth flow for Slack"""
        oauth_token_response = {
            "ok": True,
            "access_token": "slack_access_token",
            "refresh_token": "slack_refresh_token",
            "expires_in": 43200,
            "scope": "chat:write,channels:read",
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            
            def mock_json_response(*args, **kwargs):
                url = args[0] if args else kwargs.get('url', '')
                if 'oauth/token' in str(url):
                    return mock_management_api_response
                elif 'token-vault' in str(url):
                    return mock_token_vault_store_response
                else:
                    return oauth_token_response
            
            mock_response.json.side_effect = mock_json_response
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            token_vault_service = TokenVaultService()
            
            result = await token_vault_service.store_token(
                user_id="auth0|test123",
                service="slack",
                token_data=oauth_token_response
            )
            
            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_token_refresh_flow_google(self, mock_management_api_response):
        """Test token refresh flow for Google"""
        # Mock expired token retrieval
        expired_token = {
            "access_token": "expired_google_token",
            "refresh_token": "google_refresh_token",
            "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "token_type": "Bearer",
            "scope": "https://www.googleapis.com/auth/calendar"
        }
        
        # Mock refreshed token response
        refreshed_token = {
            "access_token": "new_google_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = mock_client.return_value.__aenter__.return_value
            
            # Mock management token request
            mgmt_response = AsyncMock()
            mgmt_response.status_code = 200
            mgmt_response.json.return_value = mock_management_api_response
            mgmt_response.raise_for_status.return_value = None
            
            # Mock token retrieval
            get_response = AsyncMock()
            get_response.status_code = 200
            get_response.json.return_value = expired_token
            get_response.raise_for_status.return_value = None
            
            # Mock token refresh
            refresh_response = AsyncMock()
            refresh_response.status_code = 200
            refresh_response.json.return_value = refreshed_token
            refresh_response.raise_for_status.return_value = None
            
            # Mock token update
            update_response = AsyncMock()
            update_response.status_code = 200
            update_response.json.return_value = {"success": True}
            update_response.raise_for_status.return_value = None
            
            mock_client_instance.post.side_effect = [mgmt_response, refresh_response]
            mock_client_instance.get.return_value = get_response
            mock_client_instance.put.return_value = update_response
            
            token_vault_service = TokenVaultService()
            
            # This should trigger token refresh
            result = await token_vault_service.retrieve_token("token_vault_id_123")
            
            assert result["access_token"] == "new_google_token"

    @pytest.mark.asyncio
    async def test_token_revocation_flow(self, mock_management_api_response):
        """Test token revocation flow"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = mock_client.return_value.__aenter__.return_value
            
            # Mock management token request
            mgmt_response = AsyncMock()
            mgmt_response.status_code = 200
            mgmt_response.json.return_value = mock_management_api_response
            mgmt_response.raise_for_status.return_value = None
            
            # Mock token revocation
            revoke_response = AsyncMock()
            revoke_response.status_code = 204
            revoke_response.raise_for_status.return_value = None
            
            mock_client_instance.post.return_value = mgmt_response
            mock_client_instance.delete.return_value = revoke_response
            
            token_vault_service = TokenVaultService()
            
            result = await token_vault_service.revoke_token("token_vault_id_123")
            
            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_jwt_validation_flow(self, mock_auth0_jwks):
        """Test JWT token validation flow"""
        valid_payload = {
            "sub": "auth0|test123",
            "email": "test@example.com",
            "name": "Test User",
            "aud": "test_audience",
            "iss": "https://test-domain.auth0.com/",
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "scope": "openid profile email"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            # Mock JWKS retrieval
            jwks_response = AsyncMock()
            jwks_response.status_code = 200
            jwks_response.json.return_value = mock_auth0_jwks
            jwks_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = jwks_response
            
            with patch('jose.jwt.get_unverified_header') as mock_get_header:
                mock_get_header.return_value = {"kid": "test-key-id"}
                
                with patch('jose.jwt.decode') as mock_decode:
                    mock_decode.return_value = valid_payload
                    
                    auth_bearer = Auth0JWTBearer()
                    result = await auth_bearer.verify_token("valid.jwt.token")
                    
                    assert result["sub"] == "auth0|test123"
                    assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_end_to_end_permission_flow(self):
        """Test end-to-end permission granting and usage flow"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Mock authentication
            with patch('app.core.auth.get_current_user') as mock_get_user:
                mock_get_user.return_value = {
                    "sub": "auth0|test123",
                    "email": "test@example.com",
                    "name": "Test User"
                }
                
                # Mock OAuth flow initiation
                with patch('app.api.v1.permissions.initiate_oauth_flow') as mock_oauth:
                    mock_oauth.return_value = {
                        "authorization_url": "https://accounts.google.com/oauth/authorize?...",
                        "state": "random_state_123"
                    }
                    
                    # Step 1: Initiate OAuth flow
                    response = await client.post(
                        "/api/v1/permissions/grant",
                        json={
                            "service": "google",
                            "scopes": ["calendar.events"]
                        },
                        headers={"Authorization": "Bearer mock.jwt.token"}
                    )
                    
                    assert response.status_code == status.HTTP_200_OK
                    data = response.json()
                    assert "authorization_url" in data

    @pytest.mark.asyncio
    async def test_error_handling_invalid_token_vault_response(self, mock_management_api_response):
        """Test error handling for invalid Token Vault responses"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = mock_client.return_value.__aenter__.return_value
            
            # Mock management token success
            mgmt_response = AsyncMock()
            mgmt_response.status_code = 200
            mgmt_response.json.return_value = mock_management_api_response
            mgmt_response.raise_for_status.return_value = None
            
            # Mock Token Vault error
            vault_response = AsyncMock()
            vault_response.status_code = 400
            vault_response.raise_for_status.side_effect = Exception("Bad Request")
            
            mock_client_instance.post.side_effect = [mgmt_response, vault_response]
            
            token_vault_service = TokenVaultService()
            
            with pytest.raises(Exception):
                await token_vault_service.store_token(
                    user_id="auth0|test123",
                    service="google",
                    token_data={"access_token": "test_token"}
                )

    @pytest.mark.asyncio
    async def test_concurrent_token_operations(self, mock_management_api_response):
        """Test concurrent token operations"""
        import asyncio
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = mock_client.return_value.__aenter__.return_value
            
            # Mock management token
            mgmt_response = AsyncMock()
            mgmt_response.status_code = 200
            mgmt_response.json.return_value = mock_management_api_response
            mgmt_response.raise_for_status.return_value = None
            
            # Mock successful operations
            success_response = AsyncMock()
            success_response.status_code = 200
            success_response.json.return_value = {"success": True, "id": "token_123"}
            success_response.raise_for_status.return_value = None
            
            mock_client_instance.post.return_value = mgmt_response
            mock_client_instance.get.return_value = success_response
            
            token_vault_service = TokenVaultService()
            
            # Run multiple operations concurrently
            tasks = [
                token_vault_service.retrieve_token("token_1"),
                token_vault_service.retrieve_token("token_2"),
                token_vault_service.retrieve_token("token_3")
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # All operations should complete (may succeed or fail, but shouldn't hang)
            assert len(results) == 3

    @pytest.mark.asyncio
    async def test_token_vault_rate_limiting(self, mock_management_api_response):
        """Test Token Vault rate limiting handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = mock_client.return_value.__aenter__.return_value
            
            # Mock management token success
            mgmt_response = AsyncMock()
            mgmt_response.status_code = 200
            mgmt_response.json.return_value = mock_management_api_response
            mgmt_response.raise_for_status.return_value = None
            
            # Mock rate limit response
            rate_limit_response = AsyncMock()
            rate_limit_response.status_code = 429
            rate_limit_response.headers = {"Retry-After": "60"}
            rate_limit_response.raise_for_status.side_effect = Exception("Rate Limited")
            
            mock_client_instance.post.side_effect = [mgmt_response, rate_limit_response]
            
            token_vault_service = TokenVaultService()
            
            with pytest.raises(Exception):
                await token_vault_service.store_token(
                    user_id="auth0|test123",
                    service="google",
                    token_data={"access_token": "test_token"}
                )