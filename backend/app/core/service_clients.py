"""
Service-specific API clients for Google Calendar, Gmail, GitHub, and Slack.
Provides high-level interfaces for common operations with each service.
"""

from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timezone
import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.core.api_integration import APIIntegrationService, APIService, APIResponse, APIServiceError
from app.models.todo_task import ToDoTask, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)
    # // done hadiqa


class BaseServiceClient(ABC):
    """Base class for service-specific API clients"""
    
    def __init__(self, api_service: APIIntegrationService):
        self.api_service = api_service
    
    @property
    @abstractmethod
    def service_type(self) -> APIService:
        """Return the API service type"""
        pass
    
    async def _make_call(
        self,
        user_id: str,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """Make an API call using the integration service"""
        return await self.api_service.make_api_call(
            user_id=user_id,
            service=self.service_type,
            method=method,
            endpoint=endpoint,
            data=data,
            params=params,
            headers=headers
        )


class GoogleCalendarClient(BaseServiceClient):
    """Google Calendar API client"""
    
    @property
    def service_type(self) -> APIService:
        return APIService.GOOGLE_CALENDAR
    
    async def list_calendars(self, user_id: str) -> APIResponse:
        """List all calendars for the user"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users/me/calendarList"
        )
    
    async def get_calendar(self, user_id: str, calendar_id: str) -> APIResponse:
        """Get details of a specific calendar"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/calendars/{calendar_id}"
        )
    
    async def list_events(
        self,
        user_id: str,
        calendar_id: str = "primary",
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 10
    ) -> APIResponse:
        """List events from a calendar"""
        params = {
            "maxResults": max_results,
            "singleEvents": True,
            "orderBy": "startTime"
        }
        
        if time_min:
            params["timeMin"] = time_min.isoformat()
        if time_max:
            params["timeMax"] = time_max.isoformat()
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/calendars/{calendar_id}/events",
            params=params
        )
    
    async def create_event(
        self,
        user_id: str,
        calendar_id: str = "primary",
        summary: str = "",
        description: str = "",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        attendees: Optional[List[str]] = None
    ) -> APIResponse:
        """Create a new calendar event"""
        event_data = {
            "summary": summary,
            "description": description
        }
        
        if start_time and end_time:
            event_data["start"] = {"dateTime": start_time.isoformat(), "timeZone": "UTC"}
            event_data["end"] = {"dateTime": end_time.isoformat(), "timeZone": "UTC"}
        
        if attendees:
            event_data["attendees"] = [{"email": email} for email in attendees]
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint=f"/calendars/{calendar_id}/events",
            data=event_data
        )
    
    async def update_event(
        self,
        user_id: str,
        calendar_id: str,
        event_id: str,
        updates: Dict[str, Any]
    ) -> APIResponse:
        """Update an existing calendar event"""
        return await self._make_call(
            user_id=user_id,
            method="PUT",
            endpoint=f"/calendars/{calendar_id}/events/{event_id}",
            data=updates
        )
    
    async def delete_event(
        self,
        user_id: str,
        calendar_id: str,
        event_id: str
    ) -> APIResponse:
        """Delete a calendar event"""
        return await self._make_call(
            user_id=user_id,
            method="DELETE",
            endpoint=f"/calendars/{calendar_id}/events/{event_id}"
        )


class GmailClient(BaseServiceClient):
    """Gmail API client"""
    
    @property
    def service_type(self) -> APIService:
        return APIService.GMAIL
    
    async def get_profile(self, user_id: str) -> APIResponse:
        """Get user's Gmail profile"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users/me/profile"
        )
    
    async def list_messages(
        self,
        user_id: str,
        query: str = "",
        max_results: int = 10,
        label_ids: Optional[List[str]] = None
    ) -> APIResponse:
        """List messages in the user's mailbox"""
        params = {
            "maxResults": max_results
        }
        
        if query:
            params["q"] = query
        if label_ids:
            params["labelIds"] = label_ids
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users/me/messages",
            params=params
        )
    
    async def get_message(
        self,
        user_id: str,
        message_id: str,
        format: str = "full"
    ) -> APIResponse:
        """Get a specific message"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/users/me/messages/{message_id}",
            params={"format": format}
        )
    
    async def send_message(
        self,
        user_id: str,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None
    ) -> APIResponse:
        """Send an email message"""
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create message
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/users/me/messages/send",
            data={"raw": raw_message}
        )
    
    async def list_labels(self, user_id: str) -> APIResponse:
        """List all labels in the user's mailbox"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users/me/labels"
        )
    
    async def create_label(
        self,
        user_id: str,
        name: str,
        message_list_visibility: str = "show",
        label_list_visibility: str = "labelShow"
    ) -> APIResponse:
        """Create a new label"""
        label_data = {
            "name": name,
            "messageListVisibility": message_list_visibility,
            "labelListVisibility": label_list_visibility
        }
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/users/me/labels",
            data=label_data
        )


