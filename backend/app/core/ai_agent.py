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
        """Process user message and return structured response with proper intent detection"""
        
        # FIRST: Always detect intent using analyze_intent
        intent_result = await self.analyze_intent(user_message, user_context)
        
        # If calendar intent detected - return structured response
        if intent_result.intent_type == IntentType.CALENDAR_CREATE_EVENT:
            event_details = self._extract_event_details(user_message)
            return {
                "response": f"✅ I'll help you schedule this event!\n\nTitle: {event_details['title']}\nDate: {event_details['date']}\nTime: {event_details['time']}\n\n[Grant Permission] to Google Calendar",
                "intent_type": "calendar_create_event",
                "confidence": "high",
                "service_name": "google_calendar",
                "parameters": event_details,
                "required_permissions": ["https://www.googleapis.com/auth/calendar"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # If email intent detected
        elif intent_result.intent_type == IntentType.EMAIL_SEND:
            email_details = self._extract_email_details(user_message)
            return {
                "response": f"📧 I'll help you send this email!\n\nTo: {email_details['to']}\nSubject: {email_details['subject']}\n\n[Grant Permission] to Gmail",
                "intent_type": "email_send",
                "confidence": "high",
                "service_name": "gmail",
                "parameters": email_details,
                "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # If GitHub intent detected
        elif intent_result.intent_type == IntentType.GITHUB_CREATE_ISSUE:
            github_details = self._extract_github_details(user_message)
            return {
                "response": f"🐙 I'll help you create a GitHub issue!\n\nTitle: {github_details['title']}\nRepository: {github_details['repo']}\n\n[Grant Permission] to GitHub",
                "intent_type": "github_create_issue",
                "confidence": "high",
                "service_name": "github",
                "parameters": github_details,
                "required_permissions": ["repo"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # If Slack intent detected
        elif intent_result.intent_type == IntentType.SLACK_SEND_MESSAGE:
            slack_details = self._extract_slack_details(user_message)
            return {
                "response": f"💬 I'll help you send a Slack message!\n\nChannel: {slack_details['channel']}\nMessage: {slack_details['message']}\n\n[Grant Permission] to Slack",
                "intent_type": "slack_send_message",
                "confidence": "high",
                "service_name": "slack",
                "parameters": slack_details,
                "required_permissions": ["chat:write"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # For other intents, try using the agent if available
        if not self.available or not self.triage_agent:
            return {
                "response": "I'm CipherMate, your AI assistant! I can help with calendar events, emails, GitHub issues, and Slack messages. What would you like me to help you with?",
                "intent_type": "general_query",
                "confidence": "medium",
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
                    return self._emergency_fallback(user_message, "timeout")
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                    logger.warning(f"Quota exceeded - using emergency fallback")
                    return self._emergency_fallback(user_message, "quota")
                elif "network" in error_msg or "connection" in error_msg or "timeout" in error_msg:
                    logger.warning(f"Network issue - using emergency fallback")
                    return self._emergency_fallback(user_message, "network")
                
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
            event_details = self._extract_event_details(user_message)
            return {
                "response": f"✅ I'll help you schedule this event!\n\nTitle: {event_details['title']}\nDate: {event_details['date']}\nTime: {event_details['time']}\n\n[Grant Permission] to Google Calendar",
                "intent_type": "calendar_create_event",
                "confidence": "medium",
                "service_name": "google_calendar",
                "parameters": event_details,
                "required_permissions": ["https://www.googleapis.com/auth/calendar"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Email requests
        elif any(word in msg_lower for word in ['email', 'mail', 'send']):
            email_details = self._extract_email_details(user_message)
            return {
                "response": f"📧 I'll help you send this email!\n\nTo: {email_details['to']}\nSubject: {email_details['subject']}\n\n[Grant Permission] to Gmail",
                "intent_type": "email_send",
                "confidence": "medium",
                "service_name": "gmail",
                "parameters": email_details,
                "required_permissions": ["https://www.googleapis.com/auth/gmail.send"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # GitHub requests
        elif any(word in msg_lower for word in ['github', 'issue', 'repo']):
            github_details = self._extract_github_details(user_message)
            return {
                "response": f"🐙 I'll help you create a GitHub issue!\n\nTitle: {github_details['title']}\nRepository: {github_details['repo']}\n\n[Grant Permission] to GitHub",
                "intent_type": "github_create_issue",
                "confidence": "medium",
                "service_name": "github",
                "parameters": github_details,
                "required_permissions": ["repo"],
                "requires_auth": True,
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Slack requests
        elif any(word in msg_lower for word in ['slack', 'message', 'channel']):
            slack_details = self._extract_slack_details(user_message)
            return {
                "response": f"💬 I'll help you send a Slack message!\n\nChannel: {slack_details['channel']}\nMessage: {slack_details['message']}\n\n[Grant Permission] to Slack",
                "intent_type": "slack_send_message",
                "confidence": "medium",
                "service_name": "slack",
                "parameters": slack_details,
                "required_permissions": ["chat:write"],
                "requires_auth": True,
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

    def _extract_event_details(self, message: str) -> Dict[str, Any]:
        """Extract event details from message"""
        from datetime import datetime, timedelta
        
        msg_lower = message.lower()

        # Default values
        title = "Meeting"
        time = "15:00"
        
        # Calculate actual date from natural language
        today = datetime.now()
        if "tomorrow" in msg_lower:
            date_obj = today + timedelta(days=1)
        elif "next week" in msg_lower:
            date_obj = today + timedelta(days=7)
        elif "today" in msg_lower:
            date_obj = today
        else:
            # Default to tomorrow if no date specified
            date_obj = today + timedelta(days=1)
        
        # Convert to YYYY-MM-DD format
        date = date_obj.strftime("%Y-%m-%d")
        
        # Extract title
        if "team meeting" in msg_lower:
            title = "Team Meeting"
        elif "birthday" in msg_lower:
            title = "Birthday Party"
        elif "call" in msg_lower:
            title = "Phone Call"
        elif "appointment" in msg_lower:
            title = "Appointment"
        elif "party" in msg_lower:
            title = "Party"
        
        # Extract time
        import re
        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', msg_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) or "00"
            ampm = time_match.group(3)
            if ampm == "pm" and hour != 12:
                hour += 12
            elif ampm == "am" and hour == 12:
                hour = 0
            time = f"{hour:02d}:{minute}"

        return {
            "title": title,
            "date": date,
            "time": time,
            "description": message,
            "duration_minutes": 60
        }

    def _extract_email_details(self, message: str) -> Dict[str, Any]:
        """Extract email details from message"""
        import re

        # Extract email address
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
        recipient = email_match.group(0) if email_match else "recipient@example.com"

        # Extract subject (look for "subject" keyword)
        subject = "Message from CipherMate"
        subject_match = re.search(r'subject\s+(.*?)(?:\s+and\s+|\s+body\s+|\s+with\s+|$)', message, re.IGNORECASE)
        if subject_match:
            subject = subject_match.group(1).strip()
            # Clean up common patterns
            if subject.lower().startswith(('testing', 'test', 'hello', 'meeting')):
                subject = subject.title()

        # Extract body (look for "body" keyword or use rest of message)
        body = message
        body_match = re.search(r'body\s+(.*?)(?:$)', message, re.IGNORECASE | re.DOTALL)
        if body_match:
            body = body_match.group(1).strip()
        else:
            # Try to extract meaningful content after email address
            parts = message.split(recipient, 1)
            if len(parts) > 1:
                body = parts[1].strip()

        return {
            "to": recipient,
            "subject": subject,
            "body": body,
            "cc": [],
            "bcc": []
        }

    def _extract_github_details(self, message: str) -> Dict[str, Any]:
        """Extract GitHub issue details from message"""
        import re
        
        msg_lower = message.lower()

        issue_type = "issue"
        if "bug" in msg_lower:
            issue_type = "bug"
        elif "feature" in msg_lower:
            issue_type = "feature"

        # Try to extract repo name from message (owner/repo format)
        repo = "HadiqaGohar/ciphermate-github-test-repo"  # Default repo
        repo_match = re.search(r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)', message)
        if repo_match:
            repo = repo_match.group(1)
            logger.info(f"Extracted repo from message: {repo}")

        # Extract title if present
        title_match = re.search(r'(?:titled?|title[:\s]+)(.+?)(?:\s+with\s+body|\s*$)', message, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else f"New {issue_type} from CipherMate"

        # Extract body if present
        body_match = re.search(r'(?:with\s+body|body[:\s]+)(.+)$', message, re.IGNORECASE)
        body = body_match.group(1).strip() if body_match else message

        return {
            "title": title,
            "body": body,
            "repo": repo,
            "labels": [issue_type],
            "assignees": []
        }

    def _extract_slack_details(self, message: str) -> Dict[str, Any]:
        """Extract Slack message details from message"""
        import re
        
        # Extract channel
        channel_match = re.search(r'#[\w-]+', message)
        channel = channel_match.group(0) if channel_match else "#general"
        
        return {
            "channel": channel,
            "message": message,
            "thread_ts": None,
            "blocks": []
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
