# CipherMate 2.0 — Implementation Tasks

**Version:** 2.0  
**Created:** 2026-03-31  
**Status:** Draft  
**Related:** [spec.md](spec.md), [plan.md](plan.md)  
**Sprint Duration:** 7 days (MVP)  
**Hackathon Deadline:** April 7, 2026

---

## Task Breakdown by Priority

### Priority Legend
- **P0**: Critical for hackathon (must have)
- **P1**: Important for demo (should have)
- **P2**: Stretch goals (nice to have)
- **P3**: Future enhancements (defer)

---

## Sprint 1: Core Infrastructure (Days 1-2)

### T-001: Verify Auth0 Token Vault Setup
**Priority:** P0  
**Estimate:** 2 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Verify Auth0 Token Vault is properly configured and accessible.

**Tasks:**
- [ ] Confirm Auth0 tenant has Token Vault enabled
- [ ] Verify Management API credentials work
- [ ] Test token retrieval with existing demo script
- [ ] Document any configuration issues

**Acceptance Criteria:**
- [ ] Can retrieve Management API token
- [ ] Token Vault endpoint accessible
- [ ] No authentication errors

**Test Cases:**
```bash
# Run existing demo script
cd backend
python demo_token_vault.py

# Expected: Success message with token details
```

**Dependencies:** None  
**Files:** `backend/app/core/token_vault.py`, `backend/.env`

---

### T-002: Verify Database Schema
**Priority:** P0  
**Estimate:** 3 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Ensure all required database tables exist and are properly indexed.

**Tasks:**
- [ ] Check existing models (User, ServiceConnection, AuditLog, etc.)
- [ ] Add missing columns if needed (expires_at, is_active)
- [ ] Create database migration script
- [ ] Test database connection

**Acceptance Criteria:**
- [ ] All tables created successfully
- [ ] Indexes on user_id, service_name, timestamp
- [ ] Migration script runs without errors

**Test Cases:**
```bash
# Run database setup
cd backend
python setup_database.py

# Verify tables
psql -h localhost -U postgres -d ciphermate -c "\dt"
```

**Dependencies:** T-001  
**Files:** `backend/app/models/`, `backend/setup_database.py`

---

### T-003: Verify Backend API Endpoints
**Priority:** P0  
**Estimate:** 4 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Test existing API endpoints for permissions, integrations, and audit.

**Tasks:**
- [ ] Start backend server
- [ ] Test `/api/v1/permissions/services` endpoint
- [ ] Test `/api/v1/integrations/*` endpoints
- [ ] Test `/api/v1/audit/logs` endpoint
- [ ] Document any broken endpoints

**Acceptance Criteria:**
- [ ] All endpoints return 200 OK (or 401 for auth-required)
- [ ] Swagger docs accessible at `/docs`
- [ ] No console errors on startup

**Test Cases:**
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test Swagger UI
open http://localhost:8000/docs
```

**Dependencies:** T-001, T-002  
**Files:** `backend/app/api/v1/`, `backend/main.py`

---

### T-004: Verify Frontend Build
**Priority:** P0  
**Estimate:** 3 hours  
**Assignee:** Frontend  
**Status:** ⬜ Not Started

**Description:**
Ensure frontend builds and runs without errors.

**Tasks:**
- [ ] Install dependencies
- [ ] Run development server
- [ ] Test existing pages (dashboard, chat, audit)
- [ ] Fix any build errors

**Acceptance Criteria:**
- [ ] `npm install` completes successfully
- [ ] `npm run dev` starts without errors
- [ ] Pages load at http://localhost:3000
- [ ] No TypeScript errors

**Test Cases:**
```bash
cd frontend
npm install
npm run dev

# Visit http://localhost:3000
# Visit http://localhost:3000/dashboard
# Visit http://localhost:3000/audit
```

**Dependencies:** None  
**Files:** `frontend/package.json`, `frontend/src/`

---

### T-005: Create ToDo Service Mock
**Priority:** P0  
**Estimate:** 4 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Create mock ToDo service for hackathon demo (no external API needed).

**Tasks:**
- [ ] Create `ToDoService` class in `backend/app/core/service_clients.py`
- [ ] Implement CRUD operations (create, read, update, delete)
- [ ] Store tasks in PostgreSQL database
- [ ] Add permission checks
- [ ] Add audit logging

**Acceptance Criteria:**
- [ ] Can create tasks via API
- [ ] Can list user's tasks
- [ ] Can update task status (complete/pending)
- [ ] Can delete tasks
- [ ] All operations logged to audit

**Test Cases:**
```python
# Test ToDo service
POST /api/v1/integrations/todo/tasks
{
    "title": "Complete project report",
    "priority": "high",
    "due_date": "2026-04-07"
}

