"""Unit tests for Token Vault Service"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime, timezone, timedelta
from app.core.token_vault import (
    TokenVaultService, 
    TokenVaultError, 
    TokenNotFoundError, 
    TokenExpiredError,
    AuthenticationError,
    ServiceError,
    TokenStatus
)


class TestTokenVaultService:
    """Test cases for Token Vault Service"""

    @pytest.fixture
    def token_vault_service(self):
        """Create token vault service instance"""
        return TokenVaultService()

    @pytest.fixture
    def mock_auth0_management_token(self):
        """Mock Auth0 management token response"""
        return {
            "access_token": "mgmt_token_123",
            "token_type": "Bearer",
            "expires_in": 3600
        }

    @pytest.fixture
    def mock_stored_token(self):
        """Mock stored token data"""
        return {
            "access_token": "stored_access_token",
            "refresh_token": "stored_refresh_token",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            "token_type": "Bearer",
            "scope": "calendar.readonly"
        }

    @pytest.mark.asyncio
    async def test_get_management_token_success(self, token_vault_service, mock_auth0_management_token):
        """Test successful management token retrieval"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_auth0_management_token
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            token = await token_vault_service.get_management_token()
            
            assert token == "mgmt_token_123"

    @pytest.mark.asyncio
    async def test_get_management_token_failure(self, token_vault_service):
        """Test management token retrieval failure"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 401
            mock_response.raise_for_status.side_effect = Exception("Unauthorized")
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            with pytest.raises(AuthenticationError):
                await token_vault_service.get_management_token()

    @pytest.mark.asyncio
    async def test_store_token_success(self, token_vault_service, mock_auth0_management_token):
        """Test successful token storage"""
        token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
            "scope": "calendar.readonly"
        }
        
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 201
                mock_response.json.return_value = {"id": "token_vault_id_123"}
                mock_response.raise_for_status.return_value = None
                
                mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
                
                result = await token_vault_service.store_token(
                    "user123", "google", token_data
                )
                
                assert result["success"] is True
                assert result["token_vault_id"] == "token_vault_id_123"

    @pytest.mark.asyncio
    async def test_store_token_failure(self, token_vault_service):
        """Test token storage failure"""
        token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600
        }
        
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 400
                mock_response.raise_for_status.side_effect = Exception("Bad Request")
                
                mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
                
                with pytest.raises(TokenVaultError):
                    await token_vault_service.store_token(
                        "user123", "google", token_data
                    )

    @pytest.mark.asyncio
    async def test_retrieve_token_success(self, token_vault_service, mock_stored_token):
        """Test successful token retrieval"""
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_stored_token
                mock_response.raise_for_status.return_value = None
                
                mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
                
                token = await token_vault_service.retrieve_token("token_vault_id_123")
                
                assert token["access_token"] == "stored_access_token"
                assert token["refresh_token"] == "stored_refresh_token"

    @pytest.mark.asyncio
    async def test_retrieve_token_not_found(self, token_vault_service):
        """Test token retrieval when token not found"""
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 404
                mock_response.raise_for_status.side_effect = Exception("Not Found")
                
                mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
                
                with pytest.raises(TokenNotFoundError):
                    await token_vault_service.retrieve_token("nonexistent_id")

    @pytest.mark.asyncio
    async def test_retrieve_token_expired_with_refresh(self, token_vault_service):
        """Test token retrieval with expired token that can be refreshed"""
        expired_token = {
            "access_token": "expired_access_token",
            "refresh_token": "valid_refresh_token",
            "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "token_type": "Bearer",
            "scope": "calendar.readonly"
        }
        
        refreshed_token = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                # Mock token retrieval
                mock_get_response = AsyncMock()
                mock_get_response.status_code = 200
                mock_get_response.json.return_value = expired_token
                mock_get_response.raise_for_status.return_value = None
                
                # Mock token refresh
                mock_refresh_response = AsyncMock()
                mock_refresh_response.status_code = 200
                mock_refresh_response.json.return_value = refreshed_token
                mock_refresh_response.raise_for_status.return_value = None
                
                mock_client_instance = mock_client.return_value.__aenter__.return_value
                mock_client_instance.get.return_value = mock_get_response
                mock_client_instance.post.return_value = mock_refresh_response
                
                with patch.object(token_vault_service, 'update_token') as mock_update:
                    mock_update.return_value = {"success": True}
                    
                    token = await token_vault_service.retrieve_token("token_vault_id_123")
                    
                    assert token["access_token"] == "new_access_token"

    @pytest.mark.asyncio
    async def test_revoke_token_success(self, token_vault_service):
        """Test successful token revocation"""
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 204
                mock_response.raise_for_status.return_value = None
                
                mock_client.return_value.__aenter__.return_value.delete.return_value = mock_response
                
                result = await token_vault_service.revoke_token("token_vault_id_123")
                
                assert result["success"] is True

    @pytest.mark.asyncio
    async def test_revoke_token_not_found(self, token_vault_service):
        """Test token revocation when token not found"""
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 404
                mock_response.raise_for_status.side_effect = Exception("Not Found")
                
                mock_client.return_value.__aenter__.return_value.delete.return_value = mock_response
                
                with pytest.raises(TokenNotFoundError):
                    await token_vault_service.revoke_token("nonexistent_id")

    @pytest.mark.asyncio
    async def test_refresh_google_token_success(self, token_vault_service):
        """Test successful Google token refresh"""
        refresh_token = "google_refresh_token"
        new_token_data = {
            "access_token": "new_google_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = new_token_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await token_vault_service.refresh_google_token(refresh_token)
            
            assert result["access_token"] == "new_google_token"
            assert result["expires_in"] == 3600

    @pytest.mark.asyncio
    async def test_refresh_github_token_success(self, token_vault_service):
        """Test successful GitHub token refresh"""
        refresh_token = "github_refresh_token"
        new_token_data = {
            "access_token": "new_github_token",
            "expires_in": 28800,
            "token_type": "bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = new_token_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await token_vault_service.refresh_github_token(refresh_token)
            
            assert result["access_token"] == "new_github_token"

    @pytest.mark.asyncio
    async def test_refresh_slack_token_success(self, token_vault_service):
        """Test successful Slack token refresh"""
        refresh_token = "slack_refresh_token"
        new_token_data = {
            "ok": True,
            "access_token": "new_slack_token",
            "expires_in": 43200,
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = new_token_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await token_vault_service.refresh_slack_token(refresh_token)
            
            assert result["access_token"] == "new_slack_token"

    @pytest.mark.asyncio
    async def test_list_tokens_success(self, token_vault_service):
        """Test successful token listing"""
        token_list = {
            "tokens": [
                {
                    "id": "token1",
                    "service": "google",
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-01T01:00:00Z"
                },
                {
                    "id": "token2",
                    "service": "github",
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-01T08:00:00Z"
                }
            ]
        }
        
        with patch.object(token_vault_service, 'get_management_token') as mock_mgmt_token:
            mock_mgmt_token.return_value = "mgmt_token_123"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = AsyncMock()
                mock_response.status_code = 200
                mock_response.json.return_value = token_list
                mock_response.raise_for_status.return_value = None
                
                mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
                
                result = await token_vault_service.list_tokens("user123")
                
                assert len(result["tokens"]) == 2
                assert result["tokens"][0]["service"] == "google"

    @pytest.mark.asyncio
    async def test_get_token_status_active(self, token_vault_service):
        """Test token status check for active token"""
        active_token = {
            "access_token": "active_token",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            "token_type": "Bearer"
        }
        
        with patch.object(token_vault_service, 'retrieve_token') as mock_retrieve:
            mock_retrieve.return_value = active_token
            
            status = await token_vault_service.get_token_status("token_vault_id_123")
            
            assert status == TokenStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_get_token_status_expired(self, token_vault_service):
        """Test token status check for expired token"""
        expired_token = {
            "access_token": "expired_token",
            "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "token_type": "Bearer"
        }
        
        with patch.object(token_vault_service, 'retrieve_token') as mock_retrieve:
            mock_retrieve.return_value = expired_token
            
            status = await token_vault_service.get_token_status("token_vault_id_123")
            
            assert status == TokenStatus.EXPIRED

    @pytest.mark.asyncio
    async def test_get_token_status_not_found(self, token_vault_service):
        """Test token status check for non-existent token"""
        with patch.object(token_vault_service, 'retrieve_token') as mock_retrieve:
            mock_retrieve.side_effect = TokenNotFoundError("Token not found")
            
            status = await token_vault_service.get_token_status("nonexistent_id")
            
            assert status == TokenStatus.REVOKED

    @pytest.mark.asyncio
    async def test_cleanup_expired_tokens(self, token_vault_service):
        """Test cleanup of expired tokens"""
        expired_tokens = {
            "tokens": [
                {
                    "id": "expired_token_1",
                    "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                },
                {
                    "id": "expired_token_2",
                    "expires_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
                }
            ]
        }
        
        with patch.object(token_vault_service, 'list_tokens') as mock_list:
            mock_list.return_value = expired_tokens
            
            with patch.object(token_vault_service, 'revoke_token') as mock_revoke:
                mock_revoke.return_value = {"success": True}
                
                result = await token_vault_service.cleanup_expired_tokens("user123")
                
                assert result["cleaned_count"] == 2
                assert mock_revoke.call_count == 2

    def test_is_token_expired_true(self, token_vault_service):
        """Test token expiration check for expired token"""
        expired_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        
        assert token_vault_service.is_token_expired(expired_time) is True

    def test_is_token_expired_false(self, token_vault_service):
        """Test token expiration check for valid token"""
        future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        
        assert token_vault_service.is_token_expired(future_time) is False

    def test_is_token_expired_invalid_format(self, token_vault_service):
        """Test token expiration check with invalid date format"""
        invalid_time = "invalid-date-format"
        
        assert token_vault_service.is_token_expired(invalid_time) is True