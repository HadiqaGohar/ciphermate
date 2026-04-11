"""
Input validation and sanitization utilities
"""
    # // done hadiqa


import re
import html
import bleach
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse
import logging

from .exceptions import ValidationError, ErrorDetail
from .config import settings

logger = logging.getLogger(__name__)

# Allowed HTML tags and attributes for sanitization
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

# Common regex patterns
PATTERNS = {
    'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'phone': re.compile(r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'),
    'url': re.compile(r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'),
    'slug': re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    'username': re.compile(r'^[a-zA-Z0-9_-]{3,30}$'),
    'safe_string': re.compile(r'^[a-zA-Z0-9\s\-_.,!?()]+$'),
    'service_name': re.compile(r'^[a-z][a-z0-9_]*$'),
    'permission_scope': re.compile(r'^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*$'),
}

# Compiled SQL injection patterns for better performance
SQL_INJECTION_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in settings.SQL_INJECTION_PATTERNS]

# Compiled XSS patterns for better performance  
XSS_PATTERNS = [re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in settings.XSS_PATTERNS]

# Input length limits
LIMITS = {
    'short_text': 100,
    'medium_text': 500,
    'long_text': 2000,
    'message': 5000,
    'email': 254,
    'url': 2048,
    'username': 30,
    'service_name': 50,
    'permission_scope': 100,
}


class ValidationResult(BaseModel):
    """Result of validation operation"""
    is_valid: bool
    errors: List[ErrorDetail] = []
    sanitized_value: Optional[Any] = None
    warnings: List[str] = []


