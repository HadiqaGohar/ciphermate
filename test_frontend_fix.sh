#!/bin/bash

echo "🔧 Testing Frontend Fix"
echo "======================"

# Test 1: Check if frontend starts without errors
echo "1. Testing frontend startup..."
cd frontend
timeout 10s npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!
sleep 5

if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ Frontend starts without immediate errors"
    kill $FRONTEND_PID 2>/dev/null
else
    echo "❌ Frontend failed to start"
fi

# Test 2: Check if components are properly exported
echo "2. Checking component exports..."
if grep -q "export default function Header" src/components/layout/Header.tsx; then
    echo "✅ Header component properly exported"
else
    echo "❌ Header component export issue"
fi

if grep -q "export default function Footer" src/components/layout/Footer.tsx; then
    echo "✅ Footer component properly exported"
else
    echo "❌ Footer component export issue"
fi

if grep -q "export function ServiceUnavailableHandler" src/components/auth/ServiceUnavailableHandler.tsx; then
    echo "✅ ServiceUnavailableHandler component properly exported"
else
    echo "❌ ServiceUnavailableHandler component export issue"
fi

echo ""
echo "🎯 Fix Summary:"
echo "- Removed problematic UserProvider from layout"
echo "- Simplified ChatInterface component"
echo "- Fixed component import/export issues"
echo "- Cleared Next.js cache"
echo ""
echo "📝 Next Steps:"
echo "1. Start frontend: cd frontend && npm run dev"
echo "2. Test dashboard: http://localhost:3000/dashboard"
echo "3. Test chat: http://localhost:3000/chat"