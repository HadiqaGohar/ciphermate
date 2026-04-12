import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncio
from sqlalchemy.exc import SQLAlchemyError

from .core.config import settings

# Conditional imports based on database availability
database_enabled = not os.getenv("DISABLE_DATABASE", "false").lower() == "true"

if database_enabled:
    try:
        from .core.database import engine, Base
        from .core.session import session_manager
        from .core.cache import cache_service
        from .core.security_monitor import security_monitor
        from .core.monitoring import cache_metrics_task, health_checker
        from .core.monitoring_middleware import add_monitoring_middleware
        database_imports_success = True
    except ImportError as e:
        print(f"Database imports failed: {e}")
        database_imports_success = False
        engine = None
        Base = None
        session_manager = None
        cache_service = None
        security_monitor = None
        cache_metrics_task = None
        health_checker = None
        add_monitoring_middleware = lambda x: None
else:
    # Mock objects for no-database mode
    engine = None
    Base = None
    session_manager = None
    cache_service = None
    security_monitor = None
    cache_metrics_task = None
    health_checker = None
    add_monitoring_middleware = lambda x: None
    database_imports_success = False

from .api.v1.router import api_router
from .core.exceptions import CipherMateException
from .core.error_handlers import (
    ciphermate_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)
from .core.middleware import add_middleware

# Import models to ensure they are registered with SQLAlchemy
from .models import (
    User,
    ServiceConnection,
    AuditLog,
    AgentAction,
    PermissionTemplate,
    SecurityEvent,
    ToDoTask,
)


async def cleanup_sessions_task():
    """Background task to cleanup expired sessions"""
    while True:
        try:
            await session_manager.cleanup_expired_sessions()
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            print(f"Session cleanup error: {e}")
            await asyncio.sleep(300)  # Retry in 5 minutes on error


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting CipherMate Backend...")
    
    # Initialize based on database availability and import success
    if database_enabled and database_imports_success:
        # Database mode
        print("Database mode enabled")
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            # Start background tasks
            cleanup_task = asyncio.create_task(cleanup_sessions_task())
            metrics_task = asyncio.create_task(cache_metrics_task())
            
            # Start security monitoring
            security_monitor.start_monitoring()
            
            # Register health checks
            async def database_health_check():
                try:
                    async with engine.begin() as conn:
                        await conn.execute("SELECT 1")
                    return {"status": "healthy", "connected": True}
                except Exception as e:
                    return {"status": "unhealthy", "error": str(e), "connected": False}
            
            health_checker.register_check("database", database_health_check)
            
            print("CipherMate Backend started successfully with database")
        except Exception as e:
            print(f"Database initialization failed: {e}")
            cleanup_task = None
            metrics_task = None
            print("Falling back to no-database mode")
    else:
        # No database mode
        print("No database mode - using mock services")
        cleanup_task = None
        metrics_task = None
        print("CipherMate Backend started successfully (no database)")
    
    yield
    
    # Shutdown
    print("Shutting down CipherMate Backend...")
    if database_enabled and database_imports_success:
        try:
            if cleanup_task:
                cleanup_task.cancel()
            if metrics_task:
                metrics_task.cancel()
            if session_manager:
                await session_manager.close()
            if cache_service:
                await cache_service.close()
            if security_monitor:
                await security_monitor.shutdown()
        except Exception as e:
            print(f"Shutdown error: {e}")
    print("CipherMate Backend shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="CipherMate API",
    description="Secure AI Assistant Platform with Auth0 Token Vault",
    version="0.1.0",
    docs_url="/docs" if settings.APP_ENV == "development" else None,
    redoc_url="/redoc" if settings.APP_ENV == "development" else None,
    lifespan=lifespan,
)

# Configure CORS with enhanced security
cors_origins = settings.allowed_origins_list.copy()

# In production, be more restrictive
if settings.APP_ENV == "production":
    # Remove localhost origins in production
    cors_origins = [origin for origin in cors_origins if "localhost" not in origin and "127.0.0.1" not in origin]

# Add session middleware for OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=settings.APP_ENV == "production"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for testing
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Session-ID"
    ],
    expose_headers=["X-Process-Time", "X-Rate-Limit-Remaining"],
    max_age=86400,  # 24 hours
)

# Add custom middleware
add_middleware(app)

