"""AI Agent implementation for Calendar, Email, GitHub & Slack only"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
import re

from openai_agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from app.core.config import settings

logger = logging.getLogger(__name__)

# Configure OpenAI Agents SDK
agents_config = None
triage_agent = None
agents_available = False


def setup_agents_config():
    """Setup OpenAI Agents SDK configuration with Gemini"""
    global agents_config, triage_agent, agents_available
    
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not configured - Agents SDK disabled")
        agents_available = False
        return
    
    try:
        # Setup OpenAI-compatible client for Gemini API
        external_client = AsyncOpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        
        # Setup model
        model = OpenAIChatCompletionsModel(
            # model="gemini-2.5-flash",
            model = "gemini-3-flash-preview",
            openai_client=external_client,
        )
        
        # Setup run configuration
        agents_config = RunConfig(
            model=model,
            model_provider=external_client,
            tracing_disabled=True
        )
        
        # Setup specialized agents
        calendar_agent = Agent(
            name="calendar_agent",
            instructions=(
                "You are a calendar management specialist. "
                "You help users create, update, and manage calendar events. "
                "Extract event details like title, date, time, and duration from user requests. "
                "Always respond with structured information about calendar operations."
            ),
            handoff_description="Handles calendar and scheduling requests",
            model=model
        )
        
        email_agent = Agent(
            name="email_agent", 
            instructions=(
                "You are an email management specialist. "
                "You help users compose, send, and manage emails. "
                "Extract recipient, subject, and body content from user requests. "
                "Always respond with structured information about email operations."
            ),
            handoff_description="Handles email composition and management",
            model=model
        )
        
        github_agent = Agent(
            name="github_agent",
            instructions=(
                "You are a GitHub management specialist. "
                "You help users create issues, manage repositories, and handle pull requests. "
                "Extract repository names, issue titles, descriptions, and labels from user requests. "
                "Always respond with structured information about GitHub operations."
            ),
            handoff_description="Handles GitHub repository and issue management",
            model=model
        )
        
        slack_agent = Agent(
            name="slack_agent",
            instructions=(
                "You are a Slack communication specialist. "
                "You help users send messages, manage channels, and handle team communications. "
                "Extract channel names, message content, and recipient information from user requests. "
                "Always respond with structured information about Slack operations."
            ),
            handoff_description="Handles Slack messaging and team communication",
            model=model
        )
        
        # Setup triage agent (removed general_agent)
        triage_agent = Agent(
            name="triage_agent",
            instructions=(
                "You are an intelligent triage agent for CipherMate AI Assistant. "
                "You analyze user requests and route them to the appropriate specialist agent. "
                "Use the tools provided to handle different types of requests:\n"
                "- Calendar/scheduling requests → calendar_agent\n"
                "- Email requests → email_agent\n" 
                "- GitHub/repository or issue requests → github_agent\n"
                "- Slack/messaging or channel requests → slack_agent\n"
                "Always use the appropriate tool. Never handle requests yourself."
            ),
            tools=[
                calendar_agent.as_tool(
                    tool_name="handle_calendar_request",
                    tool_description="Handle calendar, scheduling, meeting, and event requests"
                ),
                email_agent.as_tool(
                    tool_name="handle_email_request", 
                    tool_description="Handle email composition, sending, and management requests"
                ),
                github_agent.as_tool(
                    tool_name="handle_github_request",
                    tool_description="Handle GitHub issues, repositories, and pull request requests"
                ),
                slack_agent.as_tool(
                    tool_name="handle_slack_request",
                    tool_description="Handle Slack messaging and team communication requests"
                )
            ],
            model=model
        )
        
        agents_available = True
        logger.info("✅ Gemini Agents SDK configured successfully with gemini-2.5-flash")
        
    except Exception as e:
        logger.error(f"Failed to configure Gemini Agents SDK: {e}")
        agents_available = False


# Initialize agents on module load
setup_agents_config()


class IntentType(Enum):
    """Enumeration of supported intent types"""
    CALENDAR_CREATE_EVENT = "calendar_create_event"
    CALENDAR_LIST_EVENTS = "calendar_list_events"
    CALENDAR_UPDATE_EVENT = "calendar_update_event"
    CALENDAR_DELETE_EVENT = "calendar_delete_event"

    EMAIL_SEND = "email_send"
    EMAIL_LIST = "email_list"
    EMAIL_READ = "email_read"

    GITHUB_CREATE_ISSUE = "github_create_issue"
    GITHUB_LIST_REPOS = "github_list_repos"
    GITHUB_CREATE_PR = "github_create_pr"

    SLACK_SEND_MESSAGE = "slack_send_message"
    SLACK_LIST_CHANNELS = "slack_list_channels"

    UNKNOWN = "unknown"


class ConfidenceLevel(Enum):
    """Confidence levels for intent classification"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class IntentAnalysisResult:
    """Result of intent analysis"""
    intent_type: IntentType
    confidence: ConfidenceLevel
    parameters: Dict[str, Any]
    required_permissions: List[str]
    service_name: Optional[str] = None
    clarification_needed: bool = False
    clarification_questions: List[str] = None