class GitHubClient(BaseServiceClient):
    """GitHub API client"""
    
    @property
    def service_type(self) -> APIService:
        return APIService.GITHUB
    
    async def get_user(self, user_id: str) -> APIResponse:
        """Get authenticated user information"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/user"
        )
    
    async def list_repositories(
        self,
        user_id: str,
        visibility: str = "all",
        sort: str = "updated",
        per_page: int = 30
    ) -> APIResponse:
        """List repositories for the authenticated user"""
        params = {
            "visibility": visibility,
            "sort": sort,
            "per_page": per_page
        }
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/user/repos",
            params=params
        )
    
    async def get_repository(
        self,
        user_id: str,
        owner: str,
        repo: str
    ) -> APIResponse:
        """Get a specific repository"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/repos/{owner}/{repo}"
        )
    
    async def create_repository(
        self,
        user_id: str,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True
    ) -> APIResponse:
        """Create a new repository"""
        repo_data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/user/repos",
            data=repo_data
        )
    
    async def list_issues(
        self,
        user_id: str,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> APIResponse:
        """List issues for a repository"""
        params = {
            "state": state,
            "per_page": per_page
        }
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/repos/{owner}/{repo}/issues",
            params=params
        )
    
    async def create_issue(
        self,
        user_id: str,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> APIResponse:
        """Create a new issue"""
        issue_data = {
            "title": title,
            "body": body
        }
        
        if labels:
            issue_data["labels"] = labels
        if assignees:
            issue_data["assignees"] = assignees
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint=f"/repos/{owner}/{repo}/issues",
            data=issue_data
        )
    
    async def list_pull_requests(
        self,
        user_id: str,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> APIResponse:
        """List pull requests for a repository"""
        params = {
            "state": state,
            "per_page": per_page
        }
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint=f"/repos/{owner}/{repo}/pulls",
            params=params
        )
    
    async def create_pull_request(
        self,
        user_id: str,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: str = ""
    ) -> APIResponse:
        """Create a new pull request"""
        pr_data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint=f"/repos/{owner}/{repo}/pulls",
            data=pr_data
        )


