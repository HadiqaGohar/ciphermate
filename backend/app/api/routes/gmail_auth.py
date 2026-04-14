"""Gmail OAuth authentication routes"""

from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
import os
import json
import logging
import httpx
from app.core.config import settings

router = APIRouter(prefix="/api/v1/auth/gmail", tags=["gmail-auth"])
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
    """Handle Gmail OAuth callback - exchange token directly, no redirect loop"""
    try:
        from starlette.responses import RedirectResponse
        
        code = request.query_params.get("code")
        error = request.query_params.get("error")
        state = request.query_params.get("state")
        
        # Get frontend URL
        frontend_url = getattr(settings, 'FRONTEND_URL', "https://ciphermate.vercel.app")
        
        # If there's an error from Google
        if error:
            logger.error(f"Gmail OAuth error: {error}")
            return RedirectResponse(
                url=f"{frontend_url}?error={error}&service=gmail",
                status_code=302
            )
        
        # If no code received
        if not code:
            logger.error("No authorization code received")
            return RedirectResponse(
                url=f"{frontend_url}?error=no_code&service=gmail",
                status_code=302
            )
        
        # Exchange code for token DIRECTLY (no redirect to frontend)
        logger.info(f"✅ Gmail code received, exchanging token directly")

        # Use the redirect_uri from the frontend (must match what was used in auth request)
        # For GET callback from browser flow, use frontend URL
        redirect_uri = f"{frontend_url}/api/v1/auth/gmail/callback"
        logger.info(f"🔧 Using frontend redirect URI: {redirect_uri}")

        # Call Google token endpoint
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
            logger.error(f"Gmail token exchange failed: {response.status_code} - {response.text}")
            return RedirectResponse(
                url=f"{frontend_url}?error=token_exchange_failed&service=gmail",
                status_code=302
            )
        
        token_data = response.json()
        
        # Store token
        temp_tokens['current'] = {
            'access_token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'expires_in': token_data.get('expires_in'),
            'scope': token_data.get('scope'),
            'token_type': token_data.get('token_type', 'Bearer')
        }
        
        logger.info(f"✅ Gmail token stored successfully")
        
        # Redirect to frontend with success message
        return RedirectResponse(
            url=f"{frontend_url}?success=true&service=gmail",
            status_code=302
        )

    except Exception as e:
        logger.error(f"Gmail OAuth callback error: {e}")
        from starlette.responses import RedirectResponse
        frontend_url = getattr(settings, 'FRONTEND_URL', "https://ciphermate.vercel.app")
        return RedirectResponse(
            url=f"{frontend_url}?error=callback_failed&service=gmail",
            status_code=302
        )

@router.post("/callback")
async def exchange_token(request: Request):
    """Exchange authorization code for access token (for popup flow)"""
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
                logger.info(f"🔧 Using APP_BASE_URL for Gmail: {base_url}")
            else:
                # Derive from request headers (works in Cloud Run)
                base_url = f"{scheme}://{host}"
                logger.info(f"🔧 Using request-derived URL for Gmail: {base_url}")
            
            redirect_uri = f"{base_url}/api/v1/auth/gmail/callback"
            logger.info(f"🔧 Using dynamic Gmail redirect URI: {redirect_uri}")

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

        logger.info(f"✅ Gmail token stored! Access token: {token_data.get('access_token', '')[:20]}...")
        logger.info(f"📦 Current temp_tokens keys: {list(temp_tokens.keys())}")

        return {
            "success": True,
            "message": "✅ Gmail connected successfully!",
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