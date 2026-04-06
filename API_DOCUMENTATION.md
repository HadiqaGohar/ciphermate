# CipherMate API Documentation

## Overview

CipherMate provides a comprehensive REST API for secure AI agent interactions with third-party services using Auth0 Token Vault. This documentation covers all available endpoints, authentication methods, and integration patterns.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://ciphermate-backend.onrender.com`

## Authentication

All API endpoints require authentication using Auth0 JWT tokens.

### Headers Required

```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Getting an Access Token

```javascript
// Frontend (Next.js with Auth0)
import { useUser } from '@auth0/nextjs-auth0/client';

const { user, error, isLoading } = useUser();
const token = await getAccessTokenSilently();
```

---

## API Endpoints

### 1. Authentication & User Management

#### GET /api/v1/auth/me
Get current user information.

**Response:**
```json
{
  "id": "auth0|64f8a9b2c1d2e3f4g5h6i7j8",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:00:00Z",
  "last_login": "2024-01-22T14:30:00Z",
  "preferences": {
    "timezone": "America/New_York",
    "notifications": true
  }
}
```

#### POST /api/v1/auth/logout
Logout user and invalidate session.

**Response:**
```json
{
  "message": "Successfully logged out",
  "timestamp": "2024-01-22T14:35:00Z"
}
```

---

### 2. Permission Management

#### GET /api/v1/permissions/services
List all available services for integration.

**Response:**
```json
{
  "services": [
    {
      "name": "google",
      "display_name": "Google",
      "description": "Google Calendar, Gmail, and Drive",
      "scopes": [
        {
          "name": "calendar.readonly",
          "description": "Read calendar events",
          "risk_level": "low"
        },
        {
          "name": "calendar.events",
          "description": "Create and modify calendar events",
          "risk_level": "medium"
        }
      ]
    },
    {
      "name": "github",
      "display_name": "GitHub",
      "description": "Repository and issue management",
      "scopes": [
        {
          "name": "repo",
          "description": "Full repository access",
          "risk_level": "high"
        }
      ]
    }
  ]
}
```

#### GET /api/v1/permissions/list
Get user's current permissions.

**Response:**
```json
{
  "permissions": [
    {
      "id": 1,
      "service_name": "google",
      "scopes": ["calendar.readonly", "calendar.events"],
      "granted_at": "2024-01-15T10:00:00Z",
      "expires_at": "2024-02-15T10:00:00Z",
      "last_used_at": "2024-01-22T14:00:00Z",
      "is_active": true,
      "token_vault_id": "tv_abc123def456"
    }
  ]
}
```

#### POST /api/v1/permissions/grant
Initiate OAuth flow to grant permissions.

**Request:**
```json
{
  "service": "google",
  "scopes": ["calendar.readonly", "calendar.events"],
  "redirect_uri": "https://ciphermate.vercel.app/callback"
}
```

**Response:**
```json
{
  "authorization_url": "https://accounts.google.com/oauth/authorize?client_id=...",
  "state": "random_state_string",
  "expires_in": 600
}
```

#### POST /api/v1/permissions/revoke
Revoke permissions for a service.

**Request:**
```json
{
  "service": "google"
}
```

**Response:**
```json
{
  "message": "Permissions revoked successfully",
  "service": "google",
  "revoked_at": "2024-01-22T14:35:00Z",
  "audit_log_id": 12345
}
```

#### GET /api/v1/permissions/scopes/{service}
Get available scopes for a specific service.

**Parameters:**
- `service` (path): Service name (google, github, slack)

**Response:**
```json
{
  "service": "google",
  "scopes": [
    {
      "name": "calendar.readonly",
      "description": "Read calendar events",
      "risk_level": "low",
      "required_for": ["view_calendar", "list_events"]
    },
    {
      "name": "calendar.events",
      "description": "Create and modify calendar events",
      "risk_level": "medium",
      "required_for": ["create_event", "update_event"]
    }
  ]
}
```

---

### 3. Token Vault Operations

#### GET /api/v1/token-vault/list
List all stored tokens (metadata only, no actual tokens).

**Response:**
```json
{
  "tokens": [
    {
      "service": "google",
      "token_vault_id": "tv_abc123def456",
      "scopes": ["calendar.readonly", "calendar.events"],
      "created_at": "2024-01-15T10:00:00Z",
      "expires_at": "2024-02-15T10:00:00Z",
      "last_used_at": "2024-01-22T14:00:00Z",
      "status": "active"
    }
  ]
}
```

#### POST /api/v1/token-vault/store
Store OAuth tokens in Token Vault (internal use).

**Request:**
```json
{
  "service": "google",
  "access_token": "ya29.a0AfH6SMC...",
  "refresh_token": "1//04...",
  "expires_in": 3600,
  "scopes": ["calendar.readonly", "calendar.events"]
}
```

**Response:**
```json
{
  "token_vault_id": "tv_abc123def456",
  "service": "google",
  "stored_at": "2024-01-22T14:35:00Z",
  "expires_at": "2024-01-22T15:35:00Z"
}
```

#### GET /api/v1/token-vault/retrieve/{service}
Retrieve token from Token Vault for API calls (internal use).

**Parameters:**
- `service` (path): Service name

**Response:**
```json
{
  "access_token": "ya29.a0AfH6SMC...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scopes": ["calendar.readonly", "calendar.events"]
}
```

#### DELETE /api/v1/token-vault/revoke/{service}
Remove tokens from Token Vault.

**Parameters:**
- `service` (path): Service name

**Response:**
```json
{
  "message": "Token removed from vault",
  "service": "google",
  "revoked_at": "2024-01-22T14:35:00Z"
}
```

---

### 4. AI Agent Interactions

#### POST /api/v1/chat
Send message to AI agent.

**Request:**
```json
{
  "message": "Schedule a team meeting for tomorrow at 2 PM",
  "context": {
    "timezone": "America/New_York",
    "preferences": {
      "default_duration": 60
    }
  }
}
```

**Response:**
```json
{
  "response": "I'd be happy to schedule that meeting! I need access to your Google Calendar to create events. Would you like to grant me permission?",
  "intent": "schedule_meeting",
  "required_permissions": [
    {
      "service": "google",
      "scopes": ["calendar.events"],
      "reason": "Create calendar events"
    }
  ],
  "suggested_actions": [
    {
      "type": "grant_permission",
      "service": "google",
      "scopes": ["calendar.events"]
    }
  ],
  "conversation_id": "conv_abc123def456"
}
```

#### POST /api/v1/execute-action
Execute an AI agent action.

**Request:**
```json
{
  "action": "create_calendar_event",
  "parameters": {
    "title": "Team Meeting",
    "start_time": "2024-01-23T14:00:00Z",
    "end_time": "2024-01-23T15:00:00Z",
    "attendees": ["colleague@example.com"]
  },
  "conversation_id": "conv_abc123def456"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "event_id": "evt_google_abc123",
    "event_url": "https://calendar.google.com/event?eid=...",
    "created_at": "2024-01-22T14:35:00Z"
  },
  "message": "Team meeting scheduled successfully for January 23rd at 2:00 PM",
  "audit_log_id": 12346
}
```

---

### 5. Third-Party API Integration

#### POST /api/v1/integrations/call
Make authenticated API call to third-party service.

**Request:**
```json
{
  "service": "google",
  "method": "GET",
  "endpoint": "/calendar/v3/calendars/primary/events",
  "params": {
    "timeMin": "2024-01-22T00:00:00Z",
    "timeMax": "2024-01-23T00:00:00Z"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "evt_abc123",
        "summary": "Team Meeting",
        "start": {
          "dateTime": "2024-01-23T14:00:00Z"
        },
        "end": {
          "dateTime": "2024-01-23T15:00:00Z"
        }
      }
    ]
  },
  "rate_limit": {
    "remaining": 99,
    "reset_time": "2024-01-22T15:00:00Z"
  }
}
```

#### GET /api/v1/integrations/health
Check integration service health.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "google": {
      "status": "operational",
      "last_check": "2024-01-22T14:35:00Z",
      "response_time": "245ms"
    },
    "github": {
      "status": "operational",
      "last_check": "2024-01-22T14:35:00Z",
      "response_time": "180ms"
    },
    "slack": {
      "status": "degraded",
      "last_check": "2024-01-22T14:35:00Z",
      "response_time": "1200ms",
      "message": "Elevated response times"
    }
  }
}
```

