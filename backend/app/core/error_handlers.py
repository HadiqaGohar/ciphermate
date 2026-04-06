"""
Global error handlers for FastAPI application
"""

import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

from .exceptions import (
    CipherMateException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    TokenError,
    ServiceUnavailableError,
    RateLimitError,
    AIProcessingError,
    DataIntegrityError,
    ConfigurationError,
    ErrorResponse,
    ErrorDetail
)
from .audit_service import audit_service

logger = logging.getLogger(__name__)


def generate_request_id() -> str:
    """Generate a unique request ID for error tracking"""
    return str(uuid.uuid4())[:8]


async def log_error(
    request: Request,
    error: Exception,
    request_id: str,
    user_id: Optional[str] = None
):
    """Log error details for debugging and monitoring"""
    error_details = {
        "request_id": request_id,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "url": str(request.url),
        "method": request.method,
        "user_agent": request.headers.get("user-agent"),
        "ip_address": request.client.host if request.client else None,
    }
    
    # Log to application logger
    logger.error(f"Request {request_id} failed: {error_details}")
    
    # Log to audit system if user is authenticated
    if user_id and audit_service:
        try:
            await audit_service.log_security_event(
                user_id=user_id,
                event_type="api_error",
                severity="error",
                details=error_details,
                request=request
            )
        except Exception as audit_error:
            logger.error(f"Failed to log audit event: {audit_error}")


def create_error_response(
    error: Exception,
    request_id: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    user_action: Optional[Dict[str, Any]] = None
) -> ErrorResponse:
    """Create standardized error response"""
    
    if isinstance(error, CipherMateException):
        return ErrorResponse(
            error=error.error_code,
            message=error.message,
            details=error.details,
            status_code=error.status_code,
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id,
            user_action=error.user_action or user_action
        )
    
    # Handle different error types
    error_code = "INTERNAL_ERROR"
    message = "An internal error occurred"
    details = None
    
    if isinstance(error, HTTPException):
        status_code = error.status_code
        message = error.detail
        error_code = "HTTP_ERROR"
    elif isinstance(error, (PydanticValidationError, RequestValidationError)):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        error_code = "VALIDATION_ERROR"
        message = "Request validation failed"
        details = format_validation_errors(error)
    elif isinstance(error, SQLAlchemyError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = "DATABASE_ERROR"
        message = "Database operation failed"
        if isinstance(error, IntegrityError):
            error_code = "DATA_INTEGRITY_ERROR"
            message = "Data integrity constraint violated"
    
    return ErrorResponse(
        error=error_code,
        message=message,
        details=details,
        status_code=status_code,
        timestamp=datetime.utcnow().isoformat(),
        request_id=request_id,
        user_action=user_action
    )


def format_validation_errors(error: Union[PydanticValidationError, RequestValidationError]) -> list:
    """Format Pydantic validation errors into our standard format"""
    formatted_errors = []
    
    if isinstance(error, RequestValidationError):
        errors = error.errors()
    else:
        errors = error.errors()
    
    for err in errors:
        field_path = ".".join(str(loc) for loc in err["loc"])
        formatted_errors.append(ErrorDetail(
            code=err["type"].upper(),
            message=err["msg"],
            field=field_path,
            details={"input": err.get("input")}
        ).dict())
    
    return formatted_errors


async def ciphermate_exception_handler(request: Request, exc: CipherMateException) -> JSONResponse:
    """Handle CipherMate custom exceptions"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log error
    await log_error(request, exc, request_id, user_id)
    
    # Create response
    error_response = create_error_response(exc, request_id)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log error for server errors
    if exc.status_code >= 500:
        await log_error(request, exc, request_id, user_id)
    
    # Create response
    error_response = create_error_response(exc, request_id)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log validation error
    await log_error(request, exc, request_id, user_id)
    
    # Create response
    error_response = create_error_response(exc, request_id)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict()
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle SQLAlchemy database errors"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log database error
    await log_error(request, exc, request_id, user_id)
    
    # Create appropriate error response
    if isinstance(exc, IntegrityError):
        error = DataIntegrityError(
            message="Data integrity constraint violated",
            details={"constraint": str(exc.orig) if hasattr(exc, 'orig') else None}
        )
    else:
        error = CipherMateException(
            message="Database operation failed",
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    error_response = create_error_response(error, request_id)
    
    return JSONResponse(
        status_code=error_response.status_code,
        content=error_response.dict()
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other unhandled exceptions"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log the full traceback for debugging
    logger.error(f"Unhandled exception in request {request_id}: {traceback.format_exc()}")
    
    # Log error
    await log_error(request, exc, request_id, user_id)
    
    # Create generic error response (don't expose internal details)
    error = CipherMateException(
        message="An unexpected error occurred",
        error_code="INTERNAL_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        user_action={
            "type": "retry",
            "message": "Please try again. If the problem persists, contact support.",
            "contact_support": True
        }
    )
    
    error_response = create_error_response(error, request_id)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


# Rate limiting error handler
async def rate_limit_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle rate limiting errors"""
    request_id = generate_request_id()
    
    # Extract user ID if available
    user_id = None
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub")
    
    # Log rate limit violation
    await log_error(request, exc, request_id, user_id)
    
    # Create rate limit error
    error = RateLimitError(
        message="Rate limit exceeded",
        retry_after=60,  # Default retry after 60 seconds
        details={"endpoint": str(request.url.path)}
    )
    
    error_response = create_error_response(error, request_id)
    
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=error_response.dict(),
        headers={"Retry-After": "60"}
    )


