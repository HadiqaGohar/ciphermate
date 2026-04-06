# Design Document

## Overview

CipherMate is a secure AI assistant platform that demonstrates the power of Auth0 for AI Agents Token Vault by enabling users to safely delegate third-party API access to AI agents. The platform follows a microservices architecture with clear separation between authentication, authorization, AI processing, and data persistence layers.

The system is designed around the principle of explicit user consent and granular permission management, ensuring that AI agents can only perform actions that users have explicitly authorized while maintaining full audit trails of all activities.

## Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Next.js Frontend]
        Chat[Chat Interface]
        Perms[Permission Management]
        Audit[Audit Dashboard]
    end
    
    subgraph "Authentication Layer"
        Auth0[Auth0 for AI Agents]
        TokenVault[Token Vault]
        OAuth[OAuth Flows]
    end
    
    subgraph "Backend Layer"
        API[FastAPI Backend]
        Agent[AI Agent Engine]
        Proxy[API Proxy Service]
    end
    
    subgraph "AI Layer"
        Gemini[Gemini API]
        OpenAI[OpenAI Agents SDK]
        Intent[Intent Analysis]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL)]
        Redis[(Redis Cache)]
        Logs[Audit Logs]
    end
    
    subgraph "External Services"
        Google[Google APIs]
        GitHub[GitHub API]
        Slack[Slack API]
    end
    
    UI --> Auth0
    UI --> API
    Auth0 --> TokenVault
    API --> Agent
    Agent --> Gemini
    Agent --> OpenAI
    API --> Proxy
    Proxy --> TokenVault
    Proxy --> Google
    Proxy --> GitHub
    Proxy --> Slack
    API --> DB
    API --> Redis
    DB --> Logs
```

### Security Architecture

```mermaid
graph LR
    subgraph "User Context"
        User[User]
        Browser[Browser]
    end
    
    subgraph "Auth0 Security Layer"
        AuthN[Authentication]
        AuthZ[Authorization]
        TV[Token Vault]
        Consent[Consent Management]
    end
    
    subgraph "Application Security"
        JWT[JWT Validation]
        RBAC[Role-Based Access]
        Audit[Audit Logging]
        Encrypt[Data Encryption]
    end
    
    User --> Browser
    Browser --> AuthN
    AuthN --> AuthZ
    AuthZ --> TV
    TV --> Consent
    Browser --> JWT
    JWT --> RBAC
    RBAC --> Audit
    Audit --> Encrypt