#### GET /api/v1/integrations/rate-limits/{service}
Get rate limit status for a service.

**Parameters:**
- `service` (path): Service name

**Response:**
```json
{
  "service": "github",
  "rate_limit": {
    "limit": 5000,
    "remaining": 4987,
    "reset_time": "2024-01-22T15:00:00Z",
    "used": 13
  },
  "status": "healthy"
}
```

---

### 6. Service-Specific Endpoints

#### Google Calendar

##### GET /api/v1/integrations/google-calendar/calendars
List user's calendars.

**Response:**
```json
{
  "calendars": [
    {
      "id": "primary",
      "summary": "John Doe",
      "primary": true,
      "access_role": "owner"
    },
    {
      "id": "work@company.com",
      "summary": "Work Calendar",
      "primary": false,
      "access_role": "writer"
    }
  ]
}
```

##### GET /api/v1/integrations/google-calendar/events
List calendar events.

**Query Parameters:**
- `calendar_id` (optional): Calendar ID (default: primary)
- `time_min` (optional): Start time filter
- `time_max` (optional): End time filter
- `max_results` (optional): Maximum number of events (default: 10)

**Response:**
```json
{
  "events": [
    {
      "id": "evt_abc123",
      "summary": "Team Meeting",
      "description": "Weekly team sync",
      "start": {
        "dateTime": "2024-01-23T14:00:00Z",
        "timeZone": "America/New_York"
      },
      "end": {
        "dateTime": "2024-01-23T15:00:00Z",
        "timeZone": "America/New_York"
      },
      "attendees": [
        {
          "email": "colleague@example.com",
          "responseStatus": "accepted"
        }
      ]
    }
  ]
}
```

