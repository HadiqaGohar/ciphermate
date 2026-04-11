"""Execute Action API endpoint for handling OAuth and action execution"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlencode
import secrets
import httpx

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user, get_optional_user
from app.core.token_vault import token_vault_service
from app.core.config import settings
from app.models.user import User
from app.models.agent_action import AgentAction
from app.models.service_connection import ServiceConnection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/execute", tags=["Execute Action"])


async def get_user_service_token(user_id: str, service_name: str, db: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get service token for a user. Checks temp_tokens first (for OAuth flow), then database.
    """
    # First check temp_tokens (for immediate use after OAuth)
    try:
        from app.api.routes.gmail_auth import temp_tokens as gmail_tokens
        
        if service_name == "gmail" and 'current' in gmail_tokens:
            logger.info(f"✅ Using Gmail token from temp_tokens for user {user_id}")
            return gmail_tokens['current']
    except Exception as e:
        logger.warning(f"Error checking gmail temp_tokens: {e}")
    
    try:
        from app.api.routes.google_calendar_auth import temp_tokens as calendar_tokens
        
        if service_name == "google_calendar" and 'current' in calendar_tokens:
            logger.info(f"✅ Using Google Calendar token from temp_tokens for user {user_id}")
            return calendar_tokens['current']
    except Exception as e:
        logger.warning(f"Error checking calendar temp_tokens: {e}")
    
    # Fallback to database (future implementation)
    logger.info(f"ℹ️ No temp token found for {service_name}, would check database in production")
    return None


class ExecuteActionRequest(BaseModel):
    """Request to execute an action"""
    intent_type: str
    parameters: Dict[str, Any]
    action_id: Optional[int] = None


class ExecuteActionResponse(BaseModel):
    """Response for action execution"""
    success: bool
    message: str
    requires_auth: Optional[bool] = None
    auth_url: Optional[str] = None
    provider: Optional[str] = None
    event_link: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


def generate_google_calendar_auth_url(user_id: str) -> str:
    """Generate complete Google Calendar OAuth URL"""
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        logger.warning("Google Client ID not configured")
        return ""

    auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:3000/api/auth/google/callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent",
        "state": f"calendar_{secrets.token_urlsafe(16)}"
    }

    logger.info(f"Generated Google Calendar auth URL for user: {user_id}")
    return f"{auth_base_url}?{urlencode(params)}"


def generate_google_gmail_auth_url(user_id: str) -> str:
    """Generate Google Gmail OAuth URL"""
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        logger.warning("Google Client ID not configured")
        return ""

    auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:3000/api/auth/google/callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/gmail.send",
        "access_type": "offline",
        "prompt": "consent",
        "state": secrets.token_urlsafe(32)
    }

    logger.info(f"Generated Google Gmail auth URL for user: {user_id}")
    return f"{auth_base_url}?{urlencode(params)}"


def generate_github_auth_url(user_id: str) -> str:
    """Generate GitHub OAuth URL"""
    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '')
    if not client_id:
        logger.warning("GitHub Client ID not configured")
        return ""

    auth_base_url = "https://github.com/login/oauth/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:3000/api/auth/github/callback",
        "scope": "repo",
        "state": secrets.token_urlsafe(32)
    }

    logger.info(f"Generated GitHub auth URL for user: {user_id}")
    return f"{auth_base_url}?{urlencode(params)}"


def generate_slack_auth_url(user_id: str) -> str:
    """Generate Slack OAuth URL"""
    client_id = getattr(settings, 'SLACK_CLIENT_ID', '')
    if not client_id:
        logger.warning("Slack Client ID not configured")
        return ""

    auth_base_url = "https://slack.com/oauth/v2/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:3000/api/auth/slack/callback",
        "scope": "chat:write",
        "state": secrets.token_urlsafe(32)
    }

    logger.info(f"Generated Slack auth URL for user: {user_id}")
    return f"{auth_base_url}?{urlencode(params)}"


