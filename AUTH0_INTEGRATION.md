# Auth0 Integration Documentation

## Overview

This document describes the complete Auth0 integration implemented for CipherMate, including Token Vault functionality for secure AI agent operations.

## Features Implemented

### 1. Auth0 Authentication Setup ✅

- **Frontend Integration**: Next.js with `@auth0/nextjs-auth0`
- **Backend JWT Validation**: FastAPI with Auth0 JWT verification
- **Session Management**: Redis-based session storage
- **Token Refresh**: Automatic token refresh handling

### 2. Token Vault Integration ✅

- **Secure Token Storage**: Auth0 Token Vault for third-party API tokens
- **Token Management**: Store, retrieve, and revoke tokens securely
- **Service Connections**: Track user permissions per service
- **Audit Logging**: Complete audit trail for all token operations

### 3. Session Management ✅

- **Redis Sessions**: Scalable session storage with Redis
- **Session Lifecycle**: Create, update, refresh, and delete sessions
- **User Context**: Maintain user state across requests
- **Cleanup Tasks**: Automatic cleanup of expired sessions

## File Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── api/
│   │       ├── auth/
│   │       │   └── [...auth0]/
│   │       │       └── route.ts          # Auth0 route handler
│   │       └── token-vault/
│   │           ├── store/route.ts         # Store tokens
│   │           ├── retrieve/[service]/route.ts  # Retrieve tokens
│   │           ├── revoke/[service]/route.ts    # Revoke tokens
│   │           └── list/route.ts          # List tokens
│   ├── components/
│   │   └── auth/
│   │       ├── LoginButton.tsx           # Login/logout component
│   │       └── ProtectedRoute.tsx        # Route protection
│   └── lib/
│       ├── auth0.ts                      # Auth0 configuration
│       └── token-vault.ts                # Token Vault client

backend/
├── app/
│   ├── core/
│   │   ├── auth.py                       # JWT validation & session mgmt
│   │   ├── token_vault.py                # Token Vault service
│   │   ├── session.py                    # Redis session manager
│   │   └── config.py                     # Configuration
│   ├── api/v1/
│   │   ├── auth.py                       # Auth endpoints
│   │   └── token_vault.py                # Token Vault endpoints
│   └── models/
│       ├── user.py                       # User model
│       └── service_connection.py         # Service connection model
```

## Configuration

### Environment Variables

#### Frontend (.env.local)
```bash
AUTH0_SECRET='use [openssl rand -hex 32] to generate a 32 bytes value'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://your-domain.auth0.com'
AUTH0_CLIENT_ID='your-client-id'
AUTH0_CLIENT_SECRET='your-client-secret'
AUTH0_AUDIENCE='https://your-domain.auth0.com/api/v2/'
NEXT_PUBLIC_API_URL='http://localhost:8000'
```

#### Backend (.env)
```bash
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_AUDIENCE=https://your-domain.auth0.com/api/v2/
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ciphermate
REDIS_URL=redis://localhost:6379
```

## API Endpoints

### Authentication Endpoints

#### `GET /api/v1/auth/profile`
Get current user profile information.

**Response:**
```json
{
  "sub": "auth0|user_id",
  "email": "user@example.com",
  "name": "User Name",
  "permissions": ["read:profile"],
  "scope": ["openid", "profile", "email"]
}
```

#### `GET /api/v1/auth/session`
Get current session information.

#### `POST /api/v1/auth/session/refresh`
Refresh current session.

#### `DELETE /api/v1/auth/session`
Logout and delete session.

### Token Vault Endpoints

#### `POST /api/v1/token-vault/store`
Store a token in Auth0 Token Vault.

**Request:**
```json
{
  "service": "google_calendar",
  "token": {
    "access_token": "token_value",
    "refresh_token": "refresh_value",
    "expires_in": 3600
  },
  "scopes": ["https://www.googleapis.com/auth/calendar"],
  "user_id": "auth0|user_id"
}
```

#### `GET /api/v1/token-vault/retrieve/{service}?user_id={user_id}`
Retrieve a token from Token Vault.

#### `DELETE /api/v1/token-vault/revoke/{service}`
Revoke a token from Token Vault.

#### `GET /api/v1/token-vault/list?user_id={user_id}`
List all tokens for a user.

## Security Features

### JWT Validation
- **JWKS Integration**: Automatic key rotation support
- **Token Verification**: Full JWT signature validation
- **Scope Checking**: Granular permission validation
- **Expiration Handling**: Automatic token refresh

### Token Vault Security
- **Encrypted Storage**: All tokens encrypted in Auth0 Token Vault
- **Access Control**: Users can only access their own tokens
- **Audit Logging**: Complete audit trail for all operations
- **Automatic Cleanup**: Expired tokens automatically removed

### Session Security
- **Redis Storage**: Secure, scalable session storage
- **Session Rotation**: Regular session refresh
- **IP Tracking**: Session tied to IP address
- **Automatic Expiry**: Sessions expire after inactivity

## Usage Examples

### Frontend Authentication

```typescript
// Login button component
import { useUser } from '@auth0/nextjs-auth0/client';