##### POST /api/v1/integrations/google-calendar/events
Create calendar event.

**Request:**
```json
{
  "calendar_id": "primary",
  "summary": "Project Kickoff",
  "description": "Q1 project planning session",
  "start": {
    "dateTime": "2024-01-25T10:00:00Z",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2024-01-25T11:00:00Z",
    "timeZone": "America/New_York"
  },
  "attendees": [
    {"email": "team@company.com"}
  ]
}
```

**Response:**
```json
{
  "id": "evt_def456",
  "summary": "Project Kickoff",
  "htmlLink": "https://calendar.google.com/event?eid=...",
  "created": "2024-01-22T14:35:00Z",
  "status": "confirmed"
}
```

#### GitHub

##### GET /api/v1/integrations/github/user
Get GitHub user information.

**Response:**
```json
{
  "login": "johndoe",
  "id": 12345,
  "name": "John Doe",
  "email": "john@example.com",
  "public_repos": 25,
  "followers": 100,
  "following": 50
}
```

##### GET /api/v1/integrations/github/repositories
List user repositories.

**Query Parameters:**
- `type` (optional): Repository type (all, owner, member)
- `sort` (optional): Sort order (created, updated, pushed, full_name)
- `per_page` (optional): Results per page (default: 30)

**Response:**
```json
{
  "repositories": [
    {
      "id": 123456,
      "name": "my-project",
      "full_name": "johndoe/my-project",
      "description": "A sample project",
      "private": false,
      "html_url": "https://github.com/johndoe/my-project",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-22T14:00:00Z",
      "language": "Python",
      "stargazers_count": 15
    }
  ]
}
```

##### POST /api/v1/integrations/github/repositories
Create new repository.

**Request:**
```json
{
  "name": "new-project",
  "description": "A new project repository",
  "private": false,
  "auto_init": true,
  "gitignore_template": "Python"
}
```

**Response:**
```json
{
  "id": 789012,
  "name": "new-project",
  "full_name": "johndoe/new-project",
  "html_url": "https://github.com/johndoe/new-project",
  "clone_url": "https://github.com/johndoe/new-project.git",
  "created_at": "2024-01-22T14:35:00Z"
}
```

#### Slack

##### GET /api/v1/integrations/slack/user
Get Slack user information.

**Response:**
```json
{
  "id": "U1234567890",
  "name": "johndoe",
  "real_name": "John Doe",
  "email": "john@company.com",
  "team_id": "T1234567890",
  "is_admin": false,
  "is_owner": false
}
```

##### GET /api/v1/integrations/slack/channels
List Slack channels.

**Query Parameters:**
- `types` (optional): Channel types (public_channel, private_channel, mpim, im)
- `limit` (optional): Maximum number of channels (default: 100)

**Response:**
```json
{
  "channels": [
    {
      "id": "C1234567890",
      "name": "general",
      "is_channel": true,
      "is_private": false,
      "is_member": true,
      "topic": {
        "value": "Company-wide announcements",
        "creator": "U1234567890",
        "last_set": 1642857600
      },
      "num_members": 25
    }
  ]
}
```