async def create_calendar_event_with_token(user_id: str, params: Dict[str, Any], token_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create actual calendar event using Google Calendar API"""
    try:
        from app.services.google_calendar import google_calendar_service
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import get_db

        title = params.get('title', 'Meeting')
        date = params.get('date', 'tomorrow')
        time = params.get('time', '15:00')
        description = params.get('description', f'Event created by CipherMate AI Assistant')

        # Create event via Google Calendar service
        # We need to get a DB session - this is a workaround
        async for db in get_db():
            calendar_result = await google_calendar_service.create_event(
                db=db,
                user_id=int(user_id) if user_id.isdigit() else 0,
                title=title,
                date=date,
                time=time,
                duration_minutes=60,
                description=description
            )

            if calendar_result.get("success"):
                return {
                    "success": True,
                    "message": calendar_result.get("message", f"✅ Calendar event '{title}' created for {date} at {time}!"),
                    "event_link": calendar_result.get("event_link", ""),
                    "provider": "google_calendar"
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to create calendar event: {calendar_result.get('error', 'Unknown error')}",
                    "provider": "google_calendar"
                }

        return {
            "success": False,
            "message": "❌ Failed to create calendar event: Database session error",
            "provider": "google_calendar"
        }
    except Exception as e:
        logger.error(f"Calendar creation error: {e}")
        return {
            "success": False,
            "message": f"❌ Cannot create calendar event: {str(e)}",
            "provider": "google_calendar"
        }


async def send_email_with_token(user_id: str, params: Dict[str, Any], token_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send actual email using Gmail API"""
    try:
        from app.services.gmail_real import RealGmailService

        access_token = token_data.get('access_token')
        if not access_token:
            return {
                "success": False,
                "message": "❌ Invalid token: missing access_token",
                "provider": "gmail"
            }

        gmail_service = RealGmailService(access_token=access_token)

        to_email = params.get('to', '')
        subject = params.get('subject', 'Message from CipherMate')
        body = params.get('body', '')

        if not to_email:
            return {
                "success": False,
                "message": "❌ Missing recipient email address",
                "provider": "gmail"
            }

        email_result = gmail_service.send_email_sync(
            to=to_email,
            subject=subject,
            body=body
        )

        if email_result.get("success"):
            return {
                "success": True,
                "message": f"✅ Email sent successfully to {to_email}!",
                "provider": "gmail"
            }
        else:
            return {
                "success": False,
                "message": f"❌ Failed to send email: {email_result.get('error', 'Unknown error')}",
                "provider": "gmail"
            }
    except Exception as e:
        logger.error(f"Email sending error: {e}")
        return {
            "success": False,
            "message": f"❌ Cannot send email: {str(e)}",
            "provider": "gmail"
        }


async def create_github_issue_with_token(user_id: str, params: Dict[str, Any], token_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create GitHub issue using GitHub API"""
    try:
        access_token = token_data.get('access_token')
        if not access_token:
            return {
                "success": False,
                "message": "❌ Invalid token: missing access_token",
                "provider": "github"
            }

        repo = params.get('repo', '')
        title = params.get('title', 'New issue from CipherMate')
        body = params.get('body', '')

        # Parse repo from format "owner/repo"
        if '/' in repo:
            owner, repo_name = repo.split('/', 1)
        else:
            return {
                "success": False,
                "message": "❌ Invalid repository format. Use 'owner/repo'",
                "provider": "github"
            }

        # Call GitHub API to create issue
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.github.com/repos/{owner}/{repo_name}/issues",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github.v3+json"
                },
                json={
                    "title": title,
                    "body": body
                },
                timeout=10.0
            )

            if response.status_code == 201:
                issue_data = response.json()
                issue_url = issue_data.get('html_url', '')
                issue_number = issue_data.get('number', '')
                return {
                    "success": True,
                    "message": f"✅ GitHub issue #{issue_number} created successfully!\n\n🔗 View issue: {issue_url}",
                    "event_link": issue_url,
                    "provider": "github"
                }
            else:
                error_msg = response.json().get('message', 'Unknown error')
                return {
                    "success": False,
                    "message": f"❌ Failed to create GitHub issue: {error_msg}",
                    "provider": "github"
                }
    except Exception as e:
        logger.error(f"GitHub issue creation error: {e}")
        return {
            "success": False,
            "message": f"❌ Cannot create GitHub issue: {str(e)}",
            "provider": "github"
        }


async def send_slack_message_with_token(user_id: str, params: Dict[str, Any], token_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send Slack message using Slack API"""
    try:
        access_token = token_data.get('access_token')
        if not access_token:
            return {
                "success": False,
                "message": "❌ Invalid token: missing access_token",
                "provider": "slack"
            }

        channel = params.get('channel', '#general')
        text = params.get('text', '')

        if not text:
            return {
                "success": False,
                "message": "❌ Missing message text",
                "provider": "slack"
            }

        # Call Slack API to send message
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://slack.com/api/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "channel": channel,
                    "text": text
                },
                timeout=10.0
            )

            if response.status_code == 200:
                slack_data = response.json()
                if slack_data.get('ok'):
                    return {
                        "success": True,
                        "message": f"✅ Slack message sent to {channel} successfully!",
                        "provider": "slack"
                    }
                else:
                    error_msg = slack_data.get('error', 'Unknown error')
                    return {
                        "success": False,
                        "message": f"❌ Failed to send Slack message: {error_msg}",
                        "provider": "slack"
                    }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to send Slack message: HTTP {response.status_code}",
                    "provider": "slack"
                }
    except Exception as e:
        logger.error(f"Slack message error: {e}")
        return {
            "success": False,
            "message": f"❌ Cannot send Slack message: {str(e)}",
            "provider": "slack"
        }


