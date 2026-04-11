"""
Third-party API integration service with secure token injection and comprehensive error handling.
Supports Google Calendar, Gmail, GitHub, and Slack APIs with retry logic and rate limiting.
"""

from typing import Optional, Dict, Any, List, Union
import httpx
import json
import asyncio
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlencode

from app.core.config import settings
from app.core.token_vault import TokenVaultService, TokenVaultError, TokenNotFoundError
from app.models.audit_log import AuditLog
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class APIServiceError(Exception):
    """Base exception for API integration service"""
    pass


class RateLimitError(APIServiceError):
    """Raised when API rate limit is exceeded"""
    pass


class ServiceUnavailableError(APIServiceError):
    """Raised when external service is unavailable"""
    pass


class AuthorizationError(APIServiceError):
    """Raised when authorization fails"""
    pass


class APIService(Enum):
    """Supported API services"""
    GOOGLE_CALENDAR = "google_calendar"
    GMAIL = "gmail"
    GITHUB = "github"
    SLACK = "slack"


@dataclass
class APIResponse:
    """Standardized API response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    service: Optional[str] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None


@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


class APIIntegrationService:
    """
    Core service for integrating with third-party APIs using tokens from Auth0 Token Vault.
    Provides secure token injection, response parsing, error handling, and retry logic.
    """
    
    def __init__(self):
        self.token_vault = TokenVaultService()
        self.retry_config = RetryConfig()
        self._rate_limit_cache: Dict[str, Dict[str, Any]] = {}
        
        # Service-specific configurations
        self.service_configs = {
            APIService.GOOGLE_CALENDAR: {
                "base_url": "https://www.googleapis.com/calendar/v3",
                "token_header": "Authorization",
                "token_prefix": "Bearer",
                "rate_limit_header": "X-RateLimit-Remaining",
                "rate_limit_reset_header": "X-RateLimit-Reset"
            },
            APIService.GMAIL: {
                "base_url": "https://gmail.googleapis.com/gmail/v1",
                "token_header": "Authorization",
                "token_prefix": "Bearer",
                "rate_limit_header": "X-RateLimit-Remaining",
                "rate_limit_reset_header": "X-RateLimit-Reset"
            },
            APIService.GITHUB: {
                "base_url": "https://api.github.com",
                "token_header": "Authorization",
                "token_prefix": "token",
                "rate_limit_header": "X-RateLimit-Remaining",
                "rate_limit_reset_header": "X-RateLimit-Reset"
            },
            APIService.SLACK: {
                "base_url": "https://slack.com/api",
                "token_header": "Authorization",
                "token_prefix": "Bearer",
                "rate_limit_header": "X-RateLimit-Remaining",
                "rate_limit_reset_header": "X-RateLimit-Reset"
            }
        }
    
    async def make_api_call(
        self,
        user_id: str,
        service: APIService,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ) -> APIResponse:
        """
        Make an authenticated API call to a third-party service.
        
        Args:
            user_id: User ID for token retrieval
            service: Target API service
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            data: Request body data (for POST/PUT requests)
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            APIResponse object with standardized response data
        """
        if not user_id or not service or not method or not endpoint:
            raise ValueError("user_id, service, method, and endpoint are required")
        
        service_name = service.value
        
        try:
            # Check rate limits before making the call
            await self._check_rate_limits(user_id, service_name)
            
            # Get token from Token Vault
            token_data = await self.token_vault.retrieve_token(user_id, service_name)
            if not token_data:
                raise AuthorizationError(f"No valid token found for {service_name}")
            
            # Build the request
            config = self.service_configs[service]
            url = urljoin(config["base_url"], endpoint.lstrip('/'))
            
            # Prepare headers with token injection
            request_headers = self._prepare_headers(token_data, config, headers)
            
            # Make the API call with retry logic
            response = await self._make_request_with_retry(
                method=method,
                url=url,
                headers=request_headers,
                data=data,
                params=params,
                timeout=timeout,
                service_name=service_name
            )
            
            # Parse and return response
            api_response = await self._parse_response(response, service_name)
            
            # Log the API call for audit purposes
            await self._log_api_call(user_id, service_name, method, endpoint, api_response)
            
            return api_response
            
        except (TokenVaultError, AuthorizationError, RateLimitError, ServiceUnavailableError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in API call to {service_name}: {e}")
            raise APIServiceError(f"API call failed: {str(e)}")
    
    def _prepare_headers(
        self,
        token_data: Dict[str, Any],
        config: Dict[str, str],
        additional_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Prepare request headers with secure token injection"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"CipherMate/1.0 ({settings.APP_NAME})"
        }
        
        # Add additional headers if provided
        if additional_headers:
            headers.update(additional_headers)
        
        # Inject authentication token
        access_token = token_data.get("access_token")
        if access_token:
            token_header = config["token_header"]
            token_prefix = config["token_prefix"]
            headers[token_header] = f"{token_prefix} {access_token}"
        
        return headers
    
    async def _make_request_with_retry(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: float = 30.0,
        service_name: str = ""
    ) -> httpx.Response:
        """Make HTTP request with exponential backoff retry logic"""
        last_exception = None
        
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    # Prepare request data
                    request_kwargs = {
                        "method": method,
                        "url": url,
                        "headers": headers
                    }
                    
                    if params:
                        request_kwargs["params"] = params
                    
                    if data and method.upper() in ["POST", "PUT", "PATCH"]:
                        if headers.get("Content-Type") == "application/json":
                            request_kwargs["json"] = data
                        else:
                            request_kwargs["data"] = data
                    
                    response = await client.request(**request_kwargs)
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        retry_after = self._get_retry_after(response)
                        if attempt < self.retry_config.max_retries:
                            logger.warning(f"Rate limited by {service_name}, retrying after {retry_after}s")
                            await asyncio.sleep(retry_after)
                            continue
                        else:
                            raise RateLimitError(f"Rate limit exceeded for {service_name}")
                    
                    # Handle server errors with retry
                    if response.status_code >= 500 and attempt < self.retry_config.max_retries:
                        delay = self._calculate_retry_delay(attempt)
                        logger.warning(f"Server error from {service_name} (HTTP {response.status_code}), retrying in {delay}s")
                        await asyncio.sleep(delay)
                        continue
                    
                    # Update rate limit cache
                    self._update_rate_limit_cache(service_name, response)
                    
                    return response
                    
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self.retry_config.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    logger.warning(f"Timeout for {service_name}, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise ServiceUnavailableError(f"Service {service_name} timed out after {self.retry_config.max_retries} retries")
            
            except httpx.ConnectError as e:
                last_exception = e
                if attempt < self.retry_config.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    logger.warning(f"Connection error for {service_name}, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise ServiceUnavailableError(f"Cannot connect to {service_name} after {self.retry_config.max_retries} retries")
            
            except Exception as e:
                last_exception = e
                if attempt < self.retry_config.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    logger.warning(f"Request error for {service_name}: {e}, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    continue
                else:
                    break
        
        # If we get here, all retries failed
        if last_exception:
            raise ServiceUnavailableError(f"Service {service_name} unavailable: {str(last_exception)}")
        else:
            raise ServiceUnavailableError(f"Service {service_name} unavailable after {self.retry_config.max_retries} retries")
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate retry delay with exponential backoff and jitter"""
        delay = min(
            self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt),
            self.retry_config.max_delay
        )
        
        if self.retry_config.jitter:
            import random
            delay *= (0.5 + random.random() * 0.5)  # Add 0-50% jitter
        
        return delay
    
    def _get_retry_after(self, response: httpx.Response) -> float:
        """Extract retry-after value from response headers"""
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
        
        # Default retry delay for rate limiting
        return 60.0
    
    def _update_rate_limit_cache(self, service_name: str, response: httpx.Response) -> None:
        """Update rate limit information from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset_time = response.headers.get("X-RateLimit-Reset")
        
        if remaining is not None:
            cache_entry = {
                "remaining": int(remaining),
                "updated_at": datetime.now(timezone.utc)
            }
            
            if reset_time:
                try:
                    # Handle Unix timestamp
                    reset_timestamp = int(reset_time)
                    cache_entry["reset_at"] = datetime.fromtimestamp(reset_timestamp, timezone.utc)
                except ValueError:
                    # Handle ISO format or other formats
                    pass
            
            self._rate_limit_cache[service_name] = cache_entry
    
    async def _check_rate_limits(self, user_id: str, service_name: str) -> None:
        """Check if we're within rate limits before making a request"""
        cache_entry = self._rate_limit_cache.get(service_name)
        if not cache_entry:
            return  # No rate limit info available
        
        remaining = cache_entry.get("remaining", 1)
        reset_at = cache_entry.get("reset_at")
        
        if remaining <= 0 and reset_at:
            now = datetime.now(timezone.utc)
            if now < reset_at:
                wait_time = (reset_at - now).total_seconds()
                if wait_time > 0:
                    logger.warning(f"Rate limit exceeded for {service_name}, waiting {wait_time}s")
                    raise RateLimitError(f"Rate limit exceeded for {service_name}. Reset in {wait_time:.0f} seconds")
    
    async def _parse_response(self, response: httpx.Response, service_name: str) -> APIResponse:
        """Parse HTTP response into standardized APIResponse format"""
        try:
            # Handle different content types
            content_type = response.headers.get("content-type", "").lower()
            
            if "application/json" in content_type:
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    data = {"raw_content": response.text}
            else:
                data = {"raw_content": response.text}
            
            # Extract rate limit information
            rate_limit_remaining = None
            rate_limit_reset = None
            
            remaining_header = response.headers.get("X-RateLimit-Remaining")
            if remaining_header:
                try:
                    rate_limit_remaining = int(remaining_header)
                except ValueError:
                    pass
            
            reset_header = response.headers.get("X-RateLimit-Reset")
            if reset_header:
                try:
                    reset_timestamp = int(reset_header)
                    rate_limit_reset = datetime.fromtimestamp(reset_timestamp, timezone.utc)
                except ValueError:
                    pass
            
            # Determine success based on status code
            success = 200 <= response.status_code < 300
            error = None
            
            if not success:
                if isinstance(data, dict):
                    error = data.get("error", data.get("message", f"HTTP {response.status_code}"))
                else:
                    error = f"HTTP {response.status_code}: {response.text[:200]}"
            
            return APIResponse(
                success=success,
                data=data if success else None,
                error=error,
                status_code=response.status_code,
                service=service_name,
                rate_limit_remaining=rate_limit_remaining,
                rate_limit_reset=rate_limit_reset
            )
            
        except Exception as e:
            logger.error(f"Error parsing response from {service_name}: {e}")
            return APIResponse(
                success=False,
                error=f"Response parsing error: {str(e)}",
                status_code=response.status_code,
                service=service_name
            )
    
    async def _log_api_call(
        self,
        user_id: str,
        service_name: str,
        method: str,
        endpoint: str,
        response: APIResponse
    ) -> None:
        """Log API call for audit purposes"""
        try:
            async with AsyncSessionLocal() as db:
                audit_log = AuditLog(
                    user_id=user_id,
                    action_type="api_call",
                    service_name=service_name,
                    details={
                        "method": method,
                        "endpoint": endpoint,
                        "success": response.success,
                        "status_code": response.status_code,
                        "error": response.error,
                        "rate_limit_remaining": response.rate_limit_remaining
                    },
                    timestamp=datetime.now(timezone.utc)
                )
                db.add(audit_log)
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to log API call: {e}")
            # Don't raise here as this is non-critical
    
    async def get_rate_limit_status(self, service_name: str) -> Dict[str, Any]:
        """Get current rate limit status for a service"""
        cache_entry = self._rate_limit_cache.get(service_name, {})
        
        return {
            "service": service_name,
            "remaining": cache_entry.get("remaining"),
            "reset_at": cache_entry.get("reset_at").isoformat() if cache_entry.get("reset_at") else None,
            "last_updated": cache_entry.get("updated_at").isoformat() if cache_entry.get("updated_at") else None
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the API integration service"""
        return {
            "status": "healthy",
            "services_configured": list(self.service_configs.keys()),
            "rate_limit_cache_size": len(self._rate_limit_cache),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global instance
api_integration_service = APIIntegrationService()