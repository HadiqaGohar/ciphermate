# CipherMate Quick Start Guide

## 🚀 Start the Application (Recommended)

### Option 1: No Database Mode (Fastest)
Perfect for testing the OpenAI Agents SDK integration and AI features:

```bash
# Terminal 1: Start Backend (No Database)
cd backend
python start_without_db.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

### Option 2: Full Database Mode
If you want to test the complete system with PostgreSQL:

```bash
# Terminal 1: Setup Database (one-time)
cd backend
python setup_database.py

# Start Backend with Database
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

## 🎯 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ✅ What's Working

### Backend (No Database Mode)
- ✅ OpenAI Agents SDK with Gemini API
- ✅ AI Agent intent analysis and response generation
- ✅ All API endpoints (with mock authentication)
- ✅ CORS configured for frontend
- ✅ Health checks and monitoring
- ✅ Mock Token Vault for testing

### Frontend (Next.js 16)
- ✅ Next.js 16 with Turbopack
- ✅ Auth0 authentication ready
- ✅ API integration with backend
- ✅ Tailwind CSS styling
- ✅ TypeScript support

## 🧪 Test the AI Agent

Once both servers are running, you can test the AI agent:

### Via API Documentation (http://localhost:8000/docs)
1. Go to `/api/v1/ai-agent/chat` endpoint
2. Click "Try it out"
3. Use this test payload:
```json
{
  "message": "Schedule a meeting with John tomorrow at 2pm",
  "context": {}
}
```

### Via Frontend
1. Go to http://localhost:3000
2. Use the chat interface to interact with the AI agent
3. Try commands like:
   - "Send an email to sarah@example.com"
   - "Create a GitHub issue about the login bug"
   - "Schedule a meeting for tomorrow"

## 🔧 Troubleshooting

### Backend Issues

**Database Connection Error:**
```
asyncpg.exceptions.InvalidPasswordError: password authentication failed
```
**Solution:** Use no-database mode: `python start_without_db.py`

**Import Errors:**
```bash
cd backend
pip install -r requirements.txt
# or
pip install openai-agents-sdk openai fastapi uvicorn
```

### Frontend Issues

**Next.js Configuration Warnings:**
- These are informational and can be ignored
- The app will work fine with Turbopack

**Module Not Found:**
```bash
cd frontend
npm install
```

**Port Already in Use:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
# Or use different port
npm run dev -- -p 3001
```

## 🔐 Authentication Setup

### For Development (Mock Mode)
The no-database mode includes mock authentication, so you can test all features immediately.

### For Production Setup
1. Configure Auth0 credentials in `.env.local`
2. Set up OAuth apps for Google, GitHub, Slack
3. Configure PostgreSQL database
4. Set up Redis for caching

## 📊 Features to Test

### AI Agent Features
- ✅ Intent classification (calendar, email, GitHub, Slack)
- ✅ Parameter extraction from natural language
- ✅ Permission requirement detection
- ✅ Natural language response generation
- ✅ Multi-service support

### Security Features
- ✅ Permission validation
- ✅ Parameter validation
- ✅ Rate limiting (in full mode)
- ✅ CORS protection
- ✅ Security headers

### Integration Points
- ✅ Token Vault API (mock mode)
- ✅ OAuth flow simulation
- ✅ Audit logging (mock mode)
- ✅ Health monitoring

## 🎉 Success Indicators

You'll know everything is working when:

1. **Backend starts without errors**
2. **Frontend loads at http://localhost:3000**
3. **API docs accessible at http://localhost:8000/docs**
4. **Health check returns "healthy" status**
5. **AI agent responds to test messages**

## 🚀 Next Steps

1. Test the AI agent with various commands
2. Explore the API documentation
3. Set up OAuth for third-party services
4. Configure production database
5. Deploy to your preferred platform

The CipherMate platform is now ready for development and testing with the new OpenAI Agents SDK integration!