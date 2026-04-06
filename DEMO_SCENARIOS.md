# CipherMate Demo Scenarios

## Overview

This document provides comprehensive demonstration scenarios showcasing CipherMate's Token Vault functionality and secure AI agent interactions. Each scenario demonstrates different aspects of the platform's security model, user control, and third-party integrations.

## Scenario 1: First-Time User Onboarding

### Context
Sarah is a project manager who wants to use CipherMate to help manage her team's schedule and communications across Google Calendar, Slack, and GitHub.

### Demo Flow

#### Step 1: Authentication
1. **User Action**: Sarah visits https://ciphermate.vercel.app
2. **System Response**: Redirects to Auth0 Universal Login
3. **User Action**: Sarah logs in with her Google account
4. **System Response**: Creates secure session and redirects to dashboard
5. **Key Point**: No third-party tokens stored yet - clean slate

#### Step 2: Service Connection Request
1. **User Action**: Sarah asks the AI: "Schedule a team standup for tomorrow at 10 AM"
2. **AI Response**: "I'd love to help you schedule that meeting! However, I need access to your Google Calendar to create events. Would you like to grant me permission?"
3. **System Response**: Shows permission request dialog with specific scopes:
   - ✅ Read calendar events
   - ✅ Create calendar events
   - ❌ Delete calendar events (not requested)
   - ❌ Access other Google services

#### Step 3: OAuth Flow with Token Vault
1. **User Action**: Sarah clicks "Grant Permission"
2. **System Response**: Initiates Google OAuth flow
3. **Google Response**: Shows consent screen with requested scopes
4. **User Action**: Sarah approves the permissions
5. **System Response**: 
   - Receives OAuth tokens from Google
   - **Immediately stores tokens in Auth0 Token Vault** (not locally)
   - Records permission grant in audit log
   - Shows success message: "Google Calendar connected securely!"

#### Step 4: AI Action Execution
1. **AI Action**: Retrieves token from Token Vault (never exposed to AI)
2. **API Call**: Creates calendar event using Google Calendar API
3. **System Response**: 
   - Logs the action in audit trail
   - Shows success: "Team standup scheduled for tomorrow at 10 AM"
   - Provides calendar link and meeting details

### Key Demonstrations
- **Token Security**: Tokens never stored locally or exposed to AI
- **Granular Permissions**: User sees exactly what access is granted
- **Audit Trail**: Every action is logged with timestamp and details
- **User Control**: Clear consent flow with specific scope requests

---

## Scenario 2: Permission Management and Revocation

### Context
After using CipherMate for a week, Sarah wants to review and modify her granted permissions.

### Demo Flow

#### Step 1: Permission Dashboard
1. **User Action**: Sarah navigates to "Permissions" page
2. **System Response**: Shows comprehensive permission overview:

```
Connected Services:
┌─────────────────┬──────────────────┬─────────────────┬──────────────┐
│ Service         │ Scopes Granted   │ Connected       │ Last Used    │
├─────────────────┼──────────────────┼─────────────────┼──────────────┤
│ Google Calendar │ • Read events    │ Jan 15, 2024    │ 2 hours ago  │
│                 │ • Create events  │                 │              │
├─────────────────┼──────────────────┼─────────────────┼──────────────┤
│ Slack           │ • Send messages  │ Jan 16, 2024    │ 1 day ago    │
│                 │ • Read channels  │                 │              │
├─────────────────┼──────────────────┼─────────────────┼──────────────┤
│ GitHub          │ Not Connected    │ -               │ -            │
└─────────────────┴──────────────────┴─────────────────┴──────────────┘
```

#### Step 2: Scope Visualization
1. **User Action**: Sarah clicks "View Details" on Google Calendar
2. **System Response**: Shows detailed scope breakdown:
   - **Granted Scopes**:
     - `https://www.googleapis.com/auth/calendar.events` ✅
     - `https://www.googleapis.com/auth/calendar.readonly` ✅
   - **Available but Not Granted**:
     - `https://www.googleapis.com/auth/calendar` (Full access) ❌
     - `https://www.googleapis.com/auth/calendar.settings.readonly` ❌
   - **Risk Assessment**: Medium (Can read and create events)
   - **Token Status**: Active, expires in 45 days

