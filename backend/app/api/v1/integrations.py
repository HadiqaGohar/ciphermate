"""
API endpoints for third-party service integrations.
Provides secure access to Google Calendar, Gmail, GitHub, and Slack APIs.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Request
from pydantic import BaseModel, Field
import logging

from app.core.auth import get_current_user
from app.core.api_integration import api_integration_service, APIServiceError, RateLimitError, AuthorizationError, ServiceUnavailableError
from app.core.service_clients import service_client_factory
from app.core.audit_service import audit_service, PerformanceTracker
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/integrations", tags=["integrations"])
    # // done hadiqa


# Request/Response Models
class APICallRequest(BaseModel):
    """Request model for generic API calls"""
    service: str = Field(..., description="Service name (google_calendar, gmail, github, slack)")
    method: str = Field(..., description="HTTP method")
    endpoint: str = Field(..., description="API endpoint path")
    data: Optional[Dict[str, Any]] = Field(None, description="Request body data")
    params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")
    headers: Optional[Dict[str, str]] = Field(None, description="Additional headers")


class APICallResponse(BaseModel):
    """Response model for API calls"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    service: Optional[str] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None


class CalendarEventRequest(BaseModel):
    """Request model for creating calendar events"""
    calendar_id: str = Field(default="primary", description="Calendar ID")
    summary: str = Field(..., description="Event title")
    description: str = Field(default="", description="Event description")
    start_time: datetime = Field(..., description="Event start time")
    end_time: datetime = Field(..., description="Event end time")
    attendees: Optional[List[str]] = Field(None, description="List of attendee emails")


class EmailRequest(BaseModel):
    """Request model for sending emails"""
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    cc: Optional[str] = Field(None, description="CC email address")
    bcc: Optional[str] = Field(None, description="BCC email address")


class GitHubIssueRequest(BaseModel):
    """Request model for creating GitHub issues"""
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    title: str = Field(..., description="Issue title")
    body: str = Field(default="", description="Issue body")
    labels: Optional[List[str]] = Field(None, description="Issue labels")
    assignees: Optional[List[str]] = Field(None, description="Issue assignees")


class SlackMessageRequest(BaseModel):
    """Request model for sending Slack messages"""
    channel: str = Field(..., description="Channel ID or name")
    text: str = Field(..., description="Message text")
    blocks: Optional[List[Dict[str, Any]]] = Field(None, description="Message blocks")
    thread_ts: Optional[str] = Field(None, description="Thread timestamp for replies")


