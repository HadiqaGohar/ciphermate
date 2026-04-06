# Third-Party API Integration Service

## Overview

The CipherMate API Integration Service provides secure, authenticated access to third-party APIs using tokens stored in Auth0 Token Vault. It supports Google Calendar, Gmail, GitHub, and Slack APIs with comprehensive error handling, retry logic, and rate limiting.

## Architecture

### Core Components

1. **APIIntegrationService** - Core service for making authenticated API calls
2. **Service Clients** - High-level interfaces for specific services
3. **API Endpoints** - FastAPI routes exposing integration functionality
4. **Error Handling** - Comprehensive error management and retry logic

### Supported Services

- **Google Calendar** - Calendar management and event operations
- **Gmail** - Email operations and mailbox management
- **GitHub** - Repository, issue, and pull request management
- **Slack** - Channel messaging and workspace operations

## Key Features

### 🔐 Secure Token Management
- Automatic token retrieval from Auth0 Token Vault
- Secure token injection into API requests
- Token refresh and expiration handling
- No token exposure in logs or responses

### 🔄 Retry Logic & Rate Limiting
- Exponential backoff with jitter
- Rate limit detection and handling
- Service-specific retry strategies
- Configurable retry parameters

### 📊 Comprehensive Monitoring
- Rate limit tracking and caching
- API call audit logging
- Performance metrics collection
- Health check endpoints

### ⚠️ Error Handling
- Service-specific error mapping
- User-friendly error messages
- Graceful degradation
- Detailed error logging

## Usage Examples

### Basic API Call

```python
from app.core.api_integration import api_integration_service, APIService

# Make a GitHub API call
response = await api_integration_service.make_api_call(
    user_id="user_auth0_id",
    service=APIService.GITHUB,
    method="GET",
    endpoint="/user"
)

if response.success:
    user_data = response.data
    print(f"GitHub user: {user_data['login']}")
else:
    print(f"Error: {response.error}")
```

### Using Service Clients

```python
from app.core.service_clients import service_client_factory

# Google Calendar operations
calendar_client = service_client_factory.get_google_calendar_client()

# List calendars
calendars = await calendar_client.list_calendars("user_auth0_id")

# Create an event
event = await calendar_client.create_event(
    user_id="user_auth0_id",
    summary="Team Meeting",
    start_time=datetime(2024, 1, 15, 10, 0),
    end_time=datetime(2024, 1, 15, 11, 0),
    attendees=["colleague@example.com"]
)
```

### API Endpoints

```bash
# Health check
GET /api/v1/integrations/health

# Rate limit status
GET /api/v1/integrations/rate-limits/github

# Generic API call
POST /api/v1/integrations/call
{
  "service": "github",
  "method": "GET",
  "endpoint": "/user"
}

# Service-specific endpoints
GET /api/v1/integrations/google-calendar/calendars
GET /api/v1/integrations/github/repositories
POST /api/v1/integrations/slack/messages
```

## Service-Specific Operations

### Google Calendar

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| List Calendars | GET | `/google-calendar/calendars` | Get all user calendars |
| List Events | GET | `/google-calendar/events` | Get calendar events |
| Create Event | POST | `/google-calendar/events` | Create new event |

### Gmail

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Get Profile | GET | `/gmail/profile` | Get Gmail profile |
| List Messages | GET | `/gmail/messages` | List mailbox messages |
| Send Email | POST | `/gmail/send` | Send email message |

### GitHub

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Get User | GET | `/github/user` | Get user information |
| List Repos | GET | `/github/repositories` | List user repositories |
| Create Issue | POST | `/github/issues` | Create repository issue |

### Slack

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Get User Info | GET | `/slack/user` | Get user information |
| List Channels | GET | `/slack/channels` | List workspace channels |
| Send Message | POST | `/slack/messages` | Send channel message |

## Configuration

### Environment Variables

```bash
# Third-party service credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret

# Auth0 Token Vault
AUTH0_DOMAIN=your_domain.auth0.com
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
```

