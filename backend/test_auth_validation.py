"""
Comprehensive tests for backend Auth0 JWT token validation
Tests for task 9: Validate backend authentication handling
"""

import pytest
import asyncio
import httpx
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
import json
import time

from app.core.auth import Auth0JWTBearer, get_current_user, auth0_jwt_bearer
from app.core.config import settings
from app.main import app


class TestAuth0JWTValidation:
    """Test Auth0 JWT token validation functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.auth_bearer = Auth0JWTBearer()
        self.client = TestClient(app)
        
        # Mock Auth0 configuration
        self.mock_domain = "test-domain.auth0.com"
        self.mock_audience = "test-audience"
        self.mock_client_id = "test-client-id"
        
        # Mock JWKS response
        self.mock_jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "kid": "test-kid-123",
                    "use": "sig",
                    "n": "test-n-value",
                    "e": "AQAB"
                }
            ]
        }
        
        # Mock valid JWT payload
        self.valid_payload = {
            "sub": "auth0|test-user-123",
            "email": "test@example.com",
            "name": "Test User",
            "nickname": "testuser",
            "picture": "https://example.com/avatar.jpg",
            "email_verified": True,
            "permissions": ["read:profile", "write:profile"],
            "scope": "openid profile email",
            "aud": self.mock_audience,
            "iss": f"https://{self.mock_domain}/",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        }
        
        # Mock expired JWT payload
        self.expired_payload = {
            **self.valid_payload,
            "exp": int(time.time()) - 3600  # Expired 1 hour ago
        }

    @pytest.mark.asyncio
    async def test_get_jwks_success(self):
        """Test successful JWKS retrieval from Auth0"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = self.mock_jwks
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            jwks = await self.auth_bearer.get_jwks()
            
            assert jwks == self.mock_jwks
            assert self.auth_bearer._jwks_cache == self.mock_jwks

    @pytest.mark.asyncio
    async def test_get_jwks_failure(self):
        """Test JWKS retrieval failure handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.RequestError("Network error")
            
            with pytest.raises(HTTPException) as exc_info:
                await self.auth_bearer.get_jwks()
            
            assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert "Unable to verify token" in exc_info.value.detail

    def test_get_rsa_key_success(self):
        """Test successful RSA key extraction from JWKS"""
        rsa_key = self.auth_bearer.get_rsa_key(self.mock_jwks, "test-kid-123")
        
        expected_key = {
            "kty": "RSA",
            "kid": "test-kid-123",
            "use": "sig",
            "n": "test-n-value",
            "e": "AQAB"
        }
        
        assert rsa_key == expected_key

    def test_get_rsa_key_not_found(self):
        """Test RSA key not found in JWKS"""
        rsa_key = self.auth_bearer.get_rsa_key(self.mock_jwks, "non-existent-kid")
        assert rsa_key is None

    @pytest.mark.asyncio
    async def test_verify_token_success(self):
        """Test successful JWT token verification"""
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_header, \
             patch('jose.jwt.decode') as mock_decode, \
             patch.object(self.auth_bearer, 'get_jwks') as mock_get_jwks, \
             patch.object(self.auth_bearer, 'get_rsa_key') as mock_get_rsa_key:
            
            mock_header.return_value = {"kid": "test-kid-123"}
            mock_get_jwks.return_value = self.mock_jwks
            mock_get_rsa_key.return_value = {"kty": "RSA", "kid": "test-kid-123"}
            mock_decode.return_value = self.valid_payload
            
            payload = await self.auth_bearer.verify_token(mock_token)
            
            assert payload == self.valid_payload
            mock_decode.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_token_missing_kid(self):
        """Test JWT token verification with missing kid in header"""
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_header:
            mock_header.return_value = {}  # No kid in header
            
            with pytest.raises(HTTPException) as exc_info:
                await self.auth_bearer.verify_token(mock_token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Token missing kid in header" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_verify_token_key_not_found(self):
        """Test JWT token verification with key not found in JWKS"""
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_header, \
             patch.object(self.auth_bearer, 'get_jwks') as mock_get_jwks, \
             patch.object(self.auth_bearer, 'get_rsa_key') as mock_get_rsa_key:
            
            mock_header.return_value = {"kid": "test-kid-123"}
            mock_get_jwks.return_value = self.mock_jwks
            mock_get_rsa_key.return_value = None  # Key not found
            
            with pytest.raises(HTTPException) as exc_info:
                await self.auth_bearer.verify_token(mock_token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Unable to find appropriate key" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_verify_token_jwt_error(self):
        """Test JWT token verification with JWT decode error"""
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_header, \
             patch('jose.jwt.decode') as mock_decode, \
             patch.object(self.auth_bearer, 'get_jwks') as mock_get_jwks, \
             patch.object(self.auth_bearer, 'get_rsa_key') as mock_get_rsa_key:
            
            mock_header.return_value = {"kid": "test-kid-123"}
            mock_get_jwks.return_value = self.mock_jwks
            mock_get_rsa_key.return_value = {"kty": "RSA", "kid": "test-kid-123"}
            mock_decode.side_effect = JWTError("Invalid token")
            
            with pytest.raises(HTTPException) as exc_info:
                await self.auth_bearer.verify_token(mock_token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_verify_token_expired(self):
        """Test JWT token verification with expired token"""
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_header, \
             patch('jose.jwt.decode') as mock_decode, \
             patch.object(self.auth_bearer, 'get_jwks') as mock_get_jwks, \
             patch.object(self.auth_bearer, 'get_rsa_key') as mock_get_rsa_key:
            
            mock_header.return_value = {"kid": "test-kid-123"}
            mock_get_jwks.return_value = self.mock_jwks
            mock_get_rsa_key.return_value = {"kty": "RSA", "kid": "test-kid-123"}
            mock_decode.side_effect = JWTError("Token has expired")
            
            with pytest.raises(HTTPException) as exc_info:
                await self.auth_bearer.verify_token(mock_token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid token" in exc_info.value.detail


class TestTokenRefreshScenarios:
    """Test token expiration and refresh scenarios"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.auth_bearer = Auth0JWTBearer()
        
        # Mock user ID
        self.user_id = "auth0|test-user-123"
        
        # Mock session data with refresh token
        self.session_data = {
            "session_id": "test-session-123",
            "user_id": self.user_id,
            "user_data": {
                "refresh_token": "mock-refresh-token",
                "access_token": "mock-access-token"
            }
        }

    @pytest.mark.asyncio
    async def test_refresh_token_if_needed_not_expired(self):
        """Test token refresh when token is not near expiration"""
        # Token expires in 1 hour (not near expiration)
        payload = {
            "sub": self.user_id,
            "exp": int(time.time()) + 3600
        }
        
        result = await self.auth_bearer.refresh_token_if_needed(self.user_id, payload)
        
        # Should return original payload since no refresh needed
        assert result == payload

    @pytest.mark.asyncio
    async def test_refresh_token_if_needed_near_expiration(self):
        """Test token refresh when token is near expiration"""
        # Token expires in 2 minutes (near expiration)
        near_exp_payload = {
            "sub": self.user_id,
            "exp": int(time.time()) + 120
        }
        
        new_payload = {
            "sub": self.user_id,
            "exp": int(time.time()) + 3600
        }
        
        with patch('app.core.session.session_manager.get_user_session') as mock_get_session, \
             patch('app.core.session.session_manager.update_session') as mock_update_session, \
             patch.object(self.auth_bearer, '_refresh_auth0_token') as mock_refresh, \
             patch.object(self.auth_bearer, 'verify_token') as mock_verify:
            
            mock_get_session.return_value = self.session_data
            mock_refresh.return_value = {"access_token": "new-access-token"}
            mock_verify.return_value = new_payload
            
            result = await self.auth_bearer.refresh_token_if_needed(self.user_id, near_exp_payload)
            
            # Should return new payload after refresh
            assert result == new_payload
            mock_refresh.assert_called_once_with("mock-refresh-token")
            mock_update_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_refresh_token_if_needed_no_session(self):
        """Test token refresh when no session exists"""
        payload = {
            "sub": self.user_id,
            "exp": int(time.time()) + 120  # Near expiration
        }
        
        with patch('app.core.session.session_manager.get_user_session') as mock_get_session:
            mock_get_session.return_value = None
            
            result = await self.auth_bearer.refresh_token_if_needed(self.user_id, payload)
            
            # Should return original payload since no session to refresh from
            assert result == payload

    @pytest.mark.asyncio
    async def test_refresh_auth0_token_success(self):
        """Test successful Auth0 token refresh"""
        refresh_token = "mock-refresh-token"
        new_token_data = {
            "access_token": "new-access-token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = new_token_data
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await self.auth_bearer._refresh_auth0_token(refresh_token)
            
            assert result == new_token_data

    @pytest.mark.asyncio
    async def test_refresh_auth0_token_failure(self):
        """Test Auth0 token refresh failure"""
        refresh_token = "invalid-refresh-token"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 400
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await self.auth_bearer._refresh_auth0_token(refresh_token)
            
            assert result is None

    @pytest.mark.asyncio
    async def test_refresh_auth0_token_network_error(self):
        """Test Auth0 token refresh with network error"""
        refresh_token = "mock-refresh-token"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.RequestError("Network error")
            
            result = await self.auth_bearer._refresh_auth0_token(refresh_token)
            
            assert result is None


class TestAuthenticationErrorResponses:
    """Test proper error responses for authentication failures"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.client = TestClient(app)

    def test_missing_authorization_header(self):
        """Test API call without Authorization header"""
        response = self.client.post("/api/v1/ai-agent/chat", json={"message": "test"})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Not authenticated" in response.json()["detail"]

    def test_invalid_bearer_token_format(self):
        """Test API call with invalid Bearer token format"""
        headers = {"Authorization": "InvalidFormat token"}
        response = self.client.post(
            "/api/v1/ai-agent/chat", 
            json={"message": "test"}, 
            headers=headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_malformed_jwt_token(self):
        """Test API call with malformed JWT token"""
        headers = {"Authorization": "Bearer invalid.jwt.token"}
        
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify:
            mock_verify.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
            response = self.client.post(
                "/api/v1/ai-agent/chat", 
                json={"message": "test"}, 
                headers=headers
            )
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid token" in response.json()["detail"]

    def test_expired_jwt_token(self):
        """Test API call with expired JWT token"""
        headers = {"Authorization": "Bearer expired.jwt.token"}
        
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify:
            mock_verify.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
            
            response = self.client.post(
                "/api/v1/ai-agent/chat", 
                json={"message": "test"}, 
                headers=headers
            )
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_auth0_service_unavailable(self):
        """Test API call when Auth0 service is unavailable"""
        headers = {"Authorization": "Bearer valid.jwt.token"}
        
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify:
            mock_verify.side_effect = HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to verify token"
            )
            
            response = self.client.post(
                "/api/v1/ai-agent/chat", 
                json={"message": "test"}, 
                headers=headers
            )
            
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert "Unable to verify token" in response.json()["detail"]


class TestGetCurrentUserDependency:
    """Test the get_current_user dependency function"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_request = Mock()
        self.mock_request.client.host = "127.0.0.1"
        self.mock_request.headers = {"user-agent": "test-agent"}
        
        self.mock_credentials = Mock()
        self.mock_credentials.credentials = "mock.jwt.token"
        
        self.valid_payload = {
            "sub": "auth0|test-user-123",
            "email": "test@example.com",
            "name": "Test User",
            "nickname": "testuser",
            "picture": "https://example.com/avatar.jpg",
            "email_verified": True,
            "permissions": ["read:profile"],
            "scope": "openid profile email",
            "exp": int(time.time()) + 3600,
            "iat": int(time.time())
        }

    @pytest.mark.asyncio
    async def test_get_current_user_success(self):
        """Test successful user authentication"""
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify, \
             patch.object(auth0_jwt_bearer, 'refresh_token_if_needed') as mock_refresh, \
             patch('app.core.session.session_manager.get_user_session') as mock_get_session, \
             patch('app.core.session.session_manager.create_session') as mock_create_session:
            
            mock_verify.return_value = self.valid_payload
            mock_refresh.return_value = self.valid_payload
            mock_get_session.return_value = None  # No existing session
            mock_create_session.return_value = "new-session-id"
            
            user_info = await get_current_user(self.mock_request, self.mock_credentials)
            
            assert user_info["sub"] == "auth0|test-user-123"
            assert user_info["email"] == "test@example.com"
            assert user_info["permissions"] == ["read:profile"]
            assert user_info["scope"] == ["openid", "profile", "email"]
            
            mock_verify.assert_called_once_with("mock.jwt.token")
            mock_refresh.assert_called_once()
            mock_create_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_user_missing_sub(self):
        """Test authentication failure when token missing user ID"""
        payload_without_sub = {**self.valid_payload}
        del payload_without_sub["sub"]
        
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify:
            mock_verify.return_value = payload_without_sub
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(self.mock_request, self.mock_credentials)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid token: missing user ID" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_session_error(self):
        """Test user authentication with session management error"""
        with patch.object(auth0_jwt_bearer, 'verify_token') as mock_verify, \
             patch.object(auth0_jwt_bearer, 'refresh_token_if_needed') as mock_refresh, \
             patch('app.core.session.session_manager.get_user_session') as mock_get_session:
            
            mock_verify.return_value = self.valid_payload
            mock_refresh.return_value = self.valid_payload
            mock_get_session.side_effect = Exception("Session error")
            
            # Should still return user info even if session fails
            user_info = await get_current_user(self.mock_request, self.mock_credentials)
            
            assert user_info["sub"] == "auth0|test-user-123"


class TestIntegrationScenarios:
    """Integration tests for complete authentication flows"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.client = TestClient(app)

    @pytest.mark.asyncio
    async def test_complete_chat_flow_with_valid_token(self):
        """Test complete chat flow with valid authentication"""
        valid_user = {
            "sub": "auth0|test-user-123",
            "email": "test@example.com",
            "name": "Test User",
            "permissions": ["read:profile"],
            "scope": ["openid", "profile", "email"]
        }
        
        with patch('app.core.auth.get_current_user') as mock_get_user, \
             patch('app.core.ai_agent_simple.simple_ai_agent.process_message') as mock_process:
            
            mock_get_user.return_value = valid_user
            mock_process.return_value = {
                "response": "Hello! How can I help you?",
                "intent_type": "greeting",
                "confidence": "high",
                "parameters": {},
                "required_permissions": [],
                "clarification_needed": False,
                "clarification_questions": []
            }
            
            headers = {"Authorization": "Bearer valid.jwt.token"}
            response = self.client.post(
                "/api/v1/ai-agent/chat",
                json={"message": "Hello"},
                headers=headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["response"] == "Hello! How can I help you?"
            assert data["intent_type"] == "greeting"

    def test_auth_health_endpoint(self):
        """Test authentication health check endpoint"""
        response = self.client.get("/api/v1/auth/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "authenticated" in data
        assert data["authenticated"] is False  # No token provided

    def test_auth_health_endpoint_with_token(self):
        """Test authentication health check endpoint with valid token"""
        valid_user = {
            "sub": "auth0|test-user-123",
            "email": "test@example.com"
        }
        
        with patch('app.core.auth.get_optional_user') as mock_get_user:
            mock_get_user.return_value = valid_user
            
            headers = {"Authorization": "Bearer valid.jwt.token"}
            response = self.client.get("/api/v1/auth/health", headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["authenticated"] is True
            assert data["user_id"] == "auth0|test-user-123"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])