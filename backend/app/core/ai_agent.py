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
            timeout=30.0
        )
        
        model = OpenAIChatCompletionsModel(
            # model="gemini-2.5-flash", 
            model = "gemini-3-flash-preview",
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
        # If agents not available, return error (no fallback)
        if not self.available or not self.triage_agent:
            return {
                "response": "Error: AI Agent not configured. Please check GEMINI_API_KEY.",
                "intent_type": "error",
                "confidence": "none",
                "service_name": None,
                "parameters": {},
                "required_permissions": [],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        max_retries = 2
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                result = await asyncio.wait_for(
                    Runner.run(
                        starting_agent=self.triage_agent,
                        input=user_message,
                        run_config=self.config
                    ),
                    timeout=15.0
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
                    # Only fallback for network issues
                    return self._emergency_fallback(user_message, "timeout")
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # Only use fallback for quota/rate limit or network issues
                if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                    logger.warning(f"Quota exceeded - using emergency fallback")
                    return self._emergency_fallback(user_message, "quota")
                elif "network" in error_msg or "connection" in error_msg or "timeout" in error_msg:
                    logger.warning(f"Network issue - using emergency fallback")
                    return self._emergency_fallback(user_message, "network")
                
                # For other errors, return error without fallback
                logger.error(f"Error in process_message: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay)
                    continue
                else:
                    return {
                        "response": f"Error: AI processing failed. Details: {str(e)[:200]}",
                        "intent_type": "error",
                        "confidence": "none",
                        "service_name": None,
                        "parameters": {},
                        "required_permissions": [],
                        "clarification_needed": False,
                        "clarification_questions": []
                    }

    def _emergency_fallback(self, user_message: str, reason: str) -> Dict[str, Any]:
        """Minimal emergency fallback ONLY for quota/network issues - no chat, just direct action"""
        msg_lower = user_message.lower()
        
        # Calendar/Event requests - direct action
        if any(word in msg_lower for word in ['birthday', 'party', 'schedule', 'meeting', 'event', 'calendar']):
            return {
                "response": "⚠️ AI service temporarily unavailable (quota/network). Please try again in a few moments or connect your API key.",
                "intent_type": "calendar_create_event",
                "confidence": "low",
                "service_name": "google_calendar",
                "parameters": {"note": "AI unavailable - retry later"},
                "required_permissions": ["https://www.googleapis.com/auth/calendar"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Email requests
        elif any(word in msg_lower for word in ['email', 'mail', 'send']):
            return {
                "response": "⚠️ AI service temporarily unavailable (quota/network). Please try again in a few moments.",
                "intent_type": "email_send",
                "confidence": "low",
                "service_name": "gmail",
                "parameters": {},
                "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # GitHub requests
        elif any(word in msg_lower for word in ['github', 'issue', 'repo']):
            return {
                "response": "⚠️ AI service temporarily unavailable (quota/network). Please try again in a few moments.",
                "intent_type": "github_create_issue",
                "confidence": "low",
                "service_name": "github",
                "parameters": {},
                "required_permissions": ["repo"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Slack requests
        elif any(word in msg_lower for word in ['slack', 'message', 'channel']):
            return {
                "response": "⚠️ AI service temporarily unavailable (quota/network). Please try again in a few moments.",
                "intent_type": "slack_send_message",
                "confidence": "low",
                "service_name": "slack",
                "parameters": {},
                "required_permissions": ["chat:write"],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Default emergency response - no chat, just error
        else:
            return {
                "response": "⚠️ AI service temporarily unavailable. Please check your API quota/network and try again.",
                "intent_type": "error",
                "confidence": "none",
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


# """Final Clean AI Agent - No fallback, No general chat, Only 4 services"""

# import logging
# import asyncio
# from typing import Dict, List, Optional, Any
# from enum import Enum
# from dataclasses import dataclass

# from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
# from app.core.config import settings

# logger = logging.getLogger(__name__)

# agents_config = None
# triage_agent = None
# agents_available = False


# def setup_agents_config():
#     global agents_config, triage_agent, agents_available
    
#     if not getattr(settings, 'GEMINI_API_KEY', None):
#         logger.warning("GEMINI_API_KEY not configured")
#         agents_available = False
#         return
    
#     try:
#         client = AsyncOpenAI(
#             api_key=settings.GEMINI_API_KEY,
#             base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#             timeout=30.0  # Add timeout to prevent hanging
#         )
        
#         model = OpenAIChatCompletionsModel(
#             model="gemini-2.5-flash", 
#             openai_client=client
#         )
        
#         agents_config = RunConfig(
#             model=model, 
#             model_provider=client, 
#             tracing_disabled=True
#         )
        
#         calendar_agent = Agent(
#             name="calendar_agent",
#             instructions="You are a calendar specialist. When user wants to schedule meeting, event or birthday party, create the event with extracted title, date and time. Give short confirmation only.",
#             handoff_description="Calendar events",
#             model=model
#         )
        
#         email_agent = Agent(
#             name="email_agent",
#             instructions="You are an email specialist. Help user send emails.",
#             handoff_description="Send emails",
#             model=model
#         )
        
#         github_agent = Agent(
#             name="github_agent",
#             instructions="You are a GitHub specialist. Help create issues.",
#             handoff_description="GitHub issues",
#             model=model
#         )
        
#         slack_agent = Agent(
#             name="slack_agent",
#             instructions="You are a Slack specialist. Help send messages.",
#             handoff_description="Slack messages",
#             model=model
#         )
        
#         triage_agent = Agent(
#             name="triage_agent",
#             instructions=(
#                 "You are a strict triage agent. Route ONLY to the correct tool:\n"
#                 "- Anything about schedule, meeting, event, birthday, calendar → calendar_agent\n"
#                 "- Anything about email, send mail → email_agent\n"
#                 "- Anything about github, issue → github_agent\n"
#                 "- Anything about slack, message, channel → slack_agent\n"
#                 "Do not chat. Do not ask questions. Do not confirm. Just call the correct tool."
#             ),
#             tools=[
#                 calendar_agent.as_tool("handle_calendar_request", "Create or manage calendar events"),
#                 email_agent.as_tool("handle_email_request", "Send emails"),
#                 github_agent.as_tool("handle_github_request", "Create GitHub issues"),
#                 slack_agent.as_tool("handle_slack_request", "Send Slack messages"),
#             ],
#             model=model
#         )
        
#         agents_available = True
#         logger.info("✅ Clean Agents SDK loaded successfully")
        
#     except Exception as e:
#         logger.error(f"Failed to load Agents SDK: {e}")
#         agents_available = False


# setup_agents_config()


# class IntentType(Enum):
#     CALENDAR_CREATE_EVENT = "calendar_create_event"
#     EMAIL_SEND = "email_send"
#     GITHUB_CREATE_ISSUE = "github_create_issue"
#     SLACK_SEND_MESSAGE = "slack_send_message"
#     UNKNOWN = "unknown"


# @dataclass
# class IntentAnalysisResult:
#     intent_type: IntentType
#     confidence: str
#     parameters: Dict[str, Any]
#     required_permissions: List[str]
#     service_name: Optional[str] = None


# class AIAgentEngine:
#     def __init__(self):
#         self.triage_agent = triage_agent
#         self.config = agents_config
#         self.available = agents_available

#     async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
#         if not self.available or not self.triage_agent:
#             return self._fallback_response(user_message)
        
#         # Implement retry logic for quota errors
#         max_retries = 2  # Reduced retries
#         base_delay = 1   # Reduced delay
        
#         for attempt in range(max_retries):
#             try:
#                 # Add timeout to prevent hanging
#                 result = await asyncio.wait_for(
#                     Runner.run(
#                         starting_agent=self.triage_agent,
#                         input=user_message,
#                         run_config=self.config
#                     ),
#                     timeout=15.0  # Reduced timeout
#                 )
                
#                 return {
#                     "response": result.final_output.strip(),
#                     "intent_type": "processed",
#                     "confidence": "high",
#                     "service_name": None,
#                     "parameters": {},
#                     "required_permissions": [],
#                     "clarification_needed": False,
#                     "clarification_questions": []
#                 }
                
#             except asyncio.TimeoutError:
#                 logger.warning(f"AI agent timeout on attempt {attempt + 1}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(base_delay * (2 ** attempt))
#                     continue
#                 else:
#                     return self._fallback_response(user_message)
                    
#             except Exception as e:
#                 error_msg = str(e).lower()
                
#                 # Handle quota errors specifically - go to fallback immediately
#                 if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
#                     logger.warning(f"Quota exceeded, using fallback response")
#                     return self._fallback_response(user_message)
                
#                 logger.error(f"Error in process_message: {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(base_delay)
#                     continue
#                 else:
#                     return self._fallback_response(user_message)

#     def _fallback_response(self, user_message: str) -> Dict[str, Any]:
#         """Smart fallback responses for when Gemini API is unavailable"""
#         msg_lower = user_message.lower()
        
#         # Time-related queries
#         if any(word in msg_lower for word in ['time', 'clock', 'what time', 'current time']):
#             from datetime import datetime
#             current_time = datetime.now().strftime("%I:%M %p")
#             current_date = datetime.now().strftime("%B %d, %Y")
#             return {
#                 "response": f"Fallback response: 🕐 Current time is {current_time} on {current_date}. I can help you schedule events, send emails, create GitHub issues, or send Slack messages. What would you like me to help you with?",
#                 "intent_type": "time_query",
#                 "confidence": "high",
#                 "service_name": None,
#                 "parameters": {"current_time": current_time, "current_date": current_date},
#                 "required_permissions": [],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Calendar/Event requests
#         elif any(word in msg_lower for word in ['birthday', 'party', 'schedule', 'meeting', 'event', 'calendar', 'calender']):
#             # Extract details with better parsing
#             title = "Event"
#             if "birthday" in msg_lower:
#                 title = "Birthday Party"
#             elif "meeting" in msg_lower:
#                 title = "Team Meeting"
#             elif "appointment" in msg_lower:
#                 title = "Appointment"
#             elif "party" in msg_lower:
#                 title = "Party"
            
#             # Extract time with better parsing
#             time_str = "3:00 PM"
#             import re
#             time_match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(pm|am)', msg_lower)
#             if time_match:
#                 hour = time_match.group(1)
#                 minute = time_match.group(2) or "00"
#                 period = time_match.group(3).upper()
#                 time_str = f"{hour}:{minute} {period}"
            
#             # Extract date with better parsing
#             date_str = "April 9, 2026"
#             if "tomorrow" in msg_lower:
#                 date_str = "tomorrow"
#             elif "today" in msg_lower:
#                 date_str = "today"
#             elif "9 apr" in msg_lower or "april 9" in msg_lower:
#                 date_str = "April 9, 2026"
            
#             return {
#                 "response": f"Fallback response: ✅ I'll help you create a {title.lower()} for {date_str} at {time_str}.\n\n📅 Event Details:\n• Title: {title}\n• Date: {date_str}\n• Time: {time_str}\n• Duration: 1 hour\n\n🔗 To actually create this event, please connect your Google Calendar in the Token Vault section.",
#                 "intent_type": "calendar_create_event",
#                 "confidence": "high",
#                 "service_name": "google_calendar",
#                 "parameters": {"title": title, "time": time_str, "date": date_str},
#                 "required_permissions": ["https://www.googleapis.com/auth/calendar"],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Email requests
#         elif any(word in msg_lower for word in ['email', 'mail', 'send']) and '@' in user_message:
#             # Extract email details
#             import re
#             email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
#             recipient = email_match.group(0) if email_match else "recipient@example.com"
            
#             return {
#                 "response": f"Fallback response: ✅ I can help you send an email to {recipient}.\n\n📧 Email Details:\n• To: {recipient}\n• Subject: (Please specify)\n• Message: (Please specify)\n\n🔗 To actually send emails, please connect your Gmail account in the Token Vault section.",
#                 "intent_type": "email_send",
#                 "confidence": "high",
#                 "service_name": "gmail",
#                 "parameters": {"recipient": recipient},
#                 "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
#                 "clarification_needed": True,
#                 "clarification_questions": ["What should be the subject of the email?", "What message would you like to send?"]
#             }
        
#         # GitHub requests
#         elif any(word in msg_lower for word in ['github', 'issue', 'repo', 'bug', 'feature']):
#             issue_type = "bug" if "bug" in msg_lower else "feature" if "feature" in msg_lower else "issue"
#             return {
#                 "response": f"Fallback response: ✅ I can help you create a GitHub {issue_type}.\n\n🐙 GitHub Details:\n• Type: {issue_type.title()}\n• Repository: (Please specify)\n• Title: (Please specify)\n• Description: (Please specify)\n\n🔗 To actually create GitHub issues, please connect your GitHub account in the Token Vault section.",
#                 "intent_type": "github_create_issue",
#                 "confidence": "high",
#                 "service_name": "github",
#                 "parameters": {"issue_type": issue_type},
#                 "required_permissions": ["repo"],
#                 "clarification_needed": True,
#                 "clarification_questions": ["Which repository?", "What should be the title?", "Please provide a description."]
#             }
        
#         # Slack requests
#         elif any(word in msg_lower for word in ['slack', 'message', 'channel', 'team']):
#             channel = "#general"
#             if "#" in user_message:
#                 import re
#                 channel_match = re.search(r'#[\w-]+', user_message)
#                 if channel_match:
#                     channel = channel_match.group(0)
            
#             return {
#                 "response": f"Fallback response: ✅ I can help you send a Slack message to {channel}.\n\n💬 Slack Details:\n• Channel: {channel}\n• Message: (Please specify)\n\n🔗 To actually send Slack messages, please connect your Slack workspace in the Token Vault section.",
#                 "intent_type": "slack_send_message",
#                 "confidence": "high",
#                 "service_name": "slack",
#                 "parameters": {"channel": channel},
#                 "required_permissions": ["chat:write"],
#                 "clarification_needed": True,
#                 "clarification_questions": ["What message would you like to send?"]
#             }
        
#         # Task/capability questions
#         elif any(word in msg_lower for word in ['task', 'perform', 'do', 'help', 'what', 'which', 'can you', 'abilities']):
#             return {
#                 "response": "Fallback response: 🤖 I'm CipherMate, your AI assistant! I can help you with:\n\n📅 **Calendar Events** - Schedule meetings, appointments, birthday parties\n   Example: \"Schedule a team meeting tomorrow at 3 PM\"\n\n📧 **Email** - Send and manage emails\n   Example: \"Send an email to john@example.com about the project update\"\n\n🐙 **GitHub** - Create issues and manage repositories\n   Example: \"Create a GitHub issue for the login bug\"\n\n💬 **Slack** - Send messages to channels\n   Example: \"Send a message to #general channel\"\n\n🔗 Connect your accounts in the Token Vault to get started!",
#                 "intent_type": "general_query",
#                 "confidence": "high",
#                 "service_name": None,
#                 "parameters": {},
#                 "required_permissions": [],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Greeting responses
#         elif any(word in msg_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
#             from datetime import datetime
#             current_hour = datetime.now().hour
#             greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
            
#             return {
#                 "response": f"Fallback response: {greeting}! 👋 I'm CipherMate, your secure AI assistant.\n\nI'm ready to help you with:\n• 📅 Calendar events\n• 📧 Emails\n• 🐙 GitHub issues\n• 💬 Slack messages\n\nWhat would you like me to help you with today?",
#                 "intent_type": "greeting",
#                 "confidence": "high",
#                 "service_name": None,
#                 "parameters": {},
#                 "required_permissions": [],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
        
#         # Default response for unrecognized queries
#         else:
#             return {
#                 "response": "Fallback response: Hello! I'm CipherMate, your AI assistant. I can help you with calendar events, emails, GitHub issues, and Slack messages.\n\n💡 Try asking me something like:\n• \"What time is it?\"\n• \"Schedule a meeting for tomorrow\"\n• \"Send an email to someone@example.com\"\n• \"Create a GitHub issue\"\n• \"Send a Slack message\"\n\nWhat would you like me to help you with?",
#                 "intent_type": "general_query",
#                 "confidence": "medium",
#                 "service_name": None,
#                 "parameters": {},
#                 "required_permissions": [],
#                 "clarification_needed": False,
#                 "clarification_questions": []
#             }
#             }

#     async def analyze_intent(self, user_message: str, user_context: Dict[str, Any] = None) -> IntentAnalysisResult:
#         """Analyze intent of user message"""
#         if not self.available or not self.triage_agent:
#             return IntentAnalysisResult(
#                 intent_type=IntentType.UNKNOWN,
#                 confidence="low",
#                 parameters={},
#                 required_permissions=[]
#             )
        
#         try:
#             # Simple intent analysis based on keywords
#             msg_lower = user_message.lower()
            
#             if any(word in msg_lower for word in ['calendar', 'schedule', 'meeting', 'event', 'birthday']):
#                 return IntentAnalysisResult(
#                     intent_type=IntentType.CALENDAR_CREATE_EVENT,
#                     confidence="high",
#                     parameters={},
#                     required_permissions=["https://www.googleapis.com/auth/calendar"],
#                     service_name="google"
#                 )
#             elif any(word in msg_lower for word in ['email', 'mail', 'send']) and '@' in user_message:
#                 return IntentAnalysisResult(
#                     intent_type=IntentType.EMAIL_SEND,
#                     confidence="high",
#                     parameters={},
#                     required_permissions=["https://www.googleapis.com/auth/gmail.send"],
#                     service_name="google"
#                 )
#             elif any(word in msg_lower for word in ['github', 'issue', 'repo']):
#                 return IntentAnalysisResult(
#                     intent_type=IntentType.GITHUB_CREATE_ISSUE,
#                     confidence="high",
#                     parameters={},
#                     required_permissions=["repo"],
#                     service_name="github"
#                 )
#             elif any(word in msg_lower for word in ['slack', 'message', 'channel']):
#                 return IntentAnalysisResult(
#                     intent_type=IntentType.SLACK_SEND_MESSAGE,
#                     confidence="high",
#                     parameters={},
#                     required_permissions=["chat:write"],
#                     service_name="slack"
#                 )
#             else:
#                 return IntentAnalysisResult(
#                     intent_type=IntentType.UNKNOWN,
#                     confidence="low",
#                     parameters={},
#                     required_permissions=[]
#                 )
                
#         except Exception as e:
#             logger.error(f"Error in analyze_intent: {e}")
#             return IntentAnalysisResult(
#                 intent_type=IntentType.UNKNOWN,
#                 confidence="low",
#                 parameters={},
#                 required_permissions=[]
#             )


# # Singleton
# ai_agent_engine = AIAgentEngine()