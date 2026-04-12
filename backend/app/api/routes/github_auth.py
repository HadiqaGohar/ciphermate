"""GitHub OAuth Callback Handler"""

import logging
import json
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.core.token_vault import token_vault_service
from app.core.database import AsyncSessionLocal
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(tags=["github-auth"])


@router.get("/api/auth/github/callback")
async def github_callback(request: Request):
    """Handle GitHub OAuth callback and store tokens"""
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    error = request.query_params.get('error')

    if error:
        logger.error(f"GitHub OAuth error: {error}")
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>GitHub OAuth Failed</title></head>
        <body style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
            <h2 style="color: red;">❌ GitHub Authorization Failed</h2>
            <p>Error: ERROR_PLACEHOLDER</p>
            <script>
                if (window.opener) {
                    window.opener.postMessage({ type: 'oauth_error', service: 'github', error: 'ERROR_PLACEHOLDER' }, '*');
                }
                setTimeout(() => window.close(), 2000);
            </script>
        </body>
        </html>
        """.replace("ERROR_PLACEHOLDER", error)
        return HTMLResponse(content=html_content, status_code=400)

    if not code:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Missing Code</title></head>
        <body style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
            <h2>Missing authorization code</h2>
            <script>setTimeout(() => window.close(), 2000);</script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=400)

    try:
        # Exchange code for tokens
        client_id = getattr(settings, 'GITHUB_CLIENT_ID', '')
        client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', '')

        if not client_id or not client_secret:
            logger.error("GitHub credentials not configured")
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>Configuration Error</title></head>
            <body style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
                <h2>GitHub credentials not configured. Please configure GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in .env</h2>
                <script>setTimeout(() => window.close(), 2000);</script>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=500)

        # Get frontend URL dynamically
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        if not frontend_url or frontend_url == 'http://localhost:3000':
            if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
                frontend_url = 'https://ciphermate.vercel.app'
            else:
                frontend_url = 'http://localhost:3000'

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "state": state,
                    "redirect_uri": f"{frontend_url}/api/auth/github/callback"
                },
                timeout=10.0
            )

            if token_response.status_code != 200:
                logger.error(f"GitHub token exchange failed: {token_response.status_code}")
                return HTMLResponse(
                    content="<h2>Failed to exchange code for tokens</h2>",
                    status_code=500
                )

            token_data = token_response.json()
            access_token = token_data.get('access_token')
            token_type = token_data.get('token_type', 'bearer')
            scope = token_data.get('scope', '')

            if not access_token:
                logger.error("No access_token in GitHub response")
                return HTMLResponse(
                    content="<h2>No access token received from GitHub</h2>",
                    status_code=500
                )

            # Get GitHub user info
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if user_response.status_code != 200:
                logger.error(f"Failed to get GitHub user info: {user_response.status_code}")
                return HTMLResponse(
                    content="<h2>Failed to retrieve user information</h2>",
                    status_code=500
                )

            github_user = user_response.json()
            github_user_id = str(github_user.get('id'))
            github_username = github_user.get('login')

            logger.info(f"GitHub user authenticated: {github_username} (ID: {github_user_id})")

            # Store token DIRECTLY in database with minimal complexity
            try:
                # Use user ID 0 for all GitHub users (simplest approach)
                db_user_id = 0
                
                from sqlalchemy import text
                async with AsyncSessionLocal() as db:
                    # Deactivate old github connections
                    await db.execute(
                        text("UPDATE service_connections SET is_active = 0 WHERE service_name = 'github'")
                    )
                    await db.commit()
                    
                    # Insert new connection directly
                    result = await db.execute(
                        text("""
                            INSERT INTO service_connections 
                            (user_id, service_name, token_vault_id, scopes, is_active, created_at, metadata_json)
                            VALUES (:user_id, :service, :vault_id, :scopes, 1, datetime('now'), :metadata)
                        """),
                        {
                            "user_id": db_user_id,
                            "service": "github",
                            "vault_id": f"github_{github_user_id}",
                            "scopes": json.dumps(scope.split(',') if scope else []),
                            "metadata": json.dumps({
                                "vault_data": {
                                    "token": {
                                        "access_token": access_token,
                                        "token_type": token_type,
                                        "scope": scope
                                    }
                                },
                                "github_user_id": github_user_id,
                                "github_username": github_username
                            })
                        }
                    )
                    await db.commit()
                    logger.info(f"✅ SUCCESS: Stored GitHub token for user {github_username}")
            except Exception as e:
                import traceback
                logger.error(f"❌ FAILED to store GitHub token: {type(e).__name__}: {e}")
                logger.error(traceback.format_exc())

            # Return success HTML page
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>GitHub OAuth Successful</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }
                    .container {
                        text-align: center;
                        background: rgba(255, 255, 255, 0.1);
                        padding: 40px;
                        border-radius: 16px;
                        backdrop-filter: blur(10px);
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    }
                    h2 {
                        margin: 0 0 16px 0;
                        font-size: 28px;
                    }
                    p {
                        margin: 8px 0;
                        font-size: 16px;
                        opacity: 0.9;
                    }
                    .close-btn {
                        margin-top: 20px;
                        padding: 10px 24px;
                        background: white;
                        color: #667eea;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.2s;
                    }
                    .close-btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>✅ GitHub Connected Successfully!</h2>
                    <p>Welcome, <strong>@GITHUB_USERNAME_PLACEHOLDER</strong></p>
                    <p>Your GitHub account is now linked to CipherMate.</p>
                    <button class="close-btn" onclick="window.close()">Close Window</button>
                </div>
                <script>
                    if (window.opener) {
                        window.opener.postMessage({
                            type: 'oauth_success',
                            service: 'github',
                            user_id: 'USER_ID_PLACEHOLDER',
                            username: 'GITHUB_USERNAME_PLACEHOLDER'
                        }, '*');
                    }
                    setTimeout(() => window.close(), 3000);
                </script>
            </body>
            </html>
            """.replace("GITHUB_USERNAME_PLACEHOLDER", github_username).replace("USER_ID_PLACEHOLDER", github_user_id)

            return HTMLResponse(content=html_content, status_code=200)

    except httpx.TimeoutException:
        logger.error("GitHub OAuth timeout")
        return HTMLResponse(
            content="<h2>Request timed out. Please try again.</h2>",
            status_code=504
        )
    except Exception as e:
        logger.error(f"GitHub OAuth callback error: {e}")
        return HTMLResponse(
            content=f"<h2>An error occurred: {str(e)}</h2>",
            status_code=500
        )
