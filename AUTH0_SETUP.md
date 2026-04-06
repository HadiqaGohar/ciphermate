# Auth0 Setup Guide for CipherMate

This guide walks you through setting up Auth0 for AI Agents with Token Vault for the CipherMate platform.

## Prerequisites

- Auth0 account with access to Auth0 for AI Agents features
- Node.js and npm installed
- Python 3.11+ installed
- Redis server running
- PostgreSQL database running

## Auth0 Configuration

### 1. Create Auth0 Tenant

1. Log in to your Auth0 Dashboard
2. Create a new tenant or use an existing one
3. Ensure you have access to the "Auth0 for AI Agents" features

### 2. Configure Token Vault

1. In your Auth0 Dashboard, navigate to **Applications** > **APIs**
2. Create a new API or use the default Management API
3. Enable **Token Vault** feature for your tenant
4. Configure the following scopes for Token Vault:
   - `read:tokens`
   - `write:tokens`
   - `delete:tokens`

### 3. Create Application

1. Go to **Applications** in your Auth0 Dashboard
2. Click **Create Application**
3. Choose **Single Page Application** for the frontend
4. Configure the following settings:

#### Application Settings
- **Name**: CipherMate Frontend
- **Application Type**: Single Page Application
- **Token Endpoint Authentication Method**: None

#### Application URIs
- **Allowed Callback URLs**: `http://localhost:3000/api/auth/callback`
- **Allowed Logout URLs**: `http://localhost:3000`
- **Allowed Web Origins**: `http://localhost:3000`
- **Allowed Origins (CORS)**: `http://localhost:3000`

### 4. Create Machine-to-Machine Application

1. Create another application for the backend
2. Choose **Machine to Machine Applications**
3. Configure the following settings:

#### Application Settings
- **Name**: CipherMate Backend
- **Application Type**: Machine to Machine

#### API Authorization
- Authorize for **Auth0 Management API**
- Grant the following scopes:
  - `read:users`
  - `update:users`
  - `read:user_tokens` (Token Vault)
  - `write:user_tokens` (Token Vault)
  - `delete:user_tokens` (Token Vault)

## Environment Configuration

### Frontend (.env.local)

Create a `.env.local` file in the `frontend` directory:

```bash
# Generate a secret: openssl rand -hex 32
AUTH0_SECRET='your-32-byte-secret-here'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://your-domain.auth0.com'
AUTH0_CLIENT_ID='your-spa-client-id'
AUTH0_CLIENT_SECRET='your-spa-client-secret'
AUTH0_AUDIENCE='https://your-domain.auth0.com/api/v2/'

# Backend API URL
NEXT_PUBLIC_API_URL='http://localhost:8000'
```

### Backend (.env)

Create a `.env` file in the `backend` directory:

```bash
# Application Configuration
APP_ENV=development
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ciphermate

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Auth0 Configuration
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-m2m-client-id
AUTH0_CLIENT_SECRET=your-m2m-client-secret
AUTH0_AUDIENCE=https://your-domain.auth0.com/api/v2/

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Security Configuration
SECRET_KEY=your-super-secret-key-change-in-production
```

## Third-Party Service Setup

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Calendar API
   - Gmail API
   - Google Drive API (optional)
4. Create OAuth 2.0 credentials:
   - **Application type**: Web application
   - **Authorized redirect URIs**: `http://localhost:3000/api/auth/callback/google`

### GitHub OAuth Setup

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App:
   - **Application name**: CipherMate
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization callback URL**: `http://localhost:3000/api/auth/callback/github`

### Slack OAuth Setup

1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new Slack app
3. Configure OAuth & Permissions:
   - **Redirect URLs**: `http://localhost:3000/api/auth/callback/slack`
   - **Scopes**: Add required bot and user scopes

## Testing the Setup

### 1. Test Backend Authentication

```bash
cd backend
python test_auth.py
```

This will verify:
- Auth0 configuration
- JWKS endpoint accessibility
- Redis connection
- Management API token acquisition

### 2. Test Frontend Authentication

1. Start the frontend development server:
```bash
cd frontend
npm run dev
```

2. Navigate to `http://localhost:3000`
3. Click the "Login" button
4. Complete the Auth0 authentication flow
5. Verify you're redirected to the dashboard

### 3. Test Full Integration

1. Start both frontend and backend servers
2. Log in through the frontend
3. Check that the backend receives and validates the JWT token
4. Verify session management works correctly

## Troubleshooting

### Common Issues

1. **JWKS endpoint not accessible**
   - Check your Auth0 domain configuration
   - Ensure the domain is correct and accessible

2. **Token validation fails**
   - Verify the audience configuration matches between frontend and backend
   - Check that the JWT algorithms are correctly configured

3. **CORS errors**
   - Ensure all origins are properly configured in Auth0 dashboard
   - Check CORS middleware configuration in the backend

4. **Redis connection fails**
   - Ensure Redis server is running
   - Check the Redis URL configuration

5. **Management API token fails**
   - Verify the Machine-to-Machine application has correct scopes
   - Check client credentials are correct

### Debug Mode

Enable debug logging by setting `DEBUG=true` in your environment variables. This will provide detailed logs for troubleshooting.

## Security Considerations

1. **Never commit secrets to version control**
2. **Use strong, unique secrets for production**
3. **Regularly rotate API keys and secrets**
4. **Monitor Auth0 logs for suspicious activity**
5. **Implement proper rate limiting**
6. **Use HTTPS in production**

## Next Steps

After completing this setup:

1. Test the authentication flow end-to-end
2. Implement OAuth flows for third-party services
3. Configure Token Vault for storing service tokens
4. Set up proper monitoring and logging
5. Deploy to production with proper security measures

For more information, refer to the [Auth0 for AI Agents documentation](https://auth0.com/docs/get-started/auth0-overview/ai-agents).