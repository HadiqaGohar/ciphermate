# CipherMate 2.0 — AI Agent Manager + Productivity Hub

## 🎯 Feature Specification

**Version:** 2.0  
**Created:** 2026-03-31  
**Status:** Draft  
**Hackathon:** Authorized to Act: Auth0 for AI Agents  
**Deadline:** April 7, 2026

---

## 1. Executive Summary

### 1.1 Product Vision
CipherMate 2.0 transforms from a basic AI assistant into a **secure AI productivity hub** that enables AI agents to perform real actions across multiple applications (Google Calendar, Gmail, GitHub, ToDo) with **granular user-controlled permissions** and **complete audit transparency**.

### 1.2 Core Innovation
Not just a chatbot → AI becomes your personal assistant for multiple apps with:
- **Granular permissions** → AI can act only where allowed, only for specific time
- **Actionable intelligence** → AI suggests tasks, schedules meetings, manages emails, tracks GitHub issues
- **Live permission dashboard** → Grant/revoke AI permissions with one click
- **Trust metrics** → Security score, tasks completed, time saved

### 1.3 Hackathon Alignment
This specification directly addresses all judging criteria:
- ✅ **Security Model**: Token Vault + granular permissions + time-limited access
- ✅ **User Control**: Live dashboard, instant grant/revoke, audit logs
- ✅ **Technical Execution**: Multi-app integration with production-aware security
- ✅ **Design**: Gamified productivity dashboard with trust metrics
- ✅ **Potential Impact**: Enterprise-ready AI agent marketplace foundation

---

## 2. Scope and Boundaries

### 2.1 In Scope (Priority 1 - MVP)
| Feature | Description | Priority |
|---------|-------------|----------|
| **Auth0 Token Vault Integration** | Secure credential storage with encrypted caching | P0 (Required) |
| **Google Calendar Integration** | Schedule/reschedule meetings via AI | P0 |
| **ToDo List Management** | Add/prioritize/complete tasks via AI | P0 |
| **Live Permission Dashboard** | Grant/revoke permissions with one click | P0 |
| **Time-Limited Permissions** | Auto-expiring access (5-10 min for demo) | P0 |
| **Audit Logs (Real-time)** | Every action logged and visible | P0 |
| **AI Recommendations** | Task prioritization, meeting conflict detection | P1 |
| **Productivity Metrics Dashboard** | Tasks completed, time saved, security score | P1 |

### 2.2 In Scope (Priority 2 - Stretch Goals)
| Feature | Description | Priority |
|---------|-------------|----------|
| **Gmail Integration** | Draft/send emails via AI | P2 |
| **GitHub Integration** | Create/assign issues via AI | P2 |
| **Slack Integration** | Send messages via AI | P3 |
| **AI Marketplace UI** | Pick AI agents for specific tasks | P3 |

### 2.3 Out of Scope
- Mobile applications (future vision)
- Team collaboration features (enterprise roadmap)
- Custom integrations beyond listed services
- Advanced analytics dashboard (basic metrics only)

---

## 3. Functional Requirements

### 3.1 Multi-App AI Integration

#### FR-1: Google Calendar Integration
**Description:** AI can schedule, reschedule, and manage calendar events with user permission.

**Acceptance Criteria:**
- [ ] User can grant AI permission to access Google Calendar via OAuth
- [ ] AI can create calendar events with title, description, attendees
- [ ] AI can reschedule existing events (with permission)
- [ ] Permission toggle instantly enables/disables AI access
- [ ] All calendar actions logged in audit trail
- [ ] Time-limited permission expires automatically

**API Endpoints:**
- `POST /api/v1/integrations/calendar/events` - Create event
- `PUT /api/v1/integrations/calendar/events/{id}` - Update event
- `GET /api/v1/integrations/calendar/events` - List upcoming events

#### FR-2: ToDo List Management
**Description:** AI can add, prioritize, and manage tasks in user's ToDo list.

**Acceptance Criteria:**
- [ ] User can grant AI permission to manage ToDo list
- [ ] AI can add new tasks with priority levels
- [ ] AI can mark tasks as complete
- [ ] AI can suggest task prioritization
- [ ] Permission toggle instantly enables/disables AI access
- [ ] All ToDo actions logged in audit trail

