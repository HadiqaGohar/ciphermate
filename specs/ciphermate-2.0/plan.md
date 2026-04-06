# CipherMate 2.0 — Architecture Plan

**Version:** 2.0  
**Created:** 2026-03-31  
**Status:** Draft  
**Related:** [spec.md](spec.md)

---

## 1. Architecture Overview

### 1.1 System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CipherMate 2.0 Platform                          │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   Frontend   │───▶│   Backend    │───▶│  Auth0 Token │               │
│  │  (Next.js)   │◀───│   (FastAPI)  │◀───│    Vault     │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                                             │
│         │                   │                                             │
│         ▼                   ▼                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   Productivity│   │   AI Agent   │    │   External   │               │
│  │   Dashboard  │◀───│  (Gemini)    │───▶│   Services   │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                                     │                          │
│         │                                     ▼                          │
│         │                          ┌─────────────────────┐              │
│         │                          │  Google Calendar    │              │
│         │                          │  Gmail              │              │
│         │                          │  GitHub             │              │
│         │                          │  ToDo (Mock)        │              │
│         │                          └─────────────────────┘              │
│         │                                                                │
│         ▼                                                                │
│  ┌──────────────┐                                                        │
│  │  Audit Logs  │                                                        │
│  │  (PostgreSQL)│                                                        │
│  └──────────────┘                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Frontend** | Next.js 14 + TypeScript | SSR, type safety, hackathon-ready |
| **UI Framework** | Tailwind CSS + Headless UI | Rapid development, responsive |
| **Backend** | FastAPI (Python 3.11+) | Async support, auto docs, fast |
| **Database** | PostgreSQL | Relational, scalable, free tier |
| **Cache** | Redis | Session management, rate limiting |
| **Auth** | Auth0 Token Vault | Hackathon requirement, secure |
| **AI** | Google Gemini | Free tier, good for demos |
| **Deployment** | Docker + Render/Railway | Quick deploy, free tier |

---

## 2. Architectural Decisions

### ADR-001: Token Vault Integration Pattern

**Decision:** Use Auth0 Token Vault with encrypted local caching

**Options Considered:**
1. **Direct Token Vault calls** (chosen)
   - ✅ Most secure, tokens never stored locally
   - ✅ Hackathon requirement
   - ❌ Slight latency on each call
2. **Local token storage**
   - ❌ Violates hackathon spirit
   - ❌ Security risk
3. **Hybrid (encrypted cache)**
   - ✅ Best of both worlds
   - ✅ Performance + security

**Rationale:** Auth0 Token Vault is the hackathon requirement. We add encrypted caching (Fernet) for performance while maintaining security.

**Implementation:**
```python
class TokenVaultService:
    async def get_token(self, user_id: str, service: str) -> str:
        # 1. Check encrypted cache (5-min buffer)
        # 2. Fetch from Auth0 if missing/expiring
        # 3. Cache with encryption
        # 4. Return token
```

---

### ADR-002: Permission Management Architecture

**Decision:** Time-limited permissions with automatic expiry

**Options Considered:**
1. **Manual revocation only**
   - ❌ User must remember to revoke
   - ❌ Security risk
2. **Time-limited (chosen)**
   - ✅ Auto-expiry reduces risk
   - ✅ Demo-friendly (visual countdown)
   - ⚠️ Requires background job
3. **Session-based**
   - ⚠️ Tied to browser session
   - ❌ Doesn't work for AI agents

**Rationale:** Time-limited permissions provide better security and are more demo-friendly. Users can see countdown and understand security model.

**Implementation:**
```python
class PermissionTemplate(Base):
    expires_at = Column(DateTime)  # Auto-expiry
    is_active = Column(Boolean)    # Manual toggle

# Background job checks every minute
async def cleanup_expired_permissions():
    await db.execute(
        "UPDATE permissions SET is_active = false WHERE expires_at < NOW()"
    )
```

---

### ADR-003: AI Agent Integration Pattern

**Decision:** AI as orchestrator, backend as executor