GET /api/v1/integrations/todo/tasks
# Returns: [{id: 1, title: "...", status: "pending", ...}]

PUT /api/v1/integrations/todo/tasks/1
{
    "status": "completed"
}
```

**Dependencies:** T-002, T-003  
**Files:** 
- `backend/app/core/service_clients.py` (new)
- `backend/app/api/v1/integrations.py` (modify)
- `backend/app/models/todo_task.py` (new)

**Code Template:**
```python
# backend/app/core/service_clients.py
class ToDoService:
    def __init__(self, user_id: str, db: AsyncSession):
        self.user_id = user_id
        self.db = db
    
    async def create_task(self, title: str, priority: str, due_date: datetime):
        # Create task in database
        pass
    
    async def get_tasks(self, status: Optional[str] = None):
        # List tasks with optional filter
        pass
    
    async def complete_task(self, task_id: int):
        # Mark task as complete
        pass
```

---

## Sprint 2: Permission Management (Days 3-4)

### T-006: Implement Time-Limited Permissions
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Add automatic permission expiry with configurable duration.

**Tasks:**
- [ ] Add `expires_at` column to `service_connections` table
- [ ] Update permission grant to set expiry (10 minutes default)
- [ ] Create background job to check expired permissions
- [ ] Add endpoint to refresh expired permission
- [ ] Add permission countdown to API response

**Acceptance Criteria:**
- [ ] Permissions expire after configured duration
- [ ] Expired permissions cannot be used
- [ ] Background job runs every minute
- [ ] Users can refresh before expiry

**Test Cases:**
```python
# Grant permission with 1-minute expiry
POST /api/v1/permissions/grant
{
    "service": "google_calendar",
    "expires_in": 60  # seconds
}

# Wait 61 seconds, then try to use
POST /api/v1/integrations/calendar/events
# Expected: 403 Permission expired
```

**Dependencies:** T-003, T-005  
**Files:** 
- `backend/app/models/service_connection.py` (modify)
- `backend/app/api/v1/permissions.py` (modify)
- `backend/app/core/permission_service.py` (modify)

---

### T-007: Create Permission Toggle UI
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** Frontend  
**Status:** ⬜ Not Started

**Description:**
Build service cards with permission toggle switches.

**Tasks:**
- [ ] Create `ServiceCard` component
- [ ] Add toggle switch (ON/OFF)
- [ ] Show permission status (active/expired/revoked)
- [ ] Add countdown timer for expiring permissions
- [ ] Connect to backend toggle API

**Acceptance Criteria:**
- [ ] Card shows service name, icon, status
- [ ] Toggle switch changes color (green/red)
- [ ] Countdown timer updates every second
- [ ] Toggle API call on switch change
- [ ] Error handling for failed toggles

**Test Cases:**
```typescript
// Component test
<ServiceCard 
  service="google_calendar"
  status="active"
  expiresAt={new Date('2026-04-07T12:00:00Z')}
  onToggle={(enabled) => handleToggle(enabled)}
/>

// Expected: Card renders with green toggle
// Click toggle → API call → Card renders with red toggle
```

**Dependencies:** T-004  
**Files:** 
- `frontend/src/app/dashboard/page.tsx` (modify)
- `frontend/src/components/ServiceCard.tsx` (new)
- `frontend/src/hooks/usePermissions.ts` (new)

---

### T-008: Implement Instant Permission Revocation
**Priority:** P0  
**Estimate:** 4 hours  
**Assignee:** Backend  
**Status:** ⬜ Not Started

**Description:**
Ensure permission revocation takes effect immediately.

**Tasks:**
- [ ] Add `is_active` flag to service connections
- [ ] Update permission check to verify `is_active`
- [ ] Clear permission cache on revocation
- [ ] Add revocation audit log
- [ ] Test immediate effect

**Acceptance Criteria:**
- [ ] Toggle OFF → permission unusable within 1 second
- [ ] Cache cleared immediately
- [ ] Audit log shows revocation event
- [ ] AI cannot access revoked services

**Test Cases:**
```python
# Grant permission
PUT /api/v1/permissions/google_calendar/toggle
{
    "enabled": true
}