#### Step 3: Permission Revocation
1. **User Action**: Sarah decides to revoke Slack access and clicks "Revoke Access"
2. **System Response**: Shows confirmation dialog:
   ```
   ⚠️ Revoke Slack Access?
   
   This will:
   • Remove all Slack tokens from Token Vault
   • Disable AI access to your Slack workspace
   • Log this action in your audit trail
   
   The AI will need to request permission again to access Slack.
   
   [Cancel] [Revoke Access]
   ```
3. **User Action**: Sarah confirms revocation
4. **System Response**:
   - Immediately removes tokens from Auth0 Token Vault
   - Updates database to mark connection as inactive
   - Logs revocation action with timestamp
   - Shows success message: "Slack access revoked successfully"

#### Step 4: Verification
1. **User Action**: Sarah asks AI: "Send a message to the team channel"
2. **AI Response**: "I no longer have access to your Slack workspace. Would you like to reconnect Slack to send messages?"
3. **Key Point**: AI immediately recognizes missing permissions and requests re-authorization

### Key Demonstrations
- **Transparency**: Complete visibility into granted permissions
- **Granular Control**: Scope-level permission management
- **Immediate Effect**: Revocation takes effect instantly
- **Audit Trail**: All permission changes are logged

---

## Scenario 3: Step-Up Authentication for High-Risk Actions

### Context
Sarah wants the AI to help her delete old calendar events and manage her GitHub repository, which requires elevated permissions.

### Demo Flow

#### Step 1: High-Risk Action Detection
1. **User Action**: Sarah asks: "Delete all my calendar events from last month"
2. **AI Analysis**: Recognizes this as a high-risk action (bulk deletion)
3. **System Response**: 
   ```
   🔒 High-Risk Action Detected
   
   You're requesting to delete multiple calendar events. This action:
   • Cannot be undone
   • Affects 23 calendar events
   • Requires elevated permissions
   
   For your security, I need additional confirmation.
   ```

#### Step 2: Step-Up Authentication Flow
1. **System Response**: Initiates step-up authentication
2. **Auth0 Response**: Sends push notification to Sarah's phone
3. **User Action**: Sarah approves the action on her mobile device
4. **System Response**: 
   - Verifies step-up authentication
   - Requests additional Google Calendar permissions:
     - ✅ Delete calendar events (new scope)
     - ⏰ Time-limited: 1 hour only

#### Step 3: Temporary Elevated Access
1. **User Action**: Sarah grants the temporary elevated permission
2. **System Response**:
   - Stores elevated token in Token Vault with 1-hour expiration
   - Shows clear indication of elevated access:
   ```
   🔓 Elevated Access Active
   • Delete permissions granted
   • Expires in: 59 minutes
   • Auto-revoke: Enabled
   ```

#### Step 4: Action Execution with Audit
1. **AI Action**: Deletes specified calendar events
2. **System Response**: 
   - Logs each deletion individually in audit trail
   - Shows progress: "Deleted 23 events from December 2023"
   - Automatically revokes elevated permissions after completion
   - Confirms: "Elevated access automatically revoked"

### Key Demonstrations
- **Risk Assessment**: AI identifies high-risk actions
- **Step-Up Auth**: Additional verification for sensitive operations
- **Time-Limited Access**: Elevated permissions with automatic expiration
- **Detailed Auditing**: Granular logging of high-risk actions

---

## Scenario 4: Multi-Service Workflow with Permission Boundaries

### Context
Sarah wants to create a comprehensive project workflow that involves GitHub, Slack, and Google Calendar.

### Demo Flow

#### Step 1: Complex Multi-Service Request
1. **User Action**: Sarah asks: "Create a new GitHub repository for our Q1 project, schedule a kickoff meeting for next Monday, and notify the team in Slack"
2. **AI Analysis**: Identifies three separate service requirements:
   - GitHub: Create repository
   - Google Calendar: Create event (already has permission)
   - Slack: Send message (needs re-authorization)

#### Step 2: Permission Status Check
1. **System Response**: Shows permission matrix:
   ```
   Action Breakdown:
   ┌─────────────────────┬─────────────┬────────────────┐
   │ Action              │ Service     │ Status         │
   ├─────────────────────┼─────────────┼────────────────┤
   │ Create repository   │ GitHub      │ ❌ Need access │
   │ Schedule meeting    │ G Calendar  │ ✅ Authorized  │
   │ Send Slack message  │ Slack       │ ❌ Need access │
   └─────────────────────┴─────────────┴────────────────┘
   
   I can schedule the meeting now, but need permission for GitHub and Slack.
   ```