### Retry Configuration

```python
from app.core.api_integration import RetryConfig

# Custom retry configuration
retry_config = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True
)
```

## Error Handling

### Error Types

- **AuthorizationError** - Missing or invalid tokens
- **RateLimitError** - API rate limits exceeded
- **ServiceUnavailableError** - External service unavailable
- **APIServiceError** - General API integration errors

### Error Response Format

```json
{
  "success": false,
  "error": "Rate limit exceeded for github. Reset in 3600 seconds",
  "status_code": 429,
  "service": "github",
  "rate_limit_remaining": 0,
  "rate_limit_reset": "2024-01-15T10:00:00Z"
}
```

## Security Considerations

### Token Security
- Tokens never exposed in logs or responses
- Secure retrieval from Auth0 Token Vault
- Automatic token refresh when possible
- Immediate cleanup on permission revocation

### Request Security
- HTTPS enforcement for all external calls
- Input validation and sanitization
- Rate limiting to prevent abuse
- Comprehensive audit logging

### Data Protection
- Minimal data retention
- Secure error handling
- PII protection in logs
- GDPR compliance ready

## Performance Optimization

### Caching Strategy
- Rate limit information caching
- Token caching with expiration
- Service configuration caching
- Response caching where appropriate

### Connection Management
- HTTP connection pooling
- Async/await for non-blocking I/O
- Timeout configuration
- Resource cleanup

## Monitoring & Observability

### Metrics Collected
- API call success/failure rates
- Response times per service
- Rate limit utilization
- Error frequency and types

### Audit Logging
- All API calls logged with metadata
- User context and IP tracking
- Service-specific operation details
- Performance metrics

### Health Checks
- Service availability monitoring
- Token vault connectivity
- Rate limit status
- Configuration validation

## Testing

### Unit Tests
```bash
# Run API integration tests
python -m pytest test_api_integration.py -v

# Run endpoint tests
python -m pytest test_integration_endpoints.py -v
```

### Demo Script
```bash
# Run comprehensive demo
python demo_api_integration.py
```

## Deployment

### Dependencies
- httpx for HTTP requests
- Auth0 Python SDK for token management
- FastAPI for API endpoints
- SQLAlchemy for audit logging

### Docker Configuration
```dockerfile
# Install dependencies
RUN pip install httpx auth0-python fastapi sqlalchemy

# Copy integration service files
COPY app/core/api_integration.py /app/core/
COPY app/core/service_clients.py /app/core/
COPY app/api/v1/integrations.py /app/api/v1/
```

## Troubleshooting

### Common Issues

1. **Token Not Found**
   - Verify user has granted permissions
   - Check Token Vault configuration
   - Ensure service connection is active

2. **Rate Limit Exceeded**
   - Check rate limit status endpoint
   - Implement request queuing
   - Consider service-specific limits

3. **Service Unavailable**
   - Check external service status
   - Verify network connectivity
   - Review retry configuration

### Debug Mode
```python
import logging
logging.getLogger('app.core.api_integration').setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
- Additional service integrations (Microsoft, Dropbox)
- Webhook support for real-time updates
- Batch operation support
- Advanced caching strategies
- GraphQL API support

### Performance Improvements
- Connection pooling optimization
- Response streaming for large datasets
- Intelligent retry strategies
- Predictive rate limiting

## Contributing

### Adding New Services

1. Add service configuration to `APIIntegrationService`
2. Create service-specific client class
3. Add API endpoints in `integrations.py`
4. Write comprehensive tests
5. Update documentation

### Code Standards
- Follow existing patterns and conventions
- Include comprehensive error handling
- Add audit logging for all operations
- Write tests for all new functionality
- Update documentation and examples

## Support

For issues, questions, or contributions:
- Check existing tests and documentation
- Review error logs and audit trails
- Verify service configurations
- Test with demo script first

---

*This integration service is part of the CipherMate platform, demonstrating secure AI agent interactions with third-party services using Auth0 Token Vault.*