def sanitize_html(text: str) -> str:
    """Sanitize HTML content to prevent XSS"""
    if not text:
        return ""
    
    # First escape HTML entities
    escaped = html.escape(text)
    
    # Then allow only safe tags
    cleaned = bleach.clean(
        escaped,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    return cleaned.strip()


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize general string input"""
    if not text:
        return ""
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Normalize whitespace
    sanitized = ' '.join(sanitized.split())
    
    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip()
    
    return sanitized


def detect_sql_injection(text: str) -> List[str]:
    """Detect potential SQL injection patterns in text"""
    if not settings.ENABLE_SQL_INJECTION_DETECTION or not text:
        return []
    
    detected_patterns = []
    text_lower = text.lower()
    
    for pattern in SQL_INJECTION_PATTERNS:
        if pattern.search(text):
            detected_patterns.append(f"SQL injection pattern detected: {pattern.pattern}")
    
    # Additional heuristic checks
    suspicious_keywords = ['union', 'select', 'insert', 'update', 'delete', 'drop', 'exec', 'script']
    sql_operators = ['--', '#', '/*', '*/', ';']
    
    for keyword in suspicious_keywords:
        if keyword in text_lower and any(op in text for op in sql_operators):
            detected_patterns.append(f"Suspicious SQL keyword with operator: {keyword}")
    
    return detected_patterns


def detect_xss_patterns(text: str) -> List[str]:
    """Detect potential XSS patterns in text"""
    if not settings.ENABLE_XSS_DETECTION or not text:
        return []
    
    detected_patterns = []
    
    for pattern in XSS_PATTERNS:
        if pattern.search(text):
            detected_patterns.append(f"XSS pattern detected: {pattern.pattern}")
    
    # Additional checks for encoded attacks
    decoded_text = html.unescape(text)
    if decoded_text != text:
        # Check decoded content for XSS patterns
        for pattern in XSS_PATTERNS:
            if pattern.search(decoded_text):
                detected_patterns.append(f"Encoded XSS pattern detected: {pattern.pattern}")
    
    return detected_patterns


def validate_against_injection_attacks(text: str) -> ValidationResult:
    """Validate text against SQL injection and XSS attacks - with chat-friendly exceptions"""
    errors = []
    warnings = []
    
    if not text:
        return ValidationResult(is_valid=True, sanitized_value="")
    
    # For chat messages, be more lenient with common words
    text_lower = text.lower()
    
    # Skip validation for common chat patterns that might trigger false positives
    chat_safe_patterns = [
        r'\b(schedule|create|meeting|event|birthday|party|tomorrow|today)\b',
        r'\d{1,2}:\d{2}\s*(am|pm)',  # Time patterns
        r'\d{1,2}-\d{1,2}-\d{4}',   # Date patterns
        r'(calendar|email|github|slack)',  # Service names
    ]
    
    is_likely_chat = any(re.search(pattern, text_lower) for pattern in chat_safe_patterns)
    
    if is_likely_chat:
        # For chat messages, only check for obvious attacks
        obvious_sql_attacks = [
            r";\s*(drop|delete|truncate)\s+table",
            r"union\s+select.*from",
            r"'\s*or\s*'1'\s*=\s*'1",
            r"--\s*$",  # SQL comment at end
        ]
        
        for pattern in obvious_sql_attacks:
            if re.search(pattern, text_lower):
                errors.append(ErrorDetail(
                    code="SQL_INJECTION_DETECTED",
                    message="Potential SQL injection attack detected",
                    field="input",
                    details={"pattern": pattern}
                ))
                break
    else:
        # For non-chat content, use full validation
        # Check for SQL injection
        sql_patterns = detect_sql_injection(text)
        if sql_patterns:
            errors.append(ErrorDetail(
                code="SQL_INJECTION_DETECTED",
                message="Potential SQL injection attack detected",
                field="input",
                details={"patterns": sql_patterns}
            ))
    
    # Always check for XSS but be lenient with false positives
    xss_patterns = detect_xss_patterns(text)
    if xss_patterns:
        # Filter out false positives for chat
        real_xss = [p for p in xss_patterns if not any(safe in p.lower() for safe in ['calendar', 'schedule', 'event'])]
        if real_xss:
            errors.append(ErrorDetail(
                code="XSS_ATTACK_DETECTED", 
                message="Potential XSS attack detected",
                field="input",
                details={"patterns": real_xss}
            ))
    
    # Sanitize the input (but preserve chat content)
    if is_likely_chat:
        # For chat, just remove obvious HTML tags but preserve content
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    else:
        sanitized = sanitize_html(text)
    
    if sanitized != text:
        warnings.append("Input was sanitized to remove potentially harmful content")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=sanitized,
        warnings=warnings
    )


def validate_email_address(email: str) -> ValidationResult:
    """Validate email address"""
    errors = []
    
    if not email:
        errors.append(ErrorDetail(
            code="REQUIRED",
            message="Email address is required",
            field="email"
        ))
        return ValidationResult(is_valid=False, errors=errors)
    
    # Length check
    if len(email) > LIMITS['email']:
        errors.append(ErrorDetail(
            code="TOO_LONG",
            message=f"Email address must be less than {LIMITS['email']} characters",
            field="email"
        ))
    
    # Format validation
    sanitized = email  # Default to original email
    try:
        validated_email = validate_email(email)
        sanitized = validated_email.email
    except EmailNotValidError as e:
        errors.append(ErrorDetail(
            code="INVALID_FORMAT",
            message=f"Invalid email format: {str(e)}",
            field="email"
        ))
        sanitized = sanitize_string(email, LIMITS['email'])
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=sanitized if len(errors) == 0 else None
    )


def validate_url(url: str, require_https: bool = True) -> ValidationResult:
    """Validate URL"""
    errors = []
    
    if not url:
        errors.append(ErrorDetail(
            code="REQUIRED",
            message="URL is required",
            field="url"
        ))
        return ValidationResult(is_valid=False, errors=errors)
    
    # Length check
    if len(url) > LIMITS['url']:
        errors.append(ErrorDetail(
            code="TOO_LONG",
            message=f"URL must be less than {LIMITS['url']} characters",
            field="url"
        ))
    
    # Parse URL
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme:
            errors.append(ErrorDetail(
                code="MISSING_SCHEME",
                message="URL must include protocol (http:// or https://)",
                field="url"
            ))
        elif require_https and parsed.scheme != 'https':
            errors.append(ErrorDetail(
                code="INSECURE_PROTOCOL",
                message="URL must use HTTPS protocol",
                field="url"
            ))
        elif parsed.scheme not in ['http', 'https']:
            errors.append(ErrorDetail(
                code="INVALID_PROTOCOL",
                message="URL must use HTTP or HTTPS protocol",
                field="url"
            ))
        
        if not parsed.netloc:
            errors.append(ErrorDetail(
                code="MISSING_DOMAIN",
                message="URL must include a valid domain",
                field="url"
            ))
    
    except Exception as e:
        errors.append(ErrorDetail(
            code="INVALID_FORMAT",
            message=f"Invalid URL format: {str(e)}",
            field="url"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=url if len(errors) == 0 else None
    )


def validate_service_name(service_name: str) -> ValidationResult:
    """Validate service name"""
    errors = []
    
    if not service_name:
        errors.append(ErrorDetail(
            code="REQUIRED",
            message="Service name is required",
            field="service_name"
        ))
        return ValidationResult(is_valid=False, errors=errors)
    
    # Length check
    if len(service_name) > LIMITS['service_name']:
        errors.append(ErrorDetail(
            code="TOO_LONG",
            message=f"Service name must be less than {LIMITS['service_name']} characters",
            field="service_name"
        ))
    
    # Format check
    if not PATTERNS['service_name'].match(service_name):
        errors.append(ErrorDetail(
            code="INVALID_FORMAT",
            message="Service name must contain only lowercase letters, numbers, and underscores, starting with a letter",
            field="service_name"
        ))
    
    # Reserved names
    reserved_names = ['admin', 'api', 'www', 'mail', 'ftp', 'localhost', 'system', 'root']
    if service_name.lower() in reserved_names:
        errors.append(ErrorDetail(
            code="RESERVED_NAME",
            message=f"'{service_name}' is a reserved service name",
            field="service_name"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=service_name.lower() if len(errors) == 0 else None
    )


def validate_permission_scope(scope: str) -> ValidationResult:
    """Validate permission scope"""
    errors = []
    
    if not scope:
        errors.append(ErrorDetail(
            code="REQUIRED",
            message="Permission scope is required",
            field="scope"
        ))
        return ValidationResult(is_valid=False, errors=errors)
    
    # Length check
    if len(scope) > LIMITS['permission_scope']:
        errors.append(ErrorDetail(
            code="TOO_LONG",
            message=f"Permission scope must be less than {LIMITS['permission_scope']} characters",
            field="scope"
        ))
    
    # Format check
    if not PATTERNS['permission_scope'].match(scope):
        errors.append(ErrorDetail(
            code="INVALID_FORMAT",
            message="Permission scope must contain only lowercase letters, numbers, underscores, and dots",
            field="scope"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=scope.lower() if len(errors) == 0 else None
    )


def validate_message_content(content: str, max_length: int = LIMITS['message']) -> ValidationResult:
    """Validate message content with security checks"""
    errors = []
    warnings = []
    
    if not content:
        errors.append(ErrorDetail(
            code="REQUIRED",
            message="Message content is required",
            field="content"
        ))
        return ValidationResult(is_valid=False, errors=errors)
    
    # First check for injection attacks
    security_result = validate_against_injection_attacks(content)
    errors.extend(security_result.errors)
    warnings.extend(security_result.warnings)
    
    # Use sanitized content for further processing
    sanitized = security_result.sanitized_value or content
    
    # Length check after sanitization
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip()
        warnings.append(f"Message was truncated to {max_length} characters")
    
    # Additional content validation
    if len(sanitized.strip()) == 0:
        errors.append(ErrorDetail(
            code="EMPTY_CONTENT",
            message="Message content cannot be empty after sanitization",
            field="content"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=sanitized,
        warnings=warnings
    )


def validate_json_data(data: Dict[str, Any], max_depth: int = 5, max_keys: int = 100) -> ValidationResult:
    """Validate JSON data structure"""
    errors = []
    warnings = []
    
    def check_depth(obj, current_depth=0):
        if current_depth > max_depth:
            errors.append(ErrorDetail(
                code="TOO_DEEP",
                message=f"JSON structure exceeds maximum depth of {max_depth}",
                field="data"
            ))
            return
        
        if isinstance(obj, dict):
            if len(obj) > max_keys:
                warnings.append(f"JSON object has {len(obj)} keys, which may impact performance")
            
            for key, value in obj.items():
                # Validate key
                if not isinstance(key, str):
                    errors.append(ErrorDetail(
                        code="INVALID_KEY_TYPE",
                        message="JSON keys must be strings",
                        field="data"
                    ))
                elif len(key) > 100:
                    errors.append(ErrorDetail(
                        code="KEY_TOO_LONG",
                        message="JSON keys must be less than 100 characters",
                        field="data"
                    ))
                
                # Recursively check value
                check_depth(value, current_depth + 1)
        
        elif isinstance(obj, list):
            if len(obj) > 1000:
                warnings.append(f"JSON array has {len(obj)} items, which may impact performance")
            
            for item in obj:
                check_depth(item, current_depth + 1)
    
    try:
        check_depth(data)
    except Exception as e:
        errors.append(ErrorDetail(
            code="VALIDATION_ERROR",
            message=f"Error validating JSON structure: {str(e)}",
            field="data"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value=data if len(errors) == 0 else None,
        warnings=warnings
    )


def validate_pagination_params(page: int = 1, limit: int = 20, max_limit: int = 100) -> ValidationResult:
    """Validate pagination parameters"""
    errors = []
    
    if page < 1:
        errors.append(ErrorDetail(
            code="INVALID_VALUE",
            message="Page number must be greater than 0",
            field="page"
        ))
    
    if limit < 1:
        errors.append(ErrorDetail(
            code="INVALID_VALUE",
            message="Limit must be greater than 0",
            field="limit"
        ))
    elif limit > max_limit:
        errors.append(ErrorDetail(
            code="LIMIT_EXCEEDED",
            message=f"Limit cannot exceed {max_limit}",
            field="limit"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        sanitized_value={"page": max(1, page), "limit": min(max_limit, max(1, limit))}
    )


class RequestValidator:
    """Request validation utility class"""
    
    @staticmethod
    def validate_chat_request(message: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate chat request"""
        errors = []
        
        # Validate message
        message_result = validate_message_content(message)
        errors.extend(message_result.errors)
        
        # Validate context if provided
        if context:
            context_result = validate_json_data(context)
            errors.extend(context_result.errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_value={
                "message": message_result.sanitized_value,
                "context": context
            }
        )
    
    @staticmethod
    def validate_permission_request(service_name: str, scopes: List[str]) -> ValidationResult:
        """Validate permission request"""
        errors = []
        
        # Validate service name
        service_result = validate_service_name(service_name)
        errors.extend(service_result.errors)
        
        # Validate scopes
        sanitized_scopes = []
        for scope in scopes:
            scope_result = validate_permission_scope(scope)
            errors.extend(scope_result.errors)
            if scope_result.sanitized_value:
                sanitized_scopes.append(scope_result.sanitized_value)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_value={
                "service_name": service_result.sanitized_value,
                "scopes": sanitized_scopes
            }
        )
    
    @staticmethod
    def validate_audit_query(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        service_name: Optional[str] = None,
        action_type: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> ValidationResult:
        """Validate audit query parameters"""
        errors = []
        
        # Validate pagination
        pagination_result = validate_pagination_params(page, limit)
        errors.extend(pagination_result.errors)
        
        # Validate service name if provided
        if service_name:
            service_result = validate_service_name(service_name)
            errors.extend(service_result.errors)
        
        # Validate action type if provided
        if action_type:
            action_sanitized = sanitize_string(action_type, LIMITS['short_text'])
            if not action_sanitized:
                errors.append(ErrorDetail(
                    code="INVALID_VALUE",
                    message="Action type cannot be empty",
                    field="action_type"
                ))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_value={
                "start_date": start_date,
                "end_date": end_date,
                "service_name": service_name,
                "action_type": action_type,
                "page": pagination_result.sanitized_value["page"] if pagination_result.sanitized_value else page,
                "limit": pagination_result.sanitized_value["limit"] if pagination_result.sanitized_value else limit
            }
        )


def create_validation_exception(validation_result: ValidationResult) -> ValidationError:
    """Create a ValidationError from validation result"""
    return ValidationError(
        message="Validation failed",
        field_errors=validation_result.errors,
        details={"warnings": validation_result.warnings} if validation_result.warnings else None
    )