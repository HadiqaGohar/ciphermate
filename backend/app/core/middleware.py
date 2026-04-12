"""
Custom middleware for CipherMate API
"""

import time
import json
import logging
from typing import Callable, Optional
from fastapi import Request, Response, status, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .exceptions import ValidationError, RateLimitError, create_validation_error
from .validation import sanitize_string, LIMITS
from .audit_service import audit_service
from .security_monitor import security_monitor, security_metrics
from .config import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Enhanced security headers middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        if not settings.ENABLE_SECURITY_HEADERS:
            return response
        
        # Basic security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Enhanced Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # Relaxed for development
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "connect-src 'self' https:",
            "font-src 'self'",
            "object-src 'none'",
            "media-src 'self'",
            "frame-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "upgrade-insecure-requests"
        ]
        
        # Adjust CSP for development vs production
        if settings.APP_ENV == "production":
            # Stricter CSP for production
            csp_directives = [directive.replace("'unsafe-inline' 'unsafe-eval'", "") for directive in csp_directives]
            csp_directives = [directive.replace("'unsafe-inline'", "") for directive in csp_directives]
        
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # HSTS header for HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        # Additional security headers
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        
        # Remove server information
        if "server" in response.headers:
            del response.headers["server"]
        
        # Add security-related cache headers for sensitive endpoints
        if any(path in request.url.path for path in ["/api/v1/auth", "/api/v1/permissions", "/api/v1/token-vault"]):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Enhanced request validation and sanitization middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.max_request_size = settings.MAX_REQUEST_SIZE_MB * 1024 * 1024
        self.max_header_size = settings.MAX_HEADER_SIZE_KB * 1024
        self.suspicious_patterns = [
            "../", "..\\", "<script", "javascript:", "data:text/html", "vbscript:",
            "eval(", "expression(", "import(", "require(", "document.cookie",
            "window.location", "document.write", "innerHTML", "outerHTML"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Validate request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_request_size:
            await self._log_security_violation(
                request, "request_too_large", 
                {"size": int(content_length), "max_size": self.max_request_size}
            )
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "error": "REQUEST_TOO_LARGE",
                    "message": f"Request size exceeds maximum allowed size of {self.max_request_size} bytes"
                }
            )
        
        # Validate headers
        for name, value in request.headers.items():
            if len(value) > self.max_header_size:
                await self._log_security_violation(
                    request, "header_too_large",
                    {"header": name, "size": len(value), "max_size": self.max_header_size}
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "HEADER_TOO_LARGE",
                        "message": f"Header '{name}' exceeds maximum size"
                    }
                )
            
            # Check for suspicious header content
            if self._contains_suspicious_patterns(value):
                await self._log_security_violation(
                    request, "suspicious_header_content",
                    {"header": name, "value": value[:100]}  # Log only first 100 chars
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "SUSPICIOUS_HEADER",
                        "message": f"Header '{name}' contains potentially harmful content"
                    }
                )
        
        # Validate URL path
        if len(request.url.path) > 2048:
            await self._log_security_violation(
                request, "uri_too_long",
                {"path_length": len(request.url.path)}
            )
            return JSONResponse(
                status_code=status.HTTP_414_URI_TOO_LONG,
                content={
                    "error": "URI_TOO_LONG",
                    "message": "Request URI is too long"
                }
            )
        
        # Check for suspicious patterns in URL
        if self._contains_suspicious_patterns(request.url.path):
            await self._log_security_violation(
                request, "suspicious_url_pattern",
                {"path": request.url.path}
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "SUSPICIOUS_REQUEST",
                    "message": "Request contains potentially harmful content"
                }
            )
        
        # Check query parameters for suspicious content
        if request.url.query:
            if self._contains_suspicious_patterns(request.url.query):
                await self._log_security_violation(
                    request, "suspicious_query_params",
                    {"query": request.url.query[:200]}  # Log only first 200 chars
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "SUSPICIOUS_QUERY",
                        "message": "Query parameters contain potentially harmful content"
                    }
                )
        
        return await call_next(request)
    
    def _contains_suspicious_patterns(self, text: str) -> bool:
        """Check if text contains suspicious patterns"""
        text_lower = text.lower()
        for pattern in self.suspicious_patterns:
            if pattern.lower() in text_lower:
                return True
        return False
    
    async def _log_security_violation(self, request: Request, violation_type: str, details: dict):
        """Log security violations"""
        if audit_service:
            try:
                user_id = 0
                if hasattr(request.state, "user") and request.state.user:
                    user_id = int(request.state.user.get("sub", 0))
                
                await audit_service.log_security_event(
                    user_id=user_id,
                    event_type=violation_type,
                    severity="warning",
                    details={
                        "endpoint": str(request.url.path),
                        "method": request.method,
                        "user_agent": request.headers.get("user-agent", "unknown"),
                        **details
                    },
                    request=request
                )
            except Exception as e:
                logger.error(f"Failed to log security violation: {e}")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enhanced rate limiting middleware with burst protection and IP tracking"""
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = None, burst_size: int = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or settings.RATE_LIMIT_REQUESTS_PER_MINUTE
        self.burst_size = burst_size or settings.RATE_LIMIT_BURST_SIZE
        self.request_counts = {}  # In production, use Redis
        self.burst_counts = {}   # Track burst requests
        self.window_size = 60    # 1 minute window
        self.burst_window = 10   # 10 second burst window
        self.suspicious_ips = set()  # Track suspicious IPs
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ENABLE_RATE_LIMITING:
            return await call_next(request)
        
        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        user_id = None
        
        # Try to get user ID from request state (set by auth middleware)
        if hasattr(request.state, "user") and request.state.user:
            user_id = request.state.user.get("sub")
            client_key = f"user:{user_id}"
        else:
            client_key = f"ip:{client_ip}"
        
        current_time = time.time()
        
        # Check if IP is in suspicious list (stricter limits)
        rate_limit = self.requests_per_minute
        if client_ip in self.suspicious_ips:
            rate_limit = max(10, rate_limit // 4)  # Reduce limit for suspicious IPs
        
        # Clean old entries for rate limiting
        window_start = current_time - self.window_size
        if client_key in self.request_counts:
            self.request_counts[client_key] = [
                timestamp for timestamp in self.request_counts[client_key]
                if timestamp > window_start
            ]
        else:
            self.request_counts[client_key] = []
        
        # Clean old entries for burst protection
        burst_window_start = current_time - self.burst_window
        if client_key in self.burst_counts:
            self.burst_counts[client_key] = [
                timestamp for timestamp in self.burst_counts[client_key]
                if timestamp > burst_window_start
            ]
        else:
            self.burst_counts[client_key] = []
        
        # Check burst limit first
        if len(self.burst_counts[client_key]) >= self.burst_size:
            # Mark IP as suspicious if excessive burst requests
            if not user_id:  # Only mark IPs without authenticated users
                self.suspicious_ips.add(client_ip)
            
            await self._log_rate_limit_violation(
                user_id, client_ip, "burst_limit_exceeded", 
                len(self.burst_counts[client_key]), self.burst_size, request
            )
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "BURST_LIMIT_EXCEEDED",
                    "message": f"Too many requests in short time. Limit: {self.burst_size} requests per {self.burst_window} seconds",
                    "retry_after": self.burst_window
                },
                headers={"Retry-After": str(self.burst_window)}
            )
        
        # Check regular rate limit
        if len(self.request_counts[client_key]) >= rate_limit:
            await self._log_rate_limit_violation(
                user_id, client_ip, "rate_limit_exceeded",
                len(self.request_counts[client_key]), rate_limit, request
            )
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit of {rate_limit} requests per minute exceeded",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )
        
        # Add current request to counts
        self.request_counts[client_key].append(current_time)
        self.burst_counts[client_key].append(current_time)
        
        return await call_next(request)
    
    async def _log_rate_limit_violation(
        self, user_id: Optional[str], client_ip: str, violation_type: str,
        current_count: int, limit: int, request: Request
    ):
        """Log rate limit violations as security events"""
        if audit_service:
            try:
                await audit_service.log_security_event(
                    user_id=int(user_id) if user_id and user_id.isdigit() else 0,
                    event_type=violation_type,
                    severity="warning" if current_count < limit * 2 else "high",
                    details={
                        "client_ip": client_ip,
                        "requests_count": current_count,
                        "limit": limit,
                        "endpoint": str(request.url.path),
                        "method": request.method,
                        "user_agent": request.headers.get("user-agent", "unknown")
                    },
                    request=request
                )
            except Exception as e:
                logger.error(f"Failed to log rate limit event: {e}")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests for monitoring and debugging"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"({process_time:.3f}s) "
            f"{request.method} {request.url.path}"
        )
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log slow requests
        if process_time > 1.0:
            logger.warning(f"Slow request: {process_time:.3f}s for {request.method} {request.url.path}")
        
        return response


class ContentTypeValidationMiddleware(BaseHTTPMiddleware):
    """Validate content types for POST/PUT requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.allowed_content_types = {
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only validate content type for requests with body
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "").split(";")[0].strip()
            
            if content_type and content_type not in self.allowed_content_types:
                return JSONResponse(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    content={
                        "error": "UNSUPPORTED_MEDIA_TYPE",
                        "message": f"Content type '{content_type}' is not supported",
                        "allowed_types": list(self.allowed_content_types)
                    }
                )
        
        return await call_next(request)


