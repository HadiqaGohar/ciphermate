Hello hadiqa tasleem! I'm your secure AI assistant. I can help you with tasks across your connected services like Google Calendar, Gmail, GitHub, and Slack. What would you like me to help you with today?
05:17 PM
"Schedule a team meeting tomorrow at 3 PM"
05:17 PM
Okay, I can schedule that for you. Please confirm the details: **Calendar Operation:** Create Event **Title:** Team Meeting **Date:** [Tomorrow's Date, e.g., October 27, 2023] **Time:** 3:00 PM **Duration:** 1 hour (default) **Attendees:** [List of team members - please provide if known] **Location/Platform:** [Please specify, e.g., Conference Room A, Zoom] Would you like to add any attendees or a specific location/platform?
Intent:
general query
high
05:17 PM
schedule that for you. Please confirm the details: **Calendar Operation:** Create Event **Title:** Team Meeting **Date:** [Tomorrow's Date, e.g., October 27, 2023] **Time:** 3:00 PM **Duration:** 1 hour (default) **Attendees:** [List of team members - please provide if known] **Location/Platform:** [Please specify, e.g., Conference Room A, Zoom] Would you like to add any attendees or a specific location/platform? Intent: general query
05:17 PM
fallback I'm CipherMate, your AI assistant! I can help with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with? (Note: Backend connection issue - using mode)
Intent:
general query
medium
05:18 PM
"Birthday party create schedule 5:00pm tomorrow 7-apr-2026"
05:18 PM
I was unable to create a schedule for the birthday party due to a quota error. Please try again in 28 seconds.
Intent:
general query
high
05:18 PM



cdhadiqa@hadiqa-Latitude-3540:~/Documents/International Hackathon/Authorized-Auth-0/ciphermate$ cd frontend
hadiqa@hadiqa-Latitude-3540:~/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend$ npm run dev

> frontend@0.1.0 dev
> TURBOPACK=0 next dev

▲ Next.js 16.2.1 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.134.24:3000
- Environments: .env.local
✓ Ready in 587ms
Creating turbopack project {
  dir: '/home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend',
  testMode: true
}



Source path: ./src/app/globals.css
Setting up new context...
Finding changed files: 8.929ms
Reading changed files: 121.24ms
Sorting candidates: 5.537ms
Generate rules: 143.299ms
Build stylesheet: 2.751ms
Potential classes:  6749
Active contexts:  1
JIT TOTAL: 444.434ms


 GET / 200 in 669ms (next.js: 94ms, proxy.ts: 259ms, application-code: 316ms)
 GET / 200 in 72ms (next.js: 4ms, proxy.ts: 4ms, application-code: 65ms)
 GET /api/auth/me 200 in 86ms (next.js: 72ms, application-code: 15ms)
 GET /api/auth/me 200 in 9ms (next.js: 3ms, application-code: 6ms)
 GET /dashboard 200 in 58ms (next.js: 27ms, proxy.ts: 6ms, application-code: 25ms)
 GET /chat 200 in 72ms (next.js: 51ms, proxy.ts: 6ms, application-code: 15ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Are you online ?
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "Fallback ai_agent_simple.py I'm CipherMate, your AI assistant! I can help with:\n" +
    '\n' +
    '📅 Calendar events\n',
  intent_type: 'general_query',
  confidence: 'medium'
}
 POST /api/chat 200 in 1168ms (next.js: 51ms, proxy.ts: 15ms, application-code: 1102ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: are you online
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "Fallback agent.py --> I'm CipherMate, your AI assistant! I can help with calendar events, emails, Gi",
  intent_type: 'general_query',
  confidence: 'medium'
}
 POST /api/chat 200 in 1110ms (next.js: 7ms, proxy.ts: 7ms, application-code: 1096ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Create meeting 8pm apr-6-2026 today
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: '6-2026 = -2020',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 1114ms (next.js: 7ms, proxy.ts: 7ms, application-code: 1099ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Create meeting 8pm apr-6-2026 today
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: '6-2026 = -2020',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 1107ms (next.js: 7ms, proxy.ts: 11ms, application-code: 1089ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Create meeting 8pm apr-6-2026 today
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: '6-2026 = -2020',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 1095ms (next.js: 4ms, proxy.ts: 7ms, application-code: 1084ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Create meeting 8pm apr-6-2026 today
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "OK. I've sent the request to the calendar agent.\n",
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 7.5s (next.js: 3ms, proxy.ts: 6ms, application-code: 7.5s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: Hi
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "Hello! I'm CipherMate, your AI assistant. I can help you with calendar, email, GitHub, and Slack tas",
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 2.8s (next.js: 39ms, proxy.ts: 10ms, application-code: 2.8s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: what time is
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: 'I need more information to help you. Please tell me what event you are asking about, or what you wou',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 3.9s (next.js: 3ms, proxy.ts: 5ms, application-code: 3.9s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: who is the founder of pakistan
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: 'I am sorry, but I cannot answer that question. My purpose is to route requests to the appropriate sp',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 2.9s (next.js: 7ms, proxy.ts: 6ms, application-code: 2.9s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: ok i am testing you only can you please tell me you are working orginal or demo
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "I am sorry, but I can't help you with this request. I am a large language model, trained by Google.",
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 3.1s (next.js: 4ms, proxy.ts: 8ms, application-code: 3.1s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: "Schedule a team meeting tomorrow at 3 PM"
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: "I've drafted a calendar event for a team meeting tomorrow at 3 PM. Do you want me to go ahead and se",
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 5.4s (next.js: 18ms, proxy.ts: 8ms, application-code: 5.4s)
 GET / 200 in 42ms (next.js: 6ms, proxy.ts: 4ms, application-code: 33ms)
 GET /dashboard 200 in 40ms (next.js: 5ms, proxy.ts: 6ms, application-code: 29ms)
 GET /audit 200 in 155ms (next.js: 133ms, proxy.ts: 5ms, application-code: 17ms)
 GET /api/audit/logs?page=1&page_size=20 401 in 74ms (next.js: 46ms, proxy.ts: 5ms, application-code: 24ms)
 GET /api/audit/logs?page=1&page_size=20 401 in 25ms (next.js: 3ms, proxy.ts: 7ms, application-code: 15ms)
[browser] Error loading audit logs: Error: Failed to load audit logs
    at AuditLogViewer.useCallback[loadLogs] (file:///home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend/.next/dev/static/chunks/src_components_0xz08_e._.js:512:27) (file:///home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend/.next/dev/static/chunks/src_components_0xz08_e._.js:554:25)
[browser] Error loading audit logs: Error: Failed to load audit logs
    at AuditLogViewer.useCallback[loadLogs] (file:///home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend/.next/dev/static/chunks/src_components_0xz08_e._.js:512:27) (file:///home/hadiqa/Documents/International Hackathon/Authorized-Auth-0/ciphermate/frontend/.next/dev/static/chunks/src_components_0xz08_e._.js:554:25)
 GET /permissions 200 in 1499ms (next.js: 1474ms, proxy.ts: 6ms, application-code: 19ms)
 GET /api/permissions/list 200 in 1235ms (next.js: 174ms, proxy.ts: 8ms, application-code: 1053ms)
 GET /api/permissions/services 200 in 1237ms (next.js: 199ms, proxy.ts: 8ms, application-code: 1030ms)
 GET /api/permissions/list 200 in 22ms (next.js: 2ms, proxy.ts: 6ms, application-code: 13ms)
 GET /api/permissions/services 200 in 25ms (next.js: 4ms, proxy.ts: 6ms, application-code: 16ms)
 GET /api/permissions/scopes/google_calendar 200 in 974ms (next.js: 961ms, proxy.ts: 5ms, application-code: 8ms)
 GET /dashboard 200 in 51ms (next.js: 7ms, proxy.ts: 6ms, application-code: 39ms)
 GET /chat 200 in 44ms (next.js: 8ms, proxy.ts: 8ms, application-code: 29ms)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: "Schedule a team meeting tomorrow at 3 PM"
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: 'Okay, I can schedule that for you. Please confirm the details:\n' +
    '\n' +
    '**Calendar Operation:** Create Event',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 6.7s (next.js: 6ms, proxy.ts: 6ms, application-code: 6.6s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: schedule that for you. Please confirm the details: **Calendar Operation:** Create Event **Title:** Team Meeting **Date:** [Tomorrow's Date, e.g., October 27, 2023] **Time:** 3:00 PM **Duration:** 1 hour (default) **Attendees:** [List of team members - please provide if known] **Location/Platform:** [Please specify, e.g., Conference Room A, Zoom] Would you like to add any attendees or a specific location/platform?
Intent:
general query
✅ Backend health check passed
❌ Backend connection failed: Error [TimeoutError]: The operation was aborted due to timeout
    at async POST (src/app/api/chat/route.ts:43:31)
  41 |       console.log("✅ Backend health check passed");
  42 |
> 43 |       const backendResponse = await fetch(`${BACKEND_URL}/api/v1/agent/chat`, {
     |                               ^
  44 |         method: "POST",
  45 |         headers: { "Content-Type": "application/json" },
  46 |         body: JSON.stringify({ {
  code: 23,
  INDEX_SIZE_ERR: 1,
  DOMSTRING_SIZE_ERR: 2,
  HIERARCHY_REQUEST_ERR: 3,
  WRONG_DOCUMENT_ERR: 4,
  INVALID_CHARACTER_ERR: 5,
  NO_DATA_ALLOWED_ERR: 6,
  NO_MODIFICATION_ALLOWED_ERR: 7,
  NOT_FOUND_ERR: 8,
  NOT_SUPPORTED_ERR: 9,
  INUSE_ATTRIBUTE_ERR: 10,
  INVALID_STATE_ERR: 11,
  SYNTAX_ERR: 12,
  INVALID_MODIFICATION_ERR: 13,
  NAMESPACE_ERR: 14,
  INVALID_ACCESS_ERR: 15,
  VALIDATION_ERR: 16,
  TYPE_MISMATCH_ERR: 17,
  SECURITY_ERR: 18,
  NETWORK_ERR: 19,
  ABORT_ERR: 20,
  URL_MISMATCH_ERR: 21,
  QUOTA_EXCEEDED_ERR: 22,
  TIMEOUT_ERR: 23,
  INVALID_NODE_TYPE_ERR: 24,
  DATA_CLONE_ERR: 25
}
❌ Error details: {
  name: 'TimeoutError',
  message: 'The operation was aborted due to timeout',
  cause: undefined
}
❌ Backend URL was: http://localhost:8080
 POST /api/chat 200 in 11.2s (next.js: 6ms, proxy.ts: 4ms, application-code: 11.2s)
🚀 Calling backend: http://localhost:8080/api/v1/agent/chat
📤 Sending message: "Birthday party create schedule 5:00pm tomorrow 7-apr-2026"
✅ Backend health check passed
📡 Backend response status: 200
✅ Backend response received: {
  message: 'I was unable to create a schedule for the birthday party due to a quota error. Please try again in 2',
  intent_type: 'general_query',
  confidence: 'high'
}
 POST /api/chat 200 in 7.5s (next.js: 3ms, proxy.ts: 5ms, application-code: 7.5s)




INFO:     Started server process [28189]
INFO:     Waiting for application startup.
Starting CipherMate Backend...
2026-04-06 17:16:10,285 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:16:10,286 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("users")
2026-04-06 17:16:10,286 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("service_connections")
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("audit_logs")
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("agent_actions")
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("permission_templates")
2026-04-06 17:16:10,287 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,288 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("security_events")
2026-04-06 17:16:10,288 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,288 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("todo_tasks")
2026-04-06 17:16:10,288 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-06 17:16:10,288 INFO sqlalchemy.engine.Engine COMMIT
CipherMate Backend started successfully with monitoring
INFO:     Application startup complete.
2026-04-06 17:16:11,293 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:16:11,293 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:16:11,298 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:16:11,298 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:40960 - "GET /health HTTP/1.1" 200 OK
Slow request: 4.328s for POST /api/v1/agent/chat
INFO:     127.0.0.1:40972 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
2026-04-06 17:16:42,305 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:16:42,305 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:16:42,309 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:16:42,309 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:36746 - "GET /api/v1/audit/logs?page=1&page_size=20 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:36746 - "GET /api/v1/audit/logs?page=1&page_size=20 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:50916 - "GET /api/v1/permissions/list HTTP/1.1" 200 OK
INFO:     127.0.0.1:50922 - "GET /api/v1/permissions/services HTTP/1.1" 200 OK
INFO:     127.0.0.1:50916 - "GET /api/v1/permissions/list HTTP/1.1" 200 OK
INFO:     127.0.0.1:50922 - "GET /api/v1/permissions/services HTTP/1.1" 200 OK
2026-04-06 17:17:13,314 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:17:13,314 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:17:13,316 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:17:13,317 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:33394 - "GET /health HTTP/1.1" 200 OK
Slow request: 6.603s for POST /api/v1/agent/chat
INFO:     127.0.0.1:33402 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
2026-04-06 17:17:44,322 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:17:44,323 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:17:44,327 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:17:44,327 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:42362 - "GET /health HTTP/1.1" 200 OK
Blocked potentially malicious input: schedule that for you. Please confirm the details: **Calendar Operation:** Create Event **Title:** T
Slow request: 15.077s for POST /api/v1/agent/chat
2026-04-06 17:18:15,333 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:18:15,333 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:18:15,337 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:18:15,337 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:49928 - "GET /health HTTP/1.1" 200 OK
Blocked potentially malicious input: "Birthday party create schedule 5:00pm tomorrow 7-apr-2026"
Error getting response; filtered.input=[{'content': 'Birthday party create schedule 5:00pm tomorrow 7-apr-2026', 'role': 'user'}]
Slow request: 6.420s for POST /api/v1/agent/chat
INFO:     127.0.0.1:49938 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
2026-04-06 17:18:46,340 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:18:46,340 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:18:46,343 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:18:46,343 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:19:17,347 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:19:17,348 INFO sqlalchemy.engine.Engine ROLLBACK
2026-04-06 17:19:17,349 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-06 17:19:17,349 INFO sqlalchemy.engine.Engine ROLLBACK
