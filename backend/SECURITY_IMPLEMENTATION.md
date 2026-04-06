# CipherMate Security Implementation

This document describes the comprehensive security measures implemented in the CipherMate backend to protect against various threats and attacks.

## Overview

The security implementation includes multiple layers of protection:

1. **Rate Limiting** - Prevents abuse and DoS attacks
2. **Input Validation & Sanitization** - Prevents injection attacks
3. **Security Headers** - Protects against common web vulnerabilities
4. **Real-time Threat Detection** - Monitors and blocks suspicious activities
5. **Comprehensive Audit Logging** - Tracks all security events

## Security Features

### 1. Rate Limiting

**Implementation**: `RateLimitMiddleware` in `app/core/middleware.py`

- **Per-minute limits**: Configurable requests per minute (default: 60)
- **Burst protection**: Prevents rapid-fire requests (default: 10 requests per 10 seconds)
- **IP-based tracking**: Tracks both authenticated users and anonymous IPs
- **Adaptive limits**: Reduces limits for suspicious IPs
- **Automatic blocking**: Temporarily blocks IPs that exceed limits

**Configuration**:
```python
RATE_LIMIT_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_BURST_SIZE = 10
```

### 2. Input Validation & Sanitization

**Implementation**: Multiple validation layers

#### SQL Injection Prevention
- **Pattern detection**: Detects common SQL injection patterns
- **Keyword analysis**: Identifies suspicious SQL keywords with operators
- **Real-time blocking**: Rejects requests with malicious SQL patterns

**Detected patterns**:
- SQL keywords: SELECT, INSERT, UPDATE, DELETE, DROP, etc.
- SQL operators: --, #, /*, */, UNION
- Conditional injections: OR 1=1, AND 1=1

#### XSS Attack Prevention
- **Script tag detection**: Blocks `<script>` tags and variants
- **Event handler detection**: Blocks `onclick`, `onload`, etc.
- **URL scheme filtering**: Blocks `javascript:`, `data:text/html`, `vbscript:`
- **HTML sanitization**: Uses bleach library for safe HTML cleaning

#### Input Sanitization
- **HTML escaping**: Escapes dangerous HTML entities
- **Control character removal**: Removes null bytes and control characters
- **Length limits**: Enforces maximum input lengths
- **Whitespace normalization**: Normalizes whitespace patterns

### 3. Security Headers

**Implementation**: `SecurityHeadersMiddleware` in `app/core/middleware.py`

Applied headers:
- **X-Content-Type-Options**: `nosniff` - Prevents MIME type sniffing
- **X-Frame-Options**: `DENY` - Prevents clickjacking
- **X-XSS-Protection**: `1; mode=block` - Enables XSS filtering
- **Referrer-Policy**: `strict-origin-when-cross-origin` - Controls referrer information
- **Content-Security-Policy**: Comprehensive CSP with strict directives
- **Strict-Transport-Security**: HSTS for HTTPS connections
- **Cross-Origin-***: CORP, COEP, COOP headers for isolation

**Environment-specific CSP**:
- **Development**: Relaxed CSP for easier development
- **Production**: Strict CSP with minimal unsafe directives

### 4. Real-time Threat Detection

**Implementation**: `SecurityMonitor` in `app/core/security_monitor.py`

#### Threat Detection Capabilities
- **Failed login tracking**: Monitors authentication failures
- **Request rate analysis**: Detects rapid request patterns
- **Error rate monitoring**: Identifies scanning/probing attempts
- **IP reputation tracking**: Maintains lists of suspicious/blocked IPs

#### Automatic Response
- **Progressive blocking**: Suspicious → Blocked IP progression
- **Temporary blocks**: Automatic unblocking after cooldown period
- **Adaptive thresholds**: Adjusts limits based on threat level
- **Real-time alerts**: Logs security events for monitoring

#### Monitoring Thresholds
```python
failed_login_threshold = 5      # Failed logins in 5 minutes
rapid_request_threshold = 20    # Requests per minute
error_rate_threshold = 0.5      # 50% error rate
```

### 5. CORS Security

**Implementation**: Enhanced CORS configuration in `app/main.py`

- **Environment-aware origins**: Different origins for dev/prod
- **Restricted headers**: Only allows necessary headers
- **Credential support**: Secure credential handling
- **Method restrictions**: Limited to necessary HTTP methods
- **Cache control**: Optimized preflight caching

### 6. Request Validation

**Implementation**: `RequestValidationMiddleware` in `app/core/middleware.py`

