

# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from contextlib import asynccontextmanager
# import uvicorn
# import asyncio
# from app.core.config import settings
# from app.core.database import engine, Base
# from app.core.session import session_manager
# from app.api.v1.router import api_router

# # Import models to ensure they are registered with SQLAlchemy
# from app.models import (
#     User,
#     ServiceConnection,
#     AuditLog,
#     AgentAction,
#     PermissionTemplate,
#     SecurityEvent,
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
    
#     yield
    
#     # Shutdown
#     print("Shutting down CipherMate Backend...")
#     cleanup_task.cancel()
#     await session_manager.close()


# # Create FastAPI application
# app = FastAPI(
#     title="CipherMate API",
#     description="Secure AI Assistant Platform with Auth0 Token Vault",
#     version="0.1.0",
#     docs_url="/docs" if settings.APP_ENV == "development" else None,
#     redoc_url="/redoc" if settings.APP_ENV == "development" else None,
#     lifespan=lifespan,
# )

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
#     allow_headers=["*"],
# )

# # Include API router
# app.include_router(api_router, prefix="/api/v1")


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
#         "main:app",
#         host="0.0.0.0",
#         port=8080,
#         reload=settings.APP_ENV == "development",
#     )
