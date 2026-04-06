# Auth0 API Setup Guide

## Issue Resolution

The authentication issue you're experiencing is caused by using the wrong audience in your Auth0 configuration. The current setup uses `https://dev-m40q4uji8sb8yhq0.us.auth0.com/userinfo` as the audience, but this is for user profile access, not API access tokens.

For API access tokens to have the proper `kid` (Key ID) header that your backend expects, you need to create a proper API in Auth0.

## Quick Fix Steps

### 1. Create API in Auth0 Dashboard

1. Go to your Auth0 Dashboard: https://manage.auth0.com/
2. Navigate to **Applications** → **APIs**
3. Click **Create API**
4. Fill in the details:
   - **Name**: `CipherMate API`
   - **Identifier**: `https://ciphermate-api` (this is your audience)
   - **Signing Algorithm**: `RS256`
5. Click **Create**

### 2. Configure API Settings

1. In your new API settings, go to **Settings** tab
2. Make sure **Enable RBAC** is turned ON
3. Make sure **Add Permissions in the Access Token** is turned ON
4. Save changes

### 3. Add Scopes (Optional)

1. Go to **Permissions** tab in your API
2. Add these scopes if you want granular permissions:
   - `read:profile` - Read user profile
   - `write:profile` - Write user profile  
   - `read:permissions` - Read permissions
   - `write:permissions` - Write permissions
   - `admin:all` - Admin access

### 4. Update Application Settings

1. Go to **Applications** → **Applications**
2. Find your application (`NEuKyZB4ozzGiztiAHjSrPN6VpcPhHQz`)
3. Go to **APIs** tab
4. Make sure your new `CipherMate API` is authorized
5. Grant the scopes you want this application to have

## Configuration Already Updated

I've already updated your configuration files:

### Backend (.env)
```bash
AUTH0_AUDIENCE=https://ciphermate-api
```

### Frontend (.env.local)
```bash
AUTH0_AUDIENCE=https://ciphermate-api
```

### Frontend Auth Handler
The login URL now includes the correct audience parameter.

## Test the Fix

1. **Create the API in Auth0** (steps above)
2. **Restart both servers**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   
   # Terminal 2 - Frontend  
   cd frontend
   npm run dev
   ```
3. **Clear browser data** (important):
   - Open DevTools (F12)
   - Go to Application/Storage tab
   - Clear all cookies and local storage
   - Or use incognito/private browsing
4. **Test login flow**:
   - Go to http://localhost:3000
   - Click login
   - After successful login, try accessing permissions page

## Expected Result

After creating the API in Auth0, the access tokens will:
- Have the proper `kid` header
- Be verifiable by your backend
- Allow successful API calls to `/api/v1/permissions/list` and other endpoints

## Troubleshooting

If you still get "Token missing kid in header":

1. **Verify API Creation**: Make sure the API exists in Auth0 with identifier `https://ciphermate-api`
2. **Check Application Authorization**: Ensure your application is authorized for the API
3. **Clear Sessions**: Clear all browser data and try fresh login
4. **Check Logs**: Look at the actual token being sent in browser DevTools Network tab

## Alternative Quick Fix

If you can't create the API right now, you can temporarily use the Management API:

1. Update both `.env` files to use:
   ```bash
   AUTH0_AUDIENCE=https://dev-m40q4uji8sb8yhq0.us.auth0.com/api/v2/
   ```
2. In Auth0 Dashboard, go to Applications → Your App → APIs tab
3. Authorize the "Auth0 Management API"
4. Grant these scopes: `read:users`, `read:user_idp_tokens`

But the custom API approach is recommended for production.