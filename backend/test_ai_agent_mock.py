#!/usr/bin/env python3
"""
Mock test script for AI Agent Engine functionality without API calls
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.ai_agent import AIAgentEngine, AIProvider, IntentType, ConfidenceLevel


class MockAIAgentEngine(AIAgentEngine):
    """Mock AI Agent Engine for testing without API calls"""
    
    def __init__(self):
        # Initialize without calling parent __init__ to avoid API setup
        self.preferred_provider = AIProvider.AUTO
        self.gemini_model = MagicMock()  # Mock Gemini model
        self.openai_client = MagicMock()  # Mock OpenAI client
        self.active_provider = AIProvider.OPENAI
        self._init_permission_mappings()
    
    async def _analyze_intent_openai(self, user_message: str, user_context=None):
        """Mock OpenAI intent analysis"""
        # Simple rule-based mock responses
        message_lower = user_message.lower()
        
        if "schedule" in message_lower or "meeting" in message_lower:
            return self._create_mock_result(
                IntentType.CALENDAR_CREATE_EVENT,
                ConfidenceLevel.HIGH,
                {
                    "title": "Meeting with John",
                    "start_time": "tomorrow at 2pm",
                    "description": "project review"
                },
                "google"
            )
        elif "email" in message_lower and "send" in message_lower:
            return self._create_mock_result(
                IntentType.EMAIL_SEND,
                ConfidenceLevel.HIGH,
                {
                    "recipient": "sarah@example.com",
                    "subject": "Quarterly Report",
                    "body": "quarterly report"
                },
                "google"
            )
        elif "issue" in message_lower and ("create" in message_lower or "repository" in message_lower):
            return self._create_mock_result(
                IntentType.GITHUB_CREATE_ISSUE,
                ConfidenceLevel.HIGH,
                {
                    "repository": "my repository",
                    "title": "Login Bug",
                    "description": "login bug"
                },
                "github"
            )
        elif "weather" in message_lower:
            return self._create_mock_result(
                IntentType.GENERAL_QUERY,
                ConfidenceLevel.HIGH,
                {"query": "weather"},
                None
            )
        elif "calendar" in message_lower and ("list" in message_lower or "events" in message_lower):
            return self._create_mock_result(
                IntentType.CALENDAR_LIST_EVENTS,
                ConfidenceLevel.HIGH,
                {"time_range": "this week"},
                "google"
            )
        elif "message" in message_lower and ("send" in message_lower or "channel" in message_lower):
            return self._create_mock_result(
                IntentType.SLACK_SEND_MESSAGE,
                ConfidenceLevel.HIGH,
                {
                    "channel": "team channel",
                    "message": "deployment is complete"
                },
                "slack"
            )
        else:
            return self._create_mock_result(
                IntentType.UNKNOWN,
                ConfidenceLevel.LOW,
                {},
                None
            )
    
    def _create_mock_result(self, intent_type, confidence, parameters, service_name):
        """Create a mock intent analysis result"""
        from app.core.ai_agent import IntentAnalysisResult
        
        result = IntentAnalysisResult(
            intent_type=intent_type,
            confidence=confidence,
            parameters=parameters,
            required_permissions=[],
            service_name=service_name,
            clarification_needed=False,
            clarification_questions=[]
        )
        
        return self._add_permission_requirements(result)
    
    async def _generate_response_openai(self, intent_result, action_result=None, error_message=None):
        """Mock OpenAI response generation"""
        if error_message:
            return f"I encountered an issue: {error_message}"
        
        if intent_result.clarification_needed:
            return f"I need some clarification: {', '.join(intent_result.clarification_questions)}"
        
        # Generate mock responses based on intent
        if intent_result.intent_type == IntentType.CALENDAR_CREATE_EVENT:
            return f"I'll help you schedule a meeting. I found these details: {intent_result.parameters.get('title', 'meeting')} at {intent_result.parameters.get('start_time', 'the specified time')}."
        
        elif intent_result.intent_type == IntentType.EMAIL_SEND:
            return f"I'll help you send an email to {intent_result.parameters.get('recipient', 'the recipient')} about {intent_result.parameters.get('subject', 'the topic')}."
        
        elif intent_result.intent_type == IntentType.GITHUB_CREATE_ISSUE:
            return f"I'll create an issue in {intent_result.parameters.get('repository', 'your repository')} about {intent_result.parameters.get('title', 'the issue')}."
        
        elif intent_result.intent_type == IntentType.GENERAL_QUERY:
            return "I understand you're asking a general question. I'd be happy to help with that!"
        
        elif intent_result.intent_type == IntentType.CALENDAR_LIST_EVENTS:
            return f"I'll show you your calendar events for {intent_result.parameters.get('time_range', 'the requested time period')}."
        
        elif intent_result.intent_type == IntentType.SLACK_SEND_MESSAGE:
            return f"I'll send a message to {intent_result.parameters.get('channel', 'the channel')}: '{intent_result.parameters.get('message', 'your message')}'."
        
        else:
            return "I'm not sure how to help with that request. Could you provide more details?"


async def test_mock_ai_agent():
    """Test the AI Agent Engine functionality with mocked responses"""
    
    print("🤖 Testing AI Agent Engine (Mock Mode)")
    print("=" * 50)
    
    # Initialize mock AI agent
    agent = MockAIAgentEngine()
    
    # Check available providers
    available_providers = agent.get_available_providers()
    print(f"Available providers: {[p.value for p in available_providers]}")
    print(f"Active provider: {agent.active_provider.value}")
    print()
    
    # Test cases
    test_messages = [
        "Schedule a meeting with John tomorrow at 2pm about the project review",
        "Send an email to sarah@example.com with the quarterly report",
        "Create an issue in my repository about the login bug",
        "What's the weather like today?",
        "List my calendar events for this week",
        "Send a message to the team channel saying the deployment is complete"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        print("-" * 30)
        
        try:
            # Analyze intent
            result = await agent.analyze_intent(message)
            
            print(f"Intent: {result.intent_type.value}")
            print(f"Confidence: {result.confidence.value}")
            print(f"Service: {result.service_name}")
            print(f"Parameters: {json.dumps(result.parameters, indent=2)}")
            print(f"Required permissions: {result.required_permissions}")
            print(f"Clarification needed: {result.clarification_needed}")
            
            if result.clarification_questions:
                print(f"Questions: {result.clarification_questions}")
            
            # Generate response
            response = await agent.generate_response(result)
            print(f"Response: {response}")
            
            # Test parameter validation
            if result.intent_type not in [IntentType.GENERAL_QUERY, IntentType.UNKNOWN]:
                is_valid, missing_params = await agent.validate_intent_parameters(
                    result.intent_type, result.parameters
                )
                print(f"Parameters valid: {is_valid}")
                if missing_params:
                    print(f"Missing parameters: {missing_params}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
    
    # Test permission requirements
    print("Permission Requirements Test:")
    print("-" * 30)
    
    for intent_type in [IntentType.CALENDAR_CREATE_EVENT, IntentType.EMAIL_SEND, IntentType.GITHUB_CREATE_ISSUE]:
        perm_req = agent.get_permission_requirements(intent_type)
        if perm_req:
            print(f"{intent_type.value}:")
            print(f"  Service: {perm_req.service}")
            print(f"  Scopes: {perm_req.scopes}")
            print(f"  Risk Level: {perm_req.risk_level}")
        else:
            print(f"{intent_type.value}: No permissions required")
    
    # Test provider switching
    print("\nProvider Switching Test:")
    print("-" * 30)
    
    original_provider = agent.active_provider
    print(f"Original provider: {original_provider.value}")
    
    # Try switching to Gemini
    success = agent.switch_provider(AIProvider.GEMINI)
    print(f"Switch to Gemini: {success}")
    print(f"Current provider: {agent.active_provider.value}")
    
    # Switch back
    agent.switch_provider(original_provider)
    print(f"Switched back to: {agent.active_provider.value}")
    
    print("\n✅ AI Agent Engine mock test completed!")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_mock_ai_agent())