class SuspiciousActivityMiddleware(BaseHTTPMiddleware):
    """Detect and prevent suspicious activities using security monitor"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"

        # Never block localhost or private IPs in development
        if not client_ip.startswith(("127.", "10.", "192.168.", "172.")):
            # Check if IP is blocked by security monitor
            if security_monitor.is_ip_blocked(client_ip):
                security_metrics.increment_blocked_requests()
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "error": "IP_BLOCKED",
                        "message": "Your IP has been temporarily blocked due to suspicious activity"
                    }
                )
        
        # Process request
        response = await call_next(request)
        
        # Track request in security monitor
        is_error = response.status_code >= 400
        security_monitor.track_request(client_ip, is_error)
        
        # Track failed logins specifically
        if (response.status_code in [401, 403] and 
            any(path in request.url.path for path in ["/api/v1/auth", "/login"])):
            security_monitor.track_failed_login(client_ip)
        
        return response


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Sanitize all input data to prevent injection attacks"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only process requests with JSON body
        content_type = request.headers.get("content-type", "").split(";")[0].strip()
        
        if (content_type == "application/json" and 
            request.method in ["POST", "PUT", "PATCH"]):
            
            try:
                # Read and validate body
                body = await request.body()
                if body:
                    # Parse JSON
                    import json
                    data = json.loads(body)
                    
                    # Sanitize the data
                    sanitized_data = self._sanitize_data(data)
                    
                    # Replace request body with sanitized data
                    sanitized_body = json.dumps(sanitized_data).encode()
                    
                    async def receive():
                        return {"type": "http.request", "body": sanitized_body}
                    
                    request._receive = receive
                    
            except Exception as e:
                logger.error(f"Input sanitization error: {e}")
                # Continue with original request if sanitization fails
                pass
        
        return await call_next(request)
    
    def _sanitize_data(self, data):
        """Recursively sanitize data structure"""
        if isinstance(data, dict):
            return {key: self._sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, str):
            # Apply security validation
            from .validation import validate_against_injection_attacks
            result = validate_against_injection_attacks(data)
            if result.errors:
                logger.warning(f"Blocked potentially malicious input: {data[:100]}")
                return ""  # Replace with empty string if malicious
            return result.sanitized_value or data
        else:
            return data


class JSONValidationMiddleware(BaseHTTPMiddleware):
    """Validate JSON payloads"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.max_json_size = 1024 * 1024  # 1MB
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only validate JSON for appropriate content types
        content_type = request.headers.get("content-type", "").split(";")[0].strip()
        
        if content_type == "application/json" and request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Read body
                body = await request.body()
                
                # Check size
                if len(body) > self.max_json_size:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "error": "JSON_TOO_LARGE",
                            "message": f"JSON payload exceeds maximum size of {self.max_json_size} bytes"
                        }
                    )
                
                # Validate JSON structure
                if body:
                    try:
                        import json
                        json.loads(body)
                    except json.JSONDecodeError as e:
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "error": "INVALID_JSON",
                                "message": f"Invalid JSON format: {str(e)}"
                            }
                        )
                
                # Recreate request with validated body
                async def receive():
                    return {"type": "http.request", "body": body}
                
                request._receive = receive
                
            except Exception as e:
                logger.error(f"JSON validation error: {e}")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "REQUEST_PROCESSING_ERROR",
                        "message": "Failed to process request body"
                    }
                )
        
        return await call_next(request)


# Utility function to add all middleware to the app
def add_middleware(app: FastAPI):
    """Add all custom middleware to the FastAPI app"""
    
    # Add middleware in reverse order (last added is executed first)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(InputSanitizationMiddleware)
    app.add_middleware(JSONValidationMiddleware)
    app.add_middleware(ContentTypeValidationMiddleware)
    app.add_middleware(SuspiciousActivityMiddleware)
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(RateLimitMiddleware, 
                      requests_per_minute=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
                      burst_size=settings.RATE_LIMIT_BURST_SIZE)