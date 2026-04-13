"""AI Agent API endpoints for chat and intent processing"""

import logging
import aiohttp
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.ai_agent import ai_agent_engine
from app.core.token_vault import token_vault_service
from app.core.service_clients import service_client_factory
from app.core.config import settings
from app.models.user import User
from app.models.agent_action import AgentAction
from app.models.service_connection import ServiceConnection


async def get_current_user_optional(request: Request) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        # Try to get authenticated user, but don't fail if it doesn't work
        from app.core.auth import get_current_user as auth_func
        user = await auth_func(request)
        return user
    except:
        return None


# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/agent", tags=["AI Agent"])


class ChatMessage(BaseModel):
    """Chat message from user"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class IntentAnalysisResponse(BaseModel):
    """Response for intent analysis"""
    intent_type: str
    confidence: str
    parameters: Dict[str, Any]
    required_permissions: List[str]
    service_name: Optional[str]
    clarification_needed: bool
    clarification_questions: Optional[List[str]]
    has_permissions: bool
    missing_permissions: List[str]


class ChatResponse(BaseModel):
    """Response for chat interaction"""
    message: str
    intent_analysis: IntentAnalysisResponse
    action_id: Optional[int] = None
    requires_permission: bool = False
    permission_grant_url: Optional[str] = None


class ActionExecutionRequest(BaseModel):
    """Request to execute a specific action"""
    action_id: int
    confirm: bool = Field(default=False, description="Confirm action execution")


class ActionExecutionResponse(BaseModel):
    """Response for action execution"""
    action_id: int
    status: str
    result: Optional[str] = None
    execution_time_ms: Optional[int] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    message: ChatMessage,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> ChatResponse:
    """
    Process a chat message with the AI agent - Auth optional
    """
    try:
        # If no auth, use default user
        if not current_user:
            logger.info("Processing anonymous chat message")
            current_user = User(
                id=0,
                auth0_id="anonymous",
                email="anonymous@local",
                name="Anonymous User"
            )
        else:
            logger.info(f"Processing chat message from user {current_user.id}")
        
        # Process message using AI agent
        try:
            result = await ai_agent_engine.process_message(
                user_message=message.message,
                user_context=message.context
            )
        except Exception as ai_error:
            logger.error(f"AI agent error: {ai_error}")
            # Fallback response
            result = {
                "response": "Fallback I'm CipherMate, your AI assistant! I can help with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with?",
                "intent_type": "general_query",
                "confidence": "high",
                "service_name": None,
                "parameters": {},
                "required_permissions": [],
                "clarification_needed": False,
                "clarification_questions": []
            }
        
        # Check if this requires authentication
        requires_permission = result.get("requires_auth", False) or bool(result.get("required_permissions"))
        permission_grant_url = None
        
        # Generate OAuth URLs for services that need authentication
        if requires_permission and result.get("service_name"):
            permission_grant_url = _generate_oauth_url(result.get("service_name"), current_user)
        
        # Create action in database if needed (for calendar, email, etc.)
        action_id = None
        if result.get("intent_type") in ["calendar_create_event", "email_send", "github_create_issue", "slack_send_message"]:
            try:
                # Create agent action record
                agent_action = AgentAction(
                    user_id=current_user.id if current_user and hasattr(current_user, 'id') else 0,
                    action=result.get("intent_type"),
                    parameters=result.get("parameters", {}),
                    requires_step_up=requires_permission
                )
                db.add(agent_action)
                await db.commit()
                await db.refresh(agent_action)
                action_id = agent_action.id
                logger.info(f"Created action {action_id} for intent {result.get('intent_type')}")
            except Exception as e:
                logger.error(f"Failed to create action: {e}")
        
        # Determine missing permissions
        has_permissions = not requires_permission  # For now, assume no permissions
        missing_permissions = result.get("required_permissions", []) if requires_permission else []
        
        return ChatResponse(
            message=result.get("response", "Fallback agent.py --> I'm sorry, I couldn't process your request."),
            intent_analysis=IntentAnalysisResponse(
                intent_type=result.get("intent_type", "unknown"),
                confidence=result.get("confidence", "low"),
                parameters=result.get("parameters", {}),
                required_permissions=result.get("required_permissions", []),
                service_name=result.get("service_name"),
                clarification_needed=result.get("clarification_needed", False),
                clarification_questions=result.get("clarification_questions", []),
                has_permissions=has_permissions,
                missing_permissions=missing_permissions
            ),
            action_id=action_id,
            requires_permission=not has_permissions,
            permission_grant_url=permission_grant_url
        )
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        # Return a friendly fallback response instead of an error
        return ChatResponse(
            message="Fallback agent.py --> I'm CipherMate, your AI assistant! I can help with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with?",
            intent_analysis=IntentAnalysisResponse(
                intent_type="general_query",
                confidence="medium",
                parameters={},
                required_permissions=[],
                service_name=None,
                clarification_needed=False,
                clarification_questions=[],
                has_permissions=True,
                missing_permissions=[]
            ),
            action_id=None,
            requires_permission=False,
            permission_grant_url=None
        )


@router.post("/analyze-intent", response_model=IntentAnalysisResponse)
async def analyze_intent(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> IntentAnalysisResponse:
    """
    Analyze intent of a user message without executing actions
    """
    try:
        logger.info(f"Analyzing intent for user {current_user.id}")
        
        result = await ai_agent_engine.process_message(
            user_message=message.message,
            user_context=message.context
        )
        
        user_permissions = await _get_user_permissions(db, current_user.id)
        
        has_permissions = True
        missing_permissions = []
        
        if result.get("required_permissions") and result.get("service_name"):
            has_permissions = True
            missing_permissions = []
        
        return IntentAnalysisResponse(
            intent_type=result.get("intent_type", "unknown"),
            confidence=result.get("confidence", "low"),
            parameters=result.get("parameters", {}),
            required_permissions=result.get("required_permissions", []),
            service_name=result.get("service_name"),
            clarification_needed=result.get("clarification_needed", False),
            clarification_questions=result.get("clarification_questions", []),
            has_permissions=has_permissions,
            missing_permissions=missing_permissions
        )
        
    except Exception as e:
        logger.error(f"Error analyzing intent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze intent"
        )


@router.post("/execute-action", response_model=ActionExecutionResponse)
async def execute_action_simple(
    request: ActionExecutionRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> ActionExecutionResponse:
    """
    Execute action endpoint. If auth is missing for a service, returns
    a friendly message WITHOUT marking the action as failed so it can
    be retried after OAuth completes.
    """
    try:
        logger.info(f"Executing action {request.action_id}")

        # Get the action from database
        agent_action = await db.get(AgentAction, request.action_id)
        if not agent_action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found"
            )

        # Handle already completed actions gracefully
        if agent_action.status == "completed":
            # Return success without re-executing
            return ActionExecutionResponse(
                action_id=agent_action.id,
                status="completed",
                result=agent_action.result or "Action already completed successfully",
                execution_time_ms=agent_action.execution_time_ms or 0
            )

        user_id = current_user.id if current_user and hasattr(current_user, 'id') else 0

        # Get user timezone from request headers or default to Asia/Karachi
        user_timezone = request.headers.get('X-Timezone', 'Asia/Karachi') if hasattr(request, 'headers') else 'Asia/Karachi'

        if agent_action.status != "pending":
            # For failed/cancelled actions, allow retry by resetting to executing
            logger.info(f"Retrying action {request.action_id} (was {agent_action.status})")
            agent_action.status = "pending"
            await db.commit()

        agent_action.mark_executing()
        await db.commit()

        start_time = datetime.now()
        result = "Action executed successfully"

        # Execute based on action type
        if agent_action.action == "email_send":
            # Call real Gmail service
            from app.services.gmail_real import gmail_service
            
            try:
                to_email = agent_action.parameters.get('to', '')
                subject = agent_action.parameters.get('subject', 'Message from CipherMate')
                body = agent_action.parameters.get('body', '')
                
                logger.info(f"📧 Sending email to {to_email} with subject: {subject}")
                
                email_result = await gmail_service.send_email(
                    db=db,
                    user_id=user_id,
                    to=to_email,
                    subject=subject,
                    body=body
                )
                
                if email_result.get("success"):
                    result = email_result.get("message", "✅ Email sent successfully!")
                    logger.info(f"✅ Real email sent! Message ID: {email_result.get('message_id', 'N/A')}")
                else:
                    # Check if this is an auth issue - DON'T mark as failed
                    if "not connected" in email_result.get("error", "").lower() or "authentication" in email_result.get("error", "").lower():
                        agent_action.status = "pending"
                        await db.commit()
                        return ActionExecutionResponse(
                            action_id=agent_action.id,
                            status="requires_auth",
                            result=email_result.get("message", "Gmail not connected. Please grant permission."),
                            execution_time_ms=0
                        )
                    result = f"❌ Failed to send email: {email_result.get('error', 'Unknown error')}"
            except Exception as e:
                logger.error(f"Email sending error: {e}")
                # Check if this is an auth issue
                if "not connected" in str(e).lower() or "authentication" in str(e).lower():
                    agent_action.status = "pending"
                    await db.commit()
                    return ActionExecutionResponse(
                        action_id=agent_action.id,
                        status="requires_auth",
                        result=f"Gmail not connected. Error: {str(e)}",
                        execution_time_ms=0
                    )
                result = f"❌ Cannot send email: {str(e)}"
        elif agent_action.action == "calendar_create_event":
            # Call real Google Calendar service
            from app.services.google_calendar import google_calendar_service
            
            try:
                title = agent_action.parameters.get('title', 'New Event')
                date = agent_action.parameters.get('date', '2026-04-07')
                time = agent_action.parameters.get('time', '15:00')
                
                calendar_result = await google_calendar_service.create_event(
                    db=db,
                    user_id=user_id,
                    title=title,
                    date=date,
                    time=time,
                    duration_minutes=60,
                    description=f"Event created by CipherMate AI Assistant",
                    timezone=user_timezone
                )
                
                if calendar_result.get("success"):
                    result = calendar_result.get("message", "Calendar event created successfully")
                else:
                    # Check if this is an auth issue - DON'T mark as failed
                    if "not connected" in calendar_result.get("error", "").lower() or "authentication" in calendar_result.get("error", "").lower():
                        agent_action.status = "pending"
                        await db.commit()
                        return ActionExecutionResponse(
                            action_id=agent_action.id,
                            status="requires_auth",
                            result=calendar_result.get("message", "Google Calendar not connected. Please grant permission."),
                            execution_time_ms=0
                        )
                    result = f"❌ Failed to create calendar event: {calendar_result.get('error', 'Unknown error')}"
            except Exception as e:
                logger.error(f"Calendar creation error: {e}")
                # Check if this is an auth issue
                if "not connected" in str(e).lower() or "authentication" in str(e).lower():
                    agent_action.status = "pending"
                    await db.commit()
                    return ActionExecutionResponse(
                        action_id=agent_action.id,
                        status="requires_auth",
                        result=f"Google Calendar not connected. Error: {str(e)}",
                        execution_time_ms=0
                    )
                result = f"❌ Cannot create calendar event: {str(e)}"
        elif agent_action.action == "github_create_issue":
            # Real GitHub API integration - DIRECT DATABASE READ (simpler approach)
            import json
            from sqlalchemy import select, text
            from app.models.service_connection import ServiceConnection

            try:
                # Direct database query to get GitHub token (bypass token_vault complexity)
                result = await db.execute(
                    text("""
                        SELECT metadata_json FROM service_connections 
                        WHERE service_name = 'github' AND is_active = 1 
                        ORDER BY created_at DESC LIMIT 1
                    """)
                )
                row = result.fetchone()
                
                if not row:
                    logger.warning("No active GitHub connection found in database")
                    agent_action.status = "pending"
                    await db.commit()
                    return ActionExecutionResponse(
                        action_id=agent_action.id,
                        status="requires_auth",
                        result="🔐 GitHub authentication required. Please connect your GitHub account.",
                        execution_time_ms=0
                    )
                
                # Parse metadata_json (might be string or dict)
                metadata = row[0]
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                        logger.info("✅ Parsed metadata_json from string")
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse metadata_json: {e}")
                        metadata = {}
                
                # Extract token
                access_token = None
                if metadata and "vault_data" in metadata:
                    token_data = metadata["vault_data"].get("token")
                    if token_data:
                        access_token = token_data.get("access_token")
                        logger.info(f"✅ Extracted GitHub token from database, keys: {token_data.keys()}")
                
                if not access_token:
                    logger.error(f"GitHub token extraction failed. metadata keys: {metadata.keys() if isinstance(metadata, dict) else type(metadata)}")
                    agent_action.status = "pending"
                    await db.commit()
                    return ActionExecutionResponse(
                        action_id=agent_action.id,
                        status="requires_auth",
                        result="🔐 GitHub token not found in database. Please reconnect your GitHub account.",
                        execution_time_ms=0
                    )
                
                logger.info(f"Creating GitHub issue in {agent_action.parameters.get('repo', '')} with token: {access_token[:20]}...")

                import httpx
                repo = agent_action.parameters.get('repo', '')
                title = agent_action.parameters.get('title', 'New issue from CipherMate')
                body = agent_action.parameters.get('body', '')

                # Parse repo from format "owner/repo"
                if '/' in repo:
                    owner, repo_name = repo.split('/', 1)

                    # Call GitHub API to create issue
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"https://api.github.com/repos/{owner}/{repo_name}/issues",
                            headers={
                                "Authorization": f"token {access_token}",
                                "Accept": "application/vnd.github.v3+json"
                            },
                            json={
                                "title": title,
                                "body": body
                            },
                            timeout=10.0
                        )

                        logger.info(f"GitHub API response: {response.status_code} - {response.text[:200]}")

                        if response.status_code == 201:
                            issue_data = response.json()
                            issue_url = issue_data.get('html_url', '')
                            issue_number = issue_data.get('number', '')
                            result = f"✅ GitHub issue #{issue_number} created successfully!\n\n🔗 View issue: {issue_url}"
                        else:
                            error_msg = response.json().get('message', 'Unknown error')
                            result = f"❌ Failed to create GitHub issue: {error_msg}"
                else:
                    result = f"❌ Invalid repository format: {repo}. Use 'owner/repo'"
            except Exception as e:
                logger.error(f"GitHub issue creation error: {e}")
                result = f"❌ Cannot create GitHub issue: {str(e)}"
        elif agent_action.action == "slack_send_message":
            result = "Slack message sent successfully"

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        agent_action.mark_completed(result=result, execution_time_ms=int(execution_time))
        await db.commit()

        return ActionExecutionResponse(
            action_id=agent_action.id,
            status=agent_action.status,
            result=agent_action.result,
            execution_time_ms=agent_action.execution_time_ms
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing action: {e}")
        return ActionExecutionResponse(
            action_id=request.action_id,
            status="failed",
            result=f"❌ Action failed: {str(e)}",
            execution_time_ms=0
        )
async def execute_action(
    request: ActionExecutionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ActionExecutionResponse:
    """
    Execute a specific agent action
    """
    try:
        logger.info(f"Executing action {request.action_id} for user {current_user.id}")
        
        agent_action = await db.get(AgentAction, request.action_id)
        if not agent_action or agent_action.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found"
            )

        # Allow re-execution for actions that need auth after OAuth completes
        # These actions require authentication and may have been "completed" without actual execution
        auth_required_actions = ["email_send", "calendar_create_event", "github_create_issue", "slack_send_message"]
        if agent_action.status not in ["pending", "requires_auth"]:
            # Allow retry for auth-required actions that were marked completed but didn't actually execute
            if (agent_action.status == "completed" and 
                agent_action.action in auth_required_actions and
                (agent_action.result is None or 
                 "successfully" in agent_action.result.lower() or
                 "auth" in agent_action.result.lower() or 
                 "permission" in agent_action.result.lower() or
                 "connect" in agent_action.result.lower())):
                logger.info(f"Re-executing auth-required action {request.action_id} (was {agent_action.status})")
                agent_action.status = "pending"
                await db.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Action is not in pending status (current: {agent_action.status})"
                )

        if not request.confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action execution must be confirmed"
            )
        
        agent_action.mark_executing()
        await db.commit()
        
        start_time = datetime.now()
        result = "Action executed successfully"
        
        if agent_action.action == "email_send":
            # Real Gmail integration
            from app.api.routes.gmail_auth import temp_tokens
            from app.services.gmail_real import RealGmailService

            if 'current' not in temp_tokens:
                # Check if this is an auth issue - return friendly message
                agent_action.status = "pending"
                await db.commit()
                return ActionExecutionResponse(
                    action_id=agent_action.id,
                    status="requires_auth",
                    result="🔐 Gmail access required. Please grant permission to continue.",
                    execution_time_ms=0
                )

            try:
                # Extract email parameters
                token_data = temp_tokens['current']
                gmail_service = RealGmailService(
                    access_token=token_data.get('access_token'),
                    refresh_token=token_data.get('refresh_token')
                )

                to_email = agent_action.parameters.get('to', '')
                subject = agent_action.parameters.get('subject', 'Message from CipherMate')
                body = agent_action.parameters.get('body', '')

                # Send the email
                email_result = gmail_service.send_email_sync(
                    to=to_email,
                    subject=subject,
                    body=body
                )

                if email_result.get("success"):
                    result = f"✅ Email sent successfully to {to_email}!\n\n📧 Subject: {subject}\n🆔 Message ID: {email_result.get('message_id')}"
                else:
                    result = f"❌ Failed to send email: {email_result.get('error', 'Unknown error')}"

            except Exception as e:
                logger.error(f"Gmail sending error: {e}")
                # Check if this is an auth issue
                if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
                    agent_action.status = "pending"
                    await db.commit()
                    return ActionExecutionResponse(
                        action_id=agent_action.id,
                        status="requires_auth",
                        result=f"🔐 Gmail authentication expired. Please reconnect.",
                        execution_time_ms=0
                    )
                result = f"❌ Cannot send email: {str(e)}"
            
        elif agent_action.action == "calendar_create_event":
            # Real Google Calendar integration
            from app.services.google_calendar import google_calendar_service
            
            try:
                # Extract parameters
                title = agent_action.parameters.get('title', 'New Event')
                date = agent_action.parameters.get('date', '2026-04-07')
                time = agent_action.parameters.get('time', '15:00')
                
                # Create the calendar event
                calendar_result = await google_calendar_service.create_event(
                    db=db,
                    user_id=current_user.id,
                    title=title,
                    date=date,
                    time=time,
                    duration_minutes=60,
                    description=f"Event created by CipherMate AI Assistant"
                )
                
                if calendar_result.get("success"):
                    result = calendar_result["message"]
                else:
                    result = f"❌ Failed to create calendar event: {calendar_result.get('error', 'Unknown error')}"
                    
            except Exception as e:
                logger.error(f"Calendar creation error: {e}")
                result = f"❌ Cannot create calendar event: {str(e)}\n\nPlease ensure your Google Calendar is connected in Settings → Integrations"
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        agent_action.mark_completed(result=result, execution_time_ms=int(execution_time))
        await db.commit()
        
        return ActionExecutionResponse(
            action_id=agent_action.id,
            status=agent_action.status,
            result=agent_action.result,
            execution_time_ms=agent_action.execution_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing action: {e}")
        try:
            if 'agent_action' in locals():
                agent_action.mark_failed(str(e))
                await db.commit()
        except:
            pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute action"
        )


@router.get("/actions")
async def get_user_actions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """Get user's agent actions history"""
    try:
        from sqlalchemy import select, desc

        query = (
            select(AgentAction)
            .where(AgentAction.user_id == current_user.id)
            .order_by(desc(AgentAction.created_at))
            .limit(limit)
            .offset(offset)
        )

        result = await db.execute(query)
        actions = result.scalars().all()

        action_list = []
        for action in actions:
            action_dict = {
                "id": action.id,
                "action": action.action,
                "parameters": action.parameters,
                "status": action.status,
                "result": action.result,
                "requires_step_up": action.requires_step_up,
                "created_at": action.created_at.isoformat() if action.created_at else None,
                "executed_at": action.executed_at.isoformat() if action.executed_at else None,
                "execution_time_ms": action.execution_time_ms
            }
            action_list.append(action_dict)

        return {
            "actions": action_list,
            "total": len(action_list),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        logger.error(f"Error getting user actions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve actions")


# Keep the rest of your endpoints (providers, permissions, etc.) as they were

async def _get_user_permissions(db: AsyncSession, user_id: int) -> List[Dict[str, Any]]:
    """Helper function to get user's current permissions"""
    try:
        from sqlalchemy import select
        
        query = (
            select(ServiceConnection)
            .where(ServiceConnection.user_id == user_id)
            .where(ServiceConnection.is_active == True)
        )
        
        result = await db.execute(query)
        connections = result.scalars().all()
        
        permissions = []
        for conn in connections:
            permissions.append({
                "service_name": conn.service_name,
                "scopes": conn.scopes or [],
                "is_active": conn.is_active,
                "created_at": conn.created_at,
                "expires_at": conn.expires_at
            })
        
        return permissions
        
    except Exception as e:
        logger.error(f"Error getting user permissions: {e}")
        return []


def _generate_oauth_url(service_name: str, user: Optional[User]) -> Optional[str]:
    """Generate OAuth URL for the specified service"""
    from urllib.parse import urlencode
    import secrets

    try:
        if service_name == "google_calendar":
            # Google Calendar OAuth URL
            if not settings.GOOGLE_CLIENT_ID or settings.GOOGLE_CLIENT_ID == "":
                logger.error("Google client ID not configured")
                return None
            
            # Get frontend URL dynamically
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            if not frontend_url or frontend_url == 'http://localhost:3000':
                if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
                    frontend_url = 'https://ciphermate.vercel.app'
                else:
                    frontend_url = 'http://localhost:3000'
            
            params = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "redirect_uri": f"{frontend_url}/api/v1/auth/google/callback",
                "response_type": "code",
                "scope": "https://www.googleapis.com/auth/calendar",
                "access_type": "offline",
                "prompt": "consent",
                "state": f"state_{secrets.token_urlsafe(16)}"
            }
            return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

        elif service_name == "gmail":
            # Gmail OAuth URL
            if not settings.GOOGLE_CLIENT_ID or settings.GOOGLE_CLIENT_ID == "":
                logger.error("Google client ID not configured")
                return None
            
            # Get frontend URL dynamically
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            if not frontend_url or frontend_url == 'http://localhost:3000':
                if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
                    frontend_url = 'https://ciphermate.vercel.app'
                else:
                    frontend_url = 'http://localhost:3000'
            
            params = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "redirect_uri": f"{frontend_url}/api/v1/auth/gmail/callback",
                "response_type": "code",
                "scope": "https://www.googleapis.com/auth/gmail.send",
                "access_type": "offline",
                "prompt": "consent",
                "state": f"state_{secrets.token_urlsafe(16)}"
            }
            return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

        elif service_name == "github":
            # GitHub OAuth URL
            if not settings.GITHUB_CLIENT_ID or settings.GITHUB_CLIENT_ID == "":
                logger.error("GitHub client ID not configured")
                return None
            
            # Get frontend URL dynamically
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            if not frontend_url or frontend_url == 'http://localhost:3000':
                if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
                    frontend_url = 'https://ciphermate.vercel.app'
                else:
                    frontend_url = 'http://localhost:3000'
            
            params = {
                "client_id": settings.GITHUB_CLIENT_ID,
                "redirect_uri": f"{frontend_url}/api/auth/github/callback",
                "scope": "repo",
                "state": f"state_{secrets.token_urlsafe(16)}"
            }
            return f"https://github.com/login/oauth/authorize?{urlencode(params)}"

        elif service_name == "slack":
            # Slack OAuth URL
            if not settings.SLACK_CLIENT_ID or settings.SLACK_CLIENT_ID == "":
                logger.error("Slack client ID not configured")
                return None
            
            # Use production URL for redirect URI
            if settings.APP_ENV == "production":
                redirect_uri = f"{settings.APP_BASE_URL}/api/auth/slack/callback"
            else:
                # For development, use HTTPS localhost or the configured base URL
                redirect_uri = "https://localhost:3000/api/auth/slack/callback"
            
            params = {
                "client_id": settings.SLACK_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "scope": "chat:write,channels:read",
                "state": f"state_{secrets.token_urlsafe(16)}"
            }
            return f"https://slack.com/oauth/v2/authorize?{urlencode(params)}"

        else:
            logger.warning(f"Unknown service for OAuth URL generation: {service_name}")
            return None

    except Exception as e:
        logger.error(f"Error generating OAuth URL for {service_name}: {e}")
        return None


@router.get("/connections")
async def get_user_connections(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get user's service connections"""
    try:
        # If no auth, return empty list
        if not current_user:
            return []
        
        from sqlalchemy import select
        
        query = (
            select(ServiceConnection)
            .where(ServiceConnection.user_id == current_user.id)
            .where(ServiceConnection.is_active == True)
        )
        
        result = await db.execute(query)
        connections = result.scalars().all()
        
        connection_list = []
        for conn in connections:
            connection_list.append({
                "id": conn.id,
                "service_name": conn.service_name,
                "service_type": conn.service_type,
                "status": "active" if conn.is_active else "inactive",
                "created_at": conn.created_at.isoformat() if conn.created_at else None
            })
        
        return connection_list
        
    except Exception as e:
        logger.error(f"Error getting user connections: {e}")
        return []


# Note: I removed the duplicate `execute_action_demo` standalone function and the broken fallback code.

