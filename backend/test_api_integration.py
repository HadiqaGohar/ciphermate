"""
Comprehensive tests for the third-party API integration service.
Tests the core integration service, service clients, and API endpoints.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, timedelta
import httpx
import json

from app.core.api_integration import (
    APIIntegrationService, APIService, APIResponse, RetryConfig,
    APIServiceError, RateLimitError, ServiceUnavailableError, AuthorizationError
)
from app.core.service_clients import (
    GoogleCalendarClient, GmailClient, GitHubClient, SlackClient,
    ServiceClientFactory
)
from app.core.token_vault import TokenVaultService


class TestAPIIntegrationService:
    """Test the core API integration service"""
    
    @pytest.fixture
    def api_service(self):
        """Create API integration service instance"""
        return APIIntegrationService()
    
    @pytest.fixture
    def mock_token_vault(self):
        """Mock token vault service"""
        mock = AsyncMock(spec=TokenVaultService)
        mock.retrieve_token.return_value = {
            "access_token": "test_token",
            "token_type": "Bearer"
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_make_api_call_success(self, api_service, mock_token_vault):
        """Test successful API call"""
        api_service.token_vault = mock_token_vault
        
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"data": "test"}'
        
        with patch('httpx.AsyncClient') as mock_client, \
             patch.object(api_service, '_log_api_call', new_callable=AsyncMock):
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
            
            result = await api_service.make_api_call(
                user_id="test_user",
                service=APIService.GITHUB,
                method="GET",
                endpoint="/user"
            )
            
            assert result.success is True
            assert result.data == {"data": "test"}
            assert result.status_code == 200
            assert result.service == "github"
    
    @pytest.mark.asyncio
    async def test_make_api_call_no_token(self, api_service, mock_token_vault):
        """Test API call when no token is available"""
        mock_token_vault.retrieve_token.return_value = None
        api_service.token_vault = mock_token_vault
        
        with pytest.raises(AuthorizationError):
            await api_service.make_api_call(
                user_id="test_user",
                service=APIService.GITHUB,
                method="GET",
                endpoint="/user"
            )
    
    @pytest.mark.asyncio
    async def test_make_api_call_rate_limited(self, api_service, mock_token_vault):
        """Test API call with rate limiting"""
        api_service.token_vault = mock_token_vault
        
        # Mock rate limited response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
            
            with pytest.raises(RateLimitError):
                await api_service.make_api_call(
                    user_id="test_user",
                    service=APIService.GITHUB,
                    method="GET",
                    endpoint="/user"
                )
    
    @pytest.mark.asyncio
    async def test_retry_logic(self, api_service, mock_token_vault):
        """Test retry logic with exponential backoff"""
        api_service.token_vault = mock_token_vault
        api_service.retry_config.max_retries = 2
        
        # Mock server error responses
        mock_response = MagicMock()
        mock_response.status_code = 500
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
            
            with patch('asyncio.sleep') as mock_sleep:
                with pytest.raises(ServiceUnavailableError):
                    await api_service.make_api_call(
                        user_id="test_user",
                        service=APIService.GITHUB,
                        method="GET",
                        endpoint="/user"
                    )
                
                # Verify sleep was called for retries
                assert mock_sleep.call_count == 2
    
    def test_prepare_headers(self, api_service):
        """Test header preparation with token injection"""
        token_data = {
            "access_token": "test_token",
            "token_type": "Bearer"
        }
        
        config = {
            "token_header": "Authorization",
            "token_prefix": "Bearer"
        }
        
        headers = api_service._prepare_headers(token_data, config)
        
        assert headers["Authorization"] == "Bearer test_token"
        assert headers["Content-Type"] == "application/json"
        assert "CipherMate" in headers["User-Agent"]
    
    def test_calculate_retry_delay(self, api_service):
        """Test retry delay calculation"""
        api_service.retry_config = RetryConfig(
            base_delay=1.0,
            exponential_base=2.0,
            max_delay=60.0,
            jitter=False
        )
        
        # Test exponential backoff
        assert api_service._calculate_retry_delay(0) == 1.0
        assert api_service._calculate_retry_delay(1) == 2.0
        assert api_service._calculate_retry_delay(2) == 4.0
        
        # Test max delay cap
        assert api_service._calculate_retry_delay(10) == 60.0
    
    @pytest.mark.asyncio
    async def test_rate_limit_cache(self, api_service):
        """Test rate limit caching functionality"""
        service_name = "github"
        
        # Mock response with rate limit headers
        mock_response = MagicMock()
        mock_response.headers = {
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Reset": str(int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()))
        }
        
        api_service._update_rate_limit_cache(service_name, mock_response)
        
        # Check cache was updated
        assert service_name in api_service._rate_limit_cache
        assert api_service._rate_limit_cache[service_name]["remaining"] == 100
    
    @pytest.mark.asyncio
    async def test_health_check(self, api_service):
        """Test health check functionality"""
        health = await api_service.health_check()
        
        assert health["status"] == "healthy"
        assert "services_configured" in health
        assert "timestamp" in health


class TestServiceClients:
    """Test service-specific API clients"""
    
    @pytest.fixture
    def mock_api_service(self):
        """Mock API integration service"""
        mock = AsyncMock(spec=APIIntegrationService)
        return mock
    
    @pytest.fixture
    def google_calendar_client(self, mock_api_service):
        """Create Google Calendar client"""
        return GoogleCalendarClient(mock_api_service)
    
    @pytest.fixture
    def gmail_client(self, mock_api_service):
        """Create Gmail client"""
        return GmailClient(mock_api_service)
    
    @pytest.fixture
    def github_client(self, mock_api_service):
        """Create GitHub client"""
        return GitHubClient(mock_api_service)
    
    @pytest.fixture
    def slack_client(self, mock_api_service):
        """Create Slack client"""
        return SlackClient(mock_api_service)
    
    @pytest.mark.asyncio
    async def test_google_calendar_list_calendars(self, google_calendar_client, mock_api_service):
        """Test Google Calendar list calendars"""
        mock_response = APIResponse(
            success=True,
            data={"items": [{"id": "primary", "summary": "Primary"}]},
            service="google_calendar"
        )
        mock_api_service.make_api_call.return_value = mock_response
        
        result = await google_calendar_client.list_calendars("test_user")
        
        assert result.success is True
        assert "items" in result.data
        mock_api_service.make_api_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_google_calendar_create_event(self, google_calendar_client, mock_api_service):
        """Test Google Calendar create event"""
        mock_response = APIResponse(
            success=True,
            data={"id": "event123", "summary": "Test Event"},
            service="google_calendar"
        )
        mock_api_service.make_api_call.return_value = mock_response
        
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        
        result = await google_calendar_client.create_event(
            user_id="test_user",
            summary="Test Event",
            start_time=start_time,
            end_time=end_time
        )
        
        assert result.success is True
        assert result.data["summary"] == "Test Event"
        mock_api_service.make_api_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_gmail_send_message(self, gmail_client, mock_api_service):
        """Test Gmail send message"""
        mock_response = APIResponse(
            success=True,
            data={"id": "msg123", "labelIds": ["SENT"]},
            service="gmail"
        )
        mock_api_service.make_api_call.return_value = mock_response
        
        result = await gmail_client.send_message(
            user_id="test_user",
            to="test@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        
        assert result.success is True
        assert "id" in result.data
        mock_api_service.make_api_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_github_create_issue(self, github_client, mock_api_service):
        """Test GitHub create issue"""
        mock_response = APIResponse(
            success=True,
            data={"id": 123, "title": "Test Issue", "number": 1},
            service="github"
        )
        mock_api_service.make_api_call.return_value = mock_response
        
        result = await github_client.create_issue(
            user_id="test_user",
            owner="testowner",
            repo="testrepo",
            title="Test Issue",
            body="Test Body"
        )
        
        assert result.success is True
        assert result.data["title"] == "Test Issue"
        mock_api_service.make_api_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_slack_send_message(self, slack_client, mock_api_service):
        """Test Slack send message"""
        mock_response = APIResponse(
            success=True,
            data={"ok": True, "ts": "1234567890.123456"},
            service="slack"
        )
        mock_api_service.make_api_call.return_value = mock_response
        
        result = await slack_client.send_message(
            user_id="test_user",
            channel="#general",
            text="Hello, World!"
        )
        
        assert result.success is True
        assert result.data["ok"] is True
        mock_api_service.make_api_call.assert_called_once()


class TestServiceClientFactory:
    """Test the service client factory"""
    
    @pytest.fixture
    def factory(self):
        """Create service client factory"""
        mock_api_service = AsyncMock(spec=APIIntegrationService)
        return ServiceClientFactory(mock_api_service)
    
    def test_get_google_calendar_client(self, factory):
        """Test getting Google Calendar client"""
        client = factory.get_google_calendar_client()
        assert isinstance(client, GoogleCalendarClient)
        
        # Test caching
        client2 = factory.get_google_calendar_client()
        assert client is client2
    
    def test_get_gmail_client(self, factory):
        """Test getting Gmail client"""
        client = factory.get_gmail_client()
        assert isinstance(client, GmailClient)
    
    def test_get_github_client(self, factory):
        """Test getting GitHub client"""
        client = factory.get_github_client()
        assert isinstance(client, GitHubClient)
    
    def test_get_slack_client(self, factory):
        """Test getting Slack client"""
        client = factory.get_slack_client()
        assert isinstance(client, SlackClient)
    
    def test_get_client_by_name(self, factory):
        """Test getting client by service name"""
        # Test various service name formats
        assert isinstance(factory.get_client("google_calendar"), GoogleCalendarClient)
        assert isinstance(factory.get_client("calendar"), GoogleCalendarClient)
        assert isinstance(factory.get_client("gmail"), GmailClient)
        assert isinstance(factory.get_client("email"), GmailClient)
        assert isinstance(factory.get_client("github"), GitHubClient)
        assert isinstance(factory.get_client("slack"), SlackClient)
        
        # Test unsupported service
        with pytest.raises(ValueError):
            factory.get_client("unsupported")


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.fixture
    def api_service(self):
        """Create API integration service instance"""
        return APIIntegrationService()
    
    @pytest.mark.asyncio
    async def test_invalid_parameters(self, api_service):
        """Test validation of invalid parameters"""
        with pytest.raises(ValueError):
            await api_service.make_api_call(
                user_id="",  # Empty user ID
                service=APIService.GITHUB,
                method="GET",
                endpoint="/user"
            )
        
        with pytest.raises(ValueError):
            await api_service.make_api_call(
                user_id="test_user",
                service=APIService.GITHUB,
                method="",  # Empty method
                endpoint="/user"
            )
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, api_service):
        """Test timeout handling"""
        mock_token_vault = AsyncMock()
        mock_token_vault.retrieve_token.return_value = {"access_token": "test"}
        api_service.token_vault = mock_token_vault
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                side_effect=httpx.TimeoutException("Request timed out")
            )
            
            with pytest.raises(ServiceUnavailableError):
                await api_service.make_api_call(
                    user_id="test_user",
                    service=APIService.GITHUB,
                    method="GET",
                    endpoint="/user"
                )
    
    @pytest.mark.asyncio
    async def test_connection_error_handling(self, api_service):
        """Test connection error handling"""
        mock_token_vault = AsyncMock()
        mock_token_vault.retrieve_token.return_value = {"access_token": "test"}
        api_service.token_vault = mock_token_vault
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                side_effect=httpx.ConnectError("Connection failed")
            )
            
            with pytest.raises(ServiceUnavailableError):
                await api_service.make_api_call(
                    user_id="test_user",
                    service=APIService.GITHUB,
                    method="GET",
                    endpoint="/user"
                )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])