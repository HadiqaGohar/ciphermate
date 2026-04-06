# OpenAI Agents SDK Integration

CipherMate now uses the OpenAI Agents SDK for intelligent multi-agent processing.

## Architecture

### Triage Agent
The main entry point that routes user requests to specialized agents:
- Analyzes user intent
- Routes to appropriate specialist agent
- Never handles requests directly

### Specialized Agents

1. **Calendar Agent** (`calendar_agent`)
   - Handles scheduling, meetings, events
   - Extracts dates, times, titles
   - Routes to Google Calendar API

2. **Email Agent** (`email_agent`)
   - Handles email composition and sending
   - Extracts recipients, subjects, content
   - Routes to Gmail API

3. **GitHub Agent** (`github_agent`)
   - Handles repository management
   - Creates issues, manages PRs
   - Routes to GitHub API

4. **Slack Agent** (`slack_agent`)
   - Handles team communication
   - Sends messages, manages channels
   - Routes to Slack API

5. **General Agent** (`general_agent`)
   - Handles greetings, math, programming
   - Provides general assistance
   - No external API routing

## Usage Examples

### Calendar Request
```
User: "Schedule a team meeting tomorrow at 3pm"
Triage Agent → Calendar Agent → Response with event details
```

### Email Request
```
User: "Send an email to john@example.com about the project"
Triage Agent → Email Agent → Response with email composition
```

### Math Request
```
User: "What is 2 + 3?"
Triage Agent → General Agent → "2 + 3 = 5"
```

## Configuration

The agents are configured in `ai_agent_simple.py`:

```python
# Setup in setup_agents_config()
triage_agent = Agent(
    name="triage_agent",
    instructions="Route requests to appropriate specialists...",
    tools=[
        calendar_agent.as_tool(...),
        email_agent.as_tool(...),
        # ... other agents
    ]
)
```

## Fallback Behavior

If the Agents SDK is unavailable:
1. Falls back to rule-based processing
2. Uses pattern matching for intent detection
3. Provides basic responses for common queries
4. Maintains functionality without AI dependencies

## Benefits

1. **Specialized Processing**: Each agent is expert in its domain
2. **Intelligent Routing**: Triage agent ensures correct handling
3. **Scalable Architecture**: Easy to add new specialized agents
4. **Robust Fallbacks**: Works even when AI is unavailable
5. **Cost Effective**: Uses GPT-4o-mini for optimal cost/performance

## Testing

Run the test script to verify Agents SDK integration:

```bash
cd backend
python test_openai.py
```

This will test:
- OpenAI API connectivity
- Agents SDK configuration
- Multi-agent routing
- Response generation