#!/bin/bash

echo "🔧 Testing CipherMate Fixes"
echo "=========================="

# Test 1: Check if backend is running
echo "1. Testing backend health..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
if [ "$response" = "200" ]; then
    echo "✅ Backend is running"
else
    echo "❌ Backend is not responding (HTTP $response)"
fi

# Test 2: Check if frontend is running
echo "2. Testing frontend..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$response" = "200" ]; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding (HTTP $response)"
fi

# Test 3: Check Auth0 login endpoint
echo "3. Testing Auth0 login endpoint..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/login)
if [ "$response" = "302" ]; then
    echo "✅ Auth0 login redirect working"
else
    echo "❌ Auth0 login not working (HTTP $response)"
fi

# Test 4: Check API endpoints
echo "4. Testing API endpoints..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/me)
if [ "$response" = "200" ]; then
    echo "✅ Auth me endpoint working"
else
    echo "❌ Auth me endpoint not working (HTTP $response)"
fi

# Test 5: Check backend status endpoint
echo "5. Testing backend status..."
response=$(curl -s http://localhost:8080/health)
if echo "$response" | grep -q "healthy"; then
    echo "✅ Backend health check working"
else
    echo "❌ Backend health check failed"
fi

echo ""
echo "🎯 Fix Summary:"
echo "- Fixed Auth0 JWE Invalid error by using proper getSession import"
echo "- Made Redis optional - backend runs without Redis connection"
echo "- Fixed status page undefined property errors"
echo "- Created missing API routes for token-vault and agent actions"
echo "- Added proper error handling for Redis connection failures"
echo ""
echo "📝 Next Steps:"
echo "1. Restart both frontend and backend"
echo "2. Try logging in with Auth0"
echo "3. Test the dashboard and other pages"
echo "4. If you want Redis caching, install and start Redis server"