**Options Considered:**
1. **AI makes direct API calls**
   - ❌ Tokens exposed to AI
   - ❌ No audit control
2. **AI returns intent, backend executes** (chosen)
   - ✅ Tokens stay secure
   - ✅ Full audit trail
   - ✅ Permission checks
3. **Hybrid (AI with scoped tokens)**
   - ⚠️ Complex token management
   - ❌ Over-engineered for hackathon

**Rationale:** Separation of concerns. AI analyzes intent, backend executes with proper security checks.

**Flow:**
```
User → "Schedule meeting" 
  → AI parses intent → {action: "create_event", time: "2pm", title: "Meeting"}
  → Backend checks permission → Executes API call → Logs to audit
  → Returns result to user
```

---

### ADR-004: Audit Logging Strategy

**Decision:** 100% coverage with structured logging (structlog)

**Options Considered:**
1. **Minimal logging**
   - ❌ Insufficient for hackathon
2. **Comprehensive logging** (chosen)
   - ✅ Every auth event logged
   - ✅ Structured format (JSON)
   - ✅ Real-time feed
   - ⚠️ Storage overhead
3. **Sampling**
   - ❌ Might miss critical events

**Rationale:** Hackathon judging criteria requires complete transparency. 100% audit coverage is mandatory.

**Implementation:**
```python
@router.post("/calendar/events")
async def create_event(...):
    async with PerformanceTracker(...):  # Auto-logs
        result = await api_integration_service.make_api_call(...)
    
    await audit_service.log_action(
        user_id=user.id,
        action_type="calendar_event_created",
        details={"event_id": result.id}
    )
```

---

### ADR-005: Frontend State Management

**Decision:** React hooks + polling for real-time updates

**Options Considered:**
1. **Redux/Zustand**
   - ⚠️ Overkill for hackathon
   - ⚠️ Learning curve
2. **React Query**
   - ✅ Good caching
   - ⚠️ Additional dependency
3. **Simple hooks + polling** (chosen)
   - ✅ No new dependencies
   - ✅ Easy to implement
   - ✅ Works for demo

**Rationale:** Keep it simple. Polling every 30 seconds is sufficient for hackathon demo. Can upgrade to WebSockets later.

---

## 3. Component Architecture

### 3.1 Backend Components

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── auth.py           # Auth0 integration
│   │   ├── permissions.py    # Grant/revoke endpoints
│   │   ├── integrations.py   # Calendar, Gmail, GitHub, ToDo
│   │   ├── audit.py          # Audit log endpoints
│   │   └── ai_agent.py       # AI interaction endpoints
│   │
│   ├── core/
│   │   ├── auth.py           # JWT validation
│   │   ├── token_vault.py    # Auth0 Token Vault service
│   │   ├── oauth_handlers.py # OAuth flow handling
│   │   ├── api_integration.py # External API calls
│   │   ├── audit_service.py  # Audit logging
│   │   ├── permission_service.py # Permission checks
│   │   └── ai_agent.py       # Gemini integration
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── service_connection.py
│   │   ├── audit_log.py
│   │   └── permission_template.py
│   │
│   └── db/
│       ├── database.py       # DB connection
│       └── session.py        # Session management
```

### 3.2 Frontend Components

```
frontend/src/
├── app/
│   ├── dashboard/
│   │   ├── page.tsx          # Main dashboard
│   │   └── components/
│   │       ├── ServiceCard.tsx
│   │       ├── PermissionToggle.tsx
│   │       └── MetricsPanel.tsx
│   │
│   ├── chat/
│   │   ├── page.tsx          # AI chat interface
│   │   └── components/
│   │       ├── ChatMessage.tsx
│   │       └── ChatInput.tsx
│   │
│   ├── audit/
│   │   ├── page.tsx          # Audit log viewer
│   │   └── components/
│   │       ├── AuditFeed.tsx
│   │       └── AuditFilter.tsx
│   │
│   └── permissions/
│       └── page.tsx          # Permission management
│
├── components/
│   └── ui/                   # Reusable UI components
│
└── hooks/
    ├── usePermissions.ts
    ├── useAuditLogs.ts
    └── useProductivityMetrics.ts
