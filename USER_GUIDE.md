# CipherMate User Guide

## Welcome to CipherMate! 🚀

CipherMate is your secure AI assistant that helps you manage tasks across multiple services while keeping you in complete control of your data and permissions. This guide will help you get started and make the most of CipherMate's powerful features.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Permissions](#understanding-permissions)
3. [Connecting Services](#connecting-services)
4. [Chatting with Your AI Assistant](#chatting-with-your-ai-assistant)
5. [Managing Permissions](#managing-permissions)
6. [Understanding Audit Logs](#understanding-audit-logs)
7. [Security Features](#security-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

---

## Getting Started

### Creating Your Account

1. **Visit CipherMate**: Go to [https://ciphermate.vercel.app](https://ciphermate.vercel.app)
2. **Sign Up**: Click "Sign Up" and choose your preferred method:
   - Google Account
   - GitHub Account
   - Email and Password
3. **Verify Email**: Check your email and click the verification link
4. **Welcome Dashboard**: You'll be redirected to your personal dashboard

### First Login

When you first log in, you'll see:
- **Dashboard**: Overview of your connected services and recent activity
- **Chat Interface**: Where you'll interact with your AI assistant
- **Permissions Panel**: Manage your service connections
- **Audit Log**: Track all activities and actions

---

## Understanding Permissions

### What Are Permissions?

Permissions in CipherMate control what your AI assistant can do on your behalf. Unlike traditional apps that ask for broad access, CipherMate uses **granular permissions** that let you control exactly what the AI can access.

### Permission Levels

#### 🟢 **Read Permissions** (Low Risk)
- View your calendar events
- Read your email subjects
- See your GitHub repositories
- List Slack channels

#### 🟡 **Write Permissions** (Medium Risk)
- Create calendar events
- Send emails
- Create GitHub issues
- Post Slack messages

#### 🔴 **Admin Permissions** (High Risk)
- Delete calendar events
- Manage repository settings
- Admin Slack workspace functions

### How Permissions Work

1. **Request**: AI identifies what it needs to help you
2. **Consent**: You review and approve specific permissions
3. **Storage**: Tokens are stored securely in Auth0 Token Vault
4. **Usage**: AI uses tokens only for approved actions
5. **Audit**: Every action is logged for your review

---

## Connecting Services

### Supported Services

CipherMate currently supports:

#### 📅 **Google Calendar**
- View and create calendar events
- Manage meeting invitations
- Schedule recurring meetings
- Check availability

#### 📧 **Gmail**
- Read email summaries
- Send emails on your behalf
- Manage email labels
- Search your inbox

#### 🐙 **GitHub**
- View repositories and issues
- Create and manage issues
- Review pull requests
- Manage project boards

#### 💬 **Slack**
- Send messages to channels
- Read channel information
- Manage workspace settings
- Schedule messages

### Connecting Your First Service

Let's connect Google Calendar as an example:

#### Step 1: Trigger Connection
Ask your AI assistant: *"Schedule a team meeting for tomorrow at 2 PM"*

#### Step 2: Permission Request
The AI will respond: *"I need access to your Google Calendar to create events. Would you like to grant me permission?"*

#### Step 3: Review Permissions
A dialog will show:
```
🔐 Google Calendar Access Request

The AI is requesting permission to:
✅ Read your calendar events
✅ Create new calendar events
❌ Delete calendar events (not requested)
❌ Modify calendar settings (not requested)

Risk Level: Medium
Expires: 30 days (auto-renewable)

[Cancel] [Grant Permission]
```

#### Step 4: OAuth Flow
1. Click "Grant Permission"
2. You'll be redirected to Google's authorization page
3. Review Google's consent screen
4. Click "Allow" to grant access
5. You'll be redirected back to CipherMate

#### Step 5: Confirmation
CipherMate will show: *"✅ Google Calendar connected successfully! Your tokens are stored securely in Auth0 Token Vault."*

#### Step 6: Action Execution
The AI will now create your meeting: *"Team meeting scheduled for tomorrow at 2:00 PM. Calendar invite sent!"*

---

## Chatting with Your AI Assistant

### Starting a Conversation

Your AI assistant is available 24/7 in the chat interface. Here's how to get the most out of your conversations:

### Example Conversations

#### 📅 **Calendar Management**

**You**: *"What meetings do I have today?"*

**AI**: *"Let me check your calendar... You have 3 meetings today:
- 9:00 AM: Team Standup (30 min)
- 2:00 PM: Client Review (1 hour)  
- 4:30 PM: Project Planning (45 min)

Would you like me to show more details about any of these meetings?"*

**You**: *"Reschedule the client review to tomorrow at the same time"*

**AI**: *"I'll reschedule your Client Review meeting to tomorrow at 2:00 PM. Let me update the calendar and notify attendees... ✅ Done! Meeting rescheduled and all attendees have been notified."*

#### 📧 **Email Management**

**You**: *"Send an email to the team about tomorrow's deadline"*

**AI**: *"I'd be happy to help you send that email! I need access to your Gmail to send emails on your behalf. Would you like to grant me permission?"*

**You**: *"Yes, grant permission"*

**AI**: *"Great! Now, what would you like the email to say? I can draft something for you or you can provide the content."*

**You**: *"Draft something professional about the Q1 report deadline being tomorrow"*

**AI**: *"Here's a draft email:

**Subject**: Reminder: Q1 Report Deadline Tomorrow

**Body**: 
Hi Team,

I hope this email finds you well. This is a friendly reminder that the Q1 report deadline is tomorrow. Please ensure all sections are completed and submitted by end of day.

If you have any questions or need assistance, please don't hesitate to reach out.

Best regards,
[Your Name]

Would you like me to send this, or would you like to make any changes?"*

#### 🐙 **GitHub Management**

**You**: *"Create a new issue in my project repo for the login bug"*

**AI**: *"I'll create a GitHub issue for the login bug. Let me gather some details:

**Repository**: Which repository should I create the issue in?
**Title**: "Login Bug" - is this descriptive enough?
**Description**: Can you provide more details about the bug?
**Labels**: Should I add any specific labels?
**Assignee**: Should I assign this to anyone?"*

**You**: *"Repository is 'my-app', title is good, description: 'Users can't log in with Google OAuth', add bug label, assign to me"*

**AI**: *"Perfect! I've created the issue:

**Issue #47**: Login Bug
**Repository**: my-app
**Description**: Users can't log in with Google OAuth
**Labels**: bug
**Assignee**: You

**Link**: https://github.com/yourusername/my-app/issues/47

The issue is now live and ready for work!"*

### AI Conversation Tips

#### ✅ **Do's**
- Be specific about what you want to accomplish
- Provide context when asking for help
- Review AI suggestions before approving actions
- Ask for clarification if something isn't clear

#### ❌ **Don'ts**
- Don't share sensitive information like passwords
- Don't approve permissions you don't understand
- Don't assume the AI has access to services you haven't connected

### Understanding AI Responses

The AI will often provide structured responses with:

- **🔍 Analysis**: What the AI understands from your request
- **⚠️ Requirements**: What permissions or information it needs
- **📋 Action Plan**: What it will do step by step
- **✅ Results**: Confirmation of completed actions
- **🔗 Links**: Direct links to created items or resources

---

## Managing Permissions

### Viewing Your Permissions

Navigate to the **Permissions** page to see all your connected services:

```
📊 Permission Dashboard

Connected Services (3):
┌─────────────────┬──────────────────┬─────────────────┬──────────────┐
│ Service         │ Permissions      │ Connected       │ Last Used    │
├─────────────────┼──────────────────┼─────────────────┼──────────────┤
│ Google Calendar │ Read, Create     │ Jan 15, 2024    │ 2 hours ago  │
│ Gmail           │ Read, Send       │ Jan 16, 2024    │ 1 day ago    │
│ GitHub          │ Read, Issues     │ Jan 17, 2024    │ 3 hours ago  │
└─────────────────┴──────────────────┴─────────────────┴──────────────┘

Available Services (1):
• Slack - Not Connected
```

### Detailed Permission View

Click on any service to see detailed information:

```
🔐 Google Calendar - Detailed View

Connection Status: ✅ Active
Connected: January 15, 2024 at 10:30 AM
Last Used: 2 hours ago
Expires: February 15, 2024 (auto-renewable)

Granted Permissions:
✅ calendar.readonly - Read calendar events
✅ calendar.events - Create and modify events
❌ calendar.settings - Modify calendar settings (not granted)
❌ calendar.acls - Manage calendar sharing (not granted)

Token Information:
• Stored in: Auth0 Token Vault
• Token ID: tv_abc123def456 (for support reference)
• Security: Encrypted and isolated
• Access: Only available to authorized AI actions

Recent Activity (Last 7 days):
• 15 calendar events viewed
• 3 calendar events created
• 2 calendar events modified
• 0 security incidents

[View Full Activity] [Modify Permissions] [Revoke Access]
```

### Modifying Permissions

#### Adding New Permissions

1. Click **"Modify Permissions"** on a connected service
2. Review available permissions:
   ```
   📝 Modify Google Calendar Permissions
   
   Currently Granted:
   ✅ Read calendar events
   ✅ Create calendar events
   
   Available to Add:
   ☐ Delete calendar events
   ☐ Modify calendar settings
   ☐ Manage calendar sharing
   
   [Update Permissions]
   ```
3. Select additional permissions you want to grant
4. Click **"Update Permissions"**
5. Complete the OAuth flow for new permissions

#### Removing Permissions

**Note**: You cannot remove individual permissions from an existing connection. To reduce permissions, you must:

1. **Revoke** the entire service connection
2. **Reconnect** with only the permissions you want

This is a security feature that ensures clean permission boundaries.

### Revoking Access

#### Complete Service Revocation

1. Go to the service you want to disconnect
2. Click **"Revoke Access"**
3. Confirm your decision:
   ```
   ⚠️ Revoke Google Calendar Access?
   
   This will:
   • Remove all Google Calendar tokens from Token Vault
   • Disable AI access to your calendar
   • Stop all calendar-related AI functions
   • Log this action in your audit trail
   
   The AI will need permission again to access your calendar.
   
   This action cannot be undone.
   
   [Cancel] [Revoke Access]
   ```
4. Click **"Revoke Access"** to confirm

#### Immediate Effect

Once revoked:
- ✅ Tokens are immediately removed from Token Vault
- ✅ AI loses all access to the service
- ✅ Action is logged in audit trail
- ✅ You receive confirmation

**Testing Revocation**:
Ask the AI to perform an action with the revoked service:

**You**: *"What meetings do I have today?"*

**AI**: *"I no longer have access to your Google Calendar. To check your meetings, I'll need you to grant me calendar permissions again. Would you like to reconnect your calendar?"*

---

## Understanding Audit Logs

### What Are Audit Logs?

Audit logs are detailed records of every action performed by your AI assistant. They provide complete transparency and help you track what's happening with your data.

### Accessing Audit Logs

Navigate to the **Audit** page to view your activity:

```
📊 Audit Dashboard - Last 30 Days

Summary:
• Total Actions: 127
• Services Used: 3 (Google Calendar, Gmail, GitHub)
• Permissions Granted: 3
• Permissions Revoked: 1
• Security Events: 0

Activity Timeline:
```

### Reading Audit Entries

Each audit entry contains:

```
🕐 January 22, 2024 at 2:35 PM

📅 Calendar Event Created
Service: Google Calendar
Action: create_event
Status: ✅ Success

Details:
• Event: "Team Standup"
• Calendar: Primary Calendar
• Duration: 30 minutes
• Attendees: 3 people
• AI Request: "Schedule team standup for tomorrow at 10 AM"

Technical Info:
• API Endpoint: /calendar/v3/calendars/primary/events
• Response Time: 245ms
• Token Used: tv_abc123def456
• Session: sess_def456ghi789

[View Full Details] [Related Actions]
```

### Audit Log Categories

#### 🤖 **AI Actions**
- Calendar events created/modified
- Emails sent
- GitHub issues created
- Slack messages posted

#### 🔐 **Permission Changes**
- Services connected
- Permissions granted
- Access revoked
- Token refreshes

#### 🛡️ **Security Events**
- Failed authentication attempts
- Unusual activity patterns
- Rate limit violations
- Token vault access

#### 📊 **System Events**
- Login/logout activities
- Settings changes
- Export requests
- Error occurrences

### Filtering and Searching

Use the audit log filters to find specific activities:

```
🔍 Filter Audit Logs

Date Range: [Jan 1, 2024] to [Jan 22, 2024]

Service:
☐ All Services
☑️ Google Calendar
☐ Gmail
☐ GitHub
☐ Slack

Action Type:
☐ All Actions
☑️ AI Actions
☐ Permission Changes
☐ Security Events

Status:
☑️ Success
☑️ Failed
☐ Pending

[Apply Filters] [Clear All]
```

### Exporting Audit Data

For compliance or personal records:

1. Click **"Export Audit Data"**
2. Choose your export options:
   ```
   📤 Export Audit Data
   
   Date Range: [Custom Range]
   Format: ○ CSV ● JSON ○ PDF Report
   
   Include:
   ☑️ AI Actions
   ☑️ Permission Changes
   ☑️ Security Events
   ☑️ Technical Details
   ☑️ User Context
   
   [Generate Export]
   ```
3. Wait for processing (usually 1-2 minutes)
4. Download your audit report

---

## Security Features

### Token Vault Security

#### How Token Vault Works

1. **OAuth Flow**: You grant permissions through standard OAuth
2. **Secure Storage**: Tokens are immediately stored in Auth0 Token Vault
3. **Encrypted Access**: Tokens are encrypted and isolated from the AI
4. **Just-in-Time Retrieval**: Tokens are only retrieved when needed for specific actions
5. **No Exposure**: Tokens are never visible in logs, responses, or client-side code

#### Security Benefits

- 🔒 **Isolation**: Tokens are completely isolated from AI processing
- 🛡️ **Encryption**: All tokens encrypted at rest and in transit
- 🔄 **Automatic Refresh**: Tokens refreshed automatically when possible
- ⏰ **Expiration**: Tokens have built-in expiration dates
- 🗑️ **Clean Revocation**: Tokens completely removed on revocation

### Step-Up Authentication

For high-risk actions, CipherMate uses step-up authentication:

#### When Step-Up Is Required

- Deleting multiple items (emails, calendar events, files)
- Modifying security settings
- Bulk operations affecting many records
- Administrative actions

#### Step-Up Process

1. **Risk Detection**: AI identifies high-risk action
2. **Additional Verification**: You receive a push notification or SMS
3. **Temporary Elevation**: Higher permissions granted for limited time
4. **Automatic Revocation**: Elevated access automatically removed after use

#### Example Step-Up Flow

**You**: *"Delete all my calendar events from last month"*

**AI**: *"🔒 This is a high-risk action that will delete 23 calendar events. For your security, I need additional verification."*

**System**: *Sends push notification to your phone*

**You**: *Approves on mobile device*

**AI**: *"✅ Additional verification confirmed. I now have temporary elevated access to delete calendar events. This access will automatically expire in 1 hour or after the action is complete."*

### Security Monitoring

CipherMate continuously monitors for security threats:

#### Monitored Activities

- **Unusual Login Patterns**: Logins from new locations or devices
- **High API Usage**: Unusually high number of API calls
- **Permission Changes**: Rapid granting/revoking of permissions
- **Failed Authentications**: Multiple failed login attempts
- **Token Anomalies**: Unusual token vault access patterns

#### Security Alerts

You'll be notified of security events via:
- In-app notifications
- Email alerts
- SMS (for critical events)

#### Example Security Alert

```
🚨 Security Alert

Event: Unusual API Activity Detected
Time: January 22, 2024 at 3:15 PM
Service: GitHub

Details:
• 150 API calls in 1 hour (normal: ~20)
• Action: Repository access
• Location: New York, NY (usual location)

Recommendation:
Review your recent GitHub activity in the audit log. If this activity was not initiated by you, please revoke GitHub access immediately.

[View Audit Log] [Revoke GitHub Access] [Mark as Safe]
```

---

## Troubleshooting

### Common Issues and Solutions

#### 🔴 **"Permission Denied" Errors**

**Problem**: AI says it doesn't have permission for an action you think it should be able to do.

**Solutions**:
1. **Check Permissions**: Go to Permissions page and verify the service is connected
2. **Review Scopes**: Ensure the specific permission scope is granted
3. **Reconnect Service**: Try revoking and reconnecting the service
4. **Check Expiration**: Verify tokens haven't expired

**Example**:
```
❌ Error: Cannot create calendar event
✅ Solution: Grant "calendar.events" permission to Google Calendar
```

#### 🟡 **Token Refresh Failures**

**Problem**: You get errors about expired tokens that won't refresh.

**Solutions**:
1. **Manual Reconnection**: Revoke and reconnect the service
2. **Check Service Status**: Verify the external service (Google, GitHub, etc.) is operational
3. **Review Permissions**: Ensure you haven't revoked app access in the external service

#### 🟠 **Slow AI Responses**

**Problem**: AI takes a long time to respond or perform actions.

**Solutions**:
1. **Check Service Status**: External services might be experiencing delays
2. **Simplify Requests**: Break complex requests into smaller parts
3. **Check Rate Limits**: You might be hitting API rate limits

#### 🔵 **Missing Audit Logs**

**Problem**: Some actions aren't appearing in audit logs.

**Solutions**:
1. **Wait for Processing**: Logs can take 1-2 minutes to appear
2. **Check Filters**: Ensure your audit log filters aren't hiding entries
3. **Refresh Page**: Sometimes a simple refresh helps

### Getting Help

#### Self-Service Options

1. **Check Status Page**: Visit status.ciphermate.com for service status
2. **Review Documentation**: Check this user guide and API documentation
3. **Search FAQ**: Look through frequently asked questions below

#### Contact Support

If you need additional help:

- **Email**: support@ciphermate.com
- **Response Time**: Within 24 hours
- **Include**: Your user ID, error messages, and steps to reproduce

---

## Best Practices

### Permission Management

#### ✅ **Do's**

1. **Grant Minimal Permissions**: Only grant permissions the AI actually needs
2. **Review Regularly**: Check your permissions monthly and revoke unused ones
3. **Understand Scopes**: Read permission descriptions before granting
4. **Monitor Usage**: Check audit logs to see how permissions are being used
5. **Use Time Limits**: Take advantage of automatic permission expiration

#### ❌ **Don'ts**

1. **Don't Grant Everything**: Avoid granting broad permissions "just in case"
2. **Don't Ignore Alerts**: Pay attention to security notifications
3. **Don't Share Accounts**: Each person should have their own CipherMate account
4. **Don't Skip Reviews**: Don't approve permissions without reading them

### AI Interaction

#### ✅ **Effective Communication**

1. **Be Specific**: "Schedule a 30-minute team meeting tomorrow at 2 PM" vs "Schedule a meeting"
2. **Provide Context**: "Send an email to the marketing team about the Q1 campaign delay"
3. **Confirm Actions**: Review AI suggestions before approving destructive actions
4. **Ask Questions**: If something isn't clear, ask the AI to explain

#### ❌ **What to Avoid**

1. **Vague Requests**: "Do something with my calendar"
2. **Sensitive Information**: Don't share passwords, SSNs, or other sensitive data
3. **Blind Approval**: Don't approve actions without understanding them
4. **Impatience**: Give the AI time to process complex requests

### Security Hygiene

#### 🔒 **Regular Security Practices**

1. **Monthly Permission Review**: Check and clean up permissions monthly
2. **Audit Log Review**: Scan audit logs weekly for unusual activity
3. **Strong Authentication**: Use multi-factor authentication on your Auth0 account
4. **Device Security**: Keep your devices secure and updated
5. **Network Security**: Use secure networks when accessing CipherMate

---

## FAQ

### General Questions

#### **Q: Is CipherMate free to use?**
A: CipherMate offers a free tier with basic functionality. Premium features and higher usage limits are available with paid plans.

#### **Q: What services does CipherMate support?**
A: Currently: Google Calendar, Gmail, GitHub, and Slack. We're constantly adding new integrations.

#### **Q: Can I use CipherMate on mobile?**
A: Yes! CipherMate works on mobile browsers. Native mobile apps are coming soon.

### Security Questions

#### **Q: Where are my tokens stored?**
A: All tokens are stored in Auth0 Token Vault, which provides enterprise-grade security with encryption and isolation.

#### **Q: Can CipherMate see my passwords?**
A: No. CipherMate never sees or stores your passwords. Authentication is handled entirely by Auth0 and the service providers (Google, GitHub, etc.).

#### **Q: What happens if CipherMate gets hacked?**
A: Even if CipherMate were compromised, your tokens are stored separately in Auth0 Token Vault and would remain secure.

#### **Q: Can I delete all my data?**
A: Yes. You can delete your account and all associated data at any time from your account settings.

### Permission Questions

#### **Q: Why does the AI ask for permission so often?**
A: This is by design! CipherMate follows the principle of least privilege, only requesting permissions when needed for specific actions.

#### **Q: Can I grant permissions permanently?**
A: Permissions can be set to auto-renew, but they always have expiration dates for security. You can revoke them at any time.

#### **Q: What's the difference between read and write permissions?**
A: Read permissions let the AI view your data (like seeing calendar events). Write permissions let the AI modify your data (like creating events).

### Technical Questions

#### **Q: How long do tokens last?**
A: Token lifespans vary by service (typically 1-24 hours for access tokens), but refresh tokens allow automatic renewal.

#### **Q: What happens when a token expires?**
A: CipherMate automatically attempts to refresh expired tokens. If refresh fails, you'll be asked to reconnect the service.

#### **Q: Can I export my data?**
A: Yes! You can export your audit logs, settings, and other data from your account settings.

### Troubleshooting Questions

#### **Q: The AI says it can't access my calendar, but I granted permission. What's wrong?**
A: Check if:
1. The permission is still active (not expired or revoked)
2. You granted the right scope (calendar.events for creating events)
3. Your Google account hasn't revoked app access

#### **Q: Why are my audit logs missing some actions?**
A: Audit logs can take 1-2 minutes to process. Also check your filter settings to ensure you're viewing all log types.

#### **Q: The AI is responding slowly. Is something wrong?**
A: Slow responses can be caused by:
1. External service delays (Google, GitHub, etc.)
2. Complex requests requiring multiple API calls
3. Rate limiting from external services

---

## Getting the Most Out of CipherMate

### Advanced Tips

#### 🎯 **Workflow Optimization**

1. **Batch Similar Tasks**: "Schedule all my meetings for next week" instead of one-by-one
2. **Use Templates**: Create reusable email templates for common communications
3. **Set Preferences**: Configure default meeting durations, time zones, etc.
4. **Chain Actions**: "Create a GitHub issue and schedule a meeting to discuss it"

#### 🔄 **Automation Ideas**

1. **Daily Briefings**: "What's on my calendar today and any urgent emails?"
2. **Weekly Reports**: "Summarize my GitHub activity from this week"
3. **Meeting Prep**: "Show me emails related to my 2 PM meeting"
4. **Follow-ups**: "Remind me to follow up on the client proposal next week"

#### 📊 **Monitoring and Analytics**

1. **Regular Audits**: Review your audit logs monthly for insights
2. **Permission Hygiene**: Clean up unused permissions quarterly
3. **Usage Patterns**: Notice which services you use most and optimize accordingly
4. **Security Awareness**: Stay alert to unusual activity patterns

---

## What's Next?

### Upcoming Features

- **Microsoft Office 365** integration
- **Dropbox and Google Drive** file management
- **Zoom and Teams** meeting management
- **Mobile apps** for iOS and Android
- **Advanced automation** and workflow builders
- **Team collaboration** features

### Stay Updated

- **Newsletter**: Subscribe at ciphermate.com/newsletter
- **Blog**: Read updates at blog.ciphermate.com
- **Social Media**: Follow @CipherMate on Twitter
- **Community**: Join our Discord server for tips and support

---

## Conclusion

CipherMate puts you in control of your AI assistant while providing powerful automation capabilities. By understanding permissions, monitoring your audit logs, and following security best practices, you can safely leverage AI to enhance your productivity across all your favorite services.

Remember: **You're always in control.** CipherMate's AI can only do what you explicitly allow, and you can revoke access at any time.

Happy automating! 🚀

---

*For additional support, visit [support.ciphermate.com](https://support.ciphermate.com) or email us at support@ciphermate.com*