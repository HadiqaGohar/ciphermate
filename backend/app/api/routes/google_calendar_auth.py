"""Google Calendar OAuth authentication routes"""

from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
import httpx
import logging
from app.core.config import settings

router = APIRouter(prefix="/api/v1/auth/google", tags=["google-calendar-auth"])
logger = logging.getLogger(__name__)

# Store tokens temporarily (in production, use database)
temp_tokens = {}

# Configure OAuth
oauth = OAuth()

def get_google_oauth_client():
    """Get configured Google OAuth client"""
    try:
        if not hasattr(oauth, 'google_calendar') or oauth.google_calendar is None:
            oauth.register(
                name='google_calendar',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
                client_kwargs={
                    'scope': 'https://www.googleapis.com/auth/calendar email profile'
                }
            )
        return oauth.google_calendar
    except Exception as e:
        logger.error(f"Google OAuth client setup error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth configuration error: {str(e)}")


@router.get("/login")
async def google_calendar_login(request: Request):
    """Start Google Calendar OAuth flow"""
    try:
        google = get_google_oauth_client()
        redirect_uri = str(request.url_for('google_calendar_callback'))
        logger.info(f"Starting Google Calendar OAuth with redirect URI: {redirect_uri}")

        return await google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"Google Calendar login error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth setup error: {str(e)}")


@router.get("/callback")
async def google_calendar_callback(request: Request):
    """Handle Google Calendar OAuth callback"""
    try:
        google = get_google_oauth_client()
        token = await google.authorize_access_token(request)

        logger.info(f"✅ Google Calendar token received: {token.get('access_token', '')[:50]}...")

        # Store token (in production, save to database with user_id)
        temp_tokens['current'] = {
            'access_token': token.get('access_token'),
            'refresh_token': token.get('refresh_token'),
            'expires_in': token.get('expires_in'),
            'scope': token.get('scope'),
            'token_type': token.get('token_type', 'Bearer')
        }

        return {
            "message": "✅ Google Calendar connected successfully!",
            "access_token_received": True,
            "expires_in": token.get('expires_in'),
            "scopes": token.get('scope'),
            "next_step": "You can now manage calendar events!"
        }

    except Exception as e:
        logger.error(f"Google Calendar OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth callback error: {str(e)}")


@router.post("/exchange-token")
async def exchange_token(request: Request):
    """Exchange authorization code for access token (bypasses state validation for popup flow)"""
    try:
        body = await request.json()
        code = body.get("code")
        redirect_uri = body.get("redirect_uri")
        
        # If no redirect_uri provided, determine it dynamically
        #done
        if not redirect_uri:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            logger.info(f"🔍 FRONTEND_URL from settings: {frontend_url}")
            logger.info(f"🔍 APP_ENV from settings: {getattr(settings, 'APP_ENV', 'NOT_SET')}")
            
            if not frontend_url or frontend_url == 'http://localhost:3000':
                if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
                    frontend_url = 'https://ciphermate.vercel.app'
                    logger.info(f"🔧 Using production frontend URL: {frontend_url}")
                else:
                    frontend_url = 'http://localhost:3000'
                    logger.info(f"🔧 Using localhost frontend URL: {frontend_url}")
            else:
                logger.info(f"🔧 Using configured frontend URL: {frontend_url}")
                
            redirect_uri = f"{frontend_url}/api/auth/google/callback"

        if not code:
            raise HTTPException(status_code=400, detail="Authorization code is required")

        logger.info(f"Exchanging code for token, redirect_uri: {redirect_uri}")

        # Directly call Google token endpoint (bypass authlib state validation)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            )

        if response.status_code != 200:
            logger.error(f"Google token endpoint returned: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to exchange code: {response.text}"
            )

        token_data = response.json()

        logger.info(f"✅ Token exchange successful")

        # Store token
        temp_tokens['current'] = {
            'access_token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'expires_in': token_data.get('expires_in'),
            'scope': token_data.get('scope'),
            'token_type': token_data.get('token_type', 'Bearer')
        }

        return {
            "success": True,
            "message": "✅ Google Calendar connected successfully!",
            "access_token_received": True,
            "expires_in": token_data.get('expires_in'),
            "scopes": token_data.get('scope')
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token exchange error: {e}")
        raise HTTPException(status_code=500, detail=f"Token exchange failed: {str(e)}")


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
    return {"error": "No token available. Please login first at /api/v1/auth/google/login"}


@router.get("/status")
async def google_calendar_status():
    """Check Google Calendar API configuration status"""
    return {
        "google_calendar_enabled": bool(settings.GOOGLE_CLIENT_ID),
        "client_id_configured": bool(settings.GOOGLE_CLIENT_ID),
        "client_secret_configured": bool(settings.GOOGLE_CLIENT_SECRET),
        "token_available": 'current' in temp_tokens,
        "ready_to_use": bool(settings.GOOGLE_CLIENT_ID) and 'current' in temp_tokens
    }


@router.post("/revoke")
async def revoke_token():
    """Revoke Google Calendar token"""
    if 'current' in temp_tokens:
        del temp_tokens['current']
        return {"message": "Token revoked successfully"}
    return {"message": "No token to revoke"}
