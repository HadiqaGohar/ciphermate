"""
Custom exceptions and error handling for CipherMate API
"""

from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class ErrorDetail(BaseModel):
    """Detailed error information"""
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standardized error response format"""
    error: str
    message: str
    details: Optional[Union[str, Dict[str, Any], List[ErrorDetail]]] = None
    status_code: int
    timestamp: str
    request_id: Optional[str] = None
    user_action: Optional[Dict[str, Any]] = None


class CipherMateException(Exception):
    """Base exception for CipherMate application"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
        user_action: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.user_action = user_action
        super().__init__(message)


class ValidationError(CipherMateException):
    """Validation error with field-specific details"""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[List[ErrorDetail]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )
        self.field_errors = field_errors or []


class AuthenticationError(CipherMateException):
    """Authentication-related errors"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
            user_action={
                "type": "authenticate",
                "message": "Please log in to continue",
                "url": "/auth/login"
            }
        )


class AuthorizationError(CipherMateException):
    """Authorization-related errors"""
    
    def __init__(
        self,
        message: str = "Insufficient permissions",
        required_permissions: Optional[List[str]] = None,
        service: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        user_action = None
        if required_permissions and service:
            user_action = {
                "type": "grant_permission",
                "message": f"Grant {service} permissions to continue",
                "service": service,
                "permissions": required_permissions,
                "url": f"/permissions/grant/{service}"
            }
        
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
            user_action=user_action
        )


class TokenError(CipherMateException):
    """Token-related errors (expired, invalid, etc.)"""
    
    def __init__(
        self,
        message: str = "Token error",
        token_type: str = "access_token",
        service: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        user_action = None
        if service:
            user_action = {
                "type": "refresh_token",
                "message": f"Please reconnect your {service} account",
                "service": service,
                "url": f"/permissions/connect/{service}"
            }
        
        super().__init__(
            message=message,
            error_code="TOKEN_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
            user_action=user_action
        )


class ServiceUnavailableError(CipherMateException):
    """External service unavailable errors"""
    
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        service: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        user_action = {
            "type": "retry",
            "message": "Please try again in a few moments",
            "retry_after": retry_after
        }
        
        super().__init__(
            message=message,
            error_code="SERVICE_UNAVAILABLE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
            user_action=user_action
        )


class RateLimitError(CipherMateException):
    """Rate limiting errors"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        limit: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        user_action = {
            "type": "wait",
            "message": f"Please wait {retry_after} seconds before trying again" if retry_after else "Please wait before trying again",
            "retry_after": retry_after
        }
        
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details,
            user_action=user_action
        )


class AIProcessingError(CipherMateException):
    """AI processing related errors"""
    
    def __init__(
        self,
        message: str = "AI processing failed",
        provider: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        user_action = {
            "type": "retry",
            "message": "Please rephrase your request or try again",
            "suggestions": [
                "Try being more specific in your request",
                "Break down complex requests into smaller parts",
                "Check if you have the necessary permissions"
            ]
        }
        
        super().__init__(
            message=message,
            error_code="AI_PROCESSING_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
            user_action=user_action
        )


class DataIntegrityError(CipherMateException):
    """Data integrity and consistency errors"""
    
    def __init__(
        self,
        message: str = "Data integrity error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="DATA_INTEGRITY_ERROR",
            status_code=status.HTTP_409_CONFLICT,
            details=details,
            user_action={
                "type": "refresh",
                "message": "Please refresh and try again"
            }
        )


class ConfigurationError(CipherMateException):
    """Configuration and setup errors"""
    
    def __init__(
        self,
        message: str = "Configuration error",
        component: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
            user_action={
                "type": "contact_support",
                "message": "Please contact support if this issue persists"
            }
        )


# Utility functions for common error scenarios

def create_validation_error(field: str, message: str, value: Any = None) -> ValidationError:
    """Create a validation error for a specific field"""
    error_detail = ErrorDetail(
        code="INVALID_VALUE",
        message=message,
        field=field,
        details={"value": value} if value is not None else None
    )
    return ValidationError(
        message=f"Validation failed for field '{field}': {message}",
        field_errors=[error_detail]
    )


def create_missing_permission_error(service: str, permissions: List[str]) -> AuthorizationError:
    """Create an authorization error for missing permissions"""
    return AuthorizationError(
        message=f"Missing required permissions for {service}",
        required_permissions=permissions,
        service=service,
        details={
            "service": service,
            "missing_permissions": permissions,
            "action_required": "grant_permissions"
        }
    )


def create_token_expired_error(service: str) -> TokenError:
    """Create a token expired error"""
    return TokenError(
        message=f"Token for {service} has expired",
        token_type="access_token",
        service=service,
        details={
            "service": service,
            "reason": "token_expired",
            "action_required": "refresh_token"
        }
    )


def create_service_error(service: str, error_message: str, status_code: int = None) -> ServiceUnavailableError:
    """Create a service unavailable error"""
    return ServiceUnavailableError(
        message=f"{service} service error: {error_message}",
        service=service,
        details={
            "service": service,
            "original_error": error_message,
            "status_code": status_code
        }
    )


def create_ai_error(provider: str, error_message: str) -> AIProcessingError:
    """Create an AI processing error"""
    return AIProcessingError(
        message=f"AI processing failed with {provider}: {error_message}",
        provider=provider,
        details={
            "provider": provider,
            "original_error": error_message
        }
    )