#### Validation Checks
- **Request size limits**: Prevents oversized requests (10MB default)
- **Header size limits**: Prevents header-based attacks (8KB default)
- **URL length limits**: Prevents long URL attacks (2048 chars)
- **Suspicious pattern detection**: Blocks known attack patterns
- **Content type validation**: Ensures proper content types

#### Blocked Patterns
- Path traversal: `../`, `..\\`
- Script injection: `<script`, `javascript:`
- Data URLs: `data:text/html`
- Script languages: `vbscript:`
- DOM manipulation: `document.cookie`, `window.location`

### 7. Security Event Logging

**Implementation**: `AuditService` in `app/core/audit_service.py`

#### Logged Events
- Authentication events (login, logout, failures)
- Permission changes (grant, revoke, request)
- API access patterns
- Security violations
- Rate limit violations
- IP blocking events

#### Event Categories
- **INFO**: Normal operations
- **WARNING**: Suspicious activities
- **HIGH**: Security violations
- **CRITICAL**: Severe security events

### 8. Security Monitoring API

**Implementation**: `SecurityRouter` in `app/api/v1/security.py`

#### Admin Endpoints
- `GET /security/status` - Current security status
- `POST /security/configure` - Update security settings
- `POST /security/unblock-ip` - Manually unblock IPs
- `GET /security/blocked-ips` - List blocked IPs
- `POST /security/reset-metrics` - Reset security metrics

#### Access Control
- Admin-only access to security endpoints
- Role-based authorization
- Comprehensive audit logging

## Configuration

### Environment Variables

```bash
# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10

# Request Limits
MAX_REQUEST_SIZE_MB=10
MAX_HEADER_SIZE_KB=8

# Security Features
ENABLE_SECURITY_HEADERS=true
ENABLE_RATE_LIMITING=true
ENABLE_SQL_INJECTION_DETECTION=true
ENABLE_XSS_DETECTION=true

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Security Settings

```python
# SQL Injection Patterns
SQL_INJECTION_PATTERNS = [
    r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
    r"(--|#|/\*|\*/)",
    r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
    # ... more patterns
]

# XSS Patterns
XSS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"javascript:",
    r"data:text/html",
    # ... more patterns
]
```

## Security Best Practices

### 1. Input Handling
- Always validate and sanitize user input
- Use parameterized queries for database operations
- Implement proper error handling without information disclosure
- Apply principle of least privilege

### 2. Authentication & Authorization
- Use strong authentication mechanisms (Auth0)
- Implement proper session management
- Apply role-based access control
- Regular token rotation and validation

### 3. Monitoring & Logging
- Log all security-relevant events
- Monitor for suspicious patterns
- Implement real-time alerting
- Regular security audit reviews

### 4. Network Security
- Use HTTPS for all communications
- Implement proper CORS policies
- Apply security headers consistently
- Regular security header audits

## Testing

Run the security test suite:

```bash
cd backend
python test_security_implementation.py
```

The test suite validates:
- SQL injection detection
- XSS pattern recognition
- Message content validation
- Security monitor functionality
- Metrics collection
- Comprehensive injection validation

## Monitoring

### Security Metrics
- Blocked requests count
- Threats detected count
- IPs blocked count
- Security events by type
- Attack types distribution

### Real-time Monitoring
- Failed login attempts
- Request rate patterns
- Error rate analysis
- IP reputation tracking
- Automatic threat response

## Incident Response

### Automatic Response
1. **Detection**: Real-time pattern analysis
2. **Classification**: Threat severity assessment
3. **Response**: Automatic blocking/limiting
4. **Logging**: Comprehensive event recording
5. **Recovery**: Automatic unblocking after cooldown

### Manual Response
1. **Investigation**: Review security logs and events
2. **Analysis**: Determine threat scope and impact
3. **Mitigation**: Manual IP blocking/unblocking
4. **Configuration**: Adjust security thresholds
5. **Documentation**: Update security procedures

## Future Enhancements

1. **Machine Learning**: AI-based threat detection
2. **Geolocation**: Location-based access control
3. **Device Fingerprinting**: Enhanced user tracking
4. **Behavioral Analysis**: User behavior anomaly detection
5. **Integration**: SIEM system integration
6. **Compliance**: Additional compliance frameworks

## Compliance

The security implementation supports:
- **OWASP Top 10**: Protection against common vulnerabilities
- **GDPR**: Data protection and privacy requirements
- **SOC 2**: Security and availability controls
- **ISO 27001**: Information security management

## Support

For security-related questions or incident reporting:
- Review security logs in the audit dashboard
- Use the security monitoring API for real-time status
- Check the security configuration for current settings
- Consult this documentation for implementation details