# Use permission (should work)
POST /api/v1/integrations/calendar/events
# Expected: 200 OK

# Revoke permission
PUT /api/v1/permissions/google_calendar/toggle
{
    "enabled": false
}

# Use permission (should fail)
POST /api/v1/integrations/calendar/events
# Expected: 403 Permission revoked
```

**Dependencies:** T-006  
**Files:** `backend/app/core/permission_service.py`, `backend/app/api/v1/permissions.py`

---

## Sprint 3: AI Integration (Days 5-6)

### T-009: Implement AI Calendar Scheduling
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** Backend + AI  
**Status:** ⬜ Not Started

**Description:**
Enable AI to schedule calendar events via natural language.

**Tasks:**
- [ ] Update AI agent to parse calendar intents
- [ ] Add permission check before calendar access
- [ ] Call Google Calendar API via integration service
- [ ] Return confirmation to user
- [ ] Log action to audit

**Acceptance Criteria:**
- [ ] User types "Schedule meeting tomorrow at 2pm"
- [ ] AI extracts intent (title, time, attendees)
- [ ] AI checks permission
- [ ] Calendar event created
- [ ] User receives confirmation with event details

**Test Cases:**
```python
# Chat with AI
POST /api/v1/ai/chat
{
    "message": "Schedule a team meeting for tomorrow at 2 PM"
}

# Expected response:
{
    "message": "I've scheduled 'Team Meeting' for tomorrow at 2:00 PM. Event ID: evt_123",
    "action": "calendar_event_created",
    "details": {"event_id": "evt_123", "time": "2026-04-06T14:00:00Z"}
}
```

**Dependencies:** T-003, T-006, T-008  
**Files:** 
- `backend/app/core/ai_agent.py` (modify)
- `backend/app/api/v1/ai_agent.py` (modify)
- `backend/app/api/v1/integrations.py` (modify)

---

### T-010: Implement AI ToDo Management
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** Backend + AI  
**Status:** ⬜ Not Started

**Description:**
Enable AI to manage ToDo tasks via natural language.

**Tasks:**
- [ ] Update AI agent to parse ToDo intents
- [ ] Add permission check before ToDo access
- [ ] Call ToDo service via integration
- [ ] Return confirmation to user
- [ ] Log action to audit

**Acceptance Criteria:**
- [ ] User types "Add task: Complete project report"
- [ ] AI extracts intent (title, priority, due date)
- [ ] AI checks permission
- [ ] Task created in database
- [ ] User receives confirmation

**Test Cases:**
```python
# Chat with AI
POST /api/v1/ai/chat
{
    "message": "Add a task to finish the presentation by Friday"
}

# Expected response:
{
    "message": "I've added 'Finish the presentation' to your tasks with due date Friday.",
    "action": "todo_task_created",
    "details": {"task_id": 1, "title": "Finish the presentation", "due_date": "2026-04-10"}
}
```

**Dependencies:** T-005, T-006  
**Files:** `backend/app/core/ai_agent.py`, `backend/app/core/service_clients.py`

---

### T-011: Implement AI Recommendations
**Priority:** P1  
**Estimate:** 6 hours  
**Assignee:** Backend + AI  
**Status:** ⬜ Not Started

**Description:**
AI analyzes tasks and suggests prioritization.

**Tasks:**
- [ ] Create recommendation endpoint
- [ ] Fetch user's pending tasks
- [ ] AI analyzes deadlines, priorities
- [ ] Generate top 3-5 recommendations
- [ ] Return structured recommendations

**Acceptance Criteria:**
- [ ] GET `/api/v1/ai/recommendations` returns suggestions
- [ ] Recommendations include rationale
- [ ] User can accept/decline via API
- [ ] Accepted recommendations update task priorities

**Test Cases:**
```python
# Get recommendations
GET /api/v1/ai/recommendations

# Expected response:
{
    "recommendations": [
        {
            "type": "task_prioritization",
            "priority": 1,
            "task_id": 5,
            "title": "Complete project report",
            "reason": "Due tomorrow (high urgency)",
            "suggested_priority": "high"
        },
        ...
    ]
}

