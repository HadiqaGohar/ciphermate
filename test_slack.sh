#!/bin/bash

echo "🚀 CipherMate AI - Slack Integration Test"
echo "========================================"

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env file not found!"
    echo "Please create it from backend/.env.example"
    exit 1
fi

# Check if SLACK_BOT_TOKEN is configured
if ! grep -q "SLACK_BOT_TOKEN=xoxb-" backend/.env; then
    echo "⚠️  SLACK_BOT_TOKEN not properly configured in backend/.env"
    echo ""
    echo "📋 Quick Setup Guide:"
    echo "1. Go to https://api.slack.com/apps"
    echo "2. Create new app → 'From scratch'"
    echo "3. Choose app name (e.g., 'CipherMate AI') and workspace"
    echo "4. Go to 'OAuth & Permissions'"
    echo "5. Add Bot Token Scopes:"
    echo "   - chat:write"
    echo "   - channels:read"
    echo "6. Click 'Install to Workspace'"
    echo "7. Copy 'Bot User OAuth Token' (starts with xoxb-)"
    echo "8. Update backend/.env:"
    echo "   SLACK_BOT_TOKEN=xoxb-your-actual-token-here"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
cd backend
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q aiohttp python-dotenv

cd ..

# Run the test
echo ""
echo "🧪 Running Slack Integration Tests..."
python3 test_slack_integration.py

echo ""
echo "✨ Test completed!"