**API Endpoints:**
- `POST /api/v1/integrations/todo/tasks` - Create task
- `PUT /api/v1/integrations/todo/tasks/{id}` - Update task
- `DELETE /api/v1/integrations/todo/tasks/{id}` - Delete task
- `GET /api/v1/integrations/todo/tasks` - List tasks

#### FR-3: Gmail Integration (Stretch)
**Description:** AI can draft and send emails with user permission.

**Acceptance Criteria:**
- [ ] User can grant AI permission to access Gmail
- [ ] AI can draft emails (shown in modal for review)
- [ ] AI can send emails (with explicit permission)
- [ ] Permission toggle instantly enables/disables AI access
- [ ] All email actions logged in audit trail

#### FR-4: GitHub Integration (Stretch)
**Description:** AI can create and manage GitHub issues.

**Acceptance Criteria:**
- [ ] User can grant AI permission to access GitHub
- [ ] AI can create issues in specified repositories
- [ ] AI can assign issues to users
- [ ] Permission toggle instantly enables/disables AI access
- [ ] All GitHub actions logged in audit trail

---

### 3.2 Permission Management

#### FR-5: Live Permission Dashboard
**Description:** Real-time UI to grant/revoke AI permissions for each service.

**Acceptance Criteria:**
- [ ] Dashboard shows all integrated services as cards
- [ ] Each card has permission toggle switch (ON/OFF)
- [ ] Toggle changes take effect immediately (< 1 second)
- [ ] Visual indicator shows permission status (green/red)
- [ ] Expired permissions clearly marked
- [ ] Last used timestamp displayed

**UI Components:**
- ServiceCard (per service)
- PermissionToggle (switch component)
- StatusIndicator (color-coded)
- LastUsedLabel (timestamp)

#### FR-6: Time-Limited Permissions
**Description:** Permissions automatically expire after configured duration.

**Acceptance Criteria:**
- [ ] Default expiration: 10 minutes (configurable)
- [ ] Expiration countdown visible in UI
- [ ] Auto-revocation at expiry
- [ ] Refresh option available before expiry
- [ ] Expired permissions logged in audit trail

**Technical Requirements:**
- Background job checks expired permissions every minute
- Redis cache stores permission expiry timestamps
- Frontend polls for status updates every 30 seconds

#### FR-7: Audit Logs
**Description:** Complete transparency of all AI actions.

**Acceptance Criteria:**
- [ ] Real-time audit log feed (auto-refresh every 5 seconds)
- [ ] Each log entry shows: timestamp, action, service, status
- [ ] Filterable by service, action type, date range
- [ ] Searchable by keyword
- [ ] Export to CSV/JSON
- [ ] 100% coverage: every auth event logged

**Log Entry Schema:**
```json
{
  "id": "uuid",
  "user_id": "auth0|user123",
  "action_type": "calendar_event_created",
  "service_name": "google_calendar",
  "timestamp": "2026-03-31T10:30:00Z",
  "status": "success",
  "details": {
    "event_id": "evt_123",
    "summary": "Team Meeting",
    "attendees": ["user@example.com"]
  },
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

---

### 3.3 AI Recommendations & Insights

#### FR-8: Task Prioritization Suggestions
**Description:** AI analyzes pending tasks and suggests prioritization.

**Acceptance Criteria:**
- [ ] AI analyzes task deadlines, priorities, dependencies
- [ ] Generates top 3-5 prioritized recommendations
- [ ] User can accept/decline suggestions
- [ ] Accepted suggestions auto-update task priorities
- [ ] Recommendation rationale displayed

**Example Output:**
```
"You have 5 pending tasks. Suggested prioritization:
1. Complete project report (due tomorrow) - HIGH
2. Review pull request #42 (blocking teammate) - HIGH
3. Schedule team meeting (flexible timing) - MEDIUM
..."
```

#### FR-9: Meeting Conflict Detection
**Description:** AI detects scheduling conflicts and suggests resolutions.

**Acceptance Criteria:**
- [ ] Scans calendar for overlapping events
- [ ] Detects back-to-back meetings without breaks
- [ ] Suggests rescheduling options
- [ ] User can accept/decline suggestions
- [ ] Accepted suggestions trigger calendar API updates

**Example Output:**
```
"Tomorrow's meetings overlap:
- 2:00 PM Team Standup (30 min)
- 2:15 PM Client Call (1 hour)

