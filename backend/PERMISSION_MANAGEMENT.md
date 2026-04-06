# Permission Management System

This document describes the permission management system implemented for CipherMate, which provides secure OAuth-based access to third-party services using Auth0 Token Vault.

## Overview

The permission management system consists of several key components:

1. **OAuth Handlers** - Handle OAuth flows for Google, GitHub, and Slack
2. **Permission Service** - Manage permission templates and scope validation
3. **Token Vault Integration** - Secure token storage using Auth0 Token Vault
4. **API Endpoints** - RESTful API for permission management

## Supported Services

### Google
- **Calendar**: Read/write access to Google Calendar events
- **Gmail**: Read emails and send messages
- **Drive**: Access to Google Drive files
- **User Info**: Basic profile and email information

### GitHub
- **Repositories**: Access to public and private repositories
- **User Data**: Profile information and email addresses
- **Organizations**: Organization membership and data

### Slack
- **Channels**: Read and write access to channels
- **Messages**: Send messages and read conversations
- **Users**: Access to workspace user information
- **Files**: Upload and manage files

## API Endpoints

### Get Supported Services
```http
GET /api/v1/permissions/services
```
Returns list of supported services and their default scopes.

### Initiate Permission Grant
```http
POST /api/v1/permissions/grant
Content-Type: application/json

{
  "service": "google",
  "scopes": ["https://www.googleapis.com/auth/calendar.readonly"] // optional
}
```
Returns authorization URL for OAuth flow.

### List User Permissions
```http
GET /api/v1/permissions/list
```
Returns all permissions granted by the user.

### Get Permission Status
```http
GET /api/v1/permissions/status/{service}
```
Returns detailed status for a specific service permission.

### Revoke Permission
```http
DELETE /api/v1/permissions/revoke
Content-Type: application/json

{
  "service": "google"
}
```
Revokes permission for a specific service.

### Get Service Scopes
```http
GET /api/v1/permissions/scopes/{service}
```
Returns available scopes for a service with risk levels.

### Validate Scopes
```http
POST /api/v1/permissions/validate-scopes/{service}
Content-Type: application/json

{
  "scopes": ["scope1", "scope2"]
}
```
Validates requested scopes and returns risk analysis.

### Get Permission Summary
```http
GET /api/v1/permissions/summary
```
Returns comprehensive permission summary with risk analysis.

## OAuth Flow

### 1. Initiate Flow
Client calls `/permissions/grant` with service name and optional custom scopes.

### 2. User Authorization
User is redirected to service provider (Google, GitHub, Slack) for authorization.

### 3. Callback Handling
Service provider redirects back to `/permissions/callback/{service}` with authorization code.

### 4. Token Exchange
System exchanges authorization code for access/refresh tokens.

### 5. Token Storage
Tokens are securely stored in Auth0 Token Vault.

### 6. Database Update
Local database is updated with permission metadata.

## Security Features

### State Parameter Validation
- Cryptographically secure state parameters prevent CSRF attacks
- State includes user ID and random component
- Validated on callback to ensure request authenticity

### Scope-Based Permissions
- Granular permissions based on OAuth scopes
- Risk levels assigned to each scope (low, medium, high, critical)
- Step-up authentication required for high-risk scopes

### Token Security
- All tokens stored in Auth0 Token Vault (never in local database)
- Automatic token refresh when possible
- Secure token revocation with cleanup

### Audit Logging
- All permission operations logged for audit trail
- User actions tracked with timestamps and IP addresses
- Security events monitored and alerted

## Risk Levels

### Low Risk
- Basic profile information
- Read-only access to public data
- User email addresses

### Medium Risk
- Read access to private data
- Limited write permissions
- Organization membership

### High Risk
- Full write access to user data
- Send emails or messages on behalf of user
- Repository write access

### Critical Risk
- Administrative permissions
- Full account access
- Workspace administration

## Configuration

### Environment Variables
```bash
# Auth0 Configuration
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_AUDIENCE=https://your-domain.auth0.com/api/v2/

# Service OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
SLACK_CLIENT_ID=your-slack-client-id
SLACK_CLIENT_SECRET=your-slack-client-secret

# Application Configuration
APP_BASE_URL=http://localhost:8000
```

### Database Setup
```bash
# Initialize database tables
python -m app.db.init_db init

# Seed with permission templates
python -m app.db.init_db seed
```

## Testing

### Core Functionality Tests
```bash
python test_permission_core.py
```
Tests OAuth handlers, permission templates, and security features without database dependencies.

### Integration Tests
```bash
python test_permission_management.py
```
Tests full system integration including configuration and service communication.

## Usage Examples

### Frontend Integration
```javascript
// Initiate Google Calendar permission
const response = await fetch('/api/v1/permissions/grant', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${userToken}`
  },
  body: JSON.stringify({
    service: 'google',
    scopes: ['https://www.googleapis.com/auth/calendar.readonly']
  })
});

const { authorization_url } = await response.json();
window.location.href = authorization_url;
```

### Check Permission Status
```javascript
const response = await fetch('/api/v1/permissions/status/google', {
  headers: {
    'Authorization': `Bearer ${userToken}`
  }
});

const status = await response.json();
if (status.has_permission) {
  // User has granted Google permissions
  console.log('Scopes:', status.scopes);
}
```

### List All Permissions
```javascript
const response = await fetch('/api/v1/permissions/list', {
  headers: {
    'Authorization': `Bearer ${userToken}`
  }
});

const permissions = await response.json();
permissions.forEach(perm => {
  console.log(`${perm.service}: ${perm.status} (${perm.scopes.length} scopes)`);
});
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
- Invalid service name
- Invalid scopes
- Malformed request data

#### 401 Unauthorized
- Missing or invalid authentication token
- Expired user session

#### 403 Forbidden
- Attempting to access other user's permissions
- Insufficient privileges

#### 404 Not Found
- Permission not found for service
- Invalid callback parameters

#### 410 Gone
- Token expired and cannot be refreshed
- Permission revoked by user or service

## Best Practices

### Scope Selection
- Request minimal scopes necessary for functionality
- Use read-only scopes when possible
- Implement progressive permission requests

### Error Handling
- Always handle permission errors gracefully
- Provide clear user feedback for permission issues
- Implement retry logic for transient failures

### Security
- Validate all user inputs
- Use HTTPS for all OAuth flows
- Implement proper session management
- Monitor for suspicious activities

### User Experience
- Explain why permissions are needed
- Allow users to review and modify permissions
- Provide easy permission revocation
- Show clear permission status indicators

## Troubleshooting

### Common Issues

#### OAuth Flow Fails
- Check service client credentials
- Verify redirect URI configuration
- Ensure proper CORS settings

#### Token Storage Fails
- Verify Auth0 Token Vault configuration
- Check Auth0 Management API permissions
- Review network connectivity

#### Permission Not Found
- Ensure user has granted permission
- Check for expired or revoked tokens
- Verify service name spelling

#### Database Connection Issues
- Check database credentials
- Verify database server is running
- Review connection pool settings

### Debug Mode
Enable debug logging to troubleshoot issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new services:

1. Create OAuth handler class inheriting from `OAuthHandler`
2. Add service configuration to `permission_service.py`
3. Update permission templates in `seed_data.py`
4. Add comprehensive tests
5. Update documentation

## License

This permission management system is part of the CipherMate project and follows the same licensing terms.