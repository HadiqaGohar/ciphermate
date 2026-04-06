"""AI Agent API endpoints"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
import logging

from app.core.ai_agent import ai_agent_engine
from app.core.auth import get_current_user
from app.core.audit_service import audit_service, PerformanceTracker
from app.core.validation import RequestValidator, create_validation_exception
from app.core.exceptions import ValidationError, AIProcessingError
from app.core.error_handlers import handle_ai_error
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai-agent", tags=["ai-agent"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    @validator('message')
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('context')
    def validate_context(cls, v):
        if v is not None and len(str(v)) > 10000:
            raise ValueError('Context is too large')
        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    intent_type: str
    confidence: str
    service_name: Optional[str] = None
    parameters: Dict[str, Any]
    required_permissions: List[str]
    clarification_needed: bool
    clarification_questions: List[str]


class IntentAnalysisRequest(BaseModel):
    """Request model for intent analysis endpoint"""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    user_context: Optional[Dict[str, Any]] = Field(None, description="User context")
    
    @validator('message')
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class IntentAnalysisResponse(BaseModel):
    """Response model for intent analysis endpoint"""
    intent_type: str
    confidence: str
    service_name: Optional[str] = None
    parameters: Dict[str, Any]
    required_permissions: List[str]
    clarification_needed: bool
    clarification_questions: List[str]


class ProviderStatusResponse(BaseModel):
    """Response model for provider status endpoint"""
    active_provider: str
    available_providers: List[str]
    gemini_available: bool
    openai_available: bool
    agents_sdk_available: bool


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request_data: ChatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Process a chat message and return both intent analysis and natural language response
    """
    try:
        # Validate request data
        validation_result = RequestValidator.validate_chat_request(
            request_data.message, 
            request_data.context
        )
        
        if not validation_result.is_valid:
            raise create_validation_exception(validation_result)
        
        logger.info(f"Processing chat request from user {current_user.id}: {request_data.message[:100]}...")
        
        # Track performance
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="ai_chat",
            details={"message_length": len(request_data.message)}
        ):
            # Process message with clean AI agent
            result = await ai_agent_engine.process_message(
                validation_result.sanitized_value["message"]
            )
        
        # Log the chat interaction
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="ai_chat",
            service_name=result.get("service_name"),
            details={
                "message_preview": request_data.message[:100] + "..." if len(request_data.message) > 100 else request_data.message,
                "intent_type": result.get("intent_type"),
                "confidence": result.get("confidence"),
                "required_permissions": result.get("required_permissions", []),
                "clarification_needed": result.get("clarification_needed", False)
            },
            request=request
        )
        
        return ChatResponse(
            response=result.get("response", "I'm sorry, I couldn't process your request."),
            intent_type=result.get("intent_type", "unknown"),
            confidence=result.get("confidence", "low"),
            service_name=result.get("service_name"),
            parameters=result.get("parameters", {}),
            required_permissions=result.get("required_permissions", []),
            clarification_needed=result.get("clarification_needed", False),
            clarification_questions=result.get("clarification_questions", [])
        )
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="ai_chat_error",
            severity="error",
            details={"error": str(e), "message_preview": request_data.message[:50]},
            request=request
        )
        raise handle_ai_error("ai_agent", e)


@router.post("/analyze-intent", response_model=IntentAnalysisResponse)
async def analyze_intent(
    request_data: IntentAnalysisRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze the intent of a user message without generating a response
    """
    try:
        logger.info(f"Analyzing intent for user {current_user.id}: {request_data.message}")
        
        # Track performance
        async with PerformanceTracker(
            user_id=current_user.id,
            operation="intent_analysis",
            details={"message_length": len(request_data.message)}
        ):
            intent_result = await ai_agent_engine.analyze_intent(request_data.message)
        
        # Log the intent analysis
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="intent_analysis",
            service_name=intent_result.service_name,
            details={
                "message_preview": request_data.message[:100] + "..." if len(request_data.message) > 100 else request_data.message,
                "intent_type": intent_result.intent_type.value,
                "confidence": intent_result.confidence.value,
                "required_permissions": intent_result.required_permissions
            },
            request=request
        )
        
        return IntentAnalysisResponse(
            intent_type=intent_result.intent_type.value,
            confidence=intent_result.confidence.value,
            service_name=intent_result.service_name,
            parameters=intent_result.parameters,
            required_permissions=intent_result.required_permissions,
            clarification_needed=intent_result.clarification_needed,
            clarification_questions=intent_result.clarification_questions or []
        )
        
    except Exception as e:
        logger.error(f"Error analyzing intent: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="intent_analysis_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Failed to analyze intent")


@router.get("/status", response_model=ProviderStatusResponse)
async def get_provider_status(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Get the status of AI providers
    """
    try:
        # Check if AI agent is available
        agents_available = ai_agent_engine.available
        
        # Log provider status access
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="ai_provider_status_access",
            details={
                "active_provider": "openai_agents_sdk",
                "agents_available": agents_available
            },
            request=request
        )
        
        return ProviderStatusResponse(
            active_provider="openai_agents_sdk",
            available_providers=["openai_agents_sdk"] if ai_agent_engine.available else [],
            gemini_available=False,
            openai_available=ai_agent_engine.available,
            agents_sdk_available=ai_agent_engine.available
        )
        
    except Exception as e:
        logger.error(f"Error getting provider status: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="ai_provider_status_error",
            severity="error",
            details={"error": str(e)},
            request=request
        )
        raise HTTPException(status_code=500, detail="Failed to get provider status")