class SimpleAIAgent:
    """AI Agent for Calendar, Email, GitHub & Slack services only"""

    def __init__(self):
        self.triage_agent = triage_agent
        self.config = agents_config
        self.available = agents_available
        self._init_permission_mappings()

    async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user message using OpenAI Agents SDK with fallback"""
        if self.available and self.triage_agent and self.config:
            try:
                result = await Runner.run(
                    starting_agent=self.triage_agent,
                    input=user_message,
                    run_config=self.config
                )
                
                return {
                    "response": result.final_output or "Request processed successfully",
                    "intent_type": "general_query",
                    "confidence": "high",
                    "service_name": None,
                    "parameters": {},
                    "required_permissions": [],
                    "clarification_needed": False,
                    "clarification_questions": []
                }
                
            except Exception as e:
                logger.error(f"Agents SDK failed: {e}. Using fallback.")
                return await self._fallback_process_message(user_message, user_context)
        
        logger.info("Agents SDK not available, using fallback")
        return await self._fallback_process_message(user_message, user_context)

    async def _fallback_process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Rule-based fallback processing - only for Calendar, Email, GitHub, Slack"""
        msg_lower = user_message.lower()
        
        # Calendar requests
        if any(word in msg_lower for word in ['schedule', 'meeting', 'calendar', 'event', 'appointment', 'book', 'birthday party']):
            title = "Team Meeting"
            if "team meeting" in msg_lower:
                title = "Team Meeting"
            elif "birthday" in msg_lower or "birthday party" in msg_lower:
                title = "Birthday Party"
            elif "appointment" in msg_lower:
                title = "Appointment"
            elif "event" in msg_lower:
                title = "Event"
            
            # Extract time
            time = "21:00"
            time_match = re.search(r'(\d{1,2})\s*(pm|am)', msg_lower)
            if time_match:
                hours, period = time_match.groups()
                hour24 = int(hours)
                if period == 'pm' and hour24 != 12:
                    hour24 += 12
                elif period == 'am' and hour24 == 12:
                    hour24 = 0
                time = f"{hour24:02d}:00"
            
            # Extract date
            date = "2026-04-07"
            if "tomorrow" in msg_lower:
                date = "2026-04-07"
            elif "today" in msg_lower:
                date = "2026-04-06"
            
            return {
                "response": f"I'll schedule a {title.lower()} for {date} at {time}. Let me create that calendar event for you now...",
                "intent_type": "calendar_create_event",
                "confidence": "high",
                "service_name": "google",
                "parameters": {"title": title, "date": date, "time": time},
                "required_permissions": ["https://www.googleapis.com/auth/calendar"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Email requests
        if any(word in msg_lower for word in ['email', 'mail', 'send']) and ('@' in user_message or any(word in msg_lower for word in ['to', 'send'])):
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
            to_email = email_match.group(0) if email_match else "recipient@example.com"
            
            subject = "Message from CipherMate AI"
            if "follow-up" in msg_lower:
                subject = "Follow-up Message"
            elif "project" in msg_lower:
                subject = "Project Update"
            
            return {
                "response": f"I'll send an email to {to_email} with the subject '{subject}'. Let me compose that for you now...",
                "intent_type": "email_send",
                "confidence": "high",
                "service_name": "google",
                "parameters": {"to": to_email, "subject": subject, "body": user_message},
                "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # GitHub requests
        if any(word in msg_lower for word in ['github', 'issue', 'repository', 'repo', 'pull request']):
            return {
                "response": "I'll help you create a GitHub issue.",
                "intent_type": "github_create_issue",
                "confidence": "high",
                "service_name": "github", 
                "parameters": {"title": "New Issue", "body": user_message},
                "required_permissions": ["repo"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Slack requests
        if any(word in msg_lower for word in ['slack', 'message', 'channel', 'team']):
            return {
                "response": "I'll help you send a message on Slack.",
                "intent_type": "slack_send_message",
                "confidence": "high",
                "service_name": "slack",
                "parameters": {"channel": "#general", "message": user_message},
                "required_permissions": ["chat:write"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Default response (no math/programming/general chit-chat)
        return {
            "response": "Hello! I'm CipherMate. I can help you with:\n\n"
                       "📅 Google Calendar events\n"
                       "📧 Gmail emails\n"
                       "🐙 GitHub issues\n"
                       "💬 Slack messages\n\n"
                       f"What would you like me to do with: \"{user_message}\"?",
            "intent_type": "unknown",
            "confidence": "medium",
            "service_name": None, 
            "parameters": {},
            "required_permissions": [],
            "clarification_needed": True,
            "clarification_questions": ["Please specify if you want to create a calendar event, send an email, create a GitHub issue, or send a Slack message."]
        }

    def _init_permission_mappings(self) -> None:
        """Initialize permission requirement mappings"""
        self.permission_mappings = {
            IntentType.CALENDAR_CREATE_EVENT: {
                "service": "google",
                "scopes": ["https://www.googleapis.com/auth/calendar"],
                "description": "Create calendar events",
                "risk_level": "medium"
            },
            IntentType.EMAIL_SEND: {
                "service": "google",
                "scopes": ["https://www.googleapis.com/auth/gmail.send"],
                "description": "Send emails",
                "risk_level": "high"
            },
            IntentType.GITHUB_CREATE_ISSUE: {
                "service": "github",
                "scopes": ["repo"],
                "description": "Create GitHub issues",
                "risk_level": "medium"
            },
            IntentType.SLACK_SEND_MESSAGE: {
                "service": "slack",
                "scopes": ["chat:write"],
                "description": "Send Slack messages",
                "risk_level": "medium"
            },
        }

    async def analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
        """Analyze user message to determine intent"""
        return self._fallback_analyze_intent(user_message, user_context)

    def _fallback_analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
        """Fallback rule-based intent analysis - only services related"""
        msg = user_message.lower()

        # Calendar intent
        if any(word in msg for word in ['calendar', 'schedule', 'meeting', 'appointment', 'event', 'party', 'birthday', 'create']) and \
           any(word in msg for word in ['tomorrow', 'today', 'pm', 'am', 'time', 'date']):
            
            title = "Meeting"
            if "meeting" in msg:
                title = "Meeting"
            elif "appointment" in msg:
                title = "Appointment"
            elif "party" in msg or "birthday" in msg:
                title = "Birthday Party"
            elif "event" in msg:
                title = "Event"
            
            time = "17:00"
            time_match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(pm|am)', msg)
            if time_match:
                hours, minutes, period = time_match.groups()
                minutes = minutes or '00'
                hour24 = int(hours)
                if period == 'pm' and hour24 != 12:
                    hour24 += 12
                elif period == 'am' and hour24 == 12:
                    hour24 = 0
                time = f"{hour24:02d}:{minutes}"
            
            date = "2026-04-06"
            if "tomorrow" in msg:
                date = "2026-04-07"
            elif "today" in msg:
                date = "2026-04-06"
            
            return IntentAnalysisResult(
                intent_type=IntentType.CALENDAR_CREATE_EVENT,
                confidence=ConfidenceLevel.HIGH,
                parameters={"title": title, "date": date, "time": time},
                required_permissions=["https://www.googleapis.com/auth/calendar"],
                service_name="google",
                clarification_needed=False,
                clarification_questions=[]
            )
        
        # Email intent
        elif any(word in msg for word in ['email', 'mail', 'send']) and ('@' in user_message or any(word in msg for word in ['to', 'send'])):
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
            to_email = email_match.group(0) if email_match else "recipient@example.com"
            
            subject = "Message from CipherMate AI"
            if "follow-up" in msg:
                subject = "Follow-up Message"
            elif "project" in msg:
                subject = "Project Update"
            
            return IntentAnalysisResult(
                intent_type=IntentType.EMAIL_SEND,
                confidence=ConfidenceLevel.HIGH,
                parameters={"to": to_email, "subject": subject, "body": user_message},
                required_permissions=["https://www.googleapis.com/auth/gmail.send"],
                service_name="google",
                clarification_needed=False,
                clarification_questions=[]
            )
        
        # GitHub intent
        elif any(word in msg for word in ['github', 'issue', 'repository', 'repo', 'pull request']):
            return IntentAnalysisResult(
                intent_type=IntentType.GITHUB_CREATE_ISSUE,
                confidence=ConfidenceLevel.HIGH,
                parameters={"title": "New Issue", "body": user_message},
                required_permissions=["repo"],
                service_name="github",
                clarification_needed=False,
                clarification_questions=[]
            )
        
        # Slack intent
        elif any(word in msg for word in ['slack', 'message', 'channel', 'team']):
            return IntentAnalysisResult(
                intent_type=IntentType.SLACK_SEND_MESSAGE,
                confidence=ConfidenceLevel.HIGH,
                parameters={"channel": "#general", "message": user_message},
                required_permissions=["chat:write"],
                service_name="slack",
                clarification_needed=False,
                clarification_questions=[]
            )
        
        # Unknown
        else:
            return IntentAnalysisResult(
                intent_type=IntentType.UNKNOWN,
                confidence=ConfidenceLevel.LOW,
                parameters={},
                required_permissions=[],
                service_name=None,
                clarification_needed=True,
                clarification_questions=["Please tell me clearly if you want to create a calendar event, send an email, create a GitHub issue, or send a Slack message."]
            )

    async def generate_response(self, intent_result: IntentAnalysisResult, user_message: str) -> str:
        """Generate natural language response"""
        return self._generate_fallback_response(intent_result)

    def _generate_fallback_response(self, intent_result: IntentAnalysisResult) -> str:
        """Generate fallback response"""
        if intent_result.clarification_needed and intent_result.clarification_questions:
            return " ".join(intent_result.clarification_questions)

        if intent_result.required_permissions:
            return f"To help you with this, I'll need access to {intent_result.service_name or 'the required service'}. Please grant the necessary permissions."

        responses = {
            IntentType.CALENDAR_CREATE_EVENT: "I'll help you create a calendar event.",
            IntentType.EMAIL_SEND: "I'll help you send an email.",
            IntentType.GITHUB_CREATE_ISSUE: "I'll help you create a GitHub issue.",
            IntentType.SLACK_SEND_MESSAGE: "I'll help you send a Slack message.",
            IntentType.UNKNOWN: "I'm not sure I understand. Please specify the service (Calendar, Email, GitHub, or Slack)."
        }

        return responses.get(intent_result.intent_type, "How can I help you with Calendar, Email, GitHub, or Slack?")


# Create singleton instance
simple_ai_agent = SimpleAIAgent()





# """AI Agent implementation for Calendar, Email, GitHub & Slack only"""

# import logging
# from typing import Dict, List, Optional, Any
# from enum import Enum
# from dataclasses import dataclass
# import re

# from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
# from app.core.config import settings

# logger = logging.getLogger(__name__)

# # Configure OpenAI Agents SDK
# agents_config = None
# triage_agent = None
# agents_available = False


# def setup_agents_config():
#     """Setup OpenAI Agents SDK configuration with Gemini"""
#     global agents_config, triage_agent, agents_available
    
#     if not settings.GEMINI_API_KEY:
#         logger.warning("GEMINI_API_KEY not configured - Agents SDK disabled")
#         agents_available = False
#         return
    
#     try:
#         # Setup OpenAI-compatible client for Gemini API
#         external_client = AsyncOpenAI(
#             api_key=settings.GEMINI_API_KEY,
#             base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#         )
        
#         # Setup model
#         model = OpenAIChatCompletionsModel(
#             model="gemini-2.5-flash",
#             openai_client=external_client,
#         )
        
#         # Setup run configuration
#         agents_config = RunConfig(
#             model=model,
#             model_provider=external_client,
#             tracing_disabled=True
#         )
        
#         # Setup specialized agents
#         calendar_agent = Agent(
#             name="calendar_agent",
#             instructions=(
#                 "You are a calendar management specialist. "
#                 "You help users create, update, and manage calendar events. "
#                 "Extract event details like title, date, time, and duration from user requests. "
#                 "Always respond with structured information about calendar operations."
#             ),
#             handoff_description="Handles calendar and scheduling requests",
#             model=model
#         )
        
#         email_agent = Agent(
#             name="email_agent", 
#             instructions=(
#                 "You are an email management specialist. "
#                 "You help users compose, send, and manage emails. "
#                 "Extract recipient, subject, and body content from user requests. "
#                 "Always respond with structured information about email operations."
#             ),
#             handoff_description="Handles email composition and management",
#             model=model
#         )
        
#         github_agent = Agent(
#             name="github_agent",
#             instructions=(
#                 "You are a GitHub management specialist. "
#                 "You help users create issues, manage repositories, and handle pull requests. "
#                 "Extract repository names, issue titles, descriptions, and labels from user requests. "
#                 "Always respond with structured information about GitHub operations."
#             ),
#             handoff_description="Handles GitHub repository and issue management",
#             model=model
#         )
        
#         slack_agent = Agent(
#             name="slack_agent",
#             instructions=(
#                 "You are a Slack communication specialist. "
#                 "You help users send messages, manage channels, and handle team communications. "
#                 "Extract channel names, message content, and recipient information from user requests. "
#                 "Always respond with structured information about Slack operations."
#             ),
#             handoff_description="Handles Slack messaging and team communication",
#             model=model
#         )
        
#         # Setup triage agent (removed general_agent)
#         triage_agent = Agent(
#             name="triage_agent",
#             instructions=(
#                 "You are an intelligent triage agent for CipherMate AI Assistant. "
#                 "You analyze user requests and route them to the appropriate specialist agent. "
#                 "Use the tools provided to handle different types of requests:\n"
#                 "- Calendar/scheduling requests → calendar_agent\n"
#                 "- Email requests → email_agent\n" 
#                 "- GitHub/repository or issue requests → github_agent\n"
#                 "- Slack/messaging or channel requests → slack_agent\n"
#                 "Always use the appropriate tool. Never handle requests yourself."
#             ),
#             tools=[
#                 calendar_agent.as_tool(
#                     tool_name="handle_calendar_request",
#                     tool_description="Handle calendar, scheduling, meeting, and event requests"
#                 ),
#                 email_agent.as_tool(
#                     tool_name="handle_email_request", 
#                     tool_description="Handle email composition, sending, and management requests"
#                 ),
#                 github_agent.as_tool(
#                     tool_name="handle_github_request",
#                     tool_description="Handle GitHub issues, repositories, and pull request requests"
#                 ),
#                 slack_agent.as_tool(
#                     tool_name="handle_slack_request",
#                     tool_description="Handle Slack messaging and team communication requests"
#                 )
#             ],
#             model=model
#         )
        
#         agents_available = True
#         logger.info("✅ Gemini Agents SDK configured successfully with gemini-2.5-flash")
        
#     except Exception as e:
#         logger.error(f"Failed to configure Gemini Agents SDK: {e}")
#         agents_available = False


# # Initialize agents on module load
# setup_agents_config()


# class IntentType(Enum):
#     """Enumeration of supported intent types"""
#     CALENDAR_CREATE_EVENT = "calendar_create_event"
#     CALENDAR_LIST_EVENTS = "calendar_list_events"
#     CALENDAR_UPDATE_EVENT = "calendar_update_event"
#     CALENDAR_DELETE_EVENT = "calendar_delete_event"

#     EMAIL_SEND = "email_send"
#     EMAIL_LIST = "email_list"
#     EMAIL_READ = "email_read"

#     GITHUB_CREATE_ISSUE = "github_create_issue"
#     GITHUB_LIST_REPOS = "github_list_repos"
#     GITHUB_CREATE_PR = "github_create_pr"

#     SLACK_SEND_MESSAGE = "slack_send_message"
#     SLACK_LIST_CHANNELS = "slack_list_channels"

#     UNKNOWN = "unknown"


# class ConfidenceLevel(Enum):
#     """Confidence levels for intent classification"""
#     HIGH = "high"
#     MEDIUM = "medium"
#     LOW = "low"


# @dataclass
# class IntentAnalysisResult:
#     """Result of intent analysis"""
#     intent_type: IntentType
#     confidence: ConfidenceLevel
#     parameters: Dict[str, Any]
#     required_permissions: List[str]
#     service_name: Optional[str] = None
#     clarification_needed: bool = False
#     clarification_questions: List[str] = None


# class SimpleAIAgent:
#     """AI Agent for Calendar, Email, GitHub & Slack services only"""

#     def __init__(self):
#         self.triage_agent = triage_agent
#         self.config = agents_config
#         self.available = agents_available
#         self._init_permission_mappings()

#     async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
#         """Process a user message using OpenAI Agents SDK with fallback"""
#         if self.available and self.triage_agent and self.config:
#             try:
#                 result = await Runner.run(
#                     starting_agent=self.triage_agent,
#                     input=user_message,
#                     run_config=self.config
#                 )
                
#                 return {
#                     "response": result.final_output or "Request processed successfully",
#                     "intent_type": "general_query",
#                     "confidence": "high",
#                     "service_name": None,
#                     "parameters": {},
#                     "required_permissions": [],
#                     "clarification_needed": False,
#                     "clarification_questions": []
#                 }
                
#             except Exception as e:
#                 logger.error(f"Agents SDK failed: {e}. Using fallback.")
#                 return await self._fallback_process_message(user_message, user_context)
        
#         logger.info("Agents SDK not available, using fallback")
#         return await self._fallback_process_message(user_message, user_context)

#     async def _fallback_process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
#         """Rule-based fallback processing - only for Calendar, Email, GitHub, Slack"""
#         msg_lower = user_message.lower()
        
#         # Calendar requests
#         if any(word in msg_lower for word in ['schedule', 'meeting', 'calendar', 'event', 'appointment', 'book', 'birthday party']):
#             title = "Team Meeting"
#             if "team meeting" in msg_lower:
#                 title = "Team Meeting"
#             elif "birthday" in msg_lower or "birthday party" in msg_lower:
#                 title = "Birthday Party"
#             elif "appointment" in msg_lower:
#                 title = "Appointment"
#             elif "event" in msg_lower:
#                 title = "Event"
            
#             # Extract time
#             time = "21:00"
#             time_match = re.search(r'(\d{1,2})\s*(pm|am)', msg_lower)
#             if time_match:
#                 hours, period = time_match.groups()
#                 hour24 = int(hours)
#                 if period == 'pm' and hour24 != 12:
#                     hour24 += 12
#                 elif period == 'am' and hour24 == 12:
#                     hour24 = 0
#                 time = f"{hour24:02d}:00"
            
#             # Extract date
#             date = "2026-04-07"
#             if "tomorrow" in msg_lower:
#                 date = "2026-04-07"
#             elif "today" in msg_lower:
#                 date = "2026-04-06"
            
#             return {
#                 "response": f"I'll schedule a {title.lower()} for {date} at {time}. Let me create that calendar event for you now...",
#                 "intent_type": "calendar_create_event",
#                 "confidence": "high",
#                 "service_name": "google",
#                 "parameters": {"title": title, "date": date, "time": time},
#                 "required_permissions": ["https://www.googleapis.com/auth/calendar"],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Email requests
#         if any(word in msg_lower for word in ['email', 'mail', 'send']) and ('@' in user_message or any(word in msg_lower for word in ['to', 'send'])):
#             email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
#             to_email = email_match.group(0) if email_match else "recipient@example.com"
            
#             subject = "Message from CipherMate AI"
#             if "follow-up" in msg_lower:
#                 subject = "Follow-up Message"
#             elif "project" in msg_lower:
#                 subject = "Project Update"
            
#             return {
#                 "response": f"I'll send an email to {to_email} with the subject '{subject}'. Let me compose that for you now...",
#                 "intent_type": "email_send",
#                 "confidence": "high",
#                 "service_name": "google",
#                 "parameters": {"to": to_email, "subject": subject, "body": user_message},
#                 "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # GitHub requests
#         if any(word in msg_lower for word in ['github', 'issue', 'repository', 'repo', 'pull request']):
#             return {
#                 "response": "I'll help you create a GitHub issue.",
#                 "intent_type": "github_create_issue",
#                 "confidence": "high",
#                 "service_name": "github", 
#                 "parameters": {"title": "New Issue", "body": user_message},
#                 "required_permissions": ["repo"],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Slack requests
#         if any(word in msg_lower for word in ['slack', 'message', 'channel', 'team']):
#             return {
#                 "response": "I'll help you send a message on Slack.",
#                 "intent_type": "slack_send_message",
#                 "confidence": "high",
#                 "service_name": "slack",
#                 "parameters": {"channel": "#general", "message": user_message},
#                 "required_permissions": ["chat:write"],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Default response (no math/programming/general chit-chat)
#         return {
#             "response": "Hello! I'm CipherMate. I can help you with:\n\n"
#                        "📅 Google Calendar events\n"
#                        "📧 Gmail emails\n"
#                        "🐙 GitHub issues\n"
#                        "💬 Slack messages\n\n"
#                        f"What would you like me to do with: \"{user_message}\"?",
#             "intent_type": "unknown",
#             "confidence": "medium",
#             "service_name": None, 
#             "parameters": {},
#             "required_permissions": [],
#             "clarification_needed": True,
#             "clarification_questions": ["Please specify if you want to create a calendar event, send an email, create a GitHub issue, or send a Slack message."]
#         }

#     def _init_permission_mappings(self) -> None:
#         """Initialize permission requirement mappings"""
#         self.permission_mappings = {
#             IntentType.CALENDAR_CREATE_EVENT: {
#                 "service": "google",
#                 "scopes": ["https://www.googleapis.com/auth/calendar"],
#                 "description": "Create calendar events",
#                 "risk_level": "medium"
#             },
#             IntentType.EMAIL_SEND: {
#                 "service": "google",
#                 "scopes": ["https://www.googleapis.com/auth/gmail.send"],
#                 "description": "Send emails",
#                 "risk_level": "high"
#             },
#             IntentType.GITHUB_CREATE_ISSUE: {
#                 "service": "github",
#                 "scopes": ["repo"],
#                 "description": "Create GitHub issues",
#                 "risk_level": "medium"
#             },
#             IntentType.SLACK_SEND_MESSAGE: {
#                 "service": "slack",
#                 "scopes": ["chat:write"],
#                 "description": "Send Slack messages",
#                 "risk_level": "medium"
#             },
#         }

#     async def analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
#         """Analyze user message to determine intent"""
#         return self._fallback_analyze_intent(user_message, user_context)

#     def _fallback_analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
#         """Fallback rule-based intent analysis - only services related"""
#         msg = user_message.lower()

#         # Calendar intent
#         if any(word in msg for word in ['calendar', 'schedule', 'meeting', 'appointment', 'event', 'party', 'birthday', 'create']) and \
#            any(word in msg for word in ['tomorrow', 'today', 'pm', 'am', 'time', 'date']):
            
#             title = "Meeting"
#             if "meeting" in msg:
#                 title = "Meeting"
#             elif "appointment" in msg:
#                 title = "Appointment"
#             elif "party" in msg or "birthday" in msg:
#                 title = "Birthday Party"
#             elif "event" in msg:
#                 title = "Event"
            
#             time = "17:00"
#             time_match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(pm|am)', msg)
#             if time_match:
#                 hours, minutes, period = time_match.groups()
#                 minutes = minutes or '00'
#                 hour24 = int(hours)
#                 if period == 'pm' and hour24 != 12:
#                     hour24 += 12
#                 elif period == 'am' and hour24 == 12:
#                     hour24 = 0
#                 time = f"{hour24:02d}:{minutes}"
            
#             date = "2026-04-06"
#             if "tomorrow" in msg:
#                 date = "2026-04-07"
#             elif "today" in msg:
#                 date = "2026-04-06"
            
#             return IntentAnalysisResult(
#                 intent_type=IntentType.CALENDAR_CREATE_EVENT,
#                 confidence=ConfidenceLevel.HIGH,
#                 parameters={"title": title, "date": date, "time": time},
#                 required_permissions=["https://www.googleapis.com/auth/calendar"],
#                 service_name="google",
#                 clarification_needed=False,
#                 clarification_questions=[]
#             )
        
#         # Email intent
#         elif any(word in msg for word in ['email', 'mail', 'send']) and ('@' in user_message or any(word in msg for word in ['to', 'send'])):
#             email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
#             to_email = email_match.group(0) if email_match else "recipient@example.com"
            
#             subject = "Message from CipherMate AI"
#             if "follow-up" in msg:
#                 subject = "Follow-up Message"
#             elif "project" in msg:
#                 subject = "Project Update"
            
#             return IntentAnalysisResult(
#                 intent_type=IntentType.EMAIL_SEND,
#                 confidence=ConfidenceLevel.HIGH,
#                 parameters={"to": to_email, "subject": subject, "body": user_message},
#                 required_permissions=["https://www.googleapis.com/auth/gmail.send"],
#                 service_name="google",
#                 clarification_needed=False,
#                 clarification_questions=[]
#             )
        
#         # GitHub intent
#         elif any(word in msg for word in ['github', 'issue', 'repository', 'repo', 'pull request']):
#             return IntentAnalysisResult(
#                 intent_type=IntentType.GITHUB_CREATE_ISSUE,
#                 confidence=ConfidenceLevel.HIGH,
#                 parameters={"title": "New Issue", "body": user_message},
#                 required_permissions=["repo"],
#                 service_name="github",
#                 clarification_needed=False,
#                 clarification_questions=[]
#             )
        
#         # Slack intent
#         elif any(word in msg for word in ['slack', 'message', 'channel', 'team']):
#             return IntentAnalysisResult(
#                 intent_type=IntentType.SLACK_SEND_MESSAGE,
#                 confidence=ConfidenceLevel.HIGH,
#                 parameters={"channel": "#general", "message": user_message},
#                 required_permissions=["chat:write"],
#                 service_name="slack",
#                 clarification_needed=False,
#                 clarification_questions=[]
#             )
        
#         # Unknown
#         else:
#             return IntentAnalysisResult(
#                 intent_type=IntentType.UNKNOWN,
#                 confidence=ConfidenceLevel.LOW,
#                 parameters={},
#                 required_permissions=[],
#                 service_name=None,
#                 clarification_needed=True,
#                 clarification_questions=["Please tell me clearly if you want to create a calendar event, send an email, create a GitHub issue, or send a Slack message."]
#             )

#     async def generate_response(self, intent_result: IntentAnalysisResult, user_message: str) -> str:
#         """Generate natural language response"""
#         return self._generate_fallback_response(intent_result)

#     def _generate_fallback_response(self, intent_result: IntentAnalysisResult) -> str:
#         """Generate fallback response"""
#         if intent_result.clarification_needed and intent_result.clarification_questions:
#             return " ".join(intent_result.clarification_questions)

#         if intent_result.required_permissions:
#             return f"To help you with this, I'll need access to {intent_result.service_name or 'the required service'}. Please grant the necessary permissions."

#         responses = {
#             IntentType.CALENDAR_CREATE_EVENT: "I'll help you create a calendar event.",
#             IntentType.EMAIL_SEND: "I'll help you send an email.",
#             IntentType.GITHUB_CREATE_ISSUE: "I'll help you create a GitHub issue.",
#             IntentType.SLACK_SEND_MESSAGE: "I'll help you send a Slack message.",
#             IntentType.UNKNOWN: "I'm not sure I understand. Please specify the service (Calendar, Email, GitHub, or Slack)."
#         }

#         return responses.get(intent_result.intent_type, "How can I help you with Calendar, Email, GitHub, or Slack?")


# # Create singleton instance
# simple_ai_agent = SimpleAIAgent()








# # """AI Agent implementation using OpenAI Agents SDK"""

# # import json
# # import logging
# # import os
# # from typing import Dict, List, Optional, Any
# # from enum import Enum
# # from dataclasses import dataclass
# # import asyncio
# # from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
# # from app.core.config import settings

# # logger = logging.getLogger(__name__)

# # # Configure OpenAI Agents SDK
# # agents_config = None
# # triage_agent = None
# # agents_available = False

# # def setup_agents_config():
# #     """Setup OpenAI Agents SDK configuration with Gemini"""
# #     global agents_config, triage_agent, agents_available
    
# #     if not settings.GEMINI_API_KEY:
# #         logger.warning("GEMINI_API_KEY not configured - Using rule-based fallback only")
# #         return
    
# #     try:
# #         # Setup OpenAI-compatible client for Gemini API
# #         external_client = AsyncOpenAI(
# #             api_key=settings.GEMINI_API_KEY,
# #             base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# #         )
        
# #         # Setup model
# #         model = OpenAIChatCompletionsModel(
# #             model="gemini-2.5-flash",
# #             openai_client=external_client,
# #         )
        
# #         # Setup run configuration
# #         agents_config = RunConfig(
# #             model=model,
# #             model_provider=external_client,
# #             tracing_disabled=True
# #         )
        
# #         # Setup specialized agents
# #         calendar_agent = Agent(
# #             name="calendar_agent",
# #             instructions=(
# #                 "You are a calendar management specialist. "
# #                 "You help users create, update, and manage calendar events. "
# #                 "Extract event details like title, date, time, and duration from user requests. "
# #                 "Always respond with structured information about calendar operations."
# #             ),
# #             handoff_description="Handles calendar and scheduling requests",
# #             model=model
# #         )
        
# #         email_agent = Agent(
# #             name="email_agent", 
# #             instructions=(
# #                 "You are an email management specialist. "
# #                 "You help users compose, send, and manage emails. "
# #                 "Extract recipient, subject, and body content from user requests. "
# #                 "Always respond with structured information about email operations."
# #             ),
# #             handoff_description="Handles email composition and management",
# #             model=model
# #         )
        
# #         github_agent = Agent(
# #             name="github_agent",
# #             instructions=(
# #                 "You are a GitHub management specialist. "
# #                 "You help users create issues, manage repositories, and handle pull requests. "
# #                 "Extract repository names, issue titles, descriptions, and labels from user requests. "
# #                 "Always respond with structured information about GitHub operations."
# #             ),
# #             handoff_description="Handles GitHub repository and issue management",
# #             model=model
# #         )
        
# #         slack_agent = Agent(
# #             name="slack_agent",
# #             instructions=(
# #                 "You are a Slack communication specialist. "
# #                 "You help users send messages, manage channels, and handle team communications. "
# #                 "Extract channel names, message content, and recipient information from user requests. "
# #                 "Always respond with structured information about Slack operations."
# #             ),
# #             handoff_description="Handles Slack messaging and team communication",
# #             model=model
# #         )
        
# #         general_agent = Agent(
# #             name="general_agent",
# #             instructions=(
# #                 "You are a general purpose AI assistant. "
# #                 "You handle greetings, general questions, math calculations, and programming help. "
# #                 "Be friendly, helpful, and provide clear responses to user queries. "
# #                 "For math problems, calculate and show the result clearly."
# #             ),
# #             handoff_description="Handles general queries, greetings, and calculations",
# #             model=model
# #         )
        
# #         # Setup triage agent that routes to specialized agents
# #         triage_agent = Agent(
# #             name="triage_agent",
# #             instructions=(
# #                 "You are an intelligent triage agent for CipherMate AI Assistant. "
# #                 "You analyze user requests and route them to the appropriate specialist agent. "
# #                 "Use the tools provided to handle different types of requests:\n"
# #                 "- Calendar/scheduling requests → calendar_agent\n"
# #                 "- Email requests → email_agent\n" 
# #                 "- GitHub/repository requests → github_agent\n"
# #                 "- Slack/messaging requests → slack_agent\n"
# #                 "- General questions, greetings, math → general_agent\n"
# #                 "Always use the appropriate tool, never handle requests directly yourself."
# #             ),
# #             tools=[
# #                 calendar_agent.as_tool(
# #                     tool_name="handle_calendar_request",
# #                     tool_description="Handle calendar, scheduling, meeting, and event requests"
# #                 ),
# #                 email_agent.as_tool(
# #                     tool_name="handle_email_request", 
# #                     tool_description="Handle email composition, sending, and management requests"
# #                 ),
# #                 github_agent.as_tool(
# #                     tool_name="handle_github_request",
# #                     tool_description="Handle GitHub issues, repositories, and pull request requests"
# #                 ),
# #                 slack_agent.as_tool(
# #                     tool_name="handle_slack_request",
# #                     tool_description="Handle Slack messaging and team communication requests"
# #                 ),
# #                 general_agent.as_tool(
# #                     tool_name="handle_general_request",
# #                     tool_description="Handle general questions, greetings, math calculations, and programming help"
# #                 )
# #             ],
# #             model=model
# #         )
        
# #         agents_available = True
# #         logger.info("✅ Gemini Agents SDK configured successfully with gemini-2.5-flash")
        
# #     except Exception as e:
# #         logger.error(f"Failed to configure Gemini Agents SDK: {e}")
# #         logger.warning("⚠️ Gemini Agents DISABLED - Using rule-based fallback only")
# #         agents_available = False

# # # Initialize agents on module load
# # setup_agents_config()


# # class IntentType(Enum):
# #     """Enumeration of supported intent types"""
# #     CALENDAR_CREATE_EVENT = "calendar_create_event"
# #     CALENDAR_LIST_EVENTS = "calendar_list_events"
# #     CALENDAR_UPDATE_EVENT = "calendar_update_event"
# #     CALENDAR_DELETE_EVENT = "calendar_delete_event"

# #     EMAIL_SEND = "email_send"
# #     EMAIL_LIST = "email_list"
# #     EMAIL_READ = "email_read"

# #     GITHUB_CREATE_ISSUE = "github_create_issue"
# #     GITHUB_LIST_REPOS = "github_list_repos"
# #     GITHUB_CREATE_PR = "github_create_pr"

# #     SLACK_SEND_MESSAGE = "slack_send_message"
# #     SLACK_LIST_CHANNELS = "slack_list_channels"

# #     GENERAL_QUERY = "general_query"
# #     PERMISSION_REQUEST = "permission_request"
# #     UNKNOWN = "unknown"


# # class ConfidenceLevel(Enum):
# #     """Confidence levels for intent classification"""
# #     HIGH = "high"
# #     MEDIUM = "medium"
# #     LOW = "low"


# # @dataclass
# # class IntentAnalysisResult:
# #     """Result of intent analysis"""
# #     intent_type: IntentType
# #     confidence: ConfidenceLevel
# #     parameters: Dict[str, Any]
# #     required_permissions: List[str]
# #     service_name: Optional[str] = None
# #     clarification_needed: bool = False
# #     clarification_questions: List[str] = None


# # class SimpleAIAgent:
# #     """AI Agent using OpenAI Agents SDK for intelligent routing and processing"""

# #     def __init__(self):
# #         """Initialize the AI agent with Agents SDK"""
# #         self.triage_agent = triage_agent
# #         self.config = agents_config
# #         self.available = agents_available
# #         # Remove any reference to self.client since we're using Agents SDK
# #         self._init_permission_mappings()

# #     async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
# #         """Process a user message using OpenAI Agents SDK"""
        
# #         try:
# #             # For speed, use fallback processing directly for now
# #             # The Agents SDK is causing 3+ second delays
# #             logger.info("Using fast fallback processing for better performance")
# #             return await self._fallback_process_message(user_message, user_context)
            
# #         except Exception as e:
# #             logger.error(f"Error processing message: {e}")
# #             return await self._fallback_process_message(user_message, user_context)

# #     async def _analyze_agent_response(self, user_message: str, agent_response: str) -> Dict[str, Any]:
# #         """Analyze agent response to extract intent and parameters"""
        
# #         msg_lower = user_message.lower()
# #         response_lower = agent_response.lower()
        
# #         # Determine intent based on message content and response
# #         if any(word in msg_lower for word in ['calendar', 'schedule', 'meeting', 'event', 'appointment']):
# #             # Extract calendar parameters
# #             import re
            
# #             title = "Meeting"
# #             if "birthday" in msg_lower:
# #                 title = "Birthday Party"
# #             elif "team meeting" in msg_lower:
# #                 title = "Team Meeting"
# #             elif "appointment" in msg_lower:
# #                 title = "Appointment"
            
# #             # Extract time
# #             time = "15:00"
# #             time_match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(pm|am)', msg_lower)
# #             if time_match:
# #                 hours, minutes, period = time_match.groups()
# #                 minutes = minutes or '00'
# #                 hour24 = int(hours)
# #                 if period == 'pm' and hour24 != 12:
# #                     hour24 += 12
# #                 elif period == 'am' and hour24 == 12:
# #                     hour24 = 0
# #                 time = f"{hour24:02d}:{minutes}"
            
# #             # Extract date
# #             date = "2026-04-06"
# #             if "tomorrow" in msg_lower:
# #                 date = "2026-04-06"
# #             elif "today" in msg_lower:
# #                 date = "2026-04-05"
            
# #             return {
# #                 "intent_type": "calendar_create_event",
# #                 "confidence": "high",
# #                 "service_name": "google",
# #                 "parameters": {"title": title, "date": date, "time": time},
# #                 "required_permissions": ["https://www.googleapis.com/auth/calendar"]
# #             }
            
# #         elif any(word in msg_lower for word in ['email', 'mail', 'send']):
# #             # Extract email parameters
# #             import re
            
# #             email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
# #             to_email = email_match.group(0) if email_match else "recipient@example.com"
            
# #             subject = "Message from CipherMate AI"
# #             if "follow-up" in msg_lower:
# #                 subject = "Follow-up Message"
# #             elif "project" in msg_lower:
# #                 subject = "Project Update"
            
# #             return {
# #                 "intent_type": "email_send",
# #                 "confidence": "high", 
# #                 "service_name": "google",
# #                 "parameters": {"to": to_email, "subject": subject, "body": user_message},
# #                 "required_permissions": ["https://www.googleapis.com/auth/gmail.send"]
# #             }
            
# #         elif any(word in msg_lower for word in ['github', 'issue', 'repository', 'repo', 'pull request']):
# #             return {
# #                 "intent_type": "github_create_issue",
# #                 "confidence": "high",
# #                 "service_name": "github", 
# #                 "parameters": {"title": "New Issue", "body": user_message},
# #                 "required_permissions": ["repo"]
# #             }
            
# #         elif any(word in msg_lower for word in ['slack', 'message', 'channel', 'team']):
# #             return {
# #                 "intent_type": "slack_send_message",
# #                 "confidence": "high",
# #                 "service_name": "slack",
# #                 "parameters": {"channel": "#general", "message": user_message},
# #                 "required_permissions": ["chat:write"]
# #             }
            
# #         else:
# #             # General query
# #             return {
# #                 "intent_type": "general_query",
# #                 "confidence": "high",
# #                 "service_name": None,
# #                 "parameters": {},
# #                 "required_permissions": []
# #             }

# #     async def _fallback_process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
# #         """Fallback processing when Agents SDK is not available"""
        
# #         msg_lower = user_message.lower()
        
# #         # Math calculations
# #         # if any(pattern in msg_lower for pattern in ['+', '-', '*', '/', '=']) and any(char.isdigit() for char in msg_lower):
# #             # Handle simple math
# #             import re
            
# #             # if '2+3' in msg_lower or '2 + 3' in msg_lower:
# #             #     return {
# #             #         "response": "2 + 3 = 5",
# #             #         "intent_type": "general_query",
# #             #         "confidence": "high",
# #             #         "service_name": None,
# #             #         "parameters": {},
# #             #         "required_permissions": [],
# #             #         "clarification_needed": False,
# #             #         "clarification_questions": []
# #             #     }
            
# #             # Try to evaluate simple expressions
# #         #     math_match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', msg_lower.replace('=?', '').replace('=', ''))
# #         #     if math_match:
# #         #         try:
# #         #             expression = math_match.group(1)
# #         #             result = eval(expression)  # Safe here since it's from our validated pattern
# #         #             return {
# #         #                 "response": f"{expression} = {result}",
# #         #                 "intent_type": "general_query",
# #         #                 "confidence": "high",
# #         #                 "service_name": None,
# #         #                 "parameters": {},
# #         #                 "required_permissions": [],
# #         #                 "clarification_needed": False,
# #         #                 "clarification_questions": []
# #         #             }
# #         #         except:
# #         #             pass
        
# #         # # Programming requests
# #         # if any(word in msg_lower for word in ['python', 'code', 'program', 'hello world', 'c++', 'javascript']):
# #         #     if 'python' in msg_lower and 'hello world' in msg_lower:
# #         #         response = "Here's a Python Hello World program:\n\n```python\nprint('Hello, World!')\n```\n\nThis prints 'Hello, World!' to the console!"
# #         #     elif 'c++' in msg_lower and 'hello world' in msg_lower:
# #         #         response = "Here's a C++ Hello World program:\n\n```cpp\n#include <iostream>\n\nint main() {\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}\n```"
# #         #     elif 'javascript' in msg_lower and 'hello world' in msg_lower:
# #         #         response = "Here's a JavaScript Hello World program:\n\n```javascript\nconsole.log('Hello, World!');\n```"
# #         #     else:
# #         #         response = "I can help you with programming! What specific language or task are you working on?"
            
# #         #     return {
# #         #         "response": response,
# #         #         "intent_type": "general_query", 
# #         #         "confidence": "high",
# #         #         "service_name": None,
# #         #         "parameters": {},
# #         #         "required_permissions": [],
# #         #         "clarification_needed": False,
# #         #         "clarification_questions": []
# #         #     }
        
# #         # Calendar requests
# #         if any(word in msg_lower for word in ['schedule', 'meeting', 'calendar', 'event', 'appointment', 'book']):
# #             import re
            
# #             # Extract title
# #             title = "Team Meeting"
# #             if "team meeting" in msg_lower:
# #                 title = "Team Meeting"
# #             elif "birthday" in msg_lower:
# #                 title = "Birthday Party"
# #             elif "appointment" in msg_lower:
# #                 title = "Appointment"
# #             elif "event" in msg_lower:
# #                 title = "Event"
            
# #             # Extract time
# #             time = "21:00"  # Default to 9 PM
# #             time_match = re.search(r'(\d{1,2})\s*(pm|am)', msg_lower)
# #             if time_match:
# #                 hours, period = time_match.groups()
# #                 hour24 = int(hours)
# #                 if period == 'pm' and hour24 != 12:
# #                     hour24 += 12
# #                 elif period == 'am' and hour24 == 12:
# #                     hour24 = 0
# #                 time = f"{hour24:02d}:00"
            
# #             # Extract date
# #             date = "2026-04-07"  # Tomorrow
# #             if "tomorrow" in msg_lower:
# #                 date = "2026-04-07"
# #             elif "today" in msg_lower:
# #                 date = "2026-04-06"
            
# #             return {
# #                 "response": f"Fallback I'll schedule a {title.lower()} for {date} at {time}. Let me create that calendar event for you now...",
# #                 "intent_type": "calendar_create_event",
# #                 "confidence": "high",
# #                 "service_name": "google",
# #                 "parameters": {"title": title, "date": date, "time": time},
# #                 "required_permissions": ["https://www.googleapis.com/auth/calendar"],
# #                 "clarification_needed": False,
# #                 "clarification_questions": []
# #             }
        
# #         # Email requests
# #         if any(word in msg_lower for word in ['email', 'mail', 'send']) and any(word in msg_lower for word in ['to', '@', 'message']):
# #             import re
            
# #             # Extract email
# #             email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
# #             to_email = email_match.group(0) if email_match else "recipient@example.com"
            
# #             # Extract subject
# #             subject = "Message from CipherMate AI"
# #             if "follow-up" in msg_lower:
# #                 subject = "Follow-up Message"
# #             elif "project" in msg_lower:
# #                 subject = "Project Update"
            
# #             return {
# #                 "response": f"I'll send an email to {to_email} with the subject '{subject}'. Let me compose that for you now...",
# #                 "intent_type": "email_send",
# #                 "confidence": "high",
# #                 "service_name": "google",
# #                 "parameters": {"to": to_email, "subject": subject, "body": user_message},
# #                 "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
# #                 "clarification_needed": False,
# #                 "clarification_questions": []
# #             }
        
# #         # Name/identity questions
# #         # if any(word in msg_lower for word in ['name', 'who are you', 'what are you', 'introduce yourself']):
# #         #     return {
# #         #         "response": "I'm CipherMate, your AI assistant! I can help you with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with?",
# #         #         "intent_type": "general_query",
# #         #         "confidence": "high",
# #         #         "service_name": None,
# #         #         "parameters": {},
# #         #         "required_permissions": [],
# #         #         "clarification_needed": False,
# #         #         "clarification_questions": []
# #         #     }
        
# #         # Greetings
# #         # if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'how are you']):
# #         #     return {
# #         #         "response": "Hello! I'm CipherMate, your AI assistant. I can help you with:\n\n📅 Calendar events\n📧 Emails\n🐙 GitHub issues\n💬 Slack messages\n🔢 Math calculations\n💻 Programming help\n\nWhat would you like to do today?",
# #         #         "intent_type": "general_query",
# #         #         "confidence": "high", 
# #         #         "service_name": None,
# #         #         "parameters": {},
# #         #         "required_permissions": [],
# #         #         "clarification_needed": False,
# #         #         "clarification_questions": []
# #         #     }
        
# #         # Default response
# #         # return {
# #         #     "response": f"I'm CipherMate, your AI assistant! I can help with:\n\n📅 Calendar events\n📧 Emails\n� GidtHub issues\n�m Slack messages\n� Math callculations\n� Progaramming help\n\nFor your request \"{user_message}\", could you provide more specific details about what you'd like me to do?",
# #         #     "intent_type": "general_query",
# #         #     "confidence": "medium",
# #         #     "service_name": None, 
# #         #     "parameters": {},
# #         #     "required_permissions": [],
# #         #     "clarification_needed": False,
# #         #     "clarification_questions": []
# #         # }

# #     def _init_permission_mappings(self) -> None:
# #         """Initialize permission requirement mappings"""
# #         self.permission_mappings = {
# #             IntentType.CALENDAR_CREATE_EVENT: {
# #                 "service": "google",
# #                 "scopes": ["https://www.googleapis.com/auth/calendar"],
# #                 "description": "Create calendar events",
# #                 "risk_level": "medium"
# #             },
# #             IntentType.CALENDAR_LIST_EVENTS: {
# #                 "service": "google",
# #                 "scopes": ["https://www.googleapis.com/auth/calendar.readonly"],
# #                 "description": "Read calendar events",
# #                 "risk_level": "low"
# #             },
# #             IntentType.EMAIL_SEND: {
# #                 "service": "google",
# #                 "scopes": ["https://www.googleapis.com/auth/gmail.send"],
# #                 "description": "Send emails",
# #                 "risk_level": "high"
# #             },
# #             IntentType.EMAIL_LIST: {
# #                 "service": "google",
# #                 "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
# #                 "description": "Read emails",
# #                 "risk_level": "medium"
# #             },
# #             IntentType.GITHUB_CREATE_ISSUE: {
# #                 "service": "github",
# #                 "scopes": ["repo"],
# #                 "description": "Create GitHub issues",
# #                 "risk_level": "medium"
# #             },
# #             IntentType.GITHUB_LIST_REPOS: {
# #                 "service": "github",
# #                 "scopes": ["repo:status"],
# #                 "description": "List GitHub repositories",
# #                 "risk_level": "low"
# #             },
# #             IntentType.SLACK_SEND_MESSAGE: {
# #                 "service": "slack",
# #                 "scopes": ["chat:write"],
# #                 "description": "Send Slack messages",
# #                 "risk_level": "medium"
# #             },
# #             IntentType.SLACK_LIST_CHANNELS: {
# #                 "service": "slack",
# #                 "scopes": ["channels:read"],
# #                 "description": "List Slack channels",
# #                 "risk_level": "low"
# #             },
# #         }

# #     async def analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
# #         """Analyze user message to determine intent"""
        
# #         # Always use fallback analysis since we're using Agents SDK for process_message
# #         logger.info("Using fallback analysis for intent detection")
# #         return self._fallback_analyze_intent(user_message, user_context)

# #     # def _fallback_analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
# #     #     """Fallback rule-based intent analysis when Gemini is not available"""
# #     #     msg = user_message.lower()

# #     #     # Math/calculations
# #     #     if any(pattern in msg for pattern in ['+', '-', '*', '/', '=', 'calculate', 'what is', 'compute']) and \
# #     #        any(char.isdigit() for char in msg):
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.GENERAL_QUERY,
# #     #             confidence=ConfidenceLevel.HIGH,
# #     #             parameters={"query_type": "math", "original_message": user_message},
# #     #             required_permissions=[],
# #     #             service_name=None,
# #     #             clarification_needed=False,
# #     #             clarification_questions=[]
# #     #         )

# #     #     # Code/programming requests
# #     #     elif any(word in msg for word in ['python', 'code', 'program', 'function', 'write', 'script', 'hello world']):
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.GENERAL_QUERY,
# #     #             confidence=ConfidenceLevel.HIGH,
# #     #             parameters={"query_type": "code", "original_message": user_message},
# #     #             required_permissions=[],
# #     #             service_name=None,
# #     #             clarification_needed=False,
# #     #             clarification_questions=[]
# #     #         )

# #     #     # Calendar intent detection
# #     #     elif any(word in msg for word in ['calendar', 'schedule', 'meeting', 'appointment', 'event', 'party', 'create']) and \
# #     #        any(word in msg for word in ['tomorrow', 'today', 'pm', 'am', 'time', 'date']):
            
# #     #         # Extract parameters
# #     #         title = "Birthday party"
# #     #         if "meeting" in msg:
# #     #             title = "Meeting"
# #     #         elif "appointment" in msg:
# #     #             title = "Appointment"
# #     #         elif "party" in msg:
# #     #             title = "Birthday party"
# #     #         elif "event" in msg:
# #     #             title = "Event"
            
# #     #         # Extract time
# #     #         time = "17:00"
# #     #         import re
# #     #         time_match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(pm|am)', msg)
# #     #         if time_match:
# #     #             hours, minutes, period = time_match.groups()
# #     #             minutes = minutes or '00'
# #     #             hour24 = int(hours)
# #     #             if period == 'pm' and hour24 != 12:
# #     #                 hour24 += 12
# #     #             elif period == 'am' and hour24 == 12:
# #     #                 hour24 = 0
# #     #             time = f"{hour24:02d}:{minutes}"
            
# #     #         # Extract date
# #     #         date = "2026-04-06"
# #     #         if "tomorrow" in msg:
# #     #             date = "2026-04-06"
# #     #         elif "today" in msg:
# #     #             date = "2026-04-05"
            
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.CALENDAR_CREATE_EVENT,
# #     #             confidence=ConfidenceLevel.HIGH,
# #     #             parameters={"title": title, "date": date, "time": time},
# #     #             required_permissions=["https://www.googleapis.com/auth/calendar"],
# #     #             service_name="google",
# #     #             clarification_needed=False,
# #     #             clarification_questions=[]
# #     #         )
        
# #     #     # Email intent detection
# #     #     elif any(word in msg for word in ['email', 'mail', 'send']) and \
# #     #          (any(word in msg for word in ['to', '@', 'send']) or '@' in user_message):
            
# #     #         # Extract email
# #     #         import re
# #     #         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
# #     #         to_email = email_match.group(0) if email_match else "recipient@example.com"
            
# #     #         # Extract subject
# #     #         subject_match = re.search(r'subject\s+([^"\']+?)(?:\s+and\s+body|$)', msg)
# #     #         subject = subject_match.group(1).strip() if subject_match else "Message from CipherMate AI"
            
# #     #         # Extract body
# #     #         body_match = re.search(r'body\s+(.+)$', msg)
# #     #         body = body_match.group(1).strip() if body_match else user_message
            
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.EMAIL_SEND,
# #     #             confidence=ConfidenceLevel.HIGH,
# #     #             parameters={"to": to_email, "subject": subject, "body": body},
# #     #             required_permissions=["https://www.googleapis.com/auth/gmail.send"],
# #     #             service_name="google",
# #     #             clarification_needed=False,
# #     #             clarification_questions=[]
# #     #         )
        
# #     #     # General query for greetings and casual conversation
# #     #     elif any(word in msg for word in ['hello', 'hi', 'hey', 'how are you', 'what can you do', 'help', 'name', 'who are you', 'what are you', 'introduce yourself']):
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.GENERAL_QUERY,
# #     #             confidence=ConfidenceLevel.HIGH,
# #     #             parameters={"query_type": "greeting_or_identity"},
# #     #             required_permissions=[],
# #     #             service_name=None,
# #     #             clarification_needed=False,
# #     #             clarification_questions=[]
# #     #         )
        
# #     #     # Unknown intent
# #     #     else:
# #     #         return IntentAnalysisResult(
# #     #             intent_type=IntentType.UNKNOWN,
# #     #             confidence=ConfidenceLevel.LOW,
# #     #             parameters={},
# #     #             required_permissions=[],
# #     #             service_name=None,
# #     #             clarification_needed=True,
# #     #             clarification_questions=["I'm not sure I understand. Could you rephrase?"]
# #     #         )

# #     async def generate_response(self, intent_result: IntentAnalysisResult, user_message: str) -> str:
# #         """Generate natural language response"""
# #         # Always use fallback since we're using Agents SDK for main processing
# #         return self._generate_fallback_response(intent_result)

# #     def _create_error_result(self, message: str) -> IntentAnalysisResult:
# #         """Create error result"""
# #         return IntentAnalysisResult(
# #             intent_type=IntentType.UNKNOWN,
# #             confidence=ConfidenceLevel.LOW,
# #             parameters={},
# #             required_permissions=[],
# #             clarification_needed=True,
# #             clarification_questions=[message]
# #         )

# #     # def _generate_fallback_response(self, intent_result: IntentAnalysisResult) -> str:
# #     #     """Generate fallback response"""
# #     #     if intent_result.clarification_needed and intent_result.clarification_questions:
# #     #         return " ".join(intent_result.clarification_questions)

# #     #     if intent_result.required_permissions:
# #     #         return f"To help you with this, I'll need access to {intent_result.service_name or 'the required service'}. Please grant the necessary permissions."

# #     #     # Check for specific query types in parameters
# #     #     params = intent_result.parameters
# #     #     query_type = params.get('query_type')
# #     #     original_message = params.get('original_message', '').lower()

# #     #     # Handle math queries
# #     #     if query_type == 'math':
# #     #         # Try to evaluate simple math
# #     #         import re
# #     #         # Extract math expression
# #     #         math_match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', original_message.replace('=?', '').replace('=', ''))
# #     #         if math_match:
# #     #             try:
# #     #                 expression = math_match.group(1)
# #     #                 result = eval(expression)  # Safe here since it's from our validated pattern
# #     #                 return f"{expression} = {result}"
# #     #             except:
# #     #                 pass
# #     #         return "I can help with basic math. What would you like me to calculate?"

# #     #     # Handle code/programming queries
# #     #     if query_type == 'code':
# #     #         if 'python' in original_message and 'hello world' in original_message:
# #     #             return "Here's a Python Hello World program:\n\n```python\nprint('Hello, World!')\n```\n\nThis simple program prints 'Hello, World!' to the console. It's the classic first program for beginners!"
# #     #         elif 'python' in original_message:
# #     #             return "I can help you with Python programming! Python is a versatile programming language. What specific Python task would you like me to help with?"
# #     #         elif 'hello world' in original_message:
# #     #             return "Here's a Hello World program! In Python: `print('Hello, World!')` - What programming language are you interested in?"
# #     #         else:
# #     #             return "I'd love to help you with programming! What language and specific task are you looking for?"

# #     #     # Handle greeting/identity queries
# #     #     if query_type == 'greeting_or_identity':
# #     #         if any(word in original_message for word in ['name', 'who are you', 'what are you', 'introduce yourself']):
# #     #             return "Fallback ai_agent_simple.py I'm CipherMate, your AI assistant! I can help you with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with?"
# #     #         else:
# #     #             return "Fallback ai_agent_simple.py Hello! I'm CipherMate, your AI assistant. I can help you with:\n\n📅 Calendar events\n📧 Emails\n🐙 GitHub issues\n💬 Slack messages\n🔢 Math calculations\n💻 Programming help\n\nWhat would you like to do today?"

# #     #     responses = {
# #     #         IntentType.CALENDAR_CREATE_EVENT: "I can help you create a calendar event. Please provide details like title, date, and time.",
# #     #         IntentType.CALENDAR_LIST_EVENTS: "I can show you your upcoming calendar events.",
# #     #         IntentType.EMAIL_SEND: "I can help you send an email. Please provide recipient and message details.",
# #     #         IntentType.EMAIL_LIST: "I can show you your recent emails.",
# #     #         IntentType.GITHUB_CREATE_ISSUE: "I can help you create a GitHub issue. Please specify the repository and issue details.",
# #     #         IntentType.SLACK_SEND_MESSAGE: "I can help you send a Slack message. Please specify the channel and message content.",
# #     #         IntentType.GENERAL_QUERY: "Hello! I'm your CipherMate AI assistant. I can help you with:\n\n📅 Calendar events\n📧 Emails\n🐙 GitHub issues\n💬 Slack messages\n🔢 Math calculations\n💻 Programming help\n\nWhat would you like to do today?",
# #     #         IntentType.UNKNOWN: "I'm not sure I understand. Could you rephrase? I can help with calendar events, emails, GitHub, Slack, math, and programming."
# #     #     }

# #     #     return responses.get(intent_result.intent_type, "Hello! I'm your CipherMate AI assistant. How can I help you today?")


# # # Create singleton instance
# # simple_ai_agent = SimpleAIAgent()
