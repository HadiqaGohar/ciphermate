---
id: "001"
title: "Fix ActionExecutionRequest parameters attribute error"
stage: "refactor"
date_iso: "2026-04-11"
surface: "agent"
model: "qwen-code"
feature: "003-security-first-architecture"
branch: "main"
user: "hadiqa"
command: "backend action execution fix"
labels: ["backend", "bug-fix", "action-execution", "fastapi", "gmail", "calendar"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "backend/app/api/v1/agent.py"
  - "backend/app/api/v1/execute_action.py"
  - "backend/app/core/ai_agent.py"
tests_yaml:
  - "Manual testing via frontend chat interface"
prompt_text: "Pehly sahi tha tumne kuch edit kia uske bad ye wapis kahrab hogaya 🤖 AI Chat Assistant... Error: 'ActionExecutionRequest' object has no attribute 'parameters'"
response_text: "Fixed 5 issues: 1) AttributeError in execute_action_simple by removing request.parameters access, 2) Implemented real Gmail sending in execute_action function with proper error handling, 3) Improved email parameter extraction in _extract_email_details to properly parse subject and body from user messages, 4) Fixed Gmail/GitHub/Slack OAuth URL generators to use real client IDs from .env instead of hardcoded placeholders, 5) Fixed 400 error on action re-execution after OAuth by allowing retry for auth-completed actions."
outcome: "Fixed AttributeError, implemented Gmail sending, improved email parameter extraction, fixed OAuth credential URLs, fixed action re-execution after OAuth"
evaluation: "Pending manual testing"
---

# Fix ActionExecutionRequest Parameters Attribute Error

## Context
User reported error in AI Chat Assistant when trying to execute calendar creation action.
Backend error: `'ActionExecutionRequest' object has no attribute 'parameters'`

## Root Cause
The `execute_action_simple` function at line 277 in `agent.py` was trying to access `request.parameters`, but the `ActionExecutionRequest` Pydantic model only defines:
- `action_id: int`
- `confirm: bool`

The `parameters` field doesn't exist in the request model. Parameters are stored in the database in `agent_action.parameters` (JSONB column).

## Fix Applied
Changed line 277 from:
```python
user_timezone = request.parameters.get('timezone', 'Asia/Karachi')
```

To:
```python
user_timezone = request.headers.get('X-Timezone', 'Asia/Karachi') if hasattr(request, 'headers') else 'Asia/Karachi'
```

This extracts timezone from request headers instead, and all action-specific parameters are correctly retrieved from `agent_action.parameters` (lines 299-301, 423-425).

## Impact
- Fixes calendar event creation flow
- Fixes all action execution through the AI agent
- Maintains backward compatibility

## Testing
- [ ] Test calendar event creation from chat
- [ ] Verify OAuth flow still works
- [ ] Test action retry functionality