```

---

## 4. Data Architecture

### 4.1 Database Schema

```sql
-- Users (from Auth0)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

-- Service Connections (OAuth tokens in Token Vault)
CREATE TABLE service_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    scopes JSONB,
    token_vault_id VARCHAR(255),  -- Reference to Auth0 vault
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    UNIQUE(user_id, service_name)
);

-- Audit Logs
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type VARCHAR(100) NOT NULL,
    service_name VARCHAR(50),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(20),
    details JSONB,
    ip_address INET,
    user_agent TEXT
);

-- Permission Templates
CREATE TABLE permission_templates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service_name VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent Actions
CREATE TABLE agent_actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type VARCHAR(100),
    intent JSONB,
    result JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.2 Redis Cache Structure

```
# Session cache
session:{session_id} → {user_id, expires_at}

# Permission cache
permission:{user_id}:{service} → {is_active, expires_at}

# Token cache (encrypted)
token:{user_id}:{service} → {encrypted_token, expires_at}

# Rate limiting
ratelimit:{user_id}:{endpoint} → count
```

---

## 5. API Design

### 5.1 Core Endpoints

#### Authentication
```
POST   /api/v1/auth/login          # Auth0 login
POST   /api/v1/auth/logout         # Logout
GET    /api/v1/auth/me             # Get current user
```

#### Permissions
```
GET    /api/v1/permissions/services              # List supported services
POST   /api/v1/permissions/grant                 # Initiate grant flow
GET    /api/v1/permissions/callback              # OAuth callback
GET    /api/v1/permissions/status                # Get permission status
PUT    /api/v1/permissions/{service}/toggle      # Toggle permission
DELETE /api/v1/permissions/{service}             # Revoke permission
```

#### Integrations
```
# Calendar
POST   /api/v1/integrations/calendar/events      # Create event
GET    /api/v1/integrations/calendar/events      # List events
PUT    /api/v1/integrations/calendar/events/{id} # Update event

# ToDo
POST   /api/v1/integrations/todo/tasks           # Create task
GET    /api/v1/integrations/todo/tasks           # List tasks
PUT    /api/v1/integrations/todo/tasks/{id}      # Update task
DELETE /api/v1/integrations/todo/tasks/{id}      # Delete task

# Gmail (Stretch)
POST   /api/v1/integrations/gmail/send           # Send email
POST   /api/v1/integrations/gmail/draft          # Draft email

# GitHub (Stretch)
POST   /api/v1/integrations/github/issues        # Create issue
```

#### AI Agent
```
POST   /api/v1/ai/chat                 # Chat with AI
POST   /api/v1/ai/recommendations      # Get AI recommendations
POST   /api/v1/ai/suggest-priority     # Task prioritization
```

#### Audit
```
GET    /api/v1/audit/logs              # Get audit logs
GET    /api/v1/audit/stats             # Get audit statistics
```

---

## 6. Security Architecture

### 6.1 Authentication Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────┐
│  User   │     │Frontend │     │Backend  │     │Auth0 Token  │
│         │     │         │     │         │     │   Vault     │
└────┬────┘     └────┬────┘     └────┬────┘     └──────┬──────┘
     │               │               │                  │
     │ 1. Login      │               │                  │
     │──────────────▶│               │                  │
     │               │ 2. Auth       │                  │
     │               │──────────────▶│                  │
     │               │               │ 3. Token Request │
     │               │               │─────────────────▶│
     │               │               │ 4. Access Token  │
     │               │               │◀─────────────────│
     │               │ 5. Session    │                  │
     │               │◀──────────────│                  │
     │ 6. Redirect   │               │                  │
     │◀──────────────│               │                  │
     │               │               │                  │
     │ 7. AI Action  │               │                  │
     │──────────────▶│               │                  │
     │               │ 8. Check Perm │                  │
     │               │──────────────▶│                  │
     │               │               │ 9. Get Token     │
     │               │               │─────────────────▶│
     │               │               │ 10. Token        │
     │               │               │◀─────────────────│
     │               │               │ 11. API Call     │
     │               │               │─────────────────▶│
     │               │               │                  │
     │               │ 12. Result    │                  │
     │◀──────────────│               │                  │
