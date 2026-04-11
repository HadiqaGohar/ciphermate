"""Real Gmail API service for sending emails"""

import base64
import os
import logging
import time
from typing import Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
    # // done hadiqa

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
    
    def send_email_sync(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send real email using Gmail API (synchronous)"""
        try:
            # Check if this is a demo token
            if self.access_token == 'demo_access_token_for_hackathon':
                logger.info(f"🎭 DEMO MODE: Simulating email send to {to}")
                return {
                    "success": True,
                    "message_id": f"demo_message_id_{int(time.time())}",
                    "to": to,
                    "subject": subject,
                    "status": "demo_delivered",
                    "provider": "gmail_api_demo",
                    "timestamp": "now",
                    "note": "This is a DEMO - no real email was sent"
                }
            
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
                "timestamp": "now"
            }
            
        except Exception as e:
            logger.error(f"❌ Gmail send failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to send email: {str(e)}",
                "provider": "gmail_api"
            }