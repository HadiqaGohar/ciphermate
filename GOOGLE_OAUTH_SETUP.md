# 🔐 Google OAuth Setup Guide

## Problem: OAuth 403 Error

If you see:
```
Error 403: access_denied
CipherMate has not completed the Google verification process
```

## Solution: Add Test Users

### Step 1: Open Google Cloud Console
Go to: https://console.cloud.google.com/

### Step 2: Navigate to OAuth Consent Screen
1. Click **APIs & Services**
2. Click **OAuth consent screen**

### Step 3: Add Test Users
1. Scroll to **"Test users"** section
2. Click **"+ ADD USERS"**
3. Add your email address
4. Click **SAVE**

### Step 4: Wait & Test
1. Wait 2-5 minutes for changes to propagate
2. Clear browser cache or use incognito mode
3. Try signing in again

## Alternative: Use Auth0 Social Login

Your project has Auth0 configured which can handle Google OAuth:

1. Go to Auth0 Dashboard
2. Enable Google Social Connection
3. Add your Google OAuth credentials
4. Users authenticate through Auth0

This bypasses Google's testing mode restrictions.

## Environment Setup

Update your `.env` file with real Google OAuth credentials:

```env
GOOGLE_CLIENT_ID=[YOUR_GOOGLE_CLIENT_ID]
GOOGLE_CLIENT_SECRET=[YOUR_GOOGLE_CLIENT_SECRET]
```

Get these from Google Cloud Console → Credentials → OAuth 2.0 Client IDs.