# Generic API Integration Endpoints
@router.post("/call", response_model=APICallResponse)
async def make_api_call(
    request_data: APICallRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Make a generic API call to any supported service.
    Provides low-level access to third-party APIs with secure token injection.
    """
    try:
        # Map service names to API service enum values
        service_mapping = {
            "google_calendar": "google_calendar",
            "gmail": "gmail", 
            "github": "github",
            "slack": "slack"
        }
        
        service_name = service_mapping.get(request_data.service.lower())
        if not service_name:
            await audit_service.log_security_event(
                user_id=current_user.id,
                event_type="unsupported_service_access",
                severity="warning",
                details={"requested_service": request_data.service},
                request=request
            )
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported service: {request_data.service}"
            )
        
        # Track performance and log the API call
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="api_call",
            service_name=service_name,
            details={
                "method": request_data.method,
                "endpoint": request_data.endpoint,
                "has_data": request_data.data is not None,
                "has_params": request_data.params is not None
            }
        ):
            # Make the API call
            from app.core.api_integration import APIService
            api_service = APIService(service_name)
            
            response = await api_integration_service.make_api_call(
                user_id=current_user.auth0_id,
                service=api_service,
                method=request_data.method.upper(),
                endpoint=request_data.endpoint,
                data=request_data.data,
                params=request_data.params,
                headers=request_data.headers
            )
        
        # Log the API call result
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="api_call",
            service_name=service_name,
            details={
                "method": request_data.method.upper(),
                "endpoint": request_data.endpoint,
                "success": response.success,
                "status_code": response.status_code,
                "rate_limit_remaining": response.rate_limit_remaining
            },
            request=request
        )
        
        return APICallResponse(
            success=response.success,
            data=response.data,
            error=response.error,
            status_code=response.status_code,
            service=response.service,
            rate_limit_remaining=response.rate_limit_remaining,
            rate_limit_reset=response.rate_limit_reset
        )
        
    except AuthorizationError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="api_authorization_error",
            severity="warning",
            details={"service": service_name, "error": str(e)},
            request=request
        )
        raise HTTPException(status_code=401, detail=str(e))
    except RateLimitError as e:
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="api_rate_limited",
            service_name=service_name,
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=429, detail=str(e))
    except ServiceUnavailableError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="service_unavailable",
            severity="error",
            details={"service": service_name, "error": str(e)},
            request=request
        )
        raise HTTPException(status_code=503, detail=str(e))
    except APIServiceError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="api_service_error",
            severity="error",
            details={"service": service_name, "error": str(e)},
            request=request
        )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in API call: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="api_call_error",
            severity="error",
            details={"service": service_name, "error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/rate-limits/{service}")
async def get_rate_limit_status(
    service: str,
    current_user: User = Depends(get_current_user)
):
    """Get current rate limit status for a service"""
    try:
        status = await api_integration_service.get_rate_limit_status(service)
        return status
    except Exception as e:
        logger.error(f"Error getting rate limit status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def integration_health_check():
    """Health check for the integration service"""
    try:
        health = await api_integration_service.health_check()
        return health
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")


# Google Calendar Endpoints
@router.get("/google-calendar/calendars")
async def list_calendars(
    current_user: User = Depends(get_current_user)
):
    """List all calendars for the authenticated user"""
    try:
        client = service_client_factory.get_google_calendar_client()
        response = await client.list_calendars(current_user.auth0_id)
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing calendars: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/google-calendar/events")
async def list_calendar_events(
    calendar_id: str = Query(default="primary", description="Calendar ID"),
    max_results: int = Query(default=10, ge=1, le=100, description="Maximum number of events"),
    current_user: User = Depends(get_current_user)
):
    """List events from a calendar"""
    try:
        client = service_client_factory.get_google_calendar_client()
        response = await client.list_events(
            user_id=current_user.auth0_id,
            calendar_id=calendar_id,
            max_results=max_results
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing events: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/google-calendar/events")
async def create_calendar_event(
    request_data: CalendarEventRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Create a new calendar event"""
    try:
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="create_calendar_event",
            service_name="google_calendar",
            details={"calendar_id": request_data.calendar_id}
        ):
            client = service_client_factory.get_google_calendar_client()
            response = await client.create_event(
                user_id=current_user.auth0_id,
                calendar_id=request_data.calendar_id,
                summary=request_data.summary,
                description=request_data.description,
                start_time=request_data.start_time,
                end_time=request_data.end_time,
                attendees=request_data.attendees
            )
        
        # Log the calendar event creation
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="calendar_event_created",
            service_name="google_calendar",
            details={
                "calendar_id": request_data.calendar_id,
                "summary": request_data.summary,
                "start_time": request_data.start_time.isoformat(),
                "end_time": request_data.end_time.isoformat(),
                "attendee_count": len(request_data.attendees) if request_data.attendees else 0,
                "success": response.success
            },
            request=request
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="calendar_authorization_error",
            severity="warning",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="calendar_event_creation_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


