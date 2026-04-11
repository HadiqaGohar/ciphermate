"""Real Gmail API service for sending emails"""

import base64
import os
import logging
import time
import asyncio
from typing import Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.token_vault import token_vault_service

logger = logging.getLogger(__name__)

class RealGmailService:
    """Service for sending real emails via Gmail API"""
    
    def __init__(self, access_token: str = None, refresh_token: str = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.service = None
    
    def _get_service(self):
        """Get or create Gmail service"""
        if not self.service:
            creds = Credentials(
                token=self.access_token,
                refresh_token=self.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                scopes=["https://www.googleapis.com/auth/gmail.send"]
            )
            self.service = build('gmail', 'v1', credentials=creds)
        return self.service
    
    async def send_email(self, db, user_id: int, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send real email using Gmail API (async wrapper)"""
        try:
            # Get Gmail token from vault
            user_id_str = str(user_id)
            token_data = await token_vault_service.retrieve_token(
                user_id=user_id_str,
                service_name="gmail",
                auto_refresh=False
            )

            # Fallback to temp_tokens if no token in vault (for OAuth flow)
            if not token_data:
                logger.warning(f"No Gmail token found for user {user_id}, checking temp_tokens")
                # Import here to avoid circular imports
                from app.api.routes.gmail_auth import temp_tokens
                
                if 'current' in temp_tokens:
                    token_data = temp_tokens['current']
                    logger.info(f"✅ Using Gmail token from temp_tokens")
                else:
                    logger.warning(f"No Gmail token in temp_tokens either")
                    return {
                        "success": False,
                        "error": "Gmail not connected",
                        "message": "🔐 Gmail authentication required. Please connect your Gmail account."
                    }

            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            
            if not access_token:
                logger.error(f"Gmail token data structure: {token_data}")
                return {
                    "success": False,
                    "error": "Invalid Gmail token",
                    "message": "❌ Invalid Gmail token: missing access_token"
                }

            # Create service instance with tokens
            self.access_token = access_token
            self.refresh_token = refresh_token
            
            # Run sync method in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.send_email_sync, to, subject, body)
            
            return result
            
        except Exception as e:
            logger.error(f"Gmail send error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Cannot send email: {str(e)}"
            }
    
    def send_email_sync(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send real email using Gmail API (synchronous)"""
        try:
            service = self._get_service()
            
            # Create email message
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['subject'] = subject
            
            # HTML body with nice formatting
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">
                        {subject}
                    </h2>
                    <div style="background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; font-size: 16px;">{body}</p>
                    </div>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                    <div style="text-align: center; color: #6b7280; font-size: 14px;">
                        <p style="margin: 5px 0;">
                            <strong>🤖 Sent by CipherMate AI Assistant</strong>
                        </p>
                        <p style="margin: 5px 0;">
                            Secure AI-powered email automation
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send via Gmail API
            sent = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            logger.info(f"✅ Real email sent! Message ID: {sent['id']} to {to}")
            
            return {
                "success": True,
                "message_id": sent['id'],
                "to": to,
                "subject": subject,
                "status": "delivered",
                "provider": "gmail_api",
                "timestamp": "now",
                "message": f"✅ Email sent successfully to {to}!"
            }
            
        except Exception as e:
            logger.error(f"❌ Gmail send failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to send email: {str(e)}",
                "provider": "gmail_api"
            }

# Create global instance
gmail_service = RealGmailService()