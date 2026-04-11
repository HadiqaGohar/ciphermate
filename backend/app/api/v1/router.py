from fastapi import APIRouter
from app.api.v1 import auth, token_vault, agent, ai_agent, permissions, integrations, audit, security, health, gmail
from app.api.routes.execute_action import router as execute_action_router

# Create main API router
api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router)

# Include token vault routes
api_router.include_router(token_vault.router)

# Include AI agent routes
api_router.include_router(agent.router)

# Include AI agent engine routes
api_router.include_router(ai_agent.router)

# Include Gmail routes
api_router.include_router(gmail.router)

# Include execute action routes
api_router.include_router(execute_action_router)

# Include permission management routes
api_router.include_router(permissions.router)

# Include third-party API integration routes
api_router.include_router(integrations.router)

# Include audit logging routes
api_router.include_router(audit.router)

# Include security monitoring routes
api_router.include_router(security.router)

# Include comprehensive health monitoring routes
api_router.include_router(health.router)

@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {"message": "CipherMate API v1"}


@api_router.get("/status")
async def api_status():
    """API status endpoint"""
    return {"status": "operational", "version": "1.0.0"}


        # // done hadiqa