##### POST /api/v1/integrations/slack/messages
Send Slack message.

**Request:**
```json
{
  "channel": "C1234567890",
  "text": "Hello team! The Q1 project kickoff is scheduled for Thursday at 10 AM.",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Q1 Project Update*\nKickoff meeting scheduled for Thursday at 10 AM"
      }
    }
  ]
}
```

**Response:**
```json
{
  "ok": true,
  "channel": "C1234567890",
  "ts": "1642857600.123456",
  "message": {
    "text": "Hello team! The Q1 project kickoff is scheduled for Thursday at 10 AM.",
    "user": "U1234567890",
    "ts": "1642857600.123456"
  }
}
```

---

### 7. Audit and Logging

#### GET /api/v1/audit/logs
Get audit logs.

**Query Parameters:**
- `start_date` (optional): Start date filter (ISO 8601)
- `end_date` (optional): End date filter (ISO 8601)
- `action_type` (optional): Filter by action type
- `service` (optional): Filter by service
- `limit` (optional): Maximum number of logs (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "logs": [
    {
      "id": 12346,
      "user_id": "auth0|64f8a9b2c1d2e3f4g5h6i7j8",
      "action_type": "calendar_event_created",
      "service_name": "google",
      "details": {
        "event_id": "evt_abc123",
        "event_title": "Team Meeting",
        "calendar_id": "primary"
      },
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "timestamp": "2024-01-22T14:35:00Z",
      "session_id": "sess_abc123def456"
    }
  ],
  "total": 150,
  "has_more": true
}
```

#### GET /api/v1/audit/summary
Get audit summary statistics.

**Query Parameters:**
- `period` (optional): Time period (day, week, month) (default: week)

**Response:**
```json
{
  "period": "week",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": "2024-01-22T00:00:00Z",
  "summary": {
    "total_actions": 45,
    "services_used": 3,
    "permissions_granted": 2,
    "permissions_revoked": 1,
    "api_calls": 38,
    "errors": 2
  },
  "by_service": {
    "google": {
      "actions": 25,
      "api_calls": 22,
      "errors": 1
    },
    "github": {
      "actions": 15,
      "api_calls": 12,
      "errors": 0
    },
    "slack": {
      "actions": 5,
      "api_calls": 4,
      "errors": 1
    }
  }
}
```

#### POST /api/v1/audit/export
Export audit data.

**Request:**
```json
{
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-22T23:59:59Z",
  "format": "json",
  "include": [
    "user_actions",
    "ai_actions",
    "permission_changes",
    "api_calls"
  ]
}
```

**Response:**
```json
{
  "export_id": "exp_abc123def456",
  "status": "processing",
  "estimated_completion": "2024-01-22T14:40:00Z",
  "download_url": null
}
```

#### GET /api/v1/audit/security-events
Get security events.

**Query Parameters:**
- `severity` (optional): Filter by severity (low, medium, high, critical)
- `resolved` (optional): Filter by resolution status (true, false)
- `limit` (optional): Maximum number of events (default: 20)

**Response:**
```json
{
  "events": [
    {
      "id": 1001,
      "event_type": "unusual_api_activity",
      "severity": "medium",
      "details": {
        "service": "github",
        "api_calls": 150,
        "time_window": "1 hour",
        "threshold": 100
      },
      "timestamp": "2024-01-22T13:00:00Z",
      "resolved": false,
      "resolution_notes": null
    }
  ]
}
```

#### POST /api/v1/audit/security-events/{id}/resolve
Resolve security event.

**Parameters:**
- `id` (path): Security event ID

**Request:**
```json
{
  "resolution_notes": "Confirmed legitimate bulk repository operations"
}
```

**Response:**
```json
{
  "id": 1001,
  "resolved": true,
  "resolved_at": "2024-01-22T14:35:00Z",
  "resolved_by": "auth0|64f8a9b2c1d2e3f4g5h6i7j8",
  "resolution_notes": "Confirmed legitimate bulk repository operations"
}
```

---

## Error Handling

### Error Response Format

All API errors follow a consistent format:

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
    },
    "timestamp": "2024-01-22T14:35:00Z",
    "request_id": "req_abc123def456"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing authentication token |
| `FORBIDDEN` | 403 | Insufficient permissions for the requested action |
| `PERMISSION_REQUIRED` | 403 | Specific service permissions needed |
| `TOKEN_EXPIRED` | 401 | Access token has expired |
| `TOKEN_REFRESH_FAILED` | 401 | Unable to refresh expired token |
| `RATE_LIMIT_EXCEEDED` | 429 | API rate limit exceeded |
| `SERVICE_UNAVAILABLE` | 503 | External service is unavailable |
| `INVALID_REQUEST` | 400 | Request validation failed |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `INTERNAL_ERROR` | 500 | Internal server error |

### Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Authentication endpoints**: 10 requests per minute
- **Permission management**: 20 requests per minute
- **AI chat**: 30 requests per minute
- **Third-party integrations**: 100 requests per minute
- **Audit logs**: 50 requests per minute

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642857600
```

