#!/usr/bin/env python3
"""
Comprehensive test suite for Token Vault integration service
Tests all functionality including error handling, retry logic, and service-specific operations
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

from app.core.token_vault import (
    TokenVaultService,
    TokenVaultError,
    TokenNotFoundError,
    TokenExpiredError,
    AuthenticationError,
    ServiceError,
    TokenStatus
)
from app.models.service_connection import ServiceConnection


class TestTokenVaultService:
    """Test suite for TokenVaultService"""
    
    @pytest.fixture
    def token_vault_service(self):
        """Create a TokenVaultService instance for testing"""
        return TokenVaultService()
    
    @pytest.fixture
    def mock_token_data(self):
        """Mock token data for testing"""
        return {
            "access_token": "mock_access_token_123",
            "refresh_token": "mock_refresh_token_456",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "read write"
        }
    
    @pytest.fixture
    def mock_user_data(self):
        """Mock user data for testing"""
        return {
            "user_id": "test_user_123",
            "service_name": "google_calendar",
            "scopes": ["https://www.googleapis.com/auth/calendar"],
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
        }

    @pytest.mark.asyncio
    async def test_initialization(self, token_vault_service):
        """Test service initialization"""
        assert token_vault_service._max_retries == 3
        assert token_vault_service._retry_delay == 1.0
        assert token_vault_service.management_api_url.endswith("/api/v2")
        assert token_vault_service._management_token_cache is None

    @pytest.mark.asyncio
    async def test_input_validation(self, token_vault_service, mock_token_data):
        """Test input validation for all methods"""
        
        # Test store_token validation
        with pytest.raises(ValueError, match="user_id, service_name, and token_data are required"):
            await token_vault_service.store_token("", "service", mock_token_data, [])
        
        with pytest.raises(ValueError, match="user_id, service_name, and token_data are required"):
            await token_vault_service.store_token("user", "", mock_token_data, [])
        
        with pytest.raises(ValueError, match="user_id, service_name, and token_data are required"):
            await token_vault_service.store_token("user", "service", {}, [])
        
        # Test retrieve_token validation
        with pytest.raises(ValueError, match="user_id and service_name are required"):
            await token_vault_service.retrieve_token("", "service")
        
        with pytest.raises(ValueError, match="user_id and service_name are required"):
            await token_vault_service.retrieve_token("user", "")
        
        # Test revoke_token validation
        with pytest.raises(ValueError, match="user_id and service_name are required"):
            await token_vault_service.revoke_token("", "service")
        
        with pytest.raises(ValueError, match="user_id and service_name are required"):
            await token_vault_service.revoke_token("user", "")

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_management_token_caching(self, mock_client, token_vault_service):
        """Test management token caching mechanism"""
        
        # Mock successful token response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "mock_management_token",
            "expires_in": 3600
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # First call should make HTTP request
        token1 = await token_vault_service._get_management_token()
        assert token1 == "mock_management_token"
        assert mock_client_instance.post.call_count == 1
        
        # Second call should use cache
        token2 = await token_vault_service._get_management_token()
        assert token2 == "mock_management_token"
        assert mock_client_instance.post.call_count == 1  # No additional calls
        
        # Verify cache is set
        assert token_vault_service._management_token_cache == "mock_management_token"
        assert token_vault_service._management_token_expires is not None

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_management_token_retry_logic(self, mock_client, token_vault_service):
        """Test retry logic for management token acquisition"""
        
        # Mock client that fails twice then succeeds
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = [
            Exception("Network error"),
            Exception("Timeout error"),
            MagicMock(
                status_code=200,
                json=lambda: {"access_token": "success_token", "expires_in": 3600},
                raise_for_status=MagicMock()
            )
        ]
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Should succeed after retries
        token = await token_vault_service._get_management_token_with_retry()
        assert token == "success_token"
        assert mock_client_instance.post.call_count == 3

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_management_token_max_retries_exceeded(self, mock_client, token_vault_service):
        """Test behavior when max retries are exceeded"""
        
        # Mock client that always fails
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = Exception("Persistent error")
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Should raise AuthenticationError after max retries
        with pytest.raises(AuthenticationError, match="Unable to authenticate with Auth0"):
            await token_vault_service._get_management_token_with_retry()
        
        assert mock_client_instance.post.call_count == 3  # max_retries

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    @patch.object(TokenVaultService, '_store_in_vault_with_retry')
    @patch.object(TokenVaultService, '_get_management_token_with_retry')
    async def test_store_token_success(self, mock_get_token, mock_store_vault, mock_db, 
                                     token_vault_service, mock_token_data, mock_user_data):
        """Test successful token storage"""
        
        # Setup mocks
        mock_get_token.return_value = "mock_management_token"
        mock_store_vault.return_value = "vault_id_123"
        
        mock_db_instance = AsyncMock()
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Test token storage
        vault_id = await token_vault_service.store_token(
            mock_user_data["user_id"],
            mock_user_data["service_name"],
            mock_token_data,
            mock_user_data["scopes"],
            mock_user_data["expires_at"]
        )
        
        assert vault_id == "vault_id_123"
        mock_store_vault.assert_called_once()
        mock_db_instance.add.assert_called_once()
        mock_db_instance.commit.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    async def test_retrieve_token_not_found(self, mock_db, token_vault_service):
        """Test token retrieval when no connection exists"""
        
        # Mock database to return no connection
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Should return None for non-existent token
        result = await token_vault_service.retrieve_token("user_123", "nonexistent_service")
        assert result is None

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    async def test_retrieve_token_expired_no_refresh(self, mock_db, token_vault_service):
        """Test token retrieval when token is expired and auto_refresh is False"""
        
        # Mock expired connection
        mock_connection = MagicMock()
        mock_connection.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)  # Expired
        
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_connection
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Should raise TokenExpiredError
        with pytest.raises(TokenExpiredError, match="Token expired for service"):
            await token_vault_service.retrieve_token("user_123", "expired_service", auto_refresh=False)

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    @patch.object(TokenVaultService, '_revoke_from_vault_with_retry')
    async def test_revoke_token_success(self, mock_revoke_vault, mock_db, token_vault_service):
        """Test successful token revocation"""
        
        # Mock active connection
        mock_connection = MagicMock()
        mock_connection.token_vault_id = "vault_id_123"
        mock_connection.is_active = True
        
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_connection
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        mock_revoke_vault.return_value = True
        
        # Test revocation
        result = await token_vault_service.revoke_token("user_123", "test_service")
        
        assert result is True
        assert mock_connection.is_active is False
        mock_revoke_vault.assert_called_once_with("user_123", "vault_id_123")
        mock_db_instance.commit.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    async def test_list_tokens(self, mock_db, token_vault_service):
        """Test token listing functionality"""
        
        # Mock connections
        mock_connection1 = MagicMock()
        mock_connection1.service_name = "google_calendar"
        mock_connection1.scopes = ["calendar.read"]
        mock_connection1.is_active = True
        mock_connection1.created_at = datetime.now(timezone.utc)
        mock_connection1.expires_at = None
        mock_connection1.last_used_at = None
        mock_connection1.token_vault_id = "vault_1"
        
        mock_connection2 = MagicMock()
        mock_connection2.service_name = "github"
        mock_connection2.scopes = ["repo"]
        mock_connection2.is_active = False
        mock_connection2.created_at = datetime.now(timezone.utc)
        mock_connection2.expires_at = None
        mock_connection2.last_used_at = None
        mock_connection2.token_vault_id = "vault_2"
        
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_connection1, mock_connection2]
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Test listing active tokens only
        tokens = await token_vault_service.list_tokens("user_123", include_inactive=False)
        
        assert len(tokens) == 2
        assert tokens[0]["service"] == "google_calendar"
        assert tokens[0]["is_active"] is True
        assert tokens[1]["service"] == "github"
        assert tokens[1]["is_active"] is False

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_google_token_refresh(self, mock_client, token_vault_service):
        """Test Google token refresh functionality"""
        
        # Mock successful refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Test refresh
        result = await token_vault_service._refresh_google_token("refresh_token_123")
        
        assert result["access_token"] == "new_access_token"
        assert result["refresh_token"] == "refresh_token_123"  # Should preserve original
        mock_client_instance.post.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_google_token_refresh_invalid_grant(self, mock_client, token_vault_service):
        """Test Google token refresh with invalid grant error"""
        
        # Mock invalid grant response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "invalid_grant"}
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Should raise TokenExpiredError
        with pytest.raises(TokenExpiredError, match="Google refresh token is invalid or expired"):
            await token_vault_service._refresh_google_token("invalid_refresh_token")

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_github_token_validation(self, mock_client, token_vault_service):
        """Test GitHub token validation (GitHub tokens don't expire)"""
        
        # Mock successful validation response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Test validation
        result = await token_vault_service._refresh_github_token("github_token_123")
        
        assert result["access_token"] == "github_token_123"
        assert result["token_type"] == "bearer"
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_slack_token_refresh(self, mock_client, token_vault_service):
        """Test Slack token refresh functionality"""
        
        # Mock successful refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ok": True,
            "access_token": "new_slack_token",
            "refresh_token": "new_refresh_token",
            "scope": "chat:write,channels:read"
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Test refresh
        result = await token_vault_service._refresh_slack_token("slack_refresh_token")
        
        assert result["access_token"] == "new_slack_token"
        assert result["refresh_token"] == "new_refresh_token"
        assert result["scope"] == "chat:write,channels:read"
        mock_client_instance.post.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    async def test_bulk_revoke_tokens(self, mock_db, token_vault_service):
        """Test bulk token revocation"""
        
        # Mock connections
        mock_connection1 = MagicMock()
        mock_connection1.service_name = "google_calendar"
        mock_connection2 = MagicMock()
        mock_connection2.service_name = "github"
        
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_connection1, mock_connection2]
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Mock revoke_token method
        with patch.object(token_vault_service, 'revoke_token') as mock_revoke:
            mock_revoke.side_effect = [True, True]
            
            # Test bulk revocation
            results = await token_vault_service.bulk_revoke_tokens("user_123")
            
            assert results["google_calendar"] is True
            assert results["github"] is True
            assert mock_revoke.call_count == 2

    @pytest.mark.asyncio
    @patch('app.core.token_vault.httpx.AsyncClient')
    async def test_google_health_check(self, mock_client, token_vault_service):
        """Test Google token health check"""
        
        # Mock successful health check response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "expires_in": "3600",
            "scope": "https://www.googleapis.com/auth/calendar"
        }
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Test health check
        result = await token_vault_service._check_google_token_health("google_token_123")
        
        assert result["healthy"] is True
        assert result["status"] == "active"
        assert result["expires_in"] == "3600"
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.core.token_vault.AsyncSessionLocal')
    async def test_get_vault_statistics(self, mock_db, token_vault_service):
        """Test vault statistics generation"""
        
        # Mock database queries
        mock_db_instance = AsyncMock()
        
        # Mock total connections query
        mock_total_result = MagicMock()
        mock_total_result.scalars.return_value.all.return_value = ["conn1", "conn2", "conn3"]
        
        # Mock active connections query
        mock_active_result = MagicMock()
        mock_active_result.scalars.return_value.all.return_value = ["conn1", "conn2"]
        
        # Mock expired connections query
        mock_expired_result = MagicMock()
        mock_expired_result.scalars.return_value.all.return_value = ["conn1"]
        
        # Mock service breakdown query
        mock_service_result = MagicMock()
        mock_service_result.fetchall.return_value = [
            ("google_calendar", True),
            ("github", True),
            ("slack", False)
        ]
        
        mock_db_instance.execute.side_effect = [
            mock_total_result,
            mock_active_result,
            mock_expired_result,
            mock_service_result
        ]
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Test statistics generation
        stats = await token_vault_service.get_vault_statistics()
        
        assert stats["total_connections"] == 3
        assert stats["active_connections"] == 2
        assert stats["expired_connections"] == 1
        assert stats["inactive_connections"] == 1
        assert stats["health_percentage"] == pytest.approx(66.67, rel=1e-2)
        assert "service_breakdown" in stats
        assert "generated_at" in stats

    @pytest.mark.asyncio
    async def test_token_status_enum(self):
        """Test TokenStatus enum values"""
        assert TokenStatus.ACTIVE.value == "active"
        assert TokenStatus.EXPIRED.value == "expired"
        assert TokenStatus.REVOKED.value == "revoked"
        assert TokenStatus.REFRESH_FAILED.value == "refresh_failed"

    @pytest.mark.asyncio
    async def test_exception_hierarchy(self):
        """Test exception class hierarchy"""
        assert issubclass(TokenNotFoundError, TokenVaultError)
        assert issubclass(TokenExpiredError, TokenVaultError)
        assert issubclass(AuthenticationError, TokenVaultError)
        assert issubclass(ServiceError, TokenVaultError)
        
        # Test exception instantiation
        base_error = TokenVaultError("Base error")
        assert str(base_error) == "Base error"
        
        not_found_error = TokenNotFoundError("Token not found")
        assert str(not_found_error) == "Token not found"
        
        expired_error = TokenExpiredError("Token expired")
        assert str(expired_error) == "Token expired"
        
        auth_error = AuthenticationError("Auth failed")
        assert str(auth_error) == "Auth failed"
        
        service_error = ServiceError("Service error")
        assert str(service_error) == "Service error"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])