# Add monitoring middleware
add_monitoring_middleware(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Include Gmail auth routes (outside of v1 prefix)
from app.api.routes.gmail_auth import router as gmail_auth_router
app.include_router(gmail_auth_router)

# Include Google Calendar auth routes (outside of v1 prefix)
from app.api.routes.google_calendar_auth import router as google_calendar_auth_router
app.include_router(google_calendar_auth_router)

# Include GitHub OAuth callback handler (outside of v1 prefix)
from app.api.routes.github_auth import router as github_auth_router
app.include_router(github_auth_router)

# Add exception handlers
app.add_exception_handler(CipherMateException, ciphermate_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CipherMate API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.APP_ENV == "development",
    )





# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from fastapi.exceptions import RequestValidationError
# from starlette.middleware.sessions import SessionMiddleware
# from contextlib import asynccontextmanager
# import uvicorn
# import asyncio
# from sqlalchemy.exc import SQLAlchemyError

# from .core.config import settings
# from .core.database import engine, Base
# from .core.session import session_manager
# from .api.v1.router import api_router
# from .core.exceptions import CipherMateException
# from .core.error_handlers import (
#     ciphermate_exception_handler,
#     http_exception_handler,
#     validation_exception_handler,
#     sqlalchemy_exception_handler,
#     generic_exception_handler
# )
# from .core.middleware import add_middleware
# from .core.monitoring_middleware import add_monitoring_middleware
# from .core.monitoring import cache_metrics_task, health_checker
# from .core.cache import cache_service
# from .core.security_monitor import security_monitor

# # Import models to ensure they are registered with SQLAlchemy
# from .models import (
#     User,
#     ServiceConnection,
#     AuditLog,
#     AgentAction,
#     PermissionTemplate,
#     SecurityEvent,
#     ToDoTask,
# )


# async def cleanup_sessions_task():
#     """Background task to cleanup expired sessions"""
#     while True:
#         try:
#             await session_manager.cleanup_expired_sessions()
#             await asyncio.sleep(3600)  # Run every hour
#         except Exception as e:
#             print(f"Session cleanup error: {e}")
#             await asyncio.sleep(300)  # Retry in 5 minutes on error


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Application lifespan events"""
#     # Startup
#     print("Starting CipherMate Backend...")
    
#     # Create database tables
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
    
#     # Start background tasks
#     cleanup_task = asyncio.create_task(cleanup_sessions_task())
#     metrics_task = asyncio.create_task(cache_metrics_task())
    
#     # Start security monitoring
#     security_monitor.start_monitoring()
    
#     # Register health checks
#     async def database_health_check():
#         try:
#             async with engine.begin() as conn:
#                 await conn.execute("SELECT 1")
#             return {"status": "healthy", "connected": True}
#         except Exception as e:
#             return {"status": "unhealthy", "error": str(e), "connected": False}
    
#     health_checker.register_check("database", database_health_check)
    
#     print("CipherMate Backend started successfully with monitoring")
    
#     yield
    
#     # Shutdown
#     print("Shutting down CipherMate Backend...")
#     cleanup_task.cancel()
#     metrics_task.cancel()
#     await session_manager.close()
#     await cache_service.close()
#     await security_monitor.shutdown()
#     print("CipherMate Backend shutdown complete")


# # Create FastAPI application
# app = FastAPI(
#     title="CipherMate API",
#     description="Secure AI Assistant Platform with Auth0 Token Vault",
#     version="0.1.0",
#     docs_url="/docs" if settings.APP_ENV == "development" else None,
#     redoc_url="/redoc" if settings.APP_ENV == "development" else None,
#     lifespan=lifespan,
# )

# # Configure CORS with enhanced security
# cors_origins = settings.allowed_origins_list.copy()

# # In production, be more restrictive
# if settings.APP_ENV == "production":
#     # Remove localhost origins in production
#     cors_origins = [origin for origin in cors_origins if "localhost" not in origin and "127.0.0.1" not in origin]

# # Add session middleware for OAuth
# app.add_middleware(
#     SessionMiddleware,
#     secret_key=settings.SECRET_KEY,
#     max_age=3600,  # 1 hour
#     same_site="lax",
#     https_only=settings.APP_ENV == "production"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Temporarily allow all origins for testing
#     allow_credentials=False,  # Must be False when allow_origins=["*"]
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=[
#         "Accept",
#         "Accept-Language", 
#         "Content-Language",
#         "Content-Type",
#         "Authorization",
#         "X-Requested-With",
#         "X-Session-ID"
#     ],
#     expose_headers=["X-Process-Time", "X-Rate-Limit-Remaining"],
#     max_age=86400,  # 24 hours
# )

# # Add custom middleware
# add_middleware(app)

# # Add monitoring middleware
# add_monitoring_middleware(app)

# # Include API router
# app.include_router(api_router, prefix="/api/v1")

# # Include Gmail auth routes (outside of v1 prefix)
# from app.api.routes.gmail_auth import router as gmail_auth_router
# app.include_router(gmail_auth_router)

# # Include Google Calendar auth routes (outside of v1 prefix)
# from app.api.routes.google_calendar_auth import router as google_calendar_auth_router
# app.include_router(google_calendar_auth_router)

# # Include GitHub OAuth callback handler (outside of v1 prefix)
# from app.api.routes.github_auth import router as github_auth_router
# app.include_router(github_auth_router)

# # Add exception handlers
# app.add_exception_handler(CipherMateException, ciphermate_exception_handler)
# app.add_exception_handler(HTTPException, http_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
# app.add_exception_handler(Exception, generic_exception_handler)


# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "message": "CipherMate API",
#         "version": "0.1.0",
#         "status": "running"
#     }


# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy"}


# if __name__ == "__main__":
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8080,
#         reload=settings.APP_ENV == "development",
#     )    