export default function LoginButton() {
  const { user, error, isLoading } = useUser();
  
  if (user) {
    return <a href="/api/auth/logout">Logout</a>;
  }
  
  return <a href="/api/auth/login">Login</a>;
}
```

### Protected Routes

```typescript
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function Dashboard() {
  return (
    <ProtectedRoute>
      <div>Protected content here</div>
    </ProtectedRoute>
  );
}
```

### Token Vault Operations

```typescript
import { tokenVaultService } from '@/lib/token-vault';

// Store a token
await tokenVaultService.storeToken(
  'google_calendar',
  tokenData,
  ['https://www.googleapis.com/auth/calendar']
);

// Retrieve a token
const token = await tokenVaultService.retrieveToken('google_calendar');

// Revoke a token
await tokenVaultService.revokeToken('google_calendar');
```

### Backend Authentication

```python
from app.core.auth import get_current_user
from fastapi import Depends

@router.get("/protected")
async def protected_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    return {"user_id": current_user["sub"]}
```

## Testing

### Basic Setup Test
```bash
python backend/test_basic_setup.py
```

### Integration Test
```bash
python backend/test_auth0_integration.py
```

## Deployment Considerations

### Auth0 Configuration
1. **Create Auth0 Application**: Set up SPA + API application
2. **Configure Token Vault**: Enable Token Vault feature
3. **Set Callback URLs**: Add production URLs
4. **Configure CORS**: Allow frontend domain

### Environment Setup
1. **Database**: PostgreSQL with proper indexes
2. **Redis**: For session storage and caching
3. **SSL/TLS**: HTTPS required for production
4. **Environment Variables**: Secure secret management

### Monitoring
1. **Auth0 Logs**: Monitor authentication events
2. **Application Logs**: Track token operations
3. **Session Metrics**: Monitor session lifecycle
4. **Error Tracking**: Comprehensive error logging

## Troubleshooting

### Common Issues

#### "Token missing kid in header"
- **Cause**: Invalid JWT token format
- **Solution**: Check Auth0 configuration and token format

#### "Unable to find appropriate key"
- **Cause**: JWKS key rotation or configuration issue
- **Solution**: Clear JWKS cache, check Auth0 domain

#### "Session not found"
- **Cause**: Redis connection or session expiry
- **Solution**: Check Redis connectivity and session TTL

#### "Token Vault operation failed"
- **Cause**: Auth0 Management API permissions
- **Solution**: Verify client credentials and scopes

### Debug Mode
Enable debug logging by setting `DEBUG=true` in environment variables.

## Next Steps

1. **OAuth Flows**: Implement OAuth flows for third-party services
2. **Permission Management**: Build permission management UI
3. **Audit Dashboard**: Create comprehensive audit logging interface
4. **Rate Limiting**: Add rate limiting for API endpoints
5. **Monitoring**: Set up comprehensive monitoring and alerting

## Security Checklist

- [x] JWT signature validation
- [x] Token encryption in vault
- [x] Session security with Redis
- [x] User isolation (users can only access own data)
- [x] Audit logging for all operations
- [x] Automatic token refresh
- [x] Secure error handling (no token leakage)
- [x] CORS configuration
- [x] Input validation and sanitization
- [x] Rate limiting preparation

## Compliance

This implementation follows security best practices for:
- **OAuth 2.0**: Proper token handling and flows
- **GDPR**: User data protection and audit trails
- **SOC 2**: Security controls and monitoring
- **Auth0 Guidelines**: Token Vault best practices