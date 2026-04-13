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
    """Handle Google Calendar OAuth callback - redirect to frontend for token exchange"""
    try:
        code = request.query_params.get("code")
        error = request.query_params.get("error")
        state = request.query_params.get("state")
        
        # Get frontend URL from environment or request
        frontend_url = getattr(settings, 'FRONTEND_URL', None)
        if not frontend_url or frontend_url == 'http://localhost:3000':
            # Try to derive from request
            host = request.headers.get("host", "")
            scheme = request.headers.get("x-forwarded-proto", "http")
            # Default to production Vercel URL
            frontend_url = "https://ciphermate.vercel.app"
        
        # If there's an error from Google, redirect to frontend with error
        if error:
            logger.error(f"Google OAuth error: {error}")
            from starlette.responses import RedirectResponse
            return RedirectResponse(
                url=f"{frontend_url}/api/v1/auth/google/callback?error={error}",
                status_code=302
            )
        
        # If no code received, redirect with error
        if not code:
            logger.error("No authorization code received")
            from starlette.responses import RedirectResponse
            return RedirectResponse(
                url=f"{frontend_url}/api/v1/auth/google/callback?error=no_code",
                status_code=302
            )
        
        # Redirect to frontend callback with code for token exchange
        # Frontend will call POST /api/v1/auth/google/exchange-token
        logger.info(f"✅ Google Calendar code received, redirecting to frontend for token exchange")
        from starlette.responses import RedirectResponse
        return RedirectResponse(
            url=f"{frontend_url}/api/v1/auth/google/callback?code={code}&state={state or ''}",
            status_code=302
        )

    except Exception as e:
        logger.error(f"Google Calendar OAuth callback error: {e}")
        # Redirect to frontend with error
        from starlette.responses import RedirectResponse
        frontend_url = getattr(settings, 'FRONTEND_URL', "https://ciphermate.vercel.app")
        return RedirectResponse(
            url=f"{frontend_url}/api/v1/auth/google/callback?error=callback_failed",
            status_code=302
        )


@router.post("/exchange-token")
async def exchange_token(request: Request):
    """Exchange authorization code for access token (bypasses state validation for popup flow)"""
    try:
        body = await request.json()
        code = body.get("code")
        redirect_uri = body.get("redirect_uri")
        
        # If no redirect_uri provided, determine it dynamically
        if not redirect_uri:
            # Get the base URL from the request or environment
            host = request.headers.get("host", "")
            scheme = request.headers.get("x-forwarded-proto", "http")
            
            # Use APP_BASE_URL if configured, otherwise derive from request
            if hasattr(settings, 'APP_BASE_URL') and settings.APP_BASE_URL and settings.APP_BASE_URL != "http://localhost:8080":
                base_url = settings.APP_BASE_URL.strip()
                logger.info(f"🔧 Using APP_BASE_URL: {base_url}")
            else:
                # Derive from request headers (works in Cloud Run)
                base_url = f"{scheme}://{host}"
                logger.info(f"🔧 Using request-derived URL: {base_url}")
            
            redirect_uri = f"{base_url}/api/v1/auth/google/callback"
            logger.info(f"🔧 Using dynamic redirect URI: {redirect_uri}")
        
        # Clean up any trailing spaces
        redirect_uri = redirect_uri.strip()

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
