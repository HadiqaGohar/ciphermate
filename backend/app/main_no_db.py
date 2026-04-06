"""
CipherMate Backend - No Database Mode
For development and testing without PostgreSQL/Redis dependencies
"""

import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Set environment flags
os.environ["DISABLE_DATABASE"] = "true"
os.environ["DISABLE_REDIS"] = "true"

from app.core.config import settings


class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to handle request timeouts"""
    
    def __init__(self, app, timeout: float = 60.0):
        super().__init__(app)
        self.timeout = timeout
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504,
                content={
                    "message": "Request timeout - the operation took too long to complete",
                    "timeout": self.timeout
                }
            )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Mock authentication function for no-database mode
async def mock_get_current_user():
    """Mock user for no-database mode"""
    from app.models.user import User
    return User(
        id=123,
        auth0_id="test_user_123",
        email="test@example.com",
        name="Test User"
    )

# Monkey patch the auth dependency for no-database mode
import app.core.auth
app.core.auth.get_current_user = mock_get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - no database mode"""
    logger.info("Starting CipherMate Backend (No Database Mode)...")
    
    # Initialize AI Agent (this should work without database)
    try:
        from app.core.ai_agent import ai_agent_engine
        logger.info(f"✅ AI Agent initialized with clean Gemini provider")
    except Exception as e:
        logger.error(f"❌ AI Agent initialization failed: {e}")
    
    logger.info("✅ CipherMate Backend started successfully (No Database Mode)")
    
    yield
    
    logger.info("Shutting down CipherMate Backend...")


# Create FastAPI app
app = FastAPI(
    title="CipherMate API",
    description="Secure AI Assistant Platform with Auth0 Token Vault (No Database Mode)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add timeout middleware (must be first)
app.add_middleware(TimeoutMiddleware, timeout=60.0)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0", "*"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CipherMate API - No Database Mode",
        "version": "1.0.0",
        "status": "running",
        "mode": "no_database",
        "features": {
            "ai_agent": True,
            "database": False,
            "redis": False,
            "token_vault": "mock"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from app.core.ai_agent import ai_agent_engine
        ai_status = {
            "available": ai_agent_engine.available,
            "provider": "clean_gemini",
            "gemini_available": ai_agent_engine.available
        }
    except Exception as e:
        ai_status = {
            "available": False,
            "error": str(e)
        }
    
    return {
        "status": "healthy",
        "mode": "no_database",
        "ai_agent": ai_status,
        "database": {"status": "disabled"},
        "redis": {"status": "disabled"}
    }


# Mock authentication for testing
@app.middleware("http")
async def mock_auth_middleware(request: Request, call_next):
    """Mock authentication middleware for testing"""
    # Add a mock user to the request for testing
    request.state.user = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "permissions": ["read:profile", "write:profile"]
    }
    
    # For API endpoints that need authentication, add a mock Authorization header
    if request.url.path.startswith("/api/v1/ai-agent"):
        # Create a mock token for the AI agent endpoints
        request.headers.__dict__["_list"].append((b"authorization", b"Bearer mock_token_123"))
    
    response = await call_next(request)
    return response


# Include AI Agent routes
try:
    from app.api.v1.ai_agent import router as ai_agent_router
    app.include_router(ai_agent_router, prefix="/api/v1")
    logger.info("✅ AI Agent routes included")
except Exception as e:
    logger.error(f"❌ Failed to include AI Agent routes: {e}")

# Mock Token Vault routes
@app.get("/api/v1/token-vault/status")
async def mock_token_vault_status():
    """Mock token vault status"""
    return {
        "status": "mock_mode",
        "message": "Token Vault is running in mock mode (no database)",
        "tokens_stored": 0
    }

@app.post("/api/v1/token-vault/store")
async def mock_store_token(request: Request):
    """Mock token storage"""
    return {
        "id": "mock_token_123",
        "status": "stored",
        "message": "Token stored in mock mode"
    }

# Mock Audit routes - Remove these and use real database
# @app.get("/api/v1/audit/logs")
# async def mock_audit_logs():
#     """Mock audit logs"""
#     return {
#         "logs": [
#             {
#                 "id": "mock_log_1",
#                 "timestamp": "2024-01-15T10:00:00Z",
#                 "user_id": "test_user_123",
#                 "action": "chat_message",
#                 "details": "User sent a chat message",
#                 "ip_address": "127.0.0.1"
#             },
#             {
#                 "id": "mock_log_2", 
#                 "timestamp": "2024-01-15T09:30:00Z",
#                 "user_id": "test_user_123",
#                 "action": "login",
#                 "details": "User logged in successfully",
#                 "ip_address": "127.0.0.1"
#             }
#         ],
#         "total": 2,
#         "page": 1,
#         "per_page": 10,
#         "mode": "mock"
#     }

# @app.get("/api/v1/audit/summary")
# async def mock_audit_summary():
#     """Mock audit summary"""
#     return {
#         "total_events": 2,
#         "recent_activity": 2,
#         "security_events": 0,
#         "mode": "mock"
#     }

# @app.get("/api/v1/audit/security-events")
# async def mock_security_events():
#     """Mock security events"""
#     return {
#         "events": [],
#         "total": 0,
#         "mode": "mock"
#     }

# @app.get("/api/v1/audit/export")
# async def mock_audit_export():
#     """Mock audit export"""
#     return {
#         "message": "Export functionality not available in mock mode",
#         "mode": "mock"
#     }

# Mock health routes
@app.get("/api/v1/health/detailed")
async def detailed_health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "mode": "no_database",
        "services": {
            "ai_agent": "healthy",
            "database": "disabled",
            "redis": "disabled",
            "token_vault": "mock"
        },
        "timestamp": "2024-01-15T10:00:00Z"
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "mode": "no_database"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)