# Gmail Endpoints
@router.get("/gmail/profile")
async def get_gmail_profile(
    current_user: User = Depends(get_current_user)
):
    """Get Gmail profile information"""
    try:
        client = service_client_factory.get_gmail_client()
        response = await client.get_profile(current_user.auth0_id)
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting Gmail profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/gmail/messages")
async def list_gmail_messages(
    query: str = Query(default="", description="Search query"),
    max_results: int = Query(default=10, ge=1, le=100, description="Maximum number of messages"),
    current_user: User = Depends(get_current_user)
):
    """List Gmail messages"""
    try:
        client = service_client_factory.get_gmail_client()
        response = await client.list_messages(
            user_id=current_user.auth0_id,
            query=query,
            max_results=max_results
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing messages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/gmail/send")
async def send_email(
    request_data: EmailRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Send an email via Gmail"""
    try:
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="send_email",
            service_name="gmail",
            details={"has_cc": request_data.cc is not None, "has_bcc": request_data.bcc is not None}
        ):
            client = service_client_factory.get_gmail_client()
            response = await client.send_message(
                user_id=current_user.auth0_id,
                to=request_data.to,
                subject=request_data.subject,
                body=request_data.body,
                cc=request_data.cc,
                bcc=request_data.bcc
            )
        
        # Log the email sending (without sensitive content)
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="email_sent",
            service_name="gmail",
            details={
                "to": request_data.to,
                "subject": request_data.subject,
                "has_cc": request_data.cc is not None,
                "has_bcc": request_data.bcc is not None,
                "body_length": len(request_data.body),
                "success": response.success
            },
            request=request
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="gmail_authorization_error",
            severity="warning",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="email_send_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


# GitHub Endpoints
@router.get("/github/user")
async def get_github_user(
    current_user: User = Depends(get_current_user)
):
    """Get GitHub user information"""
    try:
        client = service_client_factory.get_github_client()
        response = await client.get_user(current_user.auth0_id)
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting GitHub user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/github/repositories")
async def list_github_repositories(
    visibility: str = Query(default="all", description="Repository visibility"),
    per_page: int = Query(default=30, ge=1, le=100, description="Results per page"),
    current_user: User = Depends(get_current_user)
):
    """List GitHub repositories"""
    try:
        client = service_client_factory.get_github_client()
        response = await client.list_repositories(
            user_id=current_user.auth0_id,
            visibility=visibility,
            per_page=per_page
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing repositories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/github/issues")
async def create_github_issue(
    request_data: GitHubIssueRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Create a GitHub issue"""
    try:
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="create_github_issue",
            service_name="github",
            details={"repo": f"{request_data.owner}/{request_data.repo}"}
        ):
            client = service_client_factory.get_github_client()
            response = await client.create_issue(
                user_id=current_user.auth0_id,
                owner=request_data.owner,
                repo=request_data.repo,
                title=request_data.title,
                body=request_data.body,
                labels=request_data.labels,
                assignees=request_data.assignees
            )
        
        # Log the GitHub issue creation
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="github_issue_created",
            service_name="github",
            details={
                "repository": f"{request_data.owner}/{request_data.repo}",
                "title": request_data.title,
                "label_count": len(request_data.labels) if request_data.labels else 0,
                "assignee_count": len(request_data.assignees) if request_data.assignees else 0,
                "success": response.success
            },
            request=request
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="github_authorization_error",
            severity="warning",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating issue: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="github_issue_creation_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


# Slack Endpoints
@router.get("/slack/user")
async def get_slack_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get Slack user information"""
    try:
        client = service_client_factory.get_slack_client()
        response = await client.get_user_info(current_user.auth0_id)
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting Slack user info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/slack/channels")
async def list_slack_channels(
    exclude_archived: bool = Query(default=True, description="Exclude archived channels"),
    current_user: User = Depends(get_current_user)
):
    """List Slack channels"""
    try:
        client = service_client_factory.get_slack_client()
        response = await client.list_channels(
            user_id=current_user.auth0_id,
            exclude_archived=exclude_archived
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing channels: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/slack/messages")
async def send_slack_message(
    request_data: SlackMessageRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Send a Slack message"""
    try:
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="send_slack_message",
            service_name="slack",
            details={"channel": request_data.channel, "is_thread_reply": request_data.thread_ts is not None}
        ):
            client = service_client_factory.get_slack_client()
            response = await client.send_message(
                user_id=current_user.auth0_id,
                channel=request_data.channel,
                text=request_data.text,
                blocks=request_data.blocks,
                thread_ts=request_data.thread_ts
            )
        
        # Log the Slack message sending
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="slack_message_sent",
            service_name="slack",
            details={
                "channel": request_data.channel,
                "message_length": len(request_data.text),
                "has_blocks": request_data.blocks is not None,
                "is_thread_reply": request_data.thread_ts is not None,
                "success": response.success
            },
            request=request
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="slack_authorization_error",
            severity="warning",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="slack_message_send_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/slack/history/{channel}")
async def get_slack_message_history(
    channel: str,
    limit: int = Query(default=100, ge=1, le=1000, description="Number of messages to retrieve"),
    current_user: User = Depends(get_current_user)
):
    """Get Slack message history"""
    try:
        client = service_client_factory.get_slack_client()
        response = await client.get_message_history(
            user_id=current_user.auth0_id,
            channel=channel,
            limit=limit
        )
        
        if not response.success:
            raise HTTPException(status_code=response.status_code or 400, detail=response.error)
        
        return response.data
        
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting message history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ToDo List Integration Endpoints
class ToDoTaskRequest(BaseModel):
    """Request model for creating ToDo tasks"""
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Task description")
    priority: str = Field(default="medium", description="Task priority (low, medium, high, urgent)")
    due_date: Optional[datetime] = Field(None, description="Task due date")