# Accept recommendation
POST /api/v1/ai/recommendations/accept
{
    "recommendation_id": 1
}
```

**Dependencies:** T-010  
**Files:** 
- `backend/app/api/v1/ai_agent.py` (modify)
- `backend/app/core/ai_agent.py` (modify)

---

### T-012: Create AI Chat UI
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** Frontend  
**Status:** ⬜ Not Started

**Description:**
Build chat interface for AI interactions.

**Tasks:**
- [ ] Create chat page layout
- [ ] Add message list component
- [ ] Add chat input component
- [ ] Connect to AI chat API
- [ ] Show loading states
- [ ] Display AI action confirmations

**Acceptance Criteria:**
- [ ] User can type and send messages
- [ ] AI responses appear in chat
- [ ] Loading indicator during AI processing
- [ ] Action confirmations shown (e.g., "Event created")
- [ ] Error messages for failed requests

**Test Cases:**
```typescript
// User types message
<ChatInput onSend={(message) => handleSend(message)} />

// AI response appears
<ChatMessage 
  role="assistant"
  content="I've scheduled your meeting for 2 PM."
  action="calendar_event_created"
/>
```

**Dependencies:** T-004, T-009, T-010  
**Files:** 
- `frontend/src/app/chat/page.tsx` (modify)
- `frontend/src/components/ChatMessage.tsx` (new)
- `frontend/src/components/ChatInput.tsx` (new)

---

## Sprint 4: Dashboard & Audit (Day 7)

### T-013: Create Productivity Metrics Dashboard
**Priority:** P1  
**Estimate:** 6 hours  
**Assignee:** Frontend  
**Status:** ⬜ Not Started

**Description:**
Build dashboard showing productivity metrics.

**Tasks:**
- [ ] Create metrics API endpoint
- [ ] Calculate tasks completed, time saved, security score
- [ ] Build metrics panel components
- [ ] Add charts (simple bar/line)
- [ ] Auto-refresh every 30 seconds

**Acceptance Criteria:**
- [ ] Dashboard shows 4+ metrics
- [ ] Metrics update in real-time
- [ ] Visual charts render correctly
- [ ] Security score calculation visible

**Test Cases:**
```python
# Get metrics
GET /api/v1/dashboard/metrics

# Expected response:
{
    "tasks_completed": 12,
    "time_saved_minutes": 45,
    "security_score": 95,
    "ai_actions_success_rate": 98.5,
    "period": "last_7_days"
}
```

**Dependencies:** T-003, T-005  
**Files:** 
- `frontend/src/app/dashboard/page.tsx` (modify)
- `frontend/src/components/MetricsPanel.tsx` (new)
- `backend/app/api/v1/dashboard.py` (new)

---

### T-014: Implement Real-Time Audit Feed
**Priority:** P0  
**Estimate:** 5 hours  
**Assignee:** Frontend + Backend  
**Status:** ⬜ Not Started

**Description:**
Build real-time audit log viewer.

**Tasks:**
- [ ] Add pagination to audit logs API
- [ ] Create audit feed component
- [ ] Implement auto-refresh (5 seconds)
- [ ] Add filters (service, action type)
- [ ] Add search functionality

**Acceptance Criteria:**
- [ ] Audit logs load on page visit
- [ ] New logs appear automatically
- [ ] Can filter by service
- [ ] Can search by keyword
- [ ] Export to CSV works

**Test Cases:**
```python
# Get audit logs with filters
GET /api/v1/audit/logs?service=google_calendar&limit=50