```

## Components and Interfaces

### Frontend Components

#### 1. Authentication Component
- **Purpose**: Handle user authentication flows using Auth0
- **Key Features**:
  - Login/logout functionality
  - Session management
  - Token refresh handling
- **Technologies**: Next.js App Router, @auth0/nextjs-auth0
- **Interface**: Integrates with Auth0 Universal Login

#### 2. Chat Interface Component
- **Purpose**: Provide natural language interaction with AI agent
- **Key Features**:
  - Real-time messaging
  - Intent recognition feedback
  - Permission request prompts
  - Action confirmation dialogs
- **Technologies**: React, WebSocket (optional), Tailwind CSS
- **Interface**: REST API to backend agent service

#### 3. Permission Management Component
- **Purpose**: Allow users to view and manage service permissions
- **Key Features**:
  - Service connection status
  - Scope visualization
  - Permission revocation
  - OAuth flow initiation
- **Technologies**: React, Headless UI components
- **Interface**: REST API for permission CRUD operations

#### 4. Audit Dashboard Component
- **Purpose**: Display comprehensive activity logs
- **Key Features**:
  - Chronological action history
  - Service-specific filtering
  - Export functionality
  - Real-time updates
- **Technologies**: React, Chart.js (for visualizations)
- **Interface**: REST API for audit log retrieval

### Backend Components

#### 1. Authentication Middleware
- **Purpose**: Validate JWT tokens and extract user context
- **Key Features**:
  - Token validation with Auth0
  - User session management
  - Rate limiting
  - CORS handling
- **Technologies**: FastAPI, python-jose, Auth0 Python SDK
- **Interface**: HTTP middleware for all protected routes

#### 2. AI Agent Engine
- **Purpose**: Process natural language requests and execute actions
- **Key Features**:
  - Intent analysis using Gemini API
  - Permission requirement mapping
  - Action execution orchestration
  - Response generation
- **Technologies**: Google Generative AI, OpenAI Agents SDK
- **Interface**: Internal service API

#### 3. Token Vault Integration Service
- **Purpose**: Manage secure token storage and retrieval
- **Key Features**:
  - Token storage in Auth0 Token Vault
  - Secure token retrieval
  - Token refresh handling
  - Permission scope validation
- **Technologies**: Auth0 Management API, httpx
- **Interface**: Internal service for token operations

#### 4. API Proxy Service
- **Purpose**: Execute third-party API calls using stored tokens
- **Key Features**:
  - Dynamic API routing
  - Token injection
  - Response transformation
  - Error handling and retry logic
- **Technologies**: httpx, asyncio
- **Interface**: Internal service for external API calls

#### 5. Audit Service
- **Purpose**: Comprehensive logging and monitoring
- **Key Features**:
  - Action logging
  - Performance metrics
  - Security event tracking
  - Data retention management
- **Technologies**: SQLAlchemy, PostgreSQL
- **Interface**: Internal logging interface

### External Service Integrations

#### 1. Google Services Integration
- **Supported APIs**:
  - Google Calendar API (read/write events)
  - Gmail API (read/send emails)
  - Google Drive API (file operations)
- **OAuth Scopes**: Granular permissions per service
- **Implementation**: REST API calls with OAuth 2.0 tokens

#### 2. GitHub Integration
- **Supported APIs**:
  - Repository management
  - Issue tracking
  - Pull request operations
  - User profile access
- **OAuth Scopes**: Repository and user permissions
- **Implementation**: GitHub REST API v4

#### 3. Slack Integration
- **Supported APIs**:
  - Channel messaging
  - User management
  - Workspace information
- **OAuth Scopes**: Bot and user token permissions
- **Implementation**: Slack Web API

## Data Models

### User Management Schema

```sql
-- Users table for local user data
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}'
);

-- Service connections with Token Vault references
CREATE TABLE service_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service_name VARCHAR(50) NOT NULL,
    token_vault_id VARCHAR(255) NOT NULL, -- Auth0 Token Vault reference
    scopes JSONB, -- Array of granted permissions
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);
```

### Audit and Logging Schema

```sql
-- Comprehensive audit logging
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type VARCHAR(50) NOT NULL,
    service_name VARCHAR(50),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255)
);

-- Agent action tracking
CREATE TABLE agent_actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    parameters JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    result TEXT,
    requires_step_up BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP,
    execution_time_ms INTEGER
);
```

### Permission and Security Schema

```sql
-- Permission templates for different services
CREATE TABLE permission_templates (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    scope_name VARCHAR(100) NOT NULL,
    description TEXT,
    risk_level VARCHAR(20) DEFAULT 'medium',
    requires_step_up BOOLEAN DEFAULT FALSE
);