class SlackClient(BaseServiceClient):
    """Slack API client"""
    
    @property
    def service_type(self) -> APIService:
        return APIService.SLACK
    
    async def get_user_info(self, user_id: str) -> APIResponse:
        """Get information about the authenticated user"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/auth.test"
        )
    
    async def list_channels(
        self,
        user_id: str,
        exclude_archived: bool = True,
        types: str = "public_channel,private_channel"
    ) -> APIResponse:
        """List channels in the workspace"""
        params = {
            "exclude_archived": exclude_archived,
            "types": types
        }
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/conversations.list",
            params=params
        )
    
    async def get_channel_info(
        self,
        user_id: str,
        channel_id: str
    ) -> APIResponse:
        """Get information about a specific channel"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/conversations.info",
            params={"channel": channel_id}
        )
    
    async def send_message(
        self,
        user_id: str,
        channel: str,
        text: str,
        blocks: Optional[List[Dict[str, Any]]] = None,
        thread_ts: Optional[str] = None
    ) -> APIResponse:
        """Send a message to a channel"""
        message_data = {
            "channel": channel,
            "text": text
        }
        
        if blocks:
            message_data["blocks"] = blocks
        if thread_ts:
            message_data["thread_ts"] = thread_ts
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/chat.postMessage",
            data=message_data
        )
    
    async def get_message_history(
        self,
        user_id: str,
        channel: str,
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None
    ) -> APIResponse:
        """Get message history from a channel"""
        params = {
            "channel": channel,
            "limit": limit
        }
        
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/conversations.history",
            params=params
        )
    
    async def list_users(
        self,
        user_id: str,
        limit: int = 100
    ) -> APIResponse:
        """List users in the workspace"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users.list",
            params={"limit": limit}
        )
    
    async def get_user_profile(
        self,
        user_id: str,
        target_user: str
    ) -> APIResponse:
        """Get profile information for a specific user"""
        return await self._make_call(
            user_id=user_id,
            method="GET",
            endpoint="/users.profile.get",
            params={"user": target_user}
        )
    
    async def create_channel(
        self,
        user_id: str,
        name: str,
        is_private: bool = False
    ) -> APIResponse:
        """Create a new channel"""
        channel_data = {
            "name": name,
            "is_private": is_private
        }
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/conversations.create",
            data=channel_data
        )
    
    async def invite_to_channel(
        self,
        user_id: str,
        channel: str,
        users: List[str]
    ) -> APIResponse:
        """Invite users to a channel"""
        invite_data = {
            "channel": channel,
            "users": ",".join(users)
        }
        
        return await self._make_call(
            user_id=user_id,
            method="POST",
            endpoint="/conversations.invite",
            data=invite_data
        )


class ToDoService:
    """ToDo service for managing user tasks (mock service - no external API)"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(
        self,
        user_id: int,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> ToDoTask:
        """Create a new task"""
        try:
            # Map priority string to enum
            priority_enum = TaskPriority(priority.lower())
        except ValueError:
            priority_enum = TaskPriority.MEDIUM

        task = ToDoTask(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority_enum,
            due_date=due_date
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        logger.info(f"Created task {task.id} for user {user_id}")
        return task

    async def get_tasks(
        self,
        user_id: int,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[ToDoTask]:
        """Get all tasks for a user with optional filters"""
        query = select(ToDoTask).where(ToDoTask.user_id == user_id)

        if status:
            try:
                status_enum = TaskStatus(status.lower())
                query = query.where(ToDoTask.status == status_enum)
            except ValueError:
                pass

        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
                query = query.where(ToDoTask.priority == priority_enum)
            except ValueError:
                pass

        query = query.order_by(
            ToDoTask.priority,  # High priority first
            ToDoTask.due_date.nullsfirst()  # Due dates first
        )

        result = await self.db.execute(query)
        tasks = result.scalars().all()
        return tasks

    async def get_task(self, user_id: int, task_id: int) -> Optional[ToDoTask]:
        """Get a specific task by ID"""
        query = select(ToDoTask).where(
            ToDoTask.id == task_id,
            ToDoTask.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_task_status(
        self,
        user_id: int,
        task_id: int,
        status: str
    ) -> Optional[ToDoTask]:
        """Update task status"""
        task = await self.get_task(user_id, task_id)
        if not task:
            return None

        try:
            status_enum = TaskStatus(status.lower())
            task.status = status_enum

            # Set completed_at if status is completed
            if status_enum == TaskStatus.COMPLETED:
                task.completed_at = datetime.now(timezone.utc)
            else:
                task.completed_at = None

            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Updated task {task_id} status to {status}")
            return task
        except ValueError as e:
            logger.error(f"Invalid status: {status}")
            return None

    async def update_task(
        self,
        user_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None
    ) -> Optional[ToDoTask]:
        """Update task details"""
        task = await self.get_task(user_id, task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            try:
                task.priority = TaskPriority(priority.lower())
            except ValueError:
                pass
        if due_date is not None:
            task.due_date = due_date

        await self.db.commit()
        await self.db.refresh(task)
        logger.info(f"Updated task {task_id}")
        return task

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        """Delete a task"""
        task = await self.get_task(user_id, task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        logger.info(f"Deleted task {task_id}")
        return True

    async def get_pending_tasks_count(self, user_id: int) -> int:
        """Get count of pending tasks"""
        query = select(ToDoTask).where(
            ToDoTask.user_id == user_id,
            ToDoTask.status == TaskStatus.PENDING
        )
        result = await self.db.execute(query)
        tasks = result.scalars().all()
        return len(tasks)


# Service client factory
class ServiceClientFactory:
    """Factory for creating service-specific clients"""
    
    def __init__(self, api_service: APIIntegrationService):
        self.api_service = api_service
        self._clients = {}
    
    def get_google_calendar_client(self) -> GoogleCalendarClient:
        """Get Google Calendar client"""
        if "google_calendar" not in self._clients:
            self._clients["google_calendar"] = GoogleCalendarClient(self.api_service)
        return self._clients["google_calendar"]
    
    def get_gmail_client(self) -> GmailClient:
        """Get Gmail client"""
        if "gmail" not in self._clients:
            self._clients["gmail"] = GmailClient(self.api_service)
        return self._clients["gmail"]
    
    def get_github_client(self) -> GitHubClient:
        """Get GitHub client"""
        if "github" not in self._clients:
            self._clients["github"] = GitHubClient(self.api_service)
        return self._clients["github"]
    
    def get_slack_client(self) -> SlackClient:
        """Get Slack client"""
        if "slack" not in self._clients:
            self._clients["slack"] = SlackClient(self.api_service)
        return self._clients["slack"]

    def get_todo_service(self, db: AsyncSession) -> ToDoService:
        """Get ToDo service"""
        return ToDoService(db)

    def get_client(self, service_name: str) -> BaseServiceClient:
        """Get client by service name"""
        service_name = service_name.lower()

        if service_name in ["google_calendar", "calendar"]:
            return self.get_google_calendar_client()
        elif service_name in ["gmail", "email"]:
            return self.get_gmail_client()
        elif service_name == "github":
            return self.get_github_client()
        elif service_name == "slack":
            return self.get_slack_client()
        else:
            raise ValueError(f"Unsupported service: {service_name}")


# Global factory instance
from app.core.api_integration import api_integration_service
service_client_factory = ServiceClientFactory(api_integration_service)