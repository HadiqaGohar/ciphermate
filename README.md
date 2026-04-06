# 🔐 CipherMate

> **AI-Powered Security & Permission Management Platform**

CipherMate is an intelligent assistant that helps users manage their connected services (Google Calendar, Gmail, GitHub, Slack) through natural language conversations with proper security and permission controls.

![CipherMate Dashboard](https://img.shields.io/badge/Status-Hackathon%20Project-brightgreen)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue)

## 🚀 Features

### 🤖 AI-Powered Assistant

- **OpenAI Agents SDK** with specialized agent routing
- **Multi-Agent Architecture** for different service domains
- **Intent Recognition** for complex multi-service operations
- **Context-Aware Responses** with smart parameter extraction
- **Fallback Responses** when AI services are unavailable

### 🔗 Multi-Service Integration

- **📅 Google Calendar** - Create, update, and manage events
- **📧 Gmail** - Send emails with AI-powered composition
- **🐙 GitHub** - Manage repositories, issues, and pull requests
- **💬 Slack** - Send messages and manage channels
- **🔄 Extensible Architecture** for adding new services

### 🔒 Enterprise-Grade Security

- **Auth0 Authentication** with OAuth 2.0
- **Granular Permission Management** at service level
- **Secure Token Vault** for credential storage
- **Complete Audit Logging** for compliance
- **Real-time Security Monitoring**

### 📊 Management Dashboard

- **Real-time Action Monitoring** with status tracking
- **Permission Management Interface**
- **Audit Trail Visualization**
- **Service Health Monitoring**
- **Token Management System**

## 🛠️ Tech Stack

### Frontend

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **React Hooks** - Modern state management

### Backend

- **FastAPI** - High-performance Python web framework
- **Python 3.11+** - Modern Python features
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation and serialization

### Database & Storage

- **SQLite/PostgreSQL** - Flexible database options
- **Redis** - Optional caching layer
- **Secure Token Storage** - Encrypted credential management

### AI & Authentication

- **OpenAI Agents SDK** - Multi-agent architecture with specialized routing
- **GPT-4o-mini** - Cost-effective AI processing
- **Auth0** - Enterprise authentication
- **OAuth 2.0** - Secure service authorization

## 📁 Project Structure

```
ciphermate/
├── frontend/                    # Next.js Application
│   ├── src/app/                # App Router pages
│   │   ├── dashboard/          # Main dashboard
│   │   ├── ai-agent/          # AI chat interface
│   │   ├── token-vault/       # Permission management
│   │   ├── features/          # Feature showcase
│   │   ├── docs/              # Documentation
│   │   └── api/               # API routes
│   ├── components/            # Reusable React components
│   └── public/               # Static assets
│
├── backend/                   # FastAPI Application
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/       # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   └── main.py              # Application entry point
│
├── README.md                 # This file
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.11+** and pip
- **Auth0 Account** (free tier available)
- **OpenAI Account** (for GPT API access)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ciphermate.git
cd ciphermate
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Configure your environment variables
# AUTH0_DOMAIN=your-auth0-domain
# AUTH0_CLIENT_ID=your-client-id
# AUTH0_CLIENT_SECRET=your-client-secret
# OPENAI_API_KEY=your-openai-api-key
# DATABASE_URL=sqlite:///./ciphermate.db

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Configure your environment variables
# NEXT_PUBLIC_API_URL=http://localhost:8080
# AUTH0_SECRET=your-auth0-secret
# AUTH0_BASE_URL=http://localhost:3000
# AUTH0_ISSUER_BASE_URL=https://your-domain.auth0.com
# AUTH0_CLIENT_ID=your-client-id
# AUTH0_CLIENT_SECRET=your-client-secret

# Run frontend server
npm run dev
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs

## 🔧 Configuration

### Auth0 Setup

1. Create an Auth0 application
2. Configure callback URLs:
   - `http://localhost:3000/api/auth/callback`
3. Set logout URLs:
   - `http://localhost:3000`
4. Enable Google, GitHub OAuth connections

### OpenAI API Setup

1. Create an OpenAI account at https://platform.openai.com
2. Generate an API key in the API keys section
3. Add to environment variables: `OPENAI_API_KEY=sk-your-key-here`
4. The system uses GPT-4o-mini for cost-effective AI processing

### Service Integrations

Each service requires OAuth setup:

- **Google**: Calendar and Gmail APIs
- **GitHub**: GitHub Apps or OAuth Apps
- **Slack**: Slack Apps with appropriate scopes

## 💡 Usage Examples

### Natural Language Commands

```
🗣️ "Schedule a team meeting tomorrow at 2 PM"
🗣️ "Send a follow-up email to john@example.com about the project"
🗣️ "Create a GitHub issue for the login bug"
🗣️ "Send a message to #general channel about the deployment"
```

### API Usage

```javascript
// Chat with AI Agent
const response = await fetch("/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Create a meeting tomorrow at 2 PM",
    context: { user_id: "user123" },
  }),
});

// Get agent actions
const actions = await fetch("/api/v1/agent/actions");
```

## 🎯 Problem Statement & Solution

### Problems We Solve

1. **🔄 Service Fragmentation**
   - Users juggle multiple platforms daily
   - Context switching reduces productivity
   - **Solution**: Unified natural language interface

2. **🔐 Permission Complexity**
   - Difficult to manage granular permissions
   - Lack of centralized control
   - **Solution**: Centralized permission management with audit trails

3. **📊 Compliance Challenges**
   - No visibility into automated actions
   - Difficult to maintain audit trails
   - **Solution**: Complete logging and monitoring dashboard

4. **⏰ Time-Consuming Tasks**
   - Repetitive cross-platform operations
   - Manual coordination between services
   - **Solution**: AI-powered automation with natural language

### Unique Selling Points

✨ **Natural Language Interface** - Complex operations through simple conversations  
🔒 **Granular Security Controls** - Service-level permission management  
📋 **Complete Audit Trail** - Every action logged for compliance  
🔗 **Seamless Integration** - Works with existing Auth0 infrastructure  
🏗️ **Extensible Architecture** - Easy to add new services and capabilities

## 🏆 Hackathon Highlights

### Innovation

- **AI-First Approach**: Natural language as the primary interface
- **Security-Centric Design**: Built with enterprise security from day one
- **Unified Experience**: Single platform for multiple service management

### Technical Excellence

- **Modern Stack**: Latest Next.js, FastAPI, and TypeScript
- **Scalable Architecture**: Microservices-ready design
- **Production-Ready**: Comprehensive error handling and monitoring

### User Experience

- **Intuitive Interface**: Clean, responsive design
- **Real-time Feedback**: Live status updates and notifications
- **Comprehensive Documentation**: Built-in help and examples

## 🔮 Future Roadmap

### Phase 1 (Current)

- ✅ Core AI chat functionality
- ✅ Basic service integrations
- ✅ Auth0 authentication
- ✅ Permission management

### Phase 2 (Next)

- 🔄 Advanced workflow automation
- 📱 Mobile application
- 🔔 Smart notifications
- 📈 Analytics dashboard

### Phase 3 (Future)

- 🤖 Custom AI model training
- 🌐 Multi-tenant support
- 🔌 Plugin marketplace
- 📊 Advanced reporting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for powerful AI capabilities
- **Auth0** for robust authentication infrastructure
- **FastAPI** and **Next.js** communities for excellent frameworks
- **Hackathon organizers** for the opportunity to innovate

## 📞 Support

- **Documentation**: [http://localhost:3000/docs](http://localhost:3000/docs)
- **Status Page**: [http://localhost:3000/status](http://localhost:3000/status)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ciphermate/issues)

---

<div align="center">

**Built with ❤️ for the Hackathon**

[🚀 Try CipherMate](http://localhost:3000) | [📚 Documentation](http://localhost:3000/docs) | [🔍 Features](http://localhost:3000/features)

</div>



Dark = 3B1E54
1st = 9B7EBD
2nd = D4BEE4
Light = EEEEEE

Light = FFF8F0
1st = C08552
Choco = 8C5A3C
Dark choco = 4B2E2B# ciphermate
