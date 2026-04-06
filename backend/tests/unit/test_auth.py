"""Unit tests for Authentication Service"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from jose import jwt

from app.core.auth import Auth0JWTBearer, get_current_user, verify_permissions
from app.core.exceptions import AuthenticationError, AuthorizationError


class TestAuth0JWTBearer:
    """Test cases for Auth0 JWT Bearer authentication"""

    @pytest.fixture
    def auth_bearer(self):
        """Create Auth0JWTBearer instance"""
        return Auth0JWTBearer()

    @pytest.fixture
    def valid_jwt_payload(self):
        """Valid JWT payload for testing"""
        return {
            "sub": "auth0|test123",
            "email": "test@example.com",
            "name": "Test User",
            "aud": "test-audience",
            "iss": "https://test-domain.auth0.com/",
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "scope": "openid profile email"
        }

    @pytest.fixture
    def expired_jwt_payload(self):
        """Expired JWT payload for testing"""
        return {
            "sub": "auth0|test123",
            "email": "test@example.com",
            "name": "Test User",
            "aud": "test-audience",
            "iss": "https://test-domain.auth0.com/",
            "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),
            "iat": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()),
            "scope": "openid profile email"
        }

    @pytest.mark.asyncio
    async def test_get_jwks_success(self, auth_bearer, mock_auth0_jwks):
        """Test successful JWKS retrieval"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_auth0_jwks
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            jwks = await auth_bearer.get_jwks()
            
            assert "keys" in jwks
            assert len(jwks["keys"]) == 1
            assert jwks["keys"][0]["kid"] == "test-key-id"

    @pytest.mark.asyncio
    async def test_get_jwks_failure(self, auth_bearer):
        """Test JWKS retrieval failure"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception("Server Error")
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(HTTPException) as exc_info:
                await auth_bearer.get_jwks()
            
            assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    @pytest.mark.asyncio
    async def test_get_jwks_caching(self, auth_bearer, mock_auth0_jwks):
        """Test JWKS caching functionality"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_auth0_jwks
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            # First call should fetch from API
            jwks1 = await auth_bearer.get_jwks()
            
            # Second call should use cache
            jwks2 = await auth_bearer.get_jwks()
            
            assert jwks1 == jwks2
            # Should only call the API once due to caching
            mock_client.return_value.__aenter__.return_value.get.assert_called_once()

    def test_get_rsa_key_success(self, auth_bearer, mock_auth0_jwks):
        """Test successful RSA key extraction"""
        rsa_key = auth_bearer.get_rsa_key(mock_auth0_jwks, "test-key-id")
        
        assert rsa_key is not None
        assert rsa_key["kid"] == "test-key-id"
        assert rsa_key["kty"] == "RSA"
        assert rsa_key["n"] == "test-n-value"
        assert rsa_key["e"] == "AQAB"

    def test_get_rsa_key_not_found(self, auth_bearer, mock_auth0_jwks):
        """Test RSA key extraction with non-existent key ID"""
        rsa_key = auth_bearer.get_rsa_key(mock_auth0_jwks, "nonexistent-key-id")
        
        assert rsa_key is None

    @pytest.mark.asyncio
    async def test_verify_token_success(self, auth_bearer, valid_jwt_payload, mock_auth0_jwks):
        """Test successful token verification"""
        # Create a mock JWT token
        mock_token = "mock.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_get_header:
            mock_get_header.return_value = {"kid": "test-key-id"}
            
            with patch('jose.jwt.decode') as mock_decode:
                mock_decode.return_value = valid_jwt_payload
                
                with patch.object(auth_bearer, 'get_jwks') as mock_get_jwks:
                    mock_get_jwks.return_value = mock_auth0_jwks
                    
                    payload = await auth_bearer.verify_token(mock_token)
                    
                    assert payload["sub"] == "auth0|test123"
                    assert payload["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_verify_token_expired(self, auth_bearer, expired_jwt_payload, mock_auth0_jwks):
        """Test token verification with expired token"""
        mock_token = "expired.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_get_header:
            mock_get_header.return_value = {"kid": "test-key-id"}
            
            with patch('jose.jwt.decode') as mock_decode:
                mock_decode.side_effect = jwt.ExpiredSignatureError("Token expired")
                
                with patch.object(auth_bearer, 'get_jwks') as mock_get_jwks:
                    mock_get_jwks.return_value = mock_auth0_jwks
                    
                    with pytest.raises(HTTPException) as exc_info:
                        await auth_bearer.verify_token(mock_token)
                    
                    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
                    assert "expired" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_verify_token_invalid_signature(self, auth_bearer, mock_auth0_jwks):
        """Test token verification with invalid signature"""
        mock_token = "invalid.jwt.token"
        
        with patch('jose.jwt.get_unverified_header') as mock_get_header:
            mock_get_header.return_value = {"kid": "test-key-id"}
            
            with patch('jose.jwt.decode') as mock_decode:
                mock_decode.side_effect = jwt.JWTError("Invalid signature")
                
                with patch.object(auth_bearer, 'get_jwks') as mock_get_jwks:
                    mock_get_jwks.return_value = mock_auth0_jwks
                    
                    with pytest.raises(HTTPException) as exc_info:
                        await auth_bearer.verify_token(mock_token)
                    
                    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_verify_token_missing_kid(self, auth_bearer):
        """Test token verification with missing key ID"""
        mock_token = "token.without.kid"
        
        with patch('jose.jwt.get_unverified_header') as mock_get_header:
            mock_get_header.return_value = {}  # No 'kid' field
            
            with pytest.raises(HTTPException) as exc_info:
                await auth_bearer.verify_token(mock_token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_verify_token_key_not_found(self, auth_bearer, mock_auth0_jwks):
        """Test token verification with key not found in JWKS"""
        mock_token = "token.with.unknown.kid"
        
        with patch('jose.jwt.get_unverified_header') as mock_get_header:
            mock_get_header.return_value = {"kid": "unknown-key-id"}
            
            with patch.object(auth_bearer, 'get_jwks') as mock_get_jwks:
                mock_get_jwks.return_value = mock_auth0_jwks
                
                with pytest.raises(HTTPException) as exc_info:
                    await auth_bearer.verify_token(mock_token)
                
                assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticationHelpers:
    """Test cases for authentication helper functions"""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, mock_auth0_user):
        """Test successful user extraction from token"""
        mock_credentials = Mock()
        mock_credentials.credentials = "valid.jwt.token"
        
        with patch('app.core.auth.Auth0JWTBearer') as mock_bearer_class:
            mock_bearer = Mock()
            mock_bearer.verify_token.return_value = mock_auth0_user
            mock_bearer_class.return_value = mock_bearer
            
            user = await get_current_user(mock_credentials)
            
            assert user["sub"] == "auth0|test123"
            assert user["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        """Test user extraction with invalid token"""
        mock_credentials = Mock()
        mock_credentials.credentials = "invalid.jwt.token"
        
        with patch('app.core.auth.Auth0JWTBearer') as mock_bearer_class:
            mock_bearer = Mock()
            mock_bearer.verify_token.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            mock_bearer_class.return_value = mock_bearer
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(mock_credentials)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_verify_permissions_sufficient(self):
        """Test permission verification with sufficient permissions"""
        user_permissions = {
            "google": ["calendar.events", "calendar.readonly"],
            "github": ["repo", "user"]
        }
        required_permissions = {
            "google": ["calendar.events"],
            "github": ["repo"]
        }
        
        result = await verify_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is True
        assert result["missing_permissions"] == {}

    @pytest.mark.asyncio
    async def test_verify_permissions_insufficient(self):
        """Test permission verification with insufficient permissions"""
        user_permissions = {
            "google": ["calendar.readonly"]
        }
        required_permissions = {
            "google": ["calendar.events"],
            "github": ["repo"]
        }
        
        result = await verify_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is False
        assert "google" in result["missing_permissions"]
        assert "github" in result["missing_permissions"]
        assert "calendar.events" in result["missing_permissions"]["google"]
        assert "repo" in result["missing_permissions"]["github"]

    @pytest.mark.asyncio
    async def test_verify_permissions_empty_required(self):
        """Test permission verification with no required permissions"""
        user_permissions = {"google": ["calendar.readonly"]}
        required_permissions = {}
        
        result = await verify_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is True
        assert result["missing_permissions"] == {}

    @pytest.mark.asyncio
    async def test_verify_permissions_empty_user(self):
        """Test permission verification with no user permissions"""
        user_permissions = {}
        required_permissions = {
            "google": ["calendar.events"],
            "github": ["repo"]
        }
        
        result = await verify_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is False
        assert len(result["missing_permissions"]) == 2

    @pytest.mark.asyncio
    async def test_verify_permissions_partial_service_match(self):
        """Test permission verification with partial service permissions"""
        user_permissions = {
            "google": ["calendar.readonly", "gmail.send"],
            "github": ["user"]  # Missing 'repo' permission
        }
        required_permissions = {
            "google": ["calendar.readonly", "calendar.events"],  # Missing 'calendar.events'
            "github": ["repo", "user"]  # Missing 'repo'
        }
        
        result = await verify_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is False
        assert "google" in result["missing_permissions"]
        assert "github" in result["missing_permissions"]
        assert "calendar.events" in result["missing_permissions"]["google"]
        assert "repo" in result["missing_permissions"]["github"]


class TestSessionManagement:
    """Test cases for session management"""

    @pytest.mark.asyncio
    async def test_create_session_success(self):
        """Test successful session creation"""
        user_data = {
            "sub": "auth0|test123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        with patch('app.core.session.session_manager') as mock_session_manager:
            mock_session_manager.create_session.return_value = {
                "session_id": "session_123",
                "expires_at": datetime.now(timezone.utc) + timedelta(hours=24)
            }
            
            from app.core.auth import create_user_session
            session = await create_user_session(user_data)
            
            assert session["session_id"] == "session_123"
            assert "expires_at" in session

    @pytest.mark.asyncio
    async def test_validate_session_success(self):
        """Test successful session validation"""
        session_id = "valid_session_123"
        
        with patch('app.core.session.session_manager') as mock_session_manager:
            mock_session_manager.validate_session.return_value = {
                "valid": True,
                "user_id": "auth0|test123",
                "expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
            }
            
            from app.core.auth import validate_user_session
            result = await validate_user_session(session_id)
            
            assert result["valid"] is True
            assert result["user_id"] == "auth0|test123"

    @pytest.mark.asyncio
    async def test_validate_session_expired(self):
        """Test session validation with expired session"""
        session_id = "expired_session_123"
        
        with patch('app.core.session.session_manager') as mock_session_manager:
            mock_session_manager.validate_session.return_value = {
                "valid": False,
                "reason": "expired"
            }
            
            from app.core.auth import validate_user_session
            result = await validate_user_session(session_id)
            
            assert result["valid"] is False
            assert result["reason"] == "expired"

    @pytest.mark.asyncio
    async def test_refresh_session_success(self):
        """Test successful session refresh"""
        session_id = "session_to_refresh"
        
        with patch('app.core.session.session_manager') as mock_session_manager:
            mock_session_manager.refresh_session.return_value = {
                "session_id": session_id,
                "expires_at": datetime.now(timezone.utc) + timedelta(hours=24),
                "refreshed": True
            }
            
            from app.core.auth import refresh_user_session
            result = await refresh_user_session(session_id)
            
            assert result["refreshed"] is True
            assert "expires_at" in result

    @pytest.mark.asyncio
    async def test_revoke_session_success(self):
        """Test successful session revocation"""
        session_id = "session_to_revoke"
        
        with patch('app.core.session.session_manager') as mock_session_manager:
            mock_session_manager.revoke_session.return_value = {
                "revoked": True,
                "session_id": session_id
            }
            
            from app.core.auth import revoke_user_session
            result = await revoke_user_session(session_id)
            
            assert result["revoked"] is True
            assert result["session_id"] == session_id