-- Security events tracking
CREATE TABLE security_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'info',
    details JSONB,
    ip_address INET,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE
);
```

## Error Handling

### Error Classification System

#### 1. Authentication Errors
- **Token Expired**: Automatic refresh attempt, fallback to re-authentication
- **Invalid Token**: Clear session and redirect to login
- **Insufficient Permissions**: Display permission request dialog

#### 2. Authorization Errors
- **Missing Permissions**: Prompt user to grant required permissions
- **Revoked Access**: Notify user and request re-authorization
- **Scope Limitations**: Explain limitations and suggest alternatives

#### 3. API Integration Errors
- **Service Unavailable**: Retry with exponential backoff
- **Rate Limiting**: Queue requests and inform user of delays
- **Invalid Responses**: Log error and provide user-friendly message

#### 4. AI Processing Errors
- **Intent Recognition Failure**: Ask for clarification
- **Ambiguous Requests**: Present options for user selection
- **Processing Timeout**: Provide status updates and cancellation option

### Error Response Format

```json
{
  "error": {
    "code": "PERMISSION_REQUIRED",
    "message": "This action requires Google Calendar access",
    "details": {
      "required_permissions": ["google_calendar_read"],
      "service": "google",
      "action": "create_event"
    },
    "user_action": {
      "type": "grant_permission",
      "url": "/permissions/grant/google",
      "scopes": ["https://www.googleapis.com/auth/calendar"]
    }
  }
}
```

## Testing Strategy

### Unit Testing
- **Backend Services**: pytest with mocking for external APIs
- **Frontend Components**: Jest and React Testing Library
- **Database Operations**: SQLAlchemy test fixtures
- **AI Agent Logic**: Mock Gemini API responses

### Integration Testing
- **Auth0 Integration**: Test OAuth flows with Auth0 test tenant
- **Token Vault Operations**: Verify token storage and retrieval
- **Third-party APIs**: Use sandbox/test environments
- **End-to-end Workflows**: Cypress for complete user journeys

### Security Testing
- **Token Security**: Verify tokens are never exposed in logs
- **Permission Boundaries**: Test unauthorized access attempts
- **Input Validation**: SQL injection and XSS prevention
- **Rate Limiting**: Verify protection against abuse

### Performance Testing
- **API Response Times**: Target <200ms for most operations
- **Database Queries**: Optimize with proper indexing
- **Concurrent Users**: Load testing with realistic scenarios
- **Token Vault Operations**: Measure Auth0 API performance

## Deployment Architecture

### Development Environment
```yaml
# docker-compose.dev.yml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ciphermate_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@postgres:5432/ciphermate_dev
      - REDIS_URL=redis://redis:6379
      - AUTH0_DOMAIN=${AUTH0_DOMAIN}
      - AUTH0_CLIENT_ID=${AUTH0_CLIENT_ID}
      - AUTH0_CLIENT_SECRET=${AUTH0_CLIENT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
```

### Production Environment
- **Frontend**: Vercel deployment with Next.js
- **Backend**: Render or Railway with auto-scaling
- **Database**: Supabase PostgreSQL with connection pooling
- **Caching**: Redis Cloud for session and rate limiting
- **Monitoring**: Sentry for error tracking, Auth0 logs for security events

### Environment Configuration
```bash
# Production environment variables
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_AUDIENCE=https://your-domain.auth0.com/api/v2/
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://user:pass@host:6379
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=your-openai-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
SLACK_CLIENT_ID=your-slack-client-id
SLACK_CLIENT_SECRET=your-slack-client-secret
```

## Security Considerations

### Token Management
- **Storage**: All tokens stored exclusively in Auth0 Token Vault
- **Access**: Tokens retrieved only when needed for specific operations
- **Expiration**: Automatic token refresh with fallback to re-authorization
- **Revocation**: Immediate token deletion from vault on permission revocation

### Data Protection
- **Encryption**: All data encrypted at rest and in transit
- **PII Handling**: Minimal personal data storage with proper anonymization
- **Audit Trails**: Comprehensive logging without sensitive data exposure
- **Compliance**: GDPR-ready with data export and deletion capabilities

### Access Control
- **Authentication**: Multi-factor authentication support via Auth0
- **Authorization**: Granular permission scopes per service
- **Session Management**: Secure session handling with proper timeout
- **Rate Limiting**: Protection against abuse and DoS attacks

### Monitoring and Alerting
- **Security Events**: Real-time monitoring of suspicious activities
- **Performance Metrics**: API response times and error rates
- **Audit Compliance**: Automated compliance reporting
- **Incident Response**: Automated alerts for security violations

## Scalability Design

### Horizontal Scaling
- **Stateless Backend**: All services designed to be stateless
- **Database Sharding**: User-based partitioning for large datasets
- **Caching Strategy**: Redis for session data and frequently accessed information
- **Load Balancing**: Multiple backend instances with health checks

### Performance Optimization
- **Database Indexing**: Optimized queries for user and audit data
- **API Caching**: Intelligent caching of third-party API responses
- **Async Operations**: Non-blocking I/O for all external API calls
- **Connection Pooling**: Efficient database and Redis connections

### Monitoring and Metrics
- **Application Metrics**: Response times, error rates, throughput
- **Business Metrics**: User engagement, permission grants, action success rates
- **Infrastructure Metrics**: CPU, memory, database performance
- **Security Metrics**: Failed authentication attempts, permission violations