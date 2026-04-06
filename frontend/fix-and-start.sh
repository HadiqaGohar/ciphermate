#!/bin/bash

echo "🔧 CipherMate Frontend - Fix and Start Script"
echo "=============================================="

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: This script must be run from the frontend directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local with default values..."
    cat > .env.local << EOF
# Auth0 Configuration
AUTH0_SECRET='$(openssl rand -hex 32)'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://your-auth0-domain.auth0.com'
AUTH0_CLIENT_ID='your-auth0-client-id'
AUTH0_CLIENT_SECRET='your-auth0-client-secret'

# API Configuration
NEXT_PUBLIC_API_BASE_URL='http://localhost:8000'

# App Configuration
NEXT_PUBLIC_APP_NAME='CipherMate'
NEXT_PUBLIC_APP_VERSION='1.0.0'
NEXT_PUBLIC_ENVIRONMENT='development'
EOF
    echo "✅ Created .env.local with default values"
    echo "⚠️  Please update the Auth0 configuration values in .env.local"
else
    echo "✅ .env.local already exists"
fi

echo ""
echo "🚀 Starting development server..."
echo "   The server will be available at: http://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the development server with explicit Turbopack flag to avoid warnings
npm run dev -- --turbopack