@router.post("/switch-provider")
async def switch_provider(
    provider: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Switch to a different AI provider
    """
    try:
        provider_enum = AIProvider(provider)
        success = ai_agent.switch_provider(provider_enum)
        
        # Log provider switch attempt
        await audit_service.log_action(
            user_id=current_user.id,
            action_type="ai_provider_switch",
            details={
                "requested_provider": provider,
                "success": success,
                "previous_provider": ai_agent.active_provider.value if not success else None
            },
            request=request
        )
        
        if success:
            return {"message": f"Successfully switched to {provider}", "active_provider": ai_agent.active_provider.value}
        else:
            await audit_service.log_security_event(
                user_id=current_user.id,
                event_type="ai_provider_switch_failed",
                severity="warning",
                details={"requested_provider": provider, "reason": "provider_not_available"},
                request=request
            )
            raise HTTPException(status_code=400, detail=f"Cannot switch to {provider} - provider not available")
            
    except ValueError:
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="ai_provider_switch_failed",
            severity="warning",
            details={"requested_provider": provider, "reason": "invalid_provider"},
            request=request
        )
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")
    except Exception as e:
        logger.error(f"Error switching provider: {e}")
        await audit_service.log_security_event(
            user_id=current_user.id,
            event_type="ai_provider_switch_error",
            severity="error",
            details={"error": str(e), "requested_provider": provider},
            request=request
        )
        raise HTTPException(status_code=500, detail="Failed to switch provider")


@router.get("/supported-intents")
async def get_supported_intents(current_user: User = Depends(get_current_user)):
    """
    Get list of supported intent types
    """
    try:
        intents = []
        for intent_type in IntentType:
            perm_req = ai_agent.get_permission_requirements(intent_type)
            intents.append({
                "intent_type": intent_type.value,
                "description": intent_type.name.replace("_", " ").title(),
                "service": perm_req.service if perm_req else None,
                "required_permissions": perm_req.scopes if perm_req else [],
                "risk_level": perm_req.risk_level if perm_req else "low"
            })

        return {"supported_intents": intents}

    except Exception as e:
        logger.error(f"Error getting supported intents: {e}")
        raise HTTPException(status_code=500, detail="Failed to get supported intents")


# ============================================================================
# PUBLIC TEST ENDPOINTS (For Hackathon Demo - No Authentication Required)
# ============================================================================

@router.post("/chat/public")
async def chat_public(request_data: ChatRequest, request: Request):
    """
    Public chat endpoint for testing - no authentication required
    This is for hackathon demo purposes
    """
    try:
        # Validate request data
        validation_result = RequestValidator.validate_chat_request(
            request_data.message,
            request_data.context
        )

        if not validation_result.is_valid:
            raise create_validation_exception(validation_result)

        logger.info(f"Processing public chat request: {request_data.message[:100]}...")

        # Track performance
        async with PerformanceTracker(
            user_id="public_user",
            operation="ai_chat_public",
            details={"message_length": len(request_data.message)}
        ):
            # Process message with clean AI agent
            result = await ai_agent_engine.process_message(
                validation_result.sanitized_value["message"]
            )

        return ChatResponse(
            response=result.get("response", "I'm sorry, I couldn't process your request."),
            intent_type=result.get("intent_type", "unknown"),
            confidence=result.get("confidence", "low"),
            service_name=result.get("service_name"),
            parameters=result.get("parameters", {}),
            required_permissions=result.get("required_permissions", []),
            clarification_needed=result.get("clarification_needed", False),
            clarification_questions=result.get("clarification_questions", [])
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error in public chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/health")
async def test_health():
    """
    Simple health check endpoint for testing
    """
    return {
        "status": "healthy",
        "ai_agent": "available" if ai_agent_engine.available else "unavailable",
        "agents_sdk_configured": ai_agent_engine.available,
        "openai_configured": ai_agent_engine.available
    }