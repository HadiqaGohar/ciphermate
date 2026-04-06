#!/usr/bin/env python3
"""
Test script for AI Agent Engine with Gemini integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.ai_agent import AIAgentEngine, AIProvider, IntentType
from app.core.config import settings

async def test_ai_agent():
    """Test the AI Agent Engine functionality"""
    print("Testing AI Agent Engine with Gemini Integration")
    print("=" * 50)
    
    # Initialize the AI agent
    agent = AIAgentEngine(preferred_provider=AIProvider.AUTO)
    
    print(f"Active provider: {agent.active_provider.value}")
    print(f"Available providers: {[p.value for p in agent.get_available_providers()]}")
    print()
    
    # Test cases
    test_messages = [
        "Schedule a meeting with John tomorrow at 2pm",
        "Send an email to sarah@example.com about the project update",
        "Create an issue in my repository about the login bug",
        "Send a message to the team channel saying hello",
        "What's the weather like today?",
        "List my calendar events for this week"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        print("-" * 30)
        
        try:
            # Analyze intent
            result = await agent.analyze_intent(message)
            
            print(f"Intent: {result.intent_type.value}")
            print(f"Confidence: {result.confidence.value}")
            print(f"Service: {result.service_name or 'None'}")
            print(f"Parameters: {result.parameters}")
            print(f"Required permissions: {result.required_permissions}")
            print(f"Needs clarification: {result.clarification_needed}")
            
            if result.clarification_questions:
                print(f"Questions: {result.clarification_questions}")
            
            # Generate response
            response = await agent.generate_response(message, result)
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
    
    print("Testing permission requirements...")
    print("-" * 30)
    
    # Test permission requirements
    for intent_type in [IntentType.CALENDAR_CREATE_EVENT, IntentType.EMAIL_SEND, IntentType.GITHUB_CREATE_ISSUE]:
        perm_req = agent.get_permission_requirements(intent_type)
        if perm_req:
            print(f"{intent_type.value}: {perm_req.service} - {perm_req.scopes} ({perm_req.risk_level} risk)")
    
    print("\nTesting complete!")

if __name__ == "__main__":
    # Check if API keys are configured
    if not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY:
        print("Warning: No AI API keys configured. Set GEMINI_API_KEY or OPENAI_API_KEY in your .env file")
        print("The test will run but may have limited functionality.")
        print()
    
    asyncio.run(test_ai_agent())