Suggested: Reschedule Client Call to 3:00 PM?
[Accept] [Decline] [View Alternatives]
```

#### FR-10: Email Draft Suggestions
**Description:** AI drafts replies to urgent emails.

**Acceptance Criteria:**
- [ ] Identifies urgent emails (from boss, marked important)
- [ ] Generates draft reply based on email content
- [ ] Shows draft in modal for review
- [ ] User can edit before sending
- [ ] Send action logged in audit trail

---

### 3.4 Gamified Productivity Dashboard

#### FR-11: Productivity Metrics
**Description:** Dashboard shows AI-driven productivity gains.

**Metrics to Display:**
- Tasks completed via AI (count, trend)
- Time saved via AI (estimated hours)
- Security compliance score (0-100%)
- AI actions success rate (%)
- Permissions granted/revoked (count)

**UI Requirements:**
- Real-time updates (poll every 30 seconds)
- Visual charts (bar, line, pie)
- Comparison with previous period (week/month)
- Exportable reports

#### FR-12: Security Score
**Description:** Gamified security compliance metric.

**Score Calculation:**
```
Security Score = (
  permissions_properly_scoped * 0.3 +
  time_limited_permissions_used * 0.3 +
  audit_log_coverage * 0.2 +
  no_hardcoded_secrets * 0.2
) * 100
```

**Acceptance Criteria:**
- [ ] Score updates in real-time
- [ ] Breakdown by category visible
- [ ] Recommendations to improve score
- [ ] Historical trend graph

---

## 4. Non-Functional Requirements

### 4.1 Performance
| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | < 500ms | Backend monitoring |
| Permission Toggle Latency | < 1 second | Frontend to backend |
| Audit Log Refresh Rate | < 5 seconds | Polling interval |
| Dashboard Load Time | < 2 seconds | Page load |
| Token Refresh Buffer | 5 minutes before expiry | Auth0 integration |

### 4.2 Security
- **Zero hardcoded secrets**: Enforced by pre-commit hooks + CI/CD
- **100% auth event logging**: All authentication events logged
- **Token encryption at rest**: Fernet encryption for cached tokens
- **Short-lived tokens**: Maximum 1 hour lifetime
- **Scope-based access**: `credential:<name>:<permission>` format
- **Secure failure mode**: System fails safely on Token Vault unavailability

### 4.3 Reliability
- **SLO**: 99.5% uptime during hackathon demo period
- **Error budget**: 0.5% failed requests allowed
- **Degradation strategy**: Graceful fallback if Token Vault unavailable
- **Retry logic**: Exponential backoff with max 3 retries

### 4.4 Observability
- **Structured logging**: `structlog` for all security events
- **Metrics**: Cache hit rate, API call latency, error rates
- **Health checks**: Database, Redis, Auth0, external APIs
- **Alerting**: Critical errors logged for immediate attention

---

## 5. User Stories

### US-1: Grant Calendar Permission
**As a** user  
**I want to** grant AI permission to access my Google Calendar  
**So that** AI can schedule meetings on my behalf  

**Acceptance Criteria:**
1. Click "Grant Access" on Calendar service card
2. Redirected to Auth0 OAuth consent screen
3. Approve requested scopes
4. Redirected back to dashboard
5. Calendar card shows "Active" status with green indicator
6. Audit log shows permission grant event

### US-2: AI Schedules Meeting
**As a** user  
**I want to** ask AI to schedule a team meeting  
**So that** I don't have to manually create calendar events  

**Acceptance Criteria:**
1. Type "Schedule a team meeting for tomorrow at 2 PM"
2. AI confirms details and requests permission
3. User approves
4. Calendar event created
5. Audit log shows event creation
6. User receives confirmation with event details

### US-3: Revoke Permission
**As a** user  
**I want to** revoke AI's calendar access  
**So that** AI can no longer access my calendar  

**Acceptance Criteria:**
1. Toggle Calendar permission switch to OFF
2. Immediate visual feedback (red indicator)
3. AI cannot access calendar API
4. Audit log shows permission revocation
5. Previously scheduled events remain (no deletion)

### US-4: View Audit Logs
**As a** user  
**I want to** see all AI actions in real-time  
**So that** I have complete transparency  

**Acceptance Criteria:**
1. Navigate to Audit Logs page
2. See real-time feed of all actions
3. Filter by service (Calendar, ToDo, etc.)
4. Search by keyword
5. Export logs to CSV

### US-5: Receive AI Recommendation
**As a** user  
**I want to** get task prioritization suggestions  
**So that** I can focus on important tasks first  

**Acceptance Criteria:**
1. AI analyzes pending tasks
2. Dashboard shows recommendation card
3. User reviews suggested priorities
4. User accepts recommendation
5. Task priorities updated
6. Action logged in audit trail

---

## 6. Demo Flow (3 Minutes)

### 6.1 Demo Script

| Time | Segment | Action | Visual |
|------|---------|--------|--------|
| 0:00-0:20 | **Intro** | Problem: AI needs access but trust is low | Title slide |
| 0:20-0:50 | **Login & Permissions** | Auth0 login + grant Calendar access | Login screen → Dashboard |
| 0:50-1:30 | **AI Multi-App Actions** | Schedule meeting, add ToDo task | Chat interface → Calendar/ToDo updates |
| 1:30-2:00 | **AI Recommendations** | Accept/decline task prioritization | Recommendation card |
| 2:00-2:20 | **Revoke Access** | Toggle permissions OFF | Dashboard toggle → Red indicator |
| 2:20-2:40 | **Security & Audit** | Show audit logs updating | Audit log feed |
| 2:40-3:00 | **Closing & Vision** | Enterprise roadmap | Vision slide |

### 6.2 Backup Plan
- **Recorded demo video** for each segment
- **Screenshots** of all key flows
- **Fallback script** if live demo fails

---

## 7. Acceptance Criteria Summary

### MVP (Must Have for Hackathon)
- [x] Auth0 Token Vault integration working
- [ ] 2+ AI actions (Calendar + ToDo) functional
- [ ] Permission grant/revoke (live demo)
- [ ] Audit logs (real-time updates)
- [ ] 3-minute demo flow rehearsed
- [ ] Video recording ready

### Stretch Goals (If Time Permits)
- [ ] AI recommendations/suggestions
- [ ] Productivity dashboard (basic metrics)
- [ ] GitHub integration
- [ ] Email drafting
- [ ] Gamification elements

---

## 8. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Token Vault integration fails | High | Low | Use mock service for demo, fix later |
| OAuth flow issues | High | Medium | Test multiple times, have backup credentials |
| Demo technical issues | High | Medium | Record video backup, screenshots ready |
| Scope creep | Medium | High | Stick to MVP, defer stretch goals |
| Time constraints | High | High | Prioritize ruthlessly, 80/20 rule |

---

## 9. Future Vision (Post-Hackathon)

### Phase 2: Enterprise Features
- Multi-user support with team permissions
- Slack, Office 365, Trello integrations
- Advanced analytics dashboard
- Custom AI agent marketplace

### Phase 3: Platform Expansion
- Mobile applications (iOS/Android)
- API for third-party AI agents
- White-label solution for enterprises
- AI agent certification program

---

## 10. References

- [Hackathon Rules](../../Hackathon.md)
- [Auth0 Token Vault Docs](https://auth0.com/docs/ai-agents/token-vault)
- [IDEA.md](../../IDEA.md)
- [API_DOCUMENTATION.md](../../API_DOCUMENTATION.md)

---

**Next Steps:**
1. Review and approve this spec
2. Create architecture plan (`plan.md`)
3. Create implementation tasks (`tasks.md`)
4. Begin Priority 1 implementation
