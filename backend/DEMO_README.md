<!-- # OpenAI Agents SDK Demo

A clean, simple demonstration of using the OpenAI Agents SDK with Gemini API for translation services.

## Features

- **Multi-language Translation**: Supports Spanish, French, and Italian translations
- **Agent Coordination**: Uses a triage agent to coordinate specialized translation agents
- **Clean Architecture**: Simple, readable code structure
- **Gemini Integration**: Uses Gemini API through OpenAI-compatible interface

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   # or if using pyproject.toml:
   pip install -e .
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key:
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

3. **Run the Demo**:
   ```bash
   python demo_openai_agents.py
   ```

## Usage

### API Endpoints

- `GET /` - Root endpoint with service info
- `GET /health` - Health check
- `POST /chat` - Send messages to the translation agent
- `POST /reset` - Reset conversation history

### Example Requests

**Single Translation**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Translate Hello World to Spanish"}'
```

**Multiple Translations**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Translate Good morning to Spanish, French, and Italian"}'
```

**General Conversation**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What languages can you translate to?"}'
```

## Architecture

### Agent Structure

1. **Triage Agent**: Main coordinator that receives user requests
2. **Spanish Agent**: Specialized for English to Spanish translation
3. **French Agent**: Specialized for English to French translation  
4. **Italian Agent**: Specialized for English to Italian translation

### Key Components

- **OpenAI Agents SDK**: Provides the agent framework
- **Gemini API**: Powers the language model through OpenAI-compatible interface
- **FastAPI**: Web framework for the REST API
- **Conversation History**: Maintains context across requests

## Code Structure

```
demo_openai_agents.py
├── FastAPI app setup
├── Agent initialization (startup event)
├── Chat endpoint (/chat)
├── Health check (/health)
└── Conversation reset (/reset)
```

## Configuration

The demo uses these environment variables:

- `GEMINI_API_KEY`: Your Gemini API key (required)
- `PORT`: Server port (default: 8000)

## Error Handling

The demo includes basic error handling:
- API errors are caught and logged
- User receives friendly error messages
- Service continues running after errors

## Extending the Demo

To add more languages or capabilities:

1. Create new specialized agents
2. Add them as tools to the triage agent
3. Update the triage agent instructions

Example for adding German:
```python
german_agent = Agent(
    name="german_agent",
    instructions="You translate the user's message to German. Provide clear, accurate translations.",
    handoff_description="Translates English to German",
    model=model
)

# Add to triage agent tools:
german_agent.as_tool("translate_to_german", "Translate text to German")
``` -->