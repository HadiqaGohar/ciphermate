"""Database seeding utilities with initial data"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.permission_template import PermissionTemplate
import logging

logger = logging.getLogger(__name__)


async def create_permission_templates(session: AsyncSession) -> None:
    """Create initial permission templates for supported services"""
    
    # Check if permission templates already exist
    result = await session.execute(select(PermissionTemplate).limit(1))
    if result.first():
        logger.info("Permission templates already exist, skipping creation")
        return
    
    # Google Calendar permissions
    google_calendar_templates = [
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/calendar.readonly",
            description="Read access to Google Calendar events",
            risk_level="low",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/calendar",
            description="Full access to Google Calendar (read/write events)",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/calendar.events",
            description="Manage Google Calendar events",
            risk_level="medium",
            requires_step_up=False
        ),
    ]
    
    # Gmail permissions
    gmail_templates = [
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/gmail.readonly",
            description="Read access to Gmail messages",
            risk_level="medium",
            requires_step_up=True
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/gmail.send",
            description="Send emails via Gmail",
            risk_level="high",
            requires_step_up=True
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/gmail.compose",
            description="Compose and send Gmail messages",
            risk_level="high",
            requires_step_up=True
        ),
    ]
    
    # Google Drive permissions
    google_drive_templates = [
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/drive.readonly",
            description="Read access to Google Drive files",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/drive.file",
            description="Access to Google Drive files created by the app",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="google",
            scope_name="https://www.googleapis.com/auth/drive",
            description="Full access to Google Drive",
            risk_level="critical",
            requires_step_up=True
        ),
    ]
    
    # GitHub permissions
    github_templates = [
        PermissionTemplate(
            service_name="github",
            scope_name="user:email",
            description="Access to user email addresses",
            risk_level="low",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="github",
            scope_name="repo",
            description="Full control of private repositories",
            risk_level="high",
            requires_step_up=True
        ),
        PermissionTemplate(
            service_name="github",
            scope_name="public_repo",
            description="Access to public repositories",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="github",
            scope_name="read:org",
            description="Read access to organization membership",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="github",
            scope_name="write:repo_hook",
            description="Write access to repository hooks",
            risk_level="high",
            requires_step_up=True
        ),
    ]
    
    # Slack permissions
    slack_templates = [
        PermissionTemplate(
            service_name="slack",
            scope_name="channels:read",
            description="View basic information about public channels",
            risk_level="low",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="slack",
            scope_name="channels:write",
            description="Send messages to channels",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="slack",
            scope_name="chat:write",
            description="Send messages as the user",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="slack",
            scope_name="users:read",
            description="View people in the workspace",
            risk_level="low",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="slack",
            scope_name="files:write",
            description="Upload and share files",
            risk_level="medium",
            requires_step_up=False
        ),
        PermissionTemplate(
            service_name="slack",
            scope_name="admin",
            description="Administer the workspace",
            risk_level="critical",
            requires_step_up=True
        ),
    ]
    
    # Combine all templates
    all_templates = (
        google_calendar_templates +
        gmail_templates +
        google_drive_templates +
        github_templates +
        slack_templates
    )
    
    # Add all templates to the session
    for template in all_templates:
        session.add(template)
    
    logger.info(f"Created {len(all_templates)} permission templates")


async def create_sample_user(session: AsyncSession, auth0_id: str, email: str, name: str) -> None:
    """Create a sample user for testing purposes"""
    from app.models.user import User
    
    # Check if user already exists
    result = await session.execute(select(User).where(User.auth0_id == auth0_id))
    if result.first():
        logger.info(f"User {auth0_id} already exists, skipping creation")
        return
    
    user = User(
        auth0_id=auth0_id,
        email=email,
        name=name,
        preferences={"theme": "light", "notifications": True}
    )
    
    session.add(user)
    logger.info(f"Created sample user: {email}")


async def seed_sample_data(session: AsyncSession) -> None:
    """Seed the database with sample data for development/testing"""
    
    # Create sample users
    await create_sample_user(
        session,
        "auth0|sample_user_1",
        "user1@example.com",
        "Sample User 1"
    )
    
    await create_sample_user(
        session,
        "auth0|sample_user_2", 
        "user2@example.com",
        "Sample User 2"
    )
    
    logger.info("Sample data seeded successfully")