# Utility functions for error handling in endpoints

def handle_service_error(service_name: str, error: Exception) -> ServiceUnavailableError:
    """Convert service errors to ServiceUnavailableError"""
    if "timeout" in str(error).lower():
        return ServiceUnavailableError(
            message=f"{service_name} service timeout",
            service=service_name,
            retry_after=30,
            details={"error_type": "timeout", "original_error": str(error)}
        )
    elif "rate limit" in str(error).lower():
        return RateLimitError(
            message=f"{service_name} rate limit exceeded",
            retry_after=300,
            details={"service": service_name, "original_error": str(error)}
        )
    else:
        return ServiceUnavailableError(
            message=f"{service_name} service error",
            service=service_name,
            details={"original_error": str(error)}
        )


def handle_auth_error(error: Exception, service: Optional[str] = None) -> Union[AuthenticationError, AuthorizationError, TokenError]:
    """Convert authentication/authorization errors"""
    error_str = str(error).lower()
    
    if "token" in error_str and "expired" in error_str:
        return TokenError(
            message="Token has expired",
            service=service,
            details={"reason": "token_expired"}
        )
    elif "token" in error_str and "invalid" in error_str:
        return TokenError(
            message="Invalid token",
            service=service,
            details={"reason": "token_invalid"}
        )
    elif "permission" in error_str or "scope" in error_str:
        return AuthorizationError(
            message="Insufficient permissions",
            service=service,
            details={"original_error": str(error)}
        )
    else:
        return AuthenticationError(
            message="Authentication failed",
            details={"original_error": str(error)}
        )


def handle_ai_error(provider: str, error: Exception) -> AIProcessingError:
    """Convert AI processing errors"""
    error_str = str(error).lower()
    
    if "rate limit" in error_str:
        return RateLimitError(
            message=f"{provider} rate limit exceeded",
            retry_after=60,
            details={"provider": provider, "original_error": str(error)}
        )
    elif "quota" in error_str or "billing" in error_str:
        return ConfigurationError(
            message=f"{provider} quota exceeded or billing issue",
            component=provider,
            details={"original_error": str(error)}
        )
    else:
        return AIProcessingError(
            message=f"AI processing failed",
            provider=provider,
            details={"original_error": str(error)}
        )