---

## SDK Examples

### Python SDK

```python
import requests
from typing import Dict, Any

class CipherMateClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def chat(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send message to AI agent"""
        response = requests.post(
            f'{self.base_url}/api/v1/chat',
            json={'message': message, 'context': context or {}},
            headers=self.headers
        )
        return response.json()
    
    def grant_permission(self, service: str, scopes: list) -> Dict[str, Any]:
        """Grant permissions for a service"""
        response = requests.post(
            f'{self.base_url}/api/v1/permissions/grant',
            json={'service': service, 'scopes': scopes},
            headers=self.headers
        )
        return response.json()
    
    def get_audit_logs(self, limit: int = 50) -> Dict[str, Any]:
        """Get audit logs"""
        response = requests.get(
            f'{self.base_url}/api/v1/audit/logs',
            params={'limit': limit},
            headers=self.headers
        )
        return response.json()

# Usage
client = CipherMateClient('https://api.ciphermate.com', 'your_token_here')
response = client.chat('Schedule a meeting for tomorrow')
print(response['response'])
```

### JavaScript SDK

```javascript
class CipherMateClient {
  constructor(baseUrl, accessToken) {
    this.baseUrl = baseUrl;
    this.headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    };
  }

  async chat(message, context = {}) {
    const response = await fetch(`${this.baseUrl}/api/v1/chat`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ message, context })
    });
    return response.json();
  }

  async grantPermission(service, scopes) {
    const response = await fetch(`${this.baseUrl}/api/v1/permissions/grant`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ service, scopes })
    });
    return response.json();
  }

  async getAuditLogs(limit = 50) {
    const response = await fetch(`${this.baseUrl}/api/v1/audit/logs?limit=${limit}`, {
      headers: this.headers
    });
    return response.json();
  }
}

// Usage
const client = new CipherMateClient('https://api.ciphermate.com', 'your_token_here');
const response = await client.chat('Schedule a meeting for tomorrow');
console.log(response.response);
```

---

## Webhooks (Future Feature)

### Webhook Events

CipherMate will support webhooks for real-time notifications:

- `permission.granted` - User grants new permissions
- `permission.revoked` - User revokes permissions
- `token.expired` - Token expiration warning
- `security.event` - Security event detected
- `audit.export.complete` - Audit export ready

### Webhook Payload Example

```json
{
  "event": "permission.granted",
  "timestamp": "2024-01-22T14:35:00Z",
  "user_id": "auth0|64f8a9b2c1d2e3f4g5h6i7j8",
  "data": {
    "service": "google",
    "scopes": ["calendar.readonly", "calendar.events"],
    "granted_at": "2024-01-22T14:35:00Z"
  }
}
```

---

## Testing

### Test Environment

- **Base URL**: `https://api-test.ciphermate.com`
- **Test Auth0 Domain**: `ciphermate-test.auth0.com`
- **Rate Limits**: Relaxed for testing

### Test Data

Test users and scenarios are available for integration testing:

```json
{
  "test_user": {
    "email": "test@ciphermate.com",
    "password": "TestPassword123!",
    "auth0_id": "auth0|test_user_id"
  },
  "test_tokens": {
    "google": "test_google_token",
    "github": "test_github_token",
    "slack": "test_slack_token"
  }
}
```

---

## Support

### Documentation
- **API Reference**: https://docs.ciphermate.com/api
- **Integration Guide**: https://docs.ciphermate.com/integration
- **SDK Documentation**: https://docs.ciphermate.com/sdks

### Support Channels
- **GitHub Issues**: https://github.com/ciphermate/api/issues
- **Discord**: https://discord.gg/ciphermate
- **Email**: support@ciphermate.com

---

*This API documentation demonstrates CipherMate's comprehensive integration capabilities, showcasing secure AI agent interactions powered by Auth0 Token Vault.*