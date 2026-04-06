"""Unit tests for AI Agent Engine"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from app.core.ai_agent import AIAgentEngine, IntentType, AIProvider
from app.core.exceptions import AIProcessingError, AuthorizationError


class TestAIAgentEngine:
    """Test cases for AI Agent Engine"""

    @pytest.fixture
    def ai_agent(self):
        """Create AI agent instance for testing"""
        return AIAgentEngine()

    @pytest.mark.asyncio
    async def test_analyze_intent_calendar_event(self, ai_agent, mock_gemini_response):
        """Test intent analysis for calendar event creation"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='{"intent": "calendar_create_event", "confidence": 0.95, "parameters": {"title": "Meeting", "start_time": "2024-01-01T10:00:00Z"}}'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.analyze_intent("Create a meeting tomorrow at 10am")
            
            assert result["intent"] == "calendar_create_event"
            assert result["confidence"] == 0.95
            assert "title" in result["parameters"]

    @pytest.mark.asyncio
    async def test_analyze_intent_email_send(self, ai_agent):
        """Test intent analysis for email sending"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='{"intent": "email_send", "confidence": 0.90, "parameters": {"to": "test@example.com", "subject": "Test", "body": "Hello"}}'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.analyze_intent("Send an email to test@example.com")
            
            assert result["intent"] == "email_send"
            assert result["parameters"]["to"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_analyze_intent_github_issue(self, ai_agent):
        """Test intent analysis for GitHub issue creation"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='{"intent": "github_create_issue", "confidence": 0.88, "parameters": {"title": "Bug report", "body": "Found a bug"}}'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.analyze_intent("Create a GitHub issue for the bug I found")
            
            assert result["intent"] == "github_create_issue"
            assert "title" in result["parameters"]

    @pytest.mark.asyncio
    async def test_analyze_intent_slack_message(self, ai_agent):
        """Test intent analysis for Slack messaging"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='{"intent": "slack_send_message", "confidence": 0.92, "parameters": {"channel": "#general", "message": "Hello team"}}'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.analyze_intent("Send a message to the general channel")
            
            assert result["intent"] == "slack_send_message"
            assert result["parameters"]["channel"] == "#general"

    @pytest.mark.asyncio
    async def test_analyze_intent_invalid_json(self, ai_agent):
        """Test handling of invalid JSON response from AI"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='invalid json response'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.analyze_intent("Some unclear request")
            
            assert result["intent"] == "unknown"
            assert result["confidence"] == 0.0

    @pytest.mark.asyncio
    async def test_analyze_intent_api_error(self, ai_agent):
        """Test handling of API errors"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_model.side_effect = Exception("API Error")
            
            with pytest.raises(AIProcessingError):
                await ai_agent.analyze_intent("Test message")

    def test_get_permission_requirements_calendar(self, ai_agent):
        """Test permission requirements for calendar operations"""
        requirements = ai_agent.get_permission_requirements("calendar_create_event")
        
        assert "google" in requirements
        assert "calendar.events" in requirements["google"]

    def test_get_permission_requirements_email(self, ai_agent):
        """Test permission requirements for email operations"""
        requirements = ai_agent.get_permission_requirements("email_send")
        
        assert "google" in requirements
        assert "gmail.send" in requirements["google"]

    def test_get_permission_requirements_github(self, ai_agent):
        """Test permission requirements for GitHub operations"""
        requirements = ai_agent.get_permission_requirements("github_create_issue")
        
        assert "github" in requirements
        assert "repo" in requirements["github"]

    def test_get_permission_requirements_slack(self, ai_agent):
        """Test permission requirements for Slack operations"""
        requirements = ai_agent.get_permission_requirements("slack_send_message")
        
        assert "slack" in requirements
        assert "chat:write" in requirements["slack"]

    def test_get_permission_requirements_unknown(self, ai_agent):
        """Test permission requirements for unknown intent"""
        requirements = ai_agent.get_permission_requirements("unknown_intent")
        
        assert requirements == {}

    @pytest.mark.asyncio
    async def test_check_user_permissions_sufficient(self, ai_agent):
        """Test permission checking with sufficient permissions"""
        user_permissions = {
            "google": ["calendar.events", "calendar.readonly"],
            "github": ["repo", "user"]
        }
        required_permissions = {
            "google": ["calendar.events"],
            "github": ["repo"]
        }
        
        result = await ai_agent.check_user_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is True
        assert result["missing_permissions"] == {}

    @pytest.mark.asyncio
    async def test_check_user_permissions_insufficient(self, ai_agent):
        """Test permission checking with insufficient permissions"""
        user_permissions = {
            "google": ["calendar.readonly"]
        }
        required_permissions = {
            "google": ["calendar.events"],
            "github": ["repo"]
        }
        
        result = await ai_agent.check_user_permissions(user_permissions, required_permissions)
        
        assert result["has_permissions"] is False
        assert "google" in result["missing_permissions"]
        assert "github" in result["missing_permissions"]

    @pytest.mark.asyncio
    async def test_generate_response_success(self, ai_agent):
        """Test response generation for successful action"""
        action_result = {
            "success": True,
            "data": {"event_id": "123", "title": "Meeting"},
            "message": "Event created successfully"
        }
        
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text="I've successfully created your meeting for tomorrow at 10am."
            )
            mock_model.return_value = mock_instance
            
            response = await ai_agent.generate_response(action_result, "calendar_create_event")
            
            assert "successfully" in response.lower()

    @pytest.mark.asyncio
    async def test_generate_response_failure(self, ai_agent):
        """Test response generation for failed action"""
        action_result = {
            "success": False,
            "error": "Permission denied",
            "message": "Failed to create event"
        }
        
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text="I'm sorry, I couldn't create the event due to permission issues."
            )
            mock_model.return_value = mock_instance
            
            response = await ai_agent.generate_response(action_result, "calendar_create_event")
            
            assert "sorry" in response.lower() or "couldn't" in response.lower()

    @pytest.mark.asyncio
    async def test_process_user_message_complete_flow(self, ai_agent):
        """Test complete message processing flow"""
        user_permissions = {
            "google": ["calendar.events"]
        }
        
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            # Mock intent analysis
            mock_instance.generate_content.side_effect = [
                Mock(text='{"intent": "calendar_create_event", "confidence": 0.95, "parameters": {"title": "Meeting"}}'),
                Mock(text="I've created your meeting successfully!")
            ]
            mock_model.return_value = mock_instance
            
            with patch.object(ai_agent, 'execute_action') as mock_execute:
                mock_execute.return_value = {
                    "success": True,
                    "data": {"event_id": "123"},
                    "message": "Event created"
                }
                
                result = await ai_agent.process_user_message(
                    "Create a meeting tomorrow",
                    "user123",
                    user_permissions
                )
                
                assert result["success"] is True
                assert "response" in result

    @pytest.mark.asyncio
    async def test_process_user_message_missing_permissions(self, ai_agent):
        """Test message processing with missing permissions"""
        user_permissions = {}
        
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_instance = Mock()
            mock_instance.generate_content.return_value = Mock(
                text='{"intent": "calendar_create_event", "confidence": 0.95, "parameters": {"title": "Meeting"}}'
            )
            mock_model.return_value = mock_instance
            
            result = await ai_agent.process_user_message(
                "Create a meeting tomorrow",
                "user123",
                user_permissions
            )
            
            assert result["success"] is False
            assert result["error_type"] == "permission_required"
            assert "missing_permissions" in result

    def test_switch_provider_success(self, ai_agent):
        """Test switching AI provider"""
        ai_agent.switch_provider(AIProvider.GEMINI)
        assert ai_agent.current_provider == AIProvider.GEMINI

    def test_switch_provider_invalid(self, ai_agent):
        """Test switching to invalid provider"""
        with pytest.raises(ValueError):
            ai_agent.switch_provider("invalid_provider")

    def test_get_available_providers(self, ai_agent):
        """Test getting available providers"""
        providers = ai_agent.get_available_providers()
        assert AIProvider.GEMINI in providers

    @pytest.mark.asyncio
    async def test_execute_action_not_implemented(self, ai_agent):
        """Test execute_action method (should be implemented by subclass)"""
        with pytest.raises(NotImplementedError):
            await ai_agent.execute_action("test_intent", {}, "user123")