#### Step 3: Sequential Permission Requests
1. **GitHub OAuth**:
   - Shows specific scopes: Repository creation, read access
   - User grants permission
   - Token stored in Token Vault
   
2. **Slack Re-authorization**:
   - Shows updated scopes: Send messages, read channels
   - User re-grants permission
   - New token replaces old one in Token Vault

#### Step 4: Orchestrated Execution
1. **Calendar Event**: Creates meeting (using existing permission)
2. **GitHub Repository**: Creates new repo with README
3. **Slack Notification**: Sends message with meeting and repo links
4. **System Response**: 
   ```
   ✅ Workflow Complete!
   
   • GitHub repo created: https://github.com/sarah/q1-project
   • Meeting scheduled: Monday, Jan 22, 10:00 AM
   • Team notified in #general channel
   
   All actions logged in your audit trail.
   ```

### Key Demonstrations
- **Permission Boundaries**: AI respects individual service permissions
- **Sequential Authorization**: Handles multiple permission requests gracefully
- **Service Isolation**: Each service operates independently
- **Workflow Orchestration**: Complex multi-service operations

---

## Scenario 5: Token Refresh and Error Handling

### Context
Sarah has been using CipherMate for several weeks, and some of her tokens are approaching expiration.

### Demo Flow

#### Step 1: Automatic Token Refresh
1. **Background Process**: System detects Google Calendar token expires in 5 minutes
2. **System Action**: 
   - Automatically attempts token refresh using refresh token
   - Updates Token Vault with new access token
   - Logs refresh action in audit trail
3. **User Experience**: Seamless - no interruption to service

#### Step 2: Refresh Failure Scenario
1. **Background Process**: Slack token refresh fails (user revoked app access)
2. **System Response**: 
   - Marks Slack connection as inactive
   - Logs the failure with details
   - Prepares user notification

#### Step 3: Graceful Degradation
1. **User Action**: Sarah asks: "Send a status update to the team"
2. **AI Response**: 
   ```
   I'm unable to access your Slack workspace. It appears the connection 
   was interrupted. Would you like to reconnect Slack to send the message?
   
   Alternative: I can help you draft the message and you can send it manually.
   ```
3. **User Action**: Sarah chooses to reconnect
4. **System Response**: Initiates fresh OAuth flow

#### Step 4: Service Recovery
1. **OAuth Flow**: Sarah re-authorizes Slack access
2. **System Response**: 
   - Stores new tokens in Token Vault
   - Marks connection as active
   - Sends the original message
   - Logs recovery action

### Key Demonstrations
- **Automatic Refresh**: Seamless token lifecycle management
- **Graceful Failure**: User-friendly error handling
- **Service Recovery**: Easy re-authorization process
- **Transparency**: Clear communication about service status

---

## Scenario 6: Audit Trail and Compliance

### Context
Sarah's company requires detailed audit trails for all AI agent activities. She needs to review and export her activity logs.

### Demo Flow

#### Step 1: Comprehensive Audit Dashboard
1. **User Action**: Sarah navigates to "Audit" page
2. **System Response**: Shows detailed activity timeline:

```
Recent Activity (Last 7 Days)
┌─────────────────────┬─────────────┬──────────────────┬─────────────────┐
│ Timestamp           │ Action      │ Service          │ Details         │
├─────────────────────┼─────────────┼──────────────────┼─────────────────┤
│ Jan 22, 2:30 PM     │ Event       │ Google Calendar  │ Created "Team   │
│                     │ Created     │                  │ Standup"        │
├─────────────────────┼─────────────┼──────────────────┼─────────────────┤
│ Jan 22, 2:29 PM     │ Token       │ Google Calendar  │ Retrieved for   │
│                     │ Retrieved   │                  │ API call        │
├─────────────────────┼─────────────┼──────────────────┼─────────────────┤
│ Jan 22, 2:29 PM     │ Permission  │ Google Calendar  │ Verified scope: │
│                     │ Check       │                  │ calendar.events │
├─────────────────────┼─────────────┼──────────────────┼─────────────────┤
│ Jan 21, 4:15 PM     │ Permission  │ Slack           │ Access revoked  │
│                     │ Revoked     │                  │ by user         │
└─────────────────────┴─────────────┴──────────────────┴─────────────────┘
```

