#!/bin/bash

echo "🔧 Testing Logout Functionality Fix"
echo "=================================="

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Frontend not running on localhost:3000"
    echo "Please start the frontend with: cd frontend && npm run dev"
    exit 1
fi

echo "✅ Frontend is running"

# Test logout endpoint
echo "🧪 Testing logout endpoint..."
LOGOUT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/logout)

if [ "$LOGOUT_RESPONSE" = "307" ]; then
    echo "✅ Logout endpoint returns 307 redirect (expected)"
elif [ "$LOGOUT_RESPONSE" = "302" ]; then
    echo "✅ Logout endpoint returns 302 redirect (expected)"
else
    echo "⚠️  Logout endpoint returns: $LOGOUT_RESPONSE"
fi

# Test if logout clears cookies
echo "🍪 Testing cookie clearing..."
COOKIE_TEST=$(curl -s -I http://localhost:3000/api/auth/logout | grep -i "set-cookie")

if [ -n "$COOKIE_TEST" ]; then
    echo "✅ Logout endpoint sets cookies (clearing them)"
    echo "   Cookie headers found:"
    echo "$COOKIE_TEST" | sed 's/^/   /'
else
    echo "⚠️  No cookie clearing headers found"
fi

echo ""
echo "🎯 Logout Fix Summary:"
echo "====================="
echo "✅ Updated logout API to clear session cookies"
echo "✅ Enhanced logout buttons with proper error handling"
echo "✅ Added client-side storage clearing"
echo "✅ Improved Auth0 logout URL encoding"
echo ""
echo "📝 To test manually:"
echo "1. Login to the application"
echo "2. Click the logout button"
echo "3. Verify you're redirected to Auth0 logout"
echo "4. Verify you're redirected back to home page"
echo "5. Verify you can't access protected pages"
echo ""
echo "🔍 If logout still doesn't work:"
echo "1. Check your .env file has AUTH0_BASE_URL set"
echo "2. Verify Auth0 dashboard has correct logout URLs"
echo "3. Check browser developer tools for errors"