#!/bin/bash

echo "🚀 Starting CipherMate - Complete Working Application"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ Created .env file. You can edit it to add your Auth0 credentials."
fi

# Create frontend .env.local if it doesn't exist
if [ ! -f frontend/.env.local ]; then
    echo "📝 Creating frontend/.env.local file..."
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ Created frontend/.env.local file."
fi

echo ""
echo "🐳 Starting Docker containers..."
echo "This will:"
echo "  - Build and start the backend API (port 8080)"
echo "  - Build and start the frontend (port 3000)"
echo "  - Use simplified mode (no database/redis required)"
echo ""

# Start the application
docker-compose -f docker-compose.simple.yml up --build

echo ""
echo "🎉 CipherMate is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8080"
echo "📚 API Docs: http://localhost:8080/docs"
echo "❤️  Health Check: http://localhost:8080/health"
echo ""
echo "To stop: Press Ctrl+C or run 'docker-compose -f docker-compose.simple.yml down'"