## 🧪 **Multi-Service Integration - Testing Guide**

Aap in sab services ko test karne ke liye yeh steps follow karein:

---

## ✅ **Prerequisites (Pehle Ye Karo)**

### **1. Check if Backend is Running**

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8080
```

### **2. Check if Frontend is Running**

```bash
cd frontend
npm run dev
```

### **3. Open Browser**

```
http://localhost:3000
Login with Auth0 (wondertoonia@gmail.com)
```

---

## 📅 **1. Google Calendar Test**

### **Test Command #1 - Simple Event**

```
In Chat Box type:
"Schedule a team meeting tomorrow at 3 PM"
```

### **Expected Response:**

```
✅ I'll help you schedule this event!
   Title: Team Meeting
   Date: Tomorrow
   Time: 3:00 PM

   [Grant Permission] to Google Calendar
```

### **Test Command #2 - Birthday Party (Aapka wala)**

```
"Birthday party create schedule 5:00pm tomorrow 6-apr-2026"
```

### **Expected Response:**

```
✅ Birthday Party scheduled!
   Date: Monday, April 6, 2026
   Time: 5:00 PM - 6:00 PM

   View in Google Calendar: [Link]
```

### **Verify in Google Calendar:**

```
1. Open https://calendar.google.com
2. April 6, 2026 dekhein
3. 5:00 PM pe event hona chahiye
```

---

## 📧 **2. Gmail Test**

### **Test Command:**

```
"Send email to wondertoonia@gmail.com with subject Testing CipherMate and body This is a test email from AI assistant"
```

### **Expected Response:**

```
📧 I'll help you send this email!
   To: wondertoonia@gmail.com
   Subject: Testing CipherMate

   [Grant Permission] to Gmail
```

### **Verify in Gmail:**

```
1. Open https://mail.google.com
2. Inbox mein email aana chahiye
3. Sender: CipherMate AI
```

### **Simple Test Command:**

```
"Email my doctor about appointment tomorrow"
```

---

## 🐙 **3. GitHub Test**

### **Prerequisite - GitHub Token:**

```
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes: repo, issues
4. Copy token
```

### **Add to .env:**

```bash
# backend/.env
GITHUB_TOKEN=ghp_your_token_here
```

### **Test Command:**

```
"Create issue in your-username/your-repo titled Test issue from CipherMate with body This is a test"
```

Create issue in HadiqaGohar/ciphermate-github-test-repo titled Test issue from CipherMate with body This is a test

### **Expected Response:**

```
🐙 GitHub issue created!
   Issue #: 1
   Title: Test issue from CipherMate
   URL: https://github.com/.../issues/1
```

### **Verify on GitHub:**

```
Open your repository → Issues tab
New issue should appear
```

---

## 💬 **4. Slack Test**

### **Prerequisite - Slack Bot Token:**

```
1. Go to https://api.slack.com/apps
2. Create new app
3. Add bot token scopes: chat:write, channels:read
4. Install to workspace
5. Copy Bot User OAuth Token
```

### **Add to .env:**

```bash
# backend/.env
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL=#general
```

### **Test Command:**

```
"Send Slack message to #general channel: Hello everyone from CipherMate AI!"
```

### **Expected Response:**

```
💬 Slack message sent!
   Channel: #general
   Message: Hello everyone from CipherMate AI!
   Timestamp: 2026-04-05 18:30:00
```

### **Verify on Slack:**

```
Open your Slack workspace → #general channel
Message should appear
```

---

## 🔄 **5. Extensible Architecture Test (Adding New Service)**

### **Test Adding Custom Service:**

**Step 1: Create Service Template**

```python
# backend/app/services/custom_service.py
class CustomService:
    async def execute(self, params):
        return {"status": "success", "data": params}
```

**Step 2: Register Service**

```python
# backend/app/core/service_registry.py
SERVICES = {
    "custom": {
        "class": CustomService,
        "permissions": ["custom.read", "custom.write"],
        "oauth_url": "/auth/custom"
    }
}
```

**Step 3: Test via API**

```bash
curl -X POST http://localhost:8080/api/v1/services/custom/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "test", "params": {"key": "value"}}'
```

---

## 🎯 **Quick Test All Services (One Command)**

Create test script `test_all_services.sh`:

```bash
#!/bin/bash

echo "🧪 Testing CipherMate Multi-Service Integration"
echo "============================================="

# 1. Test Backend Health
echo "1. Testing Backend..."
curl -s http://localhost:8080/health | jq .

# 2. Test Calendar API
echo "2. Testing Calendar..."
curl -X POST http://localhost:8080/api/v1/calendar/test \
  -H "Content-Type: application/json" \
  -d '{"action": "test"}' | jq .

# 3. Test Email API
echo "3. Testing Email..."
curl -X POST http://localhost:8080/api/v1/email/test \
  -H "Content-Type: application/json" \
  -d '{"to": "test@example.com"}' | jq .

# 4. Test GitHub API
echo "4. Testing GitHub..."
curl -X GET http://localhost:8080/api/v1/github/test | jq .

# 5. Test Slack API
echo "5. Testing Slack..."
curl -X POST http://localhost:8080/api/v1/slack/test \
  -H "Content-Type: application/json" \
  -d '{"channel": "#test", "message": "Test from script"}' | jq .

echo "✅ Testing complete!"
```

Run:

```bash
chmod +x test_all_services.sh
./test_all_services.sh
```

---

## 📊 **Test Results Dashboard**

### **Browser Check:**

```
1. Go to http://localhost:3000/status
2. Check each service status:
   - Google Calendar: ✅ Connected / ❌ Not Connected
   - Gmail: ✅ Connected / ❌ Not Connected
   - GitHub: ✅ Connected / ❌ Not Connected
   - Slack: ✅ Connected / ❌ Not Connected
```

### **Audit Log Check:**

```
1. Go to http://localhost:3000/audit
2. Filter by service
3. See all actions performed
```

---

## ✅ **Success Criteria Checklist**

| Service  | Test Command                    | Expected Result                  | Status |
| -------- | ------------------------------- | -------------------------------- | ------ |
| Calendar | "Schedule meeting tomorrow 3pm" | Event created in Google Calendar | ⬜     |
| Gmail    | "Send test email"               | Email received                   | ⬜     |
| GitHub   | "Create test issue"             | Issue appears on GitHub          | ⬜     |
| Slack    | "Send test message"             | Message appears in Slack         | ⬜     |

---

## 🐛 **If Tests Fail - Troubleshooting**

### **Calendar Not Working:**

```bash
# Check token
curl http://localhost:8080/api/v1/token-vault/list

# Re-authenticate
Go to http://localhost:3000/token-vault → Refresh Google Calendar
```

### **Email Not Working:**

```bash
# Check Gmail API enabled
https://console.cloud.google.com/apis/library/gmail.googleapis.com

# Check token scopes
Should include: https://www.googleapis.com/auth/gmail.send
```

### **GitHub Not Working:**

```bash
# Test token manually
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/user
```

### **Slack Not Working:**

```bash
# Test bot token
curl -H "Authorization: Bearer YOUR_BOT_TOKEN" \
  https://slack.com/api/auth.test
```

---

## 🚀 **Ready to Test?**

**Run this command now:**

```
"Birthday party create schedule 5:00pm tomorrow 6-apr-2026"
```

**Aur batao kya result aaya?** 🎯


// done hadiqa
