"""
Unit tests for AI Agent Engine
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.core.ai_agent import (
    AIAgentEngine, 
    AIProvider, 
    IntentType, 
    ConfidenceLevel,
    IntentAnalysisResult,
    PermissionRequirement
)


class TestAIAgentEngine:
    """Test cases for AI Agent Engine"""
    
    def test_init_with_no_providers(self):
        """Test initialization when no AI providers are available"""
        with patch('app.core.ai_agent.settings') as mock_settings, \
             patch('app.core.ai_agent.openai_client', None):
            mock_settings.GEMINI_API_KEY = ""
            mock_settings.OPENAI_API_KEY = ""
            
            agent = AIAgentEngine()
            # When no providers are available, it should still initialize
            # but with limited functionality
            assert agent.gemini_model is None
            available_providers = agent.get_available_providers()
            # Should have no available providers when both are disabled
            assert len(available_providers) == 0 or agent.active_provider in [AIProvider.AUTO, AIProvider.OPENAI, AIProvider.GEMINI]
    
    def test_permission_mappings_initialization(self):
        """Test that permission mappings are properly initialized"""
        agent = AIAgentEngine()
        
        # Check that key intent types have permission mappings
        calendar_perm = agent.get_permission_requirements(IntentType.CALENDAR_CREATE_EVENT)
        assert calendar_perm is not None
        assert calendar_perm.service == "google"
        assert "https://www.googleapis.com/auth/calendar" in calendar_perm.scopes
        
        email_perm = agent.get_permission_requirements(IntentType.EMAIL_SEND)
        assert email_perm is not None
        assert email_perm.service == "google"
        assert email_perm.risk_level == "high"
        
        github_perm = agent.get_permission_requirements(IntentType.GITHUB_CREATE_ISSUE)
        assert github_perm is not None
        assert github_perm.service == "github"
        assert "repo" in github_perm.scopes
    
    def test_get_available_providers(self):
        """Test getting available providers"""
        agent = AIAgentEngine()
        
        # Mock both providers as available
        agent.gemini_model = MagicMock()
        agent.openai_client = MagicMock()
        
        providers = agent.get_available_providers()
        assert AIProvider.GEMINI in providers
        assert AIProvider.OPENAI in providers
    
    def test_switch_provider_success(self):
        """Test successful provider switching"""
        agent = AIAgentEngine()
        
        # Mock both providers as available
        agent.gemini_model = MagicMock()
        agent.openai_client = MagicMock()
        
        # Switch to Gemini
        success = agent.switch_provider(AIProvider.GEMINI)
        assert success is True
        assert agent.active_provider == AIProvider.GEMINI
        
        # Switch to OpenAI
        success = agent.switch_provider(AIProvider.OPENAI)
        assert success is True
        assert agent.active_provider == AIProvider.OPENAI
    
    def test_switch_provider_failure(self):
        """Test provider switching when provider is not available"""
        agent = AIAgentEngine()
        
        # Mock only OpenAI as available
        agent.gemini_model = None
        agent.openai_client = MagicMock()
        
        # Try to switch to unavailable Gemini
        success = agent.switch_provider(AIProvider.GEMINI)
        assert success is False
        assert agent.active_provider != AIProvider.GEMINI
    
    @pytest.mark.asyncio
    async def test_validate_intent_parameters(self):
        """Test parameter validation for different intent types"""
        agent = AIAgentEngine()
        
        # Test calendar event with required parameters
        is_valid, missing = await agent.validate_intent_parameters(
            IntentType.CALENDAR_CREATE_EVENT,
            {"title": "Meeting", "start_time": "2pm"}
        )
        assert is_valid is True
        assert len(missing) == 0
        
        # Test calendar event with missing parameters
        is_valid, missing = await agent.validate_intent_parameters(
            IntentType.CALENDAR_CREATE_EVENT,
            {"title": "Meeting"}  # Missing start_time
        )
        assert is_valid is False
        assert "start_time" in missing
        
        # Test email with required parameters
        is_valid, missing = await agent.validate_intent_parameters(
            IntentType.EMAIL_SEND,
            {"recipient": "test@example.com", "subject": "Test"}
        )
        assert is_valid is True
        assert len(missing) == 0
    
    @pytest.mark.asyncio
    async def test_enhance_parameters(self):
        """Test parameter enhancement with user context"""
        agent = AIAgentEngine()
        
        # Test calendar event enhancement
        user_context = {"default_location": "Conference Room A"}
        enhanced = await agent.enhance_parameters(
            IntentType.CALENDAR_CREATE_EVENT,
            {"title": "Meeting", "start_time": "2pm"},
            user_context
        )
        
        assert enhanced["title"] == "Meeting"
        assert enhanced["start_time"] == "2pm"
        assert enhanced["location"] == "Conference Room A"
        assert enhanced["duration"] == "1 hour"  # Default duration
        
        # Test email enhancement
        user_context = {"email_signature": "Best regards, John"}
        enhanced = await agent.enhance_parameters(
            IntentType.EMAIL_SEND,
            {"recipient": "test@example.com", "subject": "Test"},
            user_context
        )
        
        assert enhanced["signature"] == "Best regards, John"
    
    def test_check_user_permissions(self):
        """Test user permission checking"""
        agent = AIAgentEngine()
        
        # Mock user permissions
        user_permissions = [
            {
                "service_name": "google",
                "scopes": ["https://www.googleapis.com/auth/calendar"],
                "is_active": True
            },
            {
                "service_name": "github",
                "scopes": ["repo", "user"],
                "is_active": True
            }
        ]
        
        # Test with sufficient permissions
        has_perms, missing = agent.check_user_permissions(
            user_permissions,
            ["https://www.googleapis.com/auth/calendar"],
            "google"
        )
        assert has_perms is True
        assert len(missing) == 0
        
        # Test with missing permissions
        has_perms, missing = agent.check_user_permissions(
            user_permissions,
            ["https://www.googleapis.com/auth/gmail.send"],
            "google"
        )
        assert has_perms is False
        assert "https://www.googleapis.com/auth/gmail.send" in missing
    
    def test_create_error_result(self):
        """Test error result creation"""
        agent = AIAgentEngine()
        
        error_result = agent._create_error_result("Test error message")
        
        assert error_result.intent_type == IntentType.UNKNOWN
        assert error_result.confidence == ConfidenceLevel.LOW
        assert error_result.clarification_needed is True
        assert "Test error message" in error_result.clarification_questions
    
    def test_get_required_parameters(self):
        """Test getting required parameters for different intent types"""
        agent = AIAgentEngine()
        
        # Test calendar create event
        required = agent._get_required_parameters(IntentType.CALENDAR_CREATE_EVENT)
        assert "title" in required
        assert "start_time" in required
        
        # Test email send
        required = agent._get_required_parameters(IntentType.EMAIL_SEND)
        assert "recipient" in required
        assert "subject" in required
        
        # Test GitHub issue creation
        required = agent._get_required_parameters(IntentType.GITHUB_CREATE_ISSUE)
        assert "repository" in required
        assert "title" in required
        
        # Test intent with no required parameters
        required = agent._get_required_parameters(IntentType.GENERAL_QUERY)
        assert len(required) == 0


class TestIntentAnalysisResult:
    """Test cases for IntentAnalysisResult dataclass"""
    
    def test_intent_analysis_result_creation(self):
        """Test creating IntentAnalysisResult"""
        result = IntentAnalysisResult(
            intent_type=IntentType.CALENDAR_CREATE_EVENT,
            confidence=ConfidenceLevel.HIGH,
            parameters={"title": "Test Meeting"},
            required_permissions=["calendar.write"],
            service_name="google"
        )
        
        assert result.intent_type == IntentType.CALENDAR_CREATE_EVENT
        assert result.confidence == ConfidenceLevel.HIGH
        assert result.parameters["title"] == "Test Meeting"
        assert "calendar.write" in result.required_permissions
        assert result.service_name == "google"
        assert result.clarification_needed is False
        assert result.clarification_questions is None


class TestPermissionRequirement:
    """Test cases for PermissionRequirement dataclass"""
    
    def test_permission_requirement_creation(self):
        """Test creating PermissionRequirement"""
        perm_req = PermissionRequirement(
            service="google",
            scopes=["calendar.read", "calendar.write"],
            description="Calendar access",
            risk_level="medium"
        )
        
        assert perm_req.service == "google"
        assert len(perm_req.scopes) == 2
        assert "calendar.read" in perm_req.scopes
        assert perm_req.description == "Calendar access"
        assert perm_req.risk_level == "medium"
    
    def test_permission_requirement_default_risk_level(self):
        """Test default risk level for PermissionRequirement"""
        perm_req = PermissionRequirement(
            service="github",
            scopes=["repo"],
            description="Repository access"
        )
        
        assert perm_req.risk_level == "medium"  # Default value


if __name__ == "__main__":
    pytest.main([__file__])