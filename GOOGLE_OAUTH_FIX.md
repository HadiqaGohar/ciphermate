# 🔴 Google OAuth Error 403 Fix Guide

## Problem
You're seeing: **"Error 403: access_denied - CipherMate has not completed the Google verification process"**

This happens because your Google Cloud Console OAuth app is in **"Testing"** status, not **"Production"**.

---

## ✅ Solution (Choose ONE option)

### Option 1: Add Test Users (Quickest - 2 minutes)
**Best for development and hackathons**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **APIs & Services** > **OAuth consent screen**
4. Scroll down to **"Test users"** section
5. Click **+ ADD USERS**
6. Add your email: `tasleemhadiqa76@gmail.com`
7. Click **SAVE**
8. Wait 2-3 minutes, then try signing in again

**✅ Pros:**
- Immediate fix
- No app verification needed
- Perfect for development/testing

**❌ Cons:**
- Only added users can sign in
- Must publish app for production use

---

### Option 2: Publish Your OAuth App (For Production)
**Required if you want anyone to sign in**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** > **OAuth consent screen**
3. Fill in ALL required fields:
   - **App name**: CipherMate
   - **User support email**: Your email
   - **App logo**: Upload a logo
   - **App domain**: Your domain (for production)
   - **Developer contact email**: Your email
4. Under **"Scopes"**, add:
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/gmail.send`
   - `email`
   - `profile`
5. Click **SAVE AND CONTINUE**
6. On the **"Test users"** page, click **BACK TO DASHBOARD**
7. Click **PUBLISH APP**
8. Wait for Google to review (can take several days)

**✅ Pros:**
- Anyone can sign in
- Production-ready

**❌ Cons:**
- Takes time to get approved
- Requires complete app information

---

### Option 3: Use Auth0 Universal Login (Recommended for Hackathon)
**Bypasses Google OAuth entirely and uses Auth0 as the central auth provider**

Your project already has Auth0 configured. Use Auth0's social connections instead of direct Google OAuth:

1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Navigate to **Authentication** > **Social**
3. Click **Google** and enable it
4. Configure with your Google Client ID and Secret
5. Auth0 handles the OAuth flow, so your app stays in testing mode
6. Users authenticate through Auth0, not directly through Google

**✅ Pros:**
- Centralized auth management
- Auth0 handles OAuth complexity
- Works with Google app in testing mode
- Easy to add more social providers

**❌ Cons:**
- Requires Auth0 account (which you already have)

---

## 🔧 Next Steps for Your Project

### Step 1: Add Test Users (Do this NOW - 2 minutes)
Follow Option 1 above to add `tasleemhadiqa76@gmail.com` as a test user.

### Step 2: Configure Environment Variables
Once you have your Google OAuth credentials:

```bash
# In /home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/backend/.env
GOOGLE_CLIENT_ID=YOUR_REAL_CLIENT_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_REAL_CLIENT_SECRET
GMAIL_ENABLED=true
```

### Step 3: Verify Redirect URIs
In Google Cloud Console > APIs & Services > Credentials > Your OAuth 2.0 Client:

Add these **Authorized redirect URIs**:
- `http://localhost:3000/api/auth/google/callback`
- `http://localhost:3000/api/auth/gmail/callback`
- `http://localhost:8080/api/v1/auth/google/callback`

### Step 4: Restart Services
```bash
# Backend
cd backend
# Kill existing process
pkill -f "uvicorn"
# Restart
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Frontend
cd frontend
npm run dev
```

---

## 🐛 Troubleshooting

### Still getting access_denied?
- ✅ Check you added the **exact email** you're signing in with
- ✅ Clear browser cache and cookies for google.com
- ✅ Try incognito mode
- ✅ Wait 5 minutes after adding test users

### Different error?
- ✅ Check browser console for details
- ✅ Verify redirect URIs match exactly (no typos)
- ✅ Ensure your Google Cloud project has the APIs enabled:
  - Google Calendar API
  - Gmail API
  - Google+ API (for profile info)

### Want to skip Google OAuth entirely?
Use Auth0's social login instead. Your app already has Auth0 configured. The Auth0 connection to Google will work even while your Google app is in testing mode.

---

## 📋 Checklist

- [ ] Add test users in Google Cloud Console
- [ ] Configure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in backend `.env`
- [ ] Set `GMAIL_ENABLED=true` in backend `.env`
- [ ] Verify redirect URIs in Google Cloud Console
- [ ] Restart backend and frontend services
- [ ] Test sign-in with Google
- [ ] Test calendar and Gmail integrations

---

## 🎯 Quick Fix for Hackathon Demo

**RIGHT NOW (takes 2 minutes):**
1. Google Cloud Console → OAuth consent screen → Test users → Add `tasleemhadiqa76@gmail.com`
2. Try signing in again

**LATER (for production):**
- Publish your OAuth app following Option 2
- Or use Auth0 social connections (Option 3)
