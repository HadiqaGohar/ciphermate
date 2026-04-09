#!/bin/bash

echo "🔧 Testing Login Functionality Fix"
echo "=================================="

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Frontend not running on localhost:3000"
    echo "Please start the frontend with: cd frontend && npm run dev"
    exit 1
fi

echo "✅ Frontend is running"

# Test login endpoint
echo "🧪 Testing login endpoint..."
LOGIN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/login)

if [ "$LOGIN_RESPONSE" = "307" ] || [ "$LOGIN_RESPONSE" = "302" ]; then
    echo "✅ Login endpoint returns redirect (expected)"
else
    echo "⚠️  Login endpoint returns: $LOGIN_RESPONSE"
fi

# Test me endpoint
echo "👤 Testing /api/auth/me endpoint..."
ME_RESPONSE=$(curl -s http://localhost:3000/api/auth/me)
echo "   Response: $ME_RESPONSE"

# Test callback endpoint structure
echo "🔄 Testing callback endpoint..."
CALLBACK_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000/api/auth/callback?code=test")

if [ "$CALLBACK_RESPONSE" = "307" ] || [ "$CALLBACK_RESPONSE" = "302" ]; then
    echo "✅ Callback endpoint returns redirect (expected)"
else
    echo "⚠️  Callback endpoint returns: $CALLBACK_RESPONSE"
fi

echo ""
echo "🎯 Login Fix Summary:"
echo "===================="
echo "✅ Enhanced callback to exchange Auth0 code for tokens"
echo "✅ Added proper session creation with user data"
echo "✅ Improved error handling for auth failures"
echo "✅ Added session cookie management"
echo "✅ Updated /api/auth/me to read session properly"
echo ""
echo "📝 To test login manually:"
echo "1. Go to http://localhost:3000"
echo "2. Click 'SIGN IN WITH AUTH0'"
echo "3. Complete Auth0 login"
echo "4. Should redirect to /dashboard"
echo "5. Check that user info appears"
echo ""
echo "🔍 If login still doesn't work:"
echo "1. Check browser developer tools for errors"
echo "2. Verify Auth0 dashboard callback URLs include:"
echo "   - http://localhost:3000/api/auth/callback"
echo "3. Check that all environment variables are set"
echo "4. Look at server logs for detailed error messages"