# Expected response:
{
    "logs": [
        {
            "id": 1,
            "action_type": "calendar_event_created",
            "timestamp": "2026-03-31T14:30:00Z",
            "status": "success",
            "details": {...}
        },
        ...
    ],
    "total": 150
}
```

**Dependencies:** T-003  
**Files:** 
- `frontend/src/app/audit/page.tsx` (modify)
- `frontend/src/components/AuditFeed.tsx` (new)
- `backend/app/api/v1/audit.py` (modify)

---

## Sprint 5: Demo Preparation (Days 8-9)

### T-015: Create Demo Script
**Priority:** P0  
**Estimate:** 3 hours  
**Assignee:** All  
**Status:** ⬜ Not Started

**Description:**
Write and rehearse 3-minute demo script.

**Tasks:**
- [ ] Write detailed demo script with timing
- [ ] Assign roles (presenter, tech support)
- [ ] Rehearse demo flow 3+ times
- [ ] Record backup video
- [ ] Prepare screenshots

**Acceptance Criteria:**
- [ ] Demo fits in 3 minutes
- [ ] All key features shown
- [ ] Backup video ready
- [ ] Screenshots for each segment

**Deliverables:**
- Demo script document
- Backup video (MP4)
- Screenshot folder (PNG)

**Dependencies:** T-009, T-010, T-012, T-014  
**Files:** `specs/ciphermate-2.0/demo-script.md`

---

### T-016: Record Demo Video
**Priority:** P0  
**Estimate:** 4 hours  
**Assignee:** All  
**Status:** ⬜ Not Started

**Description:**
Record 3-minute demo video as backup.

**Tasks:**
- [ ] Set up screen recording software
- [ ] Record full demo flow
- [ ] Edit video (trim, add captions)
- [ ] Upload to YouTube (unlisted)
- [ ] Test video plays correctly

**Acceptance Criteria:**
- [ ] Video length: 2:30-3:00
- [ ] All key features visible
- [ ] Clear audio narration
- [ ] YouTube link works
- [ ] Download backup available

**Dependencies:** T-015  
**Tools:** OBS Studio, YouTube

---

### T-017: Final Testing & Bug Fixes
**Priority:** P0  
**Estimate:** 6 hours  
**Assignee:** All  
**Status:** ⬜ Not Started

**Description:**
Comprehensive testing and bug fixes.

**Tasks:**
- [ ] Test full demo flow end-to-end
- [ ] Fix critical bugs
- [ ] Test on different browsers
- [ ] Verify Auth0 login works
- [ ] Test permission grant/revoke
- [ ] Test AI actions
- [ ] Verify audit logs

**Acceptance Criteria:**
- [ ] No critical bugs
- [ ] Demo flow works 3/3 times
- [ ] All P0 tasks complete
- [ ] Performance acceptable

**Dependencies:** All previous tasks  
**Files:** All

---

## Stretch Goals (If Time Permits)

### T-018: Gmail Integration
**Priority:** P2  
**Estimate:** 6 hours  
**Description:** Add Gmail API integration for drafting/sending emails.

### T-019: GitHub Integration
**Priority:** P2  
**Estimate:** 6 hours  
**Description:** Add GitHub API integration for creating issues.

### T-020: Meeting Conflict Detection
**Priority:** P2  
**Estimate:** 4 hours  
**Description:** AI detects calendar conflicts and suggests resolutions.

---

## Testing Checklist

### Backend Tests
- [ ] Token Vault integration tests
- [ ] Permission service tests
- [ ] API endpoint tests
- [ ] Audit logging tests
- [ ] AI agent integration tests

### Frontend Tests
- [ ] ServiceCard component tests
- [ ] PermissionToggle tests
- [ ] Chat interface tests
- [ ] Audit feed tests
- [ ] Dashboard metrics tests

### Integration Tests
- [ ] Full OAuth flow
- [ ] Permission grant → AI action → audit
- [ ] Permission revoke → immediate effect
- [ ] Time-limited permission expiry

---

## Definition of Done

A task is considered **Done** when:
1. ✅ Code implemented and committed
2. ✅ Tests written and passing
3. ✅ Acceptance criteria met
4. ✅ No linting errors
5. ✅ Documented in code comments
6. ✅ Tested manually (if applicable)

---

## Progress Tracking

| Sprint | Tasks | Complete | In Progress | Not Started |
|--------|-------|----------|-------------|-------------|
| Sprint 1 | T-001 to T-005 | 0 | 0 | 5 |
| Sprint 2 | T-006 to T-008 | 0 | 0 | 3 |
| Sprint 3 | T-009 to T-012 | 0 | 0 | 4 |
| Sprint 4 | T-013 to T-014 | 0 | 0 | 2 |
| Sprint 5 | T-015 to T-017 | 0 | 0 | 3 |
| **Total** | **17 tasks** | **0** | **0** | **17** |

---

**Next Steps:**
1. Review and approve tasks
2. Assign tasks to team members
3. Begin Sprint 1 (T-001 to T-005)
4. Update progress daily
