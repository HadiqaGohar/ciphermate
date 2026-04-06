#!/bin/bash
set -e

echo "🚀 Starting CipherMate Backend (No Database Mode)"
echo "📍 Working directory: $(pwd)"
echo "🔧 Python version: $(python --version)"
echo "🌐 Port: ${PORT:-8080}"
echo "📦 Environment: ${APP_ENV:-production}"

# Check if the app module exists
if python -c "import app.main_no_db" 2>/dev/null; then
    echo "✅ App module found successfully"
else
    echo "❌ App module not found, listing directory structure:"
    ls -la
    ls -la app/ 2>/dev/null || echo "No app/ directory found"
    exit 1
fi

# Start the application
echo "🎯 Starting uvicorn server..."
exec uvicorn app.main_no_db:app \
    --host 0.0.0.0 \
    --port ${PORT:-8080} \
    --workers 1 \
    --log-level info