```

### 6.2 Permission Model

```
Permission = {
    user_id: "auth0|user123",
    service: "google_calendar",
    scopes: ["calendar:read", "calendar:write"],
    is_active: true,
    expires_at: "2026-03-31T12:00:00Z",
    created_at: "2026-03-31T11:50:00Z"
}

# Scope format: credential:<service>:<permission>
# Example: credential:google_calendar:write
```

---

## 7. Performance Budget

| Metric | Target | Strategy |
|--------|--------|----------|
| API p95 latency | < 500ms | Caching, connection pooling |
| Permission check | < 100ms | Redis cache |
| Audit log write | < 50ms | Async writes |
| Dashboard load | < 2s | Code splitting, lazy loading |
| Token refresh | < 5 min buffer | Background refresh |

---

## 8. Deployment Architecture

### 8.1 Development

```
┌─────────────┐     ┌─────────────┐
│  Frontend   │     │   Backend   │
│  localhost  │────▶│  localhost  │
│  :3000      │◀────│  :8000      │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   PostgreSQL│
                    │   Redis     │
                    │   (Docker)  │
                    └─────────────┘
```

### 8.2 Production

```
┌─────────────┐     ┌─────────────┐
│  Frontend   │     │   Backend   │
│   Vercel    │────▶│   Render    │
│             │◀────│   (FastAPI) │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Supabase  │
                    │  (PostgreSQL│
                    │    + Redis) │
                    └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  Auth0      │
                    │  Token Vault│
                    └─────────────┘
```

---

## 9. Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Auth0 Token Vault downtime | High | Mock service for demo, retry logic |
| OAuth flow failures | High | Test with multiple accounts, backup credentials |
| Database connection issues | Medium | Connection pooling, retry logic |
| Frontend build failures | Medium | Test build early, minimal dependencies |
| Demo technical issues | High | Recorded video backup, screenshots |

---

## 10. Testing Strategy

### 10.1 Backend Testing
- **Unit tests**: Core services (token vault, permissions, audit)
- **Integration tests**: API endpoints with mock Auth0
- **E2E tests**: Full OAuth flow, AI actions

### 10.2 Frontend Testing
- **Component tests**: ServiceCard, PermissionToggle, ChatMessage
- **Integration tests**: Dashboard flow, permission grant
- **E2E tests**: 3-minute demo flow

### 10.3 Security Testing
- **Token exposure**: Verify no tokens in logs/frontend
- **Permission bypass**: Test unauthorized access attempts
- **Audit coverage**: Verify 100% logging

---

## 11. Monitoring & Observability

### 11.1 Metrics to Track
- API call latency (p50, p95, p99)
- Error rates by endpoint
- Token cache hit rate
- Permission expiry count
- Audit log volume

### 11.2 Health Checks
```python
# /api/v1/health
{
    "status": "healthy",
    "checks": {
        "database": {"status": "healthy", "latency_ms": 12},
        "redis": {"status": "healthy", "latency_ms": 3},
        "auth0": {"status": "healthy", "latency_ms": 45},
        "token_vault": {"status": "healthy", "latency_ms": 67}
    }
}
```

---

## 12. Future Considerations

### Post-Hackathon Improvements
1. **WebSocket for real-time updates** (replace polling)
2. **React Query for state management** (better caching)
3. **PostgreSQL full-text search** (audit log search)
4. **Rate limiting per user** (prevent abuse)
5. **Multi-region deployment** (global latency)

---

**Next Steps:**
1. Review and approve architecture
2. Create implementation tasks (tasks.md)
3. Begin Priority 1 implementation
