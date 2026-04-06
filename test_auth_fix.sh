#!/bin/bash

# Test script to verify authentication fixes
# This script helps verify that the authentication error fixes are working

echo "==================================="
echo "CipherMate Authentication Fix Test"
echo "==================================="
echo ""

# Check if the frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    exit 1
fi

echo "✅ Frontend directory found"
echo ""

# Check if the layout file has been updated
if grep -q "Auth0ClientProvider" frontend/src/app/layout.tsx; then
    echo "✅ Auth0Provider is present in layout.tsx"
else
    echo "❌ Auth0Provider is missing from layout.tsx"
    exit 1
fi

# Check if the ChatInterface has been updated
if grep -q "isDuplicate" frontend/src/components/chat/ChatInterface.tsx; then
    echo "✅ Duplicate error prevention is present in ChatInterface.tsx"
else
    echo "❌ Duplicate error prevention is missing from ChatInterface.tsx"
    exit 1
fi

echo ""
echo "==================================="
echo "All checks passed! ✅"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Start the frontend development server:"
echo "   cd frontend && npm run dev"
echo ""
echo "2. Open your browser and navigate to:"
echo "   http://localhost:3000"
echo ""
echo "3. Test the authentication flow:"
echo "   - Click 'Sign in with Auth0'"
echo "   - Complete authentication"
echo "   - Verify you're redirected to the dashboard"
echo ""
echo "4. Test the chat interface:"
echo "   - Send a message in the chat"
echo "   - Verify no repeated error messages appear"
echo ""
echo "5. Check the browser console for any errors"
echo ""
echo "For more details, see: AUTHENTICATION_FIX_SUMMARY.md"
echo ""
