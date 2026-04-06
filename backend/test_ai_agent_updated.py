#!/usr/bin/env python3
"""
Test script for the updated AI Agent Engine with Gemini integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.ai_agent import AIAgentEngine, IntentType, ConfidenceLevel, AIProvider


async def test_ai_agent_basic():
    """Test basic AI agent functionality"""
    print("🤖 Testing AI Agent Engine with Gemini integration...")
    
    # Initialize the AI agent
    agent = AIAgentEngine(preferred_provider=AIProvider.AUTO)
    
    print(f"✅ AI Agent initialized with provider: {agent.active_provider.value}")
    print(f"📋 Available providers: {[p.value for p in agent.get_available_providers()]}")
    
    # Test intent analysis with various messages
    test_messages = [
        "Schedule a meeting with John tomorrow at 2pm",
        "Send an email to sarah@example.com about the project update",
        "Create an issue in my repository about the login bug",
        "Send a message to the team channel saying hello",
        "What's the weather like today?",
        "List my calendar events for today"
    ]
    
    for message in test_messages:
        print(f"\n📝 Testing message: '{message}'")
        
        try:
            # Analyze intent
            result = await agent.analyze_intent(message)
            
            print(f"   🎯 Intent: {result.intent_type.value}")
            print(f"   📊 Confidence: {result.confidence.value}")
            print(f"   🔧 Service: {result.service_name or 'None'}")
            print(f"   📋 Parameters: {result.parameters}")
            print(f"   🔐 Required permissions: {result.required_permissions}")
            
            if result.clarification_needed:
                print(f"   ❓ Clarification needed: {result.clarification_questions}")
            
            # Generate response
            response = await agent.generate_response(message, result)
            print(f"   💬 Response: {response}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ AI Agent testing completed!")


async def test_permission_requirements():
    """Test permission requirement mapping"""
    print("\n🔐 Testing permission requirements...")
    
    agent = AIAgentEngine()
    
    # Test permission requirements for different intents
    test_intents = [
        IntentType.CALENDAR_CREATE_EVENT,
        IntentType.EMAIL_SEND,
        IntentType.GITHUB_CREATE_ISSUE,
        IntentType.SLACK_SEND_MESSAGE,
        IntentType.GENERAL_QUERY
    ]
    
    for intent in test_intents:
        perm_req = agent.get_permission_requirements(intent)
        if perm_req:
            print(f"   {intent.value}:")
            print(f"     Service: {perm_req.service}")
            print(f"     Scopes: {perm_req.scopes}")
            print(f"     Risk Level: {perm_req.risk_level}")
        else:
            print(f"   {intent.value}: No permissions required")


async def test_parameter_validation():
    """Test parameter validation"""
    print("\n✅ Testing parameter validation...")
    
    agent = AIAgentEngine()
    
    # Test cases with different parameter completeness
    test_cases = [
        (IntentType.CALENDAR_CREATE_EVENT, {"title": "Meeting", "start_time": "2pm"}),
        (IntentType.CALENDAR_CREATE_EVENT, {"title": "Meeting"}),  # Missing start_time
        (IntentType.EMAIL_SEND, {"recipient": "test@example.com", "subject": "Hello"}),
        (IntentType.EMAIL_SEND, {"recipient": "test@example.com"}),  # Missing subject
        (IntentType.GENERAL_QUERY, {}),  # No parameters required
    ]
    
    for intent, params in test_cases:
        is_valid, missing = await agent.validate_intent_parameters(intent, params)
        status = "✅ Valid" if is_valid else f"❌ Missing: {missing}"
        print(f"   {intent.value}: {status}")


def main():
    """Main test function"""
    print("🚀 Starting AI Agent Engine Tests")
    print("=" * 50)
    
    # Check if Gemini API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Warning: GEMINI_API_KEY not found in environment")
        print("   Some tests may not work without API access")
    
    # Run tests
    asyncio.run(test_ai_agent_basic())
    asyncio.run(test_permission_requirements())
    asyncio.run(test_parameter_validation())
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    main()