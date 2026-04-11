"""Google Calendar service for real calendar integration"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.service_connection import ServiceConnection

logger = logging.getLogger(__name__)


class GoogleCalendarService:
    """Service for interacting with Google Calendar API"""
    
    def __init__(self):
        self.service_name = "google_calendar"
        self.required_scopes = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/calendar.events"
        ]
    
    async def create_event(
        self,
        db: AsyncSession,
        user_id: int,
        title: str,
        date: str,
        time: str,
        duration_minutes: int = 60,
        description: str = None,
        location: str = None,
        timezone: str = None
    ) -> Dict[str, Any]:
        """Create a calendar event using Google Calendar API"""
        
        try:
            # Get user's Google Calendar credentials
            credentials = await self._get_user_credentials(db, user_id)
            if not credentials:
                raise Exception("Google Calendar not connected. Please connect your Google account first.")
            
            # Build the calendar service
            service = build('calendar', 'v3', credentials=credentials)
            
            # Parse date and time
            start_datetime = self._parse_datetime(date, time)
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)
            
            # Use provided timezone or default to Asia/Karachi
            event_timezone = timezone or 'Asia/Karachi'

            # Create event object
            event = {
                'summary': title,
                'description': description or f"Event created by CipherMate AI Assistant",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': event_timezone,
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': event_timezone,
                },
            }
            
            # Add location if provided
            if location:
                event['location'] = location
            
            # Insert the event
            created_event = service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            logger.info(f"✅ Calendar event created successfully: {created_event['id']}")
            
            return {
                "success": True,
                "event_id": created_event['id'],
                "html_link": created_event.get('htmlLink', ''),
                "message": f"✅ **Calendar Event Created Successfully!**\n\n**Title:** {title}\n**Date:** {date}\n**Time:** {time}\n**Duration:** {duration_minutes} minutes\n\n🔗 **View Event:** {created_event.get('htmlLink', 'Event created in your calendar')}"
            }
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            if e.resp.status == 401:
                raise Exception("Google Calendar authentication expired. Please reconnect your Google account.")
            elif e.resp.status == 403:
                raise Exception("Insufficient permissions for Google Calendar. Please reconnect with calendar permissions.")
            else:
                raise Exception(f"Google Calendar API error: {e}")
                
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            raise Exception(f"Failed to create calendar event: {str(e)}")
    
    async def list_events(
        self, 
        db: AsyncSession, 
        user_id: int, 
        max_results: int = 10,
        time_min: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """List upcoming calendar events"""
        
        try:
            credentials = await self._get_user_credentials(db, user_id)
            if not credentials:
                raise Exception("Google Calendar not connected. Please connect your Google account first.")
            
            service = build('calendar', 'v3', credentials=credentials)
            
            # Set default time_min to now if not provided
            if not time_min:
                time_min = datetime.utcnow()
            
            # Call the Calendar API
            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return {
                    "success": True,
                    "events": [],
                    "message": "No upcoming events found."
                }
            
            event_list = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_list.append({
                    "id": event['id'],
                    "summary": event.get('summary', 'No title'),
                    "start": start,
                    "html_link": event.get('htmlLink', '')
                })
            
            return {
                "success": True,
                "events": event_list,
                "message": f"Found {len(event_list)} upcoming events."
            }
            
        except Exception as e:
            logger.error(f"Error listing calendar events: {e}")
            raise Exception(f"Failed to list calendar events: {str(e)}")
    
    async def _get_user_credentials(self, db: AsyncSession, user_id: int) -> Optional[Credentials]:
        """Get user's Google Calendar credentials from database or temp tokens"""

        # First try: check temp_tokens (in-memory, for current session)
        try:
            from app.api.routes.google_calendar_auth import temp_tokens
            if 'current' in temp_tokens:
                token_data = temp_tokens['current']
                logger.info("✅ Using temp token for Google Calendar")
                return Credentials(
                    token=token_data.get('access_token'),
                    refresh_token=token_data.get('refresh_token'),
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=settings.GOOGLE_CLIENT_ID,
                    client_secret=settings.GOOGLE_CLIENT_SECRET,
                    scopes=token_data.get('scope', self.required_scopes).split() if isinstance(token_data.get('scope'), str) else self.required_scopes
                )
        except Exception as e:
            logger.warning(f"Temp tokens not available: {e}")

        # Second try: query database for stored connection
        try:
            from sqlalchemy import select

            query = select(ServiceConnection).where(
                ServiceConnection.user_id == user_id,
                ServiceConnection.service_name == "google",
                ServiceConnection.is_active == True
            )

            result = await db.execute(query)
            connection = result.scalar_one_or_none()

            if not connection:
                logger.warning(f"No active Google connection found for user {user_id}")
                return None

            if not connection.access_token:
                logger.warning(f"No access token found for user {user_id}")
                return None

            # Create credentials object
            credentials = Credentials(
                token=connection.access_token,
                refresh_token=connection.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                scopes=connection.scopes or self.required_scopes
            )

            # Check if credentials are valid and refresh if needed
            if credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())

                    # Update the stored tokens
                    connection.access_token = credentials.token
                    if credentials.refresh_token:
                        connection.refresh_token = credentials.refresh_token

                    await db.commit()
                    logger.info(f"✅ Refreshed Google credentials for user {user_id}")

                except Exception as refresh_error:
                    logger.error(f"Failed to refresh Google credentials: {refresh_error}")
                    return None

            return credentials

        except Exception as e:
            logger.error(f"Error getting user credentials: {e}")
            return None
    
    def _parse_datetime(self, date: str, time: str) -> datetime:
        """Parse date and time strings into datetime object"""
        
        try:
            # Parse date (expected format: YYYY-MM-DD)
            date_parts = date.split('-')
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
            
            # Parse time (expected format: HH:MM)
            time_parts = time.split(':')
            hour, minute = int(time_parts[0]), int(time_parts[1])
            
            return datetime(year, month, day, hour, minute)
            
        except Exception as e:
            logger.error(f"Error parsing datetime: {e}")
            # Fallback to a default time
            return datetime.now() + timedelta(hours=1)


# Create a global instance
google_calendar_service = GoogleCalendarService()