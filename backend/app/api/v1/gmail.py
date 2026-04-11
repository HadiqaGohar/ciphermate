"""Gmail API endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
import os
import logging
from typing import Dict, Any

from app.services.gmail_real import RealGmailService
from app.api.routes.gmail_auth import temp_tokens
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gmail", tags=["gmail"])

class EmailRequest(BaseModel):
    """Request model for sending email"""
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    action_id: int = Field(None, description="Action ID for tracking")

class EmailResponse(BaseModel):
    """Response model for email sending"""
    success: bool
    message: str
    message_id: str = None
    to: str = None
    subject: str = None
    status: str = None
    provider: str = None
    demo_mode: bool = False
    requires_auth: bool = False
    auth_url: str = None

@router.post("/send", response_model=EmailResponse)
async def send_email(email_data: EmailRequest):
    """Send email via Gmail API"""
    try:
        # Check if Gmail is enabled
        if not settings.GMAIL_ENABLED:
            return EmailResponse(
                success=False,
                message="⚠️ Gmail API not configured. Please add GMAIL_ENABLED=true to .env",
                demo_mode=True
            )
        
        # Check if we have OAuth token
        token_data = temp_tokens.get('current')
        if not token_data or not token_data.get('access_token'):
            return EmailResponse(
                success=False,
                message="Please authenticate with Gmail first",
                requires_auth=True,
                auth_url="/api/auth/gmail/login"
            )
        
        # Send real email
        gmail_service = RealGmailService(
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token')
        )
        
        result = gmail_service.send_email_sync(
            to=email_data.to,
            subject=email_data.subject,
            body=email_data.body
        )
        
        if result['success']:
            return EmailResponse(
                success=True,
                message=f"✅ Real email sent successfully to {email_data.to}!",
                message_id=result['message_id'],
                to=email_data.to,
                subject=email_data.subject,
                status=result['status'],
                provider=result['provider']
            )
        else:
            return EmailResponse(
                success=False,
                message=f"❌ Failed to send email: {result['message']}"
            )
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def gmail_status():
    """Get Gmail service status"""
    return {
        "gmail_enabled": settings.GMAIL_ENABLED,
        "client_id_configured": bool(settings.GOOGLE_CLIENT_ID),
        "client_secret_configured": bool(settings.GOOGLE_CLIENT_SECRET),
        "token_available": 'current' in temp_tokens,
        "ready_to_send": settings.GMAIL_ENABLED and 'current' in temp_tokens,
        "auth_url": "/api/auth/gmail/login" if 'current' not in temp_tokens else None
    }
        # // done hadiqa
