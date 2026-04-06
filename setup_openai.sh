#!/bin/bash

echo "🚀 Setting up CipherMate with OpenAI Agents SDK..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install openai>=1.0.0
pip install agents>=0.1.0
pip install -r requirements.txt

# Test OpenAI Agents SDK configuration
echo "🧪 Testing OpenAI Agents SDK configuration..."
python test_openai.py

echo ""
echo "🧪 Testing complete Agents SDK integration..."
python test_agents_integration.py

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to backend/.env:"
echo "   OPENAI_API_KEY=sk-your-actual-key-here"
echo ""
echo "2. Start the backend server:"
echo "   cd backend && python -m uvicorn app.main:app --reload --port 8080"
echo ""
echo "3. Start the frontend server:"
echo "   cd frontend && npm run dev"
echo ""
echo "4. Test the chat at http://localhost:3000/chat"
echo ""
echo "🤖 The system now uses OpenAI Agents SDK with specialized agents for:"
echo "   - Calendar management (calendar_agent)"
echo "   - Email handling (email_agent)" 
echo "   - GitHub operations (github_agent)"
echo "   - Slack messaging (slack_agent)"
echo "   - General queries and math (general_agent)"
echo "   - Intelligent routing (triage_agent)"