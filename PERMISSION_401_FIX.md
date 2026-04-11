# Permission Page 401 Error Fix

## Problem
When trying to connect a service from the Permissions page, the following error occurred:

```
POST /api/permissions/grant 401 in 431ms
Token verification error: 401: Token missing kid in header
```

## Root Cause

The `/api/auth/login` endpoint was **not sending the `audience` parameter** to Auth0 during the OAuth authorization flow.

**What happened:**
1. User logs in via Auth0
2. Auth0 receives the authorize request WITHOUT `audience` parameter
3. Without `audience`, Auth0 returns an **opaque token** (not a JWT)
4. The opaque token doesn't have a `kid` (Key ID) in its header
5. Backend tries to verify the token as a JWT, but fails because there's no `kid`
6. Result: `401: Token missing kid in header`

## Why Auth0 Returns Different Token Types

- **With `audience` parameter**: Auth0 returns a **JWT token** (signed JWT with `kid` header)
- **Without `audience` parameter**: Auth0 returns an **opaque token** (random string, not a JWT)

## Solution

### 1. Updated Login Endpoint
**File**: `frontend/src/app/api/auth/login/route.ts`

Added the `audience` parameter to the authorization URL:

```typescript
const loginUrl = `https://${domain}/authorize?` +
  `response_type=code&` +
  `client_id=${process.env.AUTH0_CLIENT_ID}&` +
  `redirect_uri=${process.env.AUTH0_BASE_URL}/api/auth/callback&` +
  `scope=openid profile email&` +
  `audience=${process.env.AUTH0_AUDIENCE}`;  // ← ADDED
```

### 2. Created Frontend `.env.local`
**File**: `frontend/.env.local`

Created the environment file with the correct Auth0 configuration matching the backend:

```env
AUTH0_ISSUER_BASE_URL=https://dev-m40q4uji8sb8yhq0.us.auth0.com
AUTH0_CLIENT_ID=NEuKyZB4ozzGiztiAHjSrPN6VpcPhHQz
AUTH0_CLIENT_SECRET=lPf97k2GsF64MbloJJxrLxU_S02cwYhEwN7bhFb3MhWQ2n5KR_EV8FN8-QN-BqrL
AUTH0_AUDIENCE=https://ciphermate-api  # ← Must match backend
```

## How to Verify the Fix

1. **Stop the frontend server** (Ctrl+C)
2. **Restart the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
3. **Logout and login again** to get a new JWT token with the audience
4. **Go to Permissions page** (`/permissions`)
5. **Click "Connect" on any service**
6. **Expected**: Should successfully initiate the OAuth flow without 401 error

## Token Flow After Fix

```
User clicks Login
  ↓
Auth0 /authorize?audience=https://ciphermate-api
  ↓
Auth0 returns JWT token (with kid header)
  ↓
Frontend stores in session cookie
  ↓
Frontend calls POST /api/permissions/grant
  ↓
Next.js API route forwards Bearer token to backend
  ↓
Backend verifies JWT using JWKS
  ↓
✅ Success (token has valid kid, signature verified)
```

## Important Notes

- The `AUTH0_AUDIENCE` must match your Auth0 API identifier (created in Auth0 Dashboard → APIs)
- After this fix, **existing sessions will still have opaque tokens** - users must logout and login again
- The audience `https://ciphermate-api` is a custom API identifier, not the Auth0 Management API

## Related Files
- `frontend/src/app/api/auth/login/route.ts` - Login endpoint (FIXED)
- `frontend/src/app/api/auth/callback/route.ts` - Callback endpoint (stores token)
- `frontend/src/app/api/permissions/grant/route.ts` - Permission grant proxy
- `backend/app/core/auth.py` - JWT verification logic
- `backend/app/api/v1/permissions.py` - Permission endpoints