#### Step 2: Detailed Event Inspection
1. **User Action**: Sarah clicks on a specific event
2. **System Response**: Shows comprehensive event details:
   ```
   Event Details: Calendar Event Creation
   
   • Timestamp: January 22, 2024, 2:30:15 PM UTC
   • User ID: auth0|64f8a9b2c1d2e3f4g5h6i7j8
   • IP Address: 192.168.1.100
   • User Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
   • Session ID: sess_abc123def456
   
   Action Details:
   • Service: Google Calendar
   • API Endpoint: /calendar/v3/calendars/primary/events
   • Method: POST
   • Scopes Used: calendar.events
   • Token Vault ID: tv_xyz789abc123
   
   Request Data:
   • Event Title: "Team Standup"
   • Start Time: 2024-01-23T10:00:00Z
   • End Time: 2024-01-23T10:30:00Z
   • Attendees: 3 people
   
   Response:
   • Status: 200 OK
   • Event ID: evt_google_abc123
   • Response Time: 245ms
   ```

#### Step 3: Security Event Monitoring
1. **System Response**: Shows security events section:
   ```
   Security Events (Last 30 Days)
   
   ✅ No suspicious activity detected
   
   Monitored Events:
   • Failed authentication attempts: 0
   • Unusual IP address access: 0
   • Rapid permission changes: 0
   • High-volume API usage: 0
   • Token vault access anomalies: 0
   ```

#### Step 4: Compliance Export
1. **User Action**: Sarah clicks "Export Audit Data"
2. **System Response**: Shows export options:
   ```
   Export Audit Data
   
   Date Range: [Jan 1, 2024] to [Jan 22, 2024]
   
   Include:
   ☑️ User actions
   ☑️ AI agent actions
   ☑️ Permission changes
   ☑️ Token operations
   ☑️ Security events
   ☑️ API call details
   
   Format: 
   ○ CSV  ● JSON  ○ PDF Report
   
   [Export Data]
   ```
3. **User Action**: Sarah selects JSON format and exports
4. **System Response**: Generates comprehensive audit report with all activities

### Key Demonstrations
- **Complete Transparency**: Every action is logged and viewable
- **Detailed Context**: Rich metadata for each event
- **Security Monitoring**: Proactive threat detection
- **Compliance Ready**: Exportable audit trails for regulatory requirements

---

## Technical Implementation Notes

### Token Vault Integration Points

1. **Token Storage**: All OAuth tokens stored exclusively in Auth0 Token Vault
2. **Token Retrieval**: Secure API calls to retrieve tokens only when needed
3. **Token Refresh**: Automatic refresh handling with vault updates
4. **Token Revocation**: Immediate removal from vault on user request

### Security Measures Demonstrated

1. **Zero Token Exposure**: Tokens never visible in logs, responses, or client-side code
2. **Granular Permissions**: Scope-level control over service access
3. **Time-Limited Access**: Temporary elevated permissions with auto-expiration
4. **Step-Up Authentication**: Additional verification for high-risk actions
5. **Comprehensive Auditing**: Complete activity trail for compliance

### User Experience Highlights

1. **Clear Consent**: Users understand exactly what permissions they're granting
2. **Immediate Control**: Real-time permission management and revocation
3. **Transparent Operations**: Users see what the AI is doing and why
4. **Graceful Failures**: User-friendly error handling and recovery
5. **Compliance Support**: Easy audit trail access and export

---

## Demo Script for Presentations

### 3-Minute Demo Flow

1. **Opening (30 seconds)**: Show login and dashboard
2. **Permission Grant (60 seconds)**: Demonstrate OAuth flow with Token Vault
3. **AI Action (45 seconds)**: Show AI executing action with audit logging
4. **Permission Management (30 seconds)**: Show revocation and immediate effect
5. **Closing (15 seconds)**: Highlight security benefits and Token Vault integration

### Key Talking Points

- "Tokens are stored in Auth0 Token Vault, never exposed to the AI"
- "Users have granular control over every permission"
- "Every action is audited and transparent"
- "Step-up authentication protects high-risk operations"
- "Immediate permission revocation with real-time effect"

---

*These scenarios demonstrate CipherMate's comprehensive security model, showcasing how Auth0 Token Vault enables secure AI agent interactions while maintaining complete user control and transparency.*