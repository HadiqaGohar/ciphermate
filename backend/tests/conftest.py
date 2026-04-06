"""Pytest configuration and fixtures for backend tests"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    TestSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def test_client() -> TestClient:
    """Create test client"""
    return TestClient(app)


@pytest.fixture
async def async_test_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_auth0_user():
    """Mock Auth0 user data"""
    return {
        "sub": "auth0|test123",
        "email": "test@example.com",
        "name": "Test User",
        "aud": settings.AUTH0_AUDIENCE,
        "iss": f"https://{settings.AUTH0_DOMAIN}/",
        "exp": 9999999999,  # Far future
        "iat": 1000000000,
        "scope": "openid profile email"
    }


@pytest.fixture
def mock_jwt_token(mock_auth0_user):
    """Mock JWT token"""
    return "mock.jwt.token"


@pytest.fixture
def mock_auth0_jwks():
    """Mock Auth0 JWKS response"""
    return {
        "keys": [
            {
                "kty": "RSA",
                "kid": "test-key-id",
                "use": "sig",
                "n": "test-n-value",
                "e": "AQAB"
            }
        ]
    }


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response"""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": '{"intent": "calendar_create_event", "confidence": 0.95, "parameters": {"title": "Test Event", "start_time": "2024-01-01T10:00:00Z"}}'
                        }
                    ]
                }
            }
        ]
    }


@pytest.fixture
def mock_token_vault_response():
    """Mock Token Vault API response"""
    return {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": "calendar.readonly"
    }


@pytest.fixture
def mock_google_api_response():
    """Mock Google API response"""
    return {
        "items": [
            {
                "id": "event123",
                "summary": "Test Event",
                "start": {"dateTime": "2024-01-01T10:00:00Z"},
                "end": {"dateTime": "2024-01-01T11:00:00Z"}
            }
        ]
    }


@pytest.fixture
def mock_github_api_response():
    """Mock GitHub API response"""
    return {
        "id": 123,
        "title": "Test Issue",
        "body": "Test issue body",
        "state": "open",
        "html_url": "https://github.com/test/repo/issues/123"
    }


@pytest.fixture
def mock_slack_api_response():
    """Mock Slack API response"""
    return {
        "ok": True,
        "channel": "C1234567890",
        "ts": "1234567890.123456",
        "message": {
            "text": "Test message",
            "user": "U1234567890"
        }
    }


@pytest.fixture
def mock_httpx_client():
    """Mock httpx AsyncClient"""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status.return_value = None
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    mock_client.put.return_value = mock_response
    mock_client.delete.return_value = mock_response
    return mock_client


@pytest.fixture(autouse=True)
def override_get_db(test_db):
    """Override database dependency for tests"""
    def _override_get_db():
        return test_db
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()