class ToDoTaskUpdateRequest(BaseModel):
    """Request model for updating ToDo tasks"""
    title: Optional[str] = Field(None, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[str] = Field(None, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    status: Optional[str] = Field(None, description="Task status (pending, in_progress, completed, cancelled)")


class ToDoTaskResponse(BaseModel):
    """Response model for ToDo tasks"""
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: str
    updated_at: str


@router.post("/todo/tasks", response_model=ToDoTaskResponse)
async def create_todo_task(
    request_data: ToDoTaskRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new ToDo task via AI.
    Requires todo permission to be granted.
    """
    try:
        from app.core.service_clients import service_client_factory
        from app.core.database import AsyncSessionLocal
        from app.core.permission_service import permission_service

        # Check permission
        has_permission = await permission_service.has_active_permission(
            user_id=current_user.auth0_id,
            service_name="todo"
        )
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="ToDo permission not granted. Please grant permission first."
            )

        # Create task
        async with AsyncSessionLocal() as session:
            todo_service = service_client_factory.get_todo_service(session)
            task = await todo_service.create_task(
                user_id=current_user.id,
                title=request_data.title,
                description=request_data.description,
                priority=request_data.priority,
                due_date=request_data.due_date
            )

        # Log the task creation
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="todo_task_created",
            service_name="todo",
            details={
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority.value,
                "has_due_date": task.due_date is not None
            },
            request=request
        )

        return ToDoTaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            due_date=task.due_date.isoformat() if task.due_date else None,
            completed_at=task.completed_at.isoformat() if task.completed_at else None,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating todo task: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="todo_task_create_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/todo/tasks", response_model=List[ToDoTaskResponse])
async def get_todo_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_user)
):
    """Get all ToDo tasks for the user"""
    try:
        from app.core.service_clients import service_client_factory
        from app.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            todo_service = service_client_factory.get_todo_service(session)
            tasks = await todo_service.get_tasks(
                user_id=current_user.id,
                status=status,
                priority=priority
            )

        return [
            ToDoTaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status.value,
                priority=task.priority.value,
                due_date=task.due_date.isoformat() if task.due_date else None,
                completed_at=task.completed_at.isoformat() if task.completed_at else None,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat()
            )
            for task in tasks
        ]

    except Exception as e:
        logger.error(f"Error getting todo tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/todo/tasks/{task_id}", response_model=ToDoTaskResponse)
async def update_todo_task(
    task_id: int,
    request_data: ToDoTaskUpdateRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Update a ToDo task"""
    try:
        from app.core.service_clients import service_client_factory
        from app.core.database import AsyncSessionLocal
        from app.core.permission_service import permission_service

        # Check permission
        has_permission = await permission_service.has_active_permission(
            user_id=current_user.auth0_id,
            service_name="todo"
        )
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="ToDo permission not granted. Please grant permission first."
            )

        async with AsyncSessionLocal() as session:
            todo_service = service_client_factory.get_todo_service(session)

            # Update status if provided
            if request_data.status:
                task = await todo_service.update_task_status(
                    user_id=current_user.id,
                    task_id=task_id,
                    status=request_data.status
                )
            # Update other fields if provided
            else:
                task = await todo_service.update_task(
                    user_id=current_user.id,
                    task_id=task_id,
                    title=request_data.title,
                    description=request_data.description,
                    priority=request_data.priority,
                    due_date=request_data.due_date
                )

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

        # Log the task update
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="todo_task_updated",
            service_name="todo",
            details={
                "task_id": task.id,
                "title": task.title,
                "status": task.status.value
            },
            request=request
        )

        return ToDoTaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            due_date=task.due_date.isoformat() if task.due_date else None,
            completed_at=task.completed_at.isoformat() if task.completed_at else None,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/todo/tasks/{task_id}")
async def delete_todo_task(
    task_id: int,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Delete a ToDo task"""
    try:
        from app.core.service_clients import service_client_factory
        from app.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            todo_service = service_client_factory.get_todo_service(session)
            success = await todo_service.delete_task(
                user_id=current_user.id,
                task_id=task_id
            )

            if not success:
                raise HTTPException(status_code=404, detail="Task not found")

        # Log the task deletion
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="todo_task_deleted",
            service_name="todo",
            details={"task_id": task_id},
            request=request
        )

        return {"message": "Task deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")