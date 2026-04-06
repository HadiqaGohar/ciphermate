"""Gmail OAuth authentication routes"""

from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
import os
import json
import logging
from app.core.config import settings

router = APIRouter(prefix="/api/auth/gmail", tags=["gmail-auth"])
logger = logging.getLogger(__name__)

# Store tokens temporarily (in production, use database)
temp_tokens = {}

# Configure OAuth
oauth = OAuth()

def get_oauth_client():
    """Get configured OAuth client"""
    try:
        if not hasattr(oauth, 'google') or oauth.google is None:
            oauth.register(
                name='google',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
                client_kwargs={
                    'scope': 'https://www.googleapis.com/auth/gmail.send'
                }
            )
        return oauth.google
    except Exception as e:
        logger.error(f"OAuth client setup error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth configuration error: {str(e)}")

@router.post("/demo-token")
async def create_demo_gmail_token():
    """Create a demo Gmail token for hackathon testing - NOT FOR PRODUCTION"""
    global temp_tokens
    
    # Create a fake token for demo purposes
    temp_tokens['current'] = {
        'access_token': 'demo_access_token_for_hackathon',
        'refresh_token': 'demo_refresh_token',
        'expires_in': 3600,
        'scope': 'https://www.googleapis.com/auth/gmail.send'
    }
    
    logger.info("✅ Demo Gmail token created for hackathon testing")
    
    return {
        "message": "✅ Demo Gmail token created for hackathon testing!",
        "warning": "This is a DEMO token - emails will be simulated",
        "access_token_received": True,
        "expires_in": 3600,
        "scopes": "https://www.googleapis.com/auth/gmail.send",
        "next_step": "You can now test email actions via the demo endpoint"
    }


@router.get("/login")
async def gmail_login(request: Request):
    """Start Gmail OAuth flow"""
    try:
        google = get_oauth_client()
        redirect_uri = str(request.url_for('gmail_callback'))
        logger.info(f"Starting Gmail OAuth with redirect URI: {redirect_uri}")
        
        return await google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"Gmail login error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth setup error: {str(e)}")

@router.get("/callback")
async def gmail_callback(request: Request):
    """Handle Gmail OAuth callback"""
    try:
        google = get_oauth_client()
        token = await google.authorize_access_token(request)
        
        logger.info(f"✅ Gmail token received: {token.get('access_token', '')[:50]}...")
        
        # Store token (in production, save to database with user_id)
        # For now, store in memory
        temp_tokens['current'] = {
            'access_token': token.get('access_token'),
            'refresh_token': token.get('refresh_token'),
            'expires_in': token.get('expires_in'),
            'scope': token.get('scope')
        }
        
        return {
            "message": "✅ Gmail connected successfully!",
            "access_token_received": True,
            "expires_in": token.get('expires_in'),
            "scopes": token.get('scope'),
            "next_step": "You can now send real emails via the chat interface!"
        }
        
    except Exception as e:
        logger.error(f"Gmail OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth callback error: {str(e)}")

@router.get("/token")
async def get_token():
    """Get current token (for testing)"""
    if 'current' in temp_tokens:
        token_data = temp_tokens['current']
        return {
            "access_token": token_data.get('access_token', '')[:50] + "...",
            "has_refresh_token": bool(token_data.get('refresh_token')),
            "expires_in": token_data.get('expires_in'),
            "scopes": token_data.get('scope')
        }
    return {"error": "No token available. Please login first at /api/auth/gmail/login"}

@router.get("/status")
async def gmail_status():
    """Check Gmail API configuration status"""
    return {
        "gmail_enabled": settings.GMAIL_ENABLED,
        "client_id_configured": bool(settings.GOOGLE_CLIENT_ID),
        "client_secret_configured": bool(settings.GOOGLE_CLIENT_SECRET),
        "token_available": 'current' in temp_tokens,
        "ready_to_send": settings.GMAIL_ENABLED and 'current' in temp_tokens
    }

@router.post("/revoke")
async def revoke_token():
    """Revoke Gmail token"""
    if 'current' in temp_tokens:
        del temp_tokens['current']
        return {"message": "Token revoked successfully"}
    return {"message": "No token to revoke"}