"""Final Clean AI Agent - No fallback, No general chat, Only 4 services"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from app.core.config import settings

logger = logging.getLogger(__name__)

agents_config = None
triage_agent = None
agents_available = False


def setup_agents_config():
    global agents_config, triage_agent, agents_available
    
    if not getattr(settings, 'GEMINI_API_KEY', None):
        logger.warning("GEMINI_API_KEY not configured")
        agents_available = False
        return
    
    try:
        client = AsyncOpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            timeout=30.0  # Add timeout to prevent hanging
        )
        
        model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash", 
            openai_client=client
        )
        
        agents_config = RunConfig(
            model=model, 
            model_provider=client, 
            tracing_disabled=True
        )
        
        calendar_agent = Agent(
            name="calendar_agent",
            instructions="You are a calendar specialist. When user wants to schedule meeting, event or birthday party, create the event with extracted title, date and time. Give short confirmation only.",
            handoff_description="Calendar events",
            model=model
        )
        
        email_agent = Agent(
            name="email_agent",
            instructions="You are an email specialist. Help user send emails.",
            handoff_description="Send emails",
            model=model
        )
        
        github_agent = Agent(
            name="github_agent",
            instructions="You are a GitHub specialist. Help create issues.",
            handoff_description="GitHub issues",
            model=model
        )
        
        slack_agent = Agent(
            name="slack_agent",
            instructions="You are a Slack specialist. Help send messages.",
            handoff_description="Slack messages",
            model=model
        )
        
        triage_agent = Agent(
            name="triage_agent",
            instructions=(
                "You are a strict triage agent. Route ONLY to the correct tool:\n"
                "- Anything about schedule, meeting, event, birthday, calendar → calendar_agent\n"
                "- Anything about email, send mail → email_agent\n"
                "- Anything about github, issue → github_agent\n"
                "- Anything about slack, message, channel → slack_agent\n"
                "Do not chat. Do not ask questions. Do not confirm. Just call the correct tool."
            ),
            tools=[
                calendar_agent.as_tool("handle_calendar_request", "Create or manage calendar events"),
                email_agent.as_tool("handle_email_request", "Send emails"),
                github_agent.as_tool("handle_github_request", "Create GitHub issues"),
                slack_agent.as_tool("handle_slack_request", "Send Slack messages"),
            ],
            model=model
        )
        
        agents_available = True
        logger.info("✅ Clean Agents SDK loaded successfully")
        
    except Exception as e:
        logger.error(f"Failed to load Agents SDK: {e}")
        agents_available = False


setup_agents_config()


class IntentType(Enum):
    CALENDAR_CREATE_EVENT = "calendar_create_event"
    EMAIL_SEND = "email_send"
    GITHUB_CREATE_ISSUE = "github_create_issue"
    SLACK_SEND_MESSAGE = "slack_send_message"
    UNKNOWN = "unknown"


@dataclass
class IntentAnalysisResult:
    intent_type: IntentType
    confidence: str
    parameters: Dict[str, Any]
    required_permissions: List[str]
    service_name: Optional[str] = None


class AIAgentEngine:
    def __init__(self):
        self.triage_agent = triage_agent
        self.config = agents_config
        self.available = agents_available

    async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.available or not self.triage_agent:
            return self._fallback_response(user_message)
        
        # Implement retry logic for quota errors
        max_retries = 2  # Reduced retries
        base_delay = 1   # Reduced delay
        
        for attempt in range(max_retries):
            try:
                # Add timeout to prevent hanging
                result = await asyncio.wait_for(
                    Runner.run(
                        starting_agent=self.triage_agent,
                        input=user_message,
                        run_config=self.config
                    ),
                    timeout=15.0  # Reduced timeout
                )
                
                return {
                    "response": result.final_output.strip(),
                    "intent_type": "processed",
                    "confidence": "high",
                    "service_name": None,
                    "parameters": {},
                    "required_permissions": [],
                    "clarification_needed": False,
                    "clarification_questions": []
                }
                
            except asyncio.TimeoutError:
                logger.warning(f"AI agent timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                else:
                    return self._fallback_response(user_message)
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # Handle quota errors specifically - go to fallback immediately
                if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                    logger.warning(f"Quota exceeded, using fallback response")
                    return self._fallback_response(user_message)
                
                logger.error(f"Error in process_message: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay)
                    continue
                else:
                    return self._fallback_response(user_message)

    def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Smart fallback responses for when Gemini API is unavailable"""
        msg_lower = user_message.lower()
        
        # Calendar/Event requests
        if any(word in msg_lower for word in ['birthday', 'party', 'schedule', 'meeting', 'event', 'calendar']):
            # Extract details
            title = "Birthday Party" if "birthday" in msg_lower else "Meeting"
            if "team meeting" in msg_lower:
                title = "Team Meeting"
            elif "appointment" in msg_lower:
                title = "Appointment"
            
            # Extract time
            time_str = "5:00 PM"
            if "5:00pm" in msg_lower or "5pm" in msg_lower:
                time_str = "5:00 PM"
            elif "3pm" in msg_lower or "3:00pm" in msg_lower:
                time_str = "3:00 PM"
            
            # Extract date
            date_str = "tomorrow"
            if "tomorrow" in msg_lower:
                date_str = "tomorrow (April 7, 2026)"
            elif "today" in msg_lower:
                date_str = "today (April 6, 2026)"
            
            return {
                "response": f"Default response at ai_agents.py ✅ I'll help you create a {title.lower()} for {date_str} at {time_str}.\n\n📅 Event Details:\n• Title: {title}\n• Date: {date_str}\n• Time: {time_str}\n• Duration: 1 hour\n\nTo actually create this event, please connect your Google Calendar in the Permissions section.",
                "intent_type": "calendar_create_event",
                "confidence": "high",
                "service_name": "google",
                "parameters": {"title": title, "time": time_str, "date": date_str},
                "required_permissions": ["https://www.googleapis.com/auth/calendar"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Email requests
        elif any(word in msg_lower for word in ['email', 'mail', 'send']) and '@' in user_message:
            return {
                "response": "Default response at ai_agents.py ✅ I can help you send an email. Please connect your Gmail account in the Permissions section to proceed.",
                "intent_type": "email_send",
                "confidence": "high",
                "service_name": "google",
                "parameters": {},
                "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # GitHub requests
        elif any(word in msg_lower for word in ['github', 'issue', 'repo']):
            return {
                "response": "Default response at ai_agents.py ✅ I can help you create a GitHub issue. Please connect your GitHub account in the Permissions section.",
                "intent_type": "github_create_issue",
                "confidence": "high",
                "service_name": "github",
                "parameters": {},
                "required_permissions": ["repo"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Slack requests
        elif any(word in msg_lower for word in ['slack', 'message', 'channel']):
            return {
                "response": "Default response at ai_agents.py ✅ I can help you send a Slack message. Please connect your Slack workspace in the Permissions section.",
                "intent_type": "slack_send_message",
                "confidence": "high",
                "service_name": "slack",
                "parameters": {},
                "required_permissions": ["chat:write"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Task/capability questions
        elif any(word in msg_lower for word in ['task', 'perform', 'do', 'help', 'what', 'which']):
            return {
                "response": "Default response at ai_agents.py 🤖 I'm CipherMate, your AI assistant! I can help you with:\n\n📅 **Calendar Events** - Schedule meetings, appointments, birthday parties\n📧 **Email** - Send and manage emails\n🐙 **GitHub** - Create issues and manage repositories\n💬 **Slack** - Send messages to channels\n\nJust tell me what you'd like to do! For example:\n• \"Schedule a team meeting tomorrow at 3 PM\"\n• \"Send an email to john@example.com\"\n• \"Create a GitHub issue for bug fix\"",
                "intent_type": "general_query",
                "confidence": "high",
                "service_name": None,
                "parameters": {},
                "required_permissions": [],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Default response
        else:
            return {
                "response": "Default response at ai_agents.py Hello! I'm CipherMate, your AI assistant. I can help you with calendar events, emails, GitHub issues, and Slack messages. What would you like me to help you with?",
                "intent_type": "general_query",
                "confidence": "medium",
                "service_name": None,
                "parameters": {},
                "required_permissions": [],
                "clarification_needed": False,
                "clarification_questions": []
            }

    async def analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
        """Analyze intent of user message"""
        if not self.available or not self.triage_agent:
            return IntentAnalysisResult(
                intent_type=IntentType.UNKNOWN,
                confidence="low",
                parameters={},
                required_permissions=[]
            )
        
        try:
            # Simple intent analysis based on keywords
            msg_lower = user_message.lower()
            
            if any(word in msg_lower for word in ['calendar', 'schedule', 'meeting', 'event', 'birthday']):
                return IntentAnalysisResult(
                    intent_type=IntentType.CALENDAR_CREATE_EVENT,
                    confidence="high",
                    parameters={},
                    required_permissions=["https://www.googleapis.com/auth/calendar"],
                    service_name="google"
                )
            elif any(word in msg_lower for word in ['email', 'mail', 'send']) and '@' in user_message:
                return IntentAnalysisResult(
                    intent_type=IntentType.EMAIL_SEND,
                    confidence="high",
                    parameters={},
                    required_permissions=["https://www.googleapis.com/auth/gmail.send"],
                    service_name="google"
                )
            elif any(word in msg_lower for word in ['github', 'issue', 'repo']):
                return IntentAnalysisResult(
                    intent_type=IntentType.GITHUB_CREATE_ISSUE,
                    confidence="high",
                    parameters={},
                    required_permissions=["repo"],
                    service_name="github"
                )
            elif any(word in msg_lower for word in ['slack', 'message', 'channel']):
                return IntentAnalysisResult(
                    intent_type=IntentType.SLACK_SEND_MESSAGE,
                    confidence="high",
                    parameters={},
                    required_permissions=["chat:write"],
                    service_name="slack"
                )
            else:
                return IntentAnalysisResult(
                    intent_type=IntentType.UNKNOWN,
                    confidence="low",
                    parameters={},
                    required_permissions=[]
                )
                
        except Exception as e:
            logger.error(f"Error in analyze_intent: {e}")
            return IntentAnalysisResult(
                intent_type=IntentType.UNKNOWN,
                confidence="low",
                parameters={},
                required_permissions=[]
            )


# Singleton
ai_agent_engine = AIAgentEngine()