@router.post("/action", response_model=ExecuteActionResponse)
async def execute_action(
    request: ExecuteActionRequest,
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
) -> ExecuteActionResponse:
    """Execute action for calendar, email, GitHub, or Slack with real token checks"""

    # Determine user ID from authenticated user or use anonymous
    if current_user:
        user_id = current_user.get("sub") or current_user.get("auth0_id") or str(current_user.get("id", "anonymous"))
    else:
        user_id = "anonymous"

    intent_type = request.intent_type
    params = request.parameters

    logger.info(f"Executing action: {intent_type} for user: {user_id}")

    # Handle Calendar Events
    if intent_type == "calendar_create_event":
        token_data = await get_user_service_token(user_id, "google_calendar", db)

        if not token_data:
            auth_url = generate_google_calendar_auth_url(user_id)
            return ExecuteActionResponse(
                success=False,
                requires_auth=True,
                auth_url=auth_url,
                message="🔐 Google Calendar access required. Please grant permission to continue.",
                provider="google_calendar",
                parameters=params
            )

        event_result = await create_calendar_event_with_token(user_id, params, token_data)
        return ExecuteActionResponse(**event_result)

    # Handle Email
    elif intent_type == "email_send":
        logger.info(f"📧 Email send action triggered for user: {user_id}")
        token_data = await get_user_service_token(user_id, "gmail", db)
        
        if not token_data:
            logger.warning(f"❌ No Gmail token found for user {user_id}")
            auth_url = generate_google_gmail_auth_url(user_id)
            return ExecuteActionResponse(
                success=False,
                requires_auth=True,
                auth_url=auth_url,
                message="🔐 Gmail access required. Please grant permission to send emails.",
                provider="gmail",
                parameters=params
            )

        logger.info(f"✅ Gmail token found! Sending email...")
        email_result = await send_email_with_token(user_id, params, token_data)
        return ExecuteActionResponse(**email_result)

    # Handle GitHub
    elif intent_type == "github_create_issue":
        token_data = await get_user_service_token(user_id, "github", db)

        if not token_data:
            auth_url = generate_github_auth_url(user_id)
            return ExecuteActionResponse(
                success=False,
                requires_auth=True,
                auth_url=auth_url,
                message="🔐 GitHub access required. Please grant permission to create issues.",
                provider="github",
                parameters=params
            )

        github_result = await create_github_issue_with_token(user_id, params, token_data)
        return ExecuteActionResponse(**github_result)

    # Handle Slack
    elif intent_type == "slack_send_message":
        token_data = await get_user_service_token(user_id, "slack", db)

        if not token_data:
            auth_url = generate_slack_auth_url(user_id)
            return ExecuteActionResponse(
                success=False,
                requires_auth=True,
                auth_url=auth_url,
                message="🔐 Slack access required. Please grant permission to send messages.",
                provider="slack",
                parameters=params
            )

        slack_result = await send_slack_message_with_token(user_id, params, token_data)
        return ExecuteActionResponse(**slack_result)

    else:
        return ExecuteActionResponse(
            success=False,
            message=f"Unknown intent type: {intent_type}",
            provider="ciphermate"
        )
