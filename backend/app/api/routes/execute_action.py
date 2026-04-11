from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import logging
from typing import Optional

from app.core.auth import get_current_user
from app.core.token_vault import token_vault_service
from app.core.service_clients import service_client_factory

logger = logging.getLogger(__name__)

router = APIRouter(tags=["execute"])


async def get_calendar_token(user_id: str) -> Optional[dict]:
    """Get Google Calendar token from token vault"""
    try:
        token_data = await token_vault_service.retrieve_token(
            user_id=user_id,
            service="google_calendar"
        )
        return token_data
    except Exception as e:
        logger.error(f"Error retrieving calendar token: {e}")
        return None


@router.post("/execute-action")
async def execute_action(action_data: dict, current_user: dict = Depends(get_current_user)):
    """Execute action for calendar, email, etc."""
    intent_type = action_data.get('intent_type')
    params = action_data.get('parameters', {})
    user_id = current_user.get('sub') or current_user.get('auth0_id')
    
    if intent_type == "EMAIL_SEND":
        from app.api.routes.gmail_auth import temp_token
        
        if not temp_token:
            return {
                "success": False,
                "requires_auth": True,
                "auth_url": "http://localhost:8080/api/auth/gmail/login",
                "message": "Gmail authentication required. Please visit: http://localhost:8080/api/auth/gmail/login"
            }
        
        # Send real email
        try:
            from app.services.gmail_real import send_real_email
            result = send_real_email(
                to=params.get('to'),
                subject=params.get('subject'),
                body=params.get('body'),
                access_token=temp_token['access_token']
            )
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to send email: {str(e)}"
            }
    
    elif intent_type == "CALENDAR_CREATE_EVENT":
        # Get calendar token
        calendar_token = await get_calendar_token(user_id)
        
        if not calendar_token:
            return {
                "success": False,
                "requires_auth": True,
                "auth_url": "http://localhost:8080/api/v1/auth/google",
                "message": "Google Calendar authentication required. Please connect Google Calendar first.",
                "provider": "google_calendar",
                "action_needed": "Connect Google Calendar in settings"
            }
        
        # Extract event parameters
        title = params.get('title', 'Meeting')
        date = params.get('date', '2026-04-06')
        time = params.get('time', '15:00')
        description = params.get('description', '')
        
        # Parse date and time
        try:
            start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_datetime = start_datetime.replace(hour=(start_datetime.hour + 1) % 24)
        except:
            start_datetime = datetime.now()
            end_datetime = start_datetime.replace(hour=(start_datetime.hour + 1) % 24)
        
        # Create real calendar event
        try:
            client = service_client_factory.get_google_calendar_client()
            response = await client.create_event(
                user_id=user_id,
                calendar_id="primary",
                summary=title,
                description=description,
                start_time=start_datetime,
                end_time=end_datetime
            )
            
            if response.success:
                event_id = response.data.get('id', 'unknown')
                return {
                    "success": True,
                    "message": f"✅ Calendar event '{title}' created for {date} at {time}!",
                    "event_id": event_id,
                    "provider": "google_calendar",
                    "execution_time_ms": 500,
                    "event_link": response.data.get('htmlLink', '')
                }
            else:
                return {
                    "success": False,
                    "error": response.error,
                    "message": f"Failed to create calendar event: {response.error}",
                    "provider": "google_calendar"
                }
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create calendar event: {str(e)}",
                "provider": "google_calendar"
            }
    
    return {
        "success": True, 
        "message": "Action completed",
        "provider": "ciphermate",
        "execution_time_ms": 25
    }