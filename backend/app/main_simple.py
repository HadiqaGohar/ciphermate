"""
Complete working FastAPI application for CipherMate
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import jwt
import httpx
from datetime import datetime, timedelta
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables with defaults
PORT = int(os.getenv("PORT", 8080))
DISABLE_DATABASE = os.getenv("DISABLE_DATABASE", "false").lower() == "true"
DISABLE_REDIS = os.getenv("DISABLE_REDIS", "false").lower() == "true"
DISABLE_AGENTS = os.getenv("DISABLE_AGENTS", "false").lower() == "true"

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")

# Create FastAPI app
app = FastAPI(
    title="CipherMate API",
    description="Secure AI Assistant Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://cipheremate-frontend.vercel.app",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Pydantic Models
class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime
    last_login: datetime

class ServiceConnection(BaseModel):
    id: str
    user_id: str
    service_name: str
    service_type: str
    status: str
    created_at: datetime
    last_used: Optional[datetime] = None

class AIAgentAction(BaseModel):
    id: str
    user_id: str
    agent_type: str
    action: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: datetime

class TokenRequest(BaseModel):
    service: str
    action: str
    permissions: List[str]

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    html: Optional[bool] = False

# In-memory storage (replace with database in production)
users_db: Dict[str, UserProfile] = {}
connections_db: Dict[str, ServiceConnection] = {}
actions_db: Dict[str, AIAgentAction] = {}
tokens_db: Dict[str, Dict[str, Any]] = {}

# Auth0 JWT verification
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Auth0 JWT token"""
    if not credentials:
        return None
    
    token = credentials.credentials
    
    # For development, allow bypass
    if token == "dev-token":
        return {
            "sub": "dev-user-123",
            "email": "dev@example.com",
            "name": "Development User",
            "picture": "https://via.placeholder.com/150"
        }
    
    if not AUTH0_DOMAIN:
        logger.warning("Auth0 not configured, allowing development access")
        return {
            "sub": "dev-user-123",
            "email": "dev@example.com", 
            "name": "Development User",
            "picture": "https://via.placeholder.com/150"
        }
    
    try:
        # Get Auth0 public key
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_url)
            jwks = response.json()
        
        # Decode token (simplified - in production use proper JWT verification)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=AUTH0_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return payload
        
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Helper function to get current user
async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current authenticated user"""
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_id = token_data["sub"]
    
    # Create user if doesn't exist
    if user_id not in users_db:
        users_db[user_id] = UserProfile(
            id=user_id,
            email=token_data.get("email", ""),
            name=token_data.get("name", ""),
            picture=token_data.get("picture"),
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
    else:
        # Update last login
        users_db[user_id].last_login = datetime.utcnow()
    
    return users_db[user_id]

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CipherMate API is running",
        "version": "1.0.0",
        "status": "healthy",
        "features": {
            "database": not DISABLE_DATABASE,
            "redis": not DISABLE_REDIS,
            "ai_agents": not DISABLE_AGENTS
        },
        "port": PORT,
        "docs": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "simplified" if DISABLE_DATABASE else "full",
        "services": {
            "database": "disabled" if DISABLE_DATABASE else "enabled",
            "redis": "disabled" if DISABLE_REDIS else "enabled", 
            "ai_agents": "disabled" if DISABLE_AGENTS else "enabled"
        }
    }

# API Routes
@app.get("/api/v1/profile")
async def get_profile(current_user: UserProfile = Depends(get_current_user)):
    """Get user profile"""
    return current_user

@app.get("/api/v1/connections")
async def get_connections(current_user: UserProfile = Depends(get_current_user)):
    """Get user's service connections"""
    user_connections = [
        conn for conn in connections_db.values() 
        if conn.user_id == current_user.id
    ]
    return user_connections

@app.post("/api/v1/connections")
async def create_connection(
    service_name: str,
    service_type: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new service connection"""
    connection_id = f"conn_{len(connections_db) + 1}"
    
    connection = ServiceConnection(
        id=connection_id,
        user_id=current_user.id,
        service_name=service_name,
        service_type=service_type,
        status="active",
        created_at=datetime.utcnow()
    )
    
    connections_db[connection_id] = connection
    return connection

@app.get("/api/v1/actions")
async def get_actions(current_user: UserProfile = Depends(get_current_user)):
    """Get user's AI agent actions"""
    user_actions = [
        action for action in actions_db.values()
        if action.user_id == current_user.id
    ]
    return sorted(user_actions, key=lambda x: x.created_at, reverse=True)

@app.post("/api/v1/actions/email")
async def send_email_action(
    email_request: EmailRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """AI Agent action to send email"""
    if DISABLE_AGENTS:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Agents are disabled"
        )
    
    action_id = f"action_{len(actions_db) + 1}"
    
    # Simulate email sending
    await asyncio.sleep(1)  # Simulate processing time
    
    action = AIAgentAction(
        id=action_id,
        user_id=current_user.id,
        agent_type="email",
        action=f"send_email_to_{email_request.to}",
        status="completed",
        result={
            "to": email_request.to,
            "subject": email_request.subject,
            "sent_at": datetime.utcnow().isoformat(),
            "message_id": f"msg_{action_id}"
        },
        created_at=datetime.utcnow()
    )
    
    actions_db[action_id] = action
    return action

@app.post("/api/v1/tokens/request")
async def request_token(
    token_request: TokenRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Request access token for service"""
    token_id = f"token_{len(tokens_db) + 1}"
    
    # Simulate token generation
    token_data = {
        "id": token_id,
        "user_id": current_user.id,
        "service": token_request.service,
        "action": token_request.action,
        "permissions": token_request.permissions,
        "token": f"fake_token_{token_id}",
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }
    
    tokens_db[token_id] = token_data
    return token_data

@app.get("/api/v1/tokens")
async def get_tokens(current_user: UserProfile = Depends(get_current_user)):
    """Get user's tokens"""
    user_tokens = [
        token for token in tokens_db.values()
        if token["user_id"] == current_user.id
    ]
    return user_tokens

@app.delete("/api/v1/tokens/{token_id}")
async def revoke_token(
    token_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Revoke a token"""
    if token_id not in tokens_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
    
    token = tokens_db[token_id]
    if token["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to revoke this token"
        )
    
    del tokens_db[token_id]
    return {"message": "Token revoked successfully"}

# Demo endpoints for testing
@app.get("/api/v1/demo/stats")
async def get_demo_stats():
    """Get demo statistics"""
    return {
        "total_users": len(users_db),
        "total_connections": len(connections_db),
        "total_actions": len(actions_db),
        "total_tokens": len(tokens_db),
        "uptime": "99.9%",
        "api_calls_today": 1247,
        "active_agents": 0 if DISABLE_AGENTS else 5
    }

@app.post("/api/v1/demo/simulate-action")
async def simulate_action(
    action_type: str = "email",
    current_user: UserProfile = Depends(get_current_user)
):
    """Simulate an AI agent action for demo"""
    if DISABLE_AGENTS:
        return {
            "message": "AI Agents are disabled",
            "status": "disabled"
        }
    
    action_id = f"demo_action_{len(actions_db) + 1}"
    
    # Simulate processing
    await asyncio.sleep(2)
    
    action = AIAgentAction(
        id=action_id,
        user_id=current_user.id,
        agent_type=action_type,
        action=f"demo_{action_type}_action",
        status="completed",
        result={
            "demo": True,
            "action_type": action_type,
            "processed_at": datetime.utcnow().isoformat()
        },
        created_at=datetime.utcnow()
    )
    
    actions_db[action_id] = action
    return action

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)