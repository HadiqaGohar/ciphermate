Read Hackathon.md for guide
Read openai-agents-sdk.md for agents
Read auth0-guide.md for auth

┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                       │
│  - User dashboard                                            │
│  - Permission management UI                                  │
│  - Agent interaction interface                               │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTPS
┌─────────────────▼───────────────────────────────────────────┐
│              Auth0 for AI Agents (Token Vault)              │
│  - OAuth flows                                              │
│  - Token management                                         │
│  - Consent delegation                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Backend (FastAPI + Python)                     │
│  - Agent orchestration                                      │
│  - Token vault integration                                  │
│  - API proxying with tokens                                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                 PostgreSQL (Supabase)                       │
│  - User permissions                                         │
│  - Audit logs                                               │
│  - Session data                                             │
└─────────────────────────────────────────────────────────────┘