#!/bin/bash

echo "🐳 Testing Docker container locally..."

# Build the image
echo "Building Docker image..."
docker build -t ciphermate-test ./backend

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker build successful"

# Test the container
echo "Testing container startup..."
docker run --rm -p 8080:8080 -e GEMINI_API_KEY="test" ciphermate-test &

# Wait a bit for startup
sleep 5

# Test if port is responding
curl -f http://localhost:8080/health || echo "❌ Health check failed"

# Stop the container
docker stop $(docker ps -q --filter ancestor=ciphermate-test)

echo "🎉 Local Docker test complete"