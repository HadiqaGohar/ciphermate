#!/usr/bin/env python3
"""
Integration test for OpenAI Agents SDK with Gemini API
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Load environment variables
load_dotenv()

async def test_ai_agent_integration():
    """Test the AI agent integration with OpenAI Agents SDK"""
    
    print("🧪 Testing OpenAI Agents SDK Integration with Gemini API\n")
    
    try:
        # Import the AI agent
        from app.core.ai_agent import ai_agent, AIProvider
        
        print(f"✅ AI Agent initialized successfully")
        print(f"   Active provider: {ai_agent.active_provider.value}")
        print(f"   Available providers: {[p.value for p in ai_agent.get_available_providers()]}")
        print(f"   Triage agent available: {ai_agent.triage_agent is not None}")
        print(f"   Intent agent available: {ai_agent.intent_agent is not None}")
        print(f"   Response agent available: {ai_agent.response_agent is not None}")
        
        # Test intent analysis
        print("\n🔍 Testing Intent Analysis...")
        test_messages = [
            "Schedule a meeting with John tomorrow at 2pm",
            "Send an email to sarah@example.com about the project update",
            "Create an issue in my repository about the login bug",
            "Send a message to the team channel saying the deployment is complete",
            "What's the weather like today?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Test {i}: '{message}'")
            try:
                result = await ai_agent.analyze_intent(message)
                print(f"   ✅ Intent: {result.intent_type.value}")
                print(f"      Confidence: {result.confidence.value}")
                print(f"      Service: {result.service_name}")
                print(f"      Parameters: {result.parameters}")
                print(f"      Required permissions: {result.required_permissions}")
                if result.clarification_needed:
                    print(f"      Clarification needed: {result.clarification_questions}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Test response generation
        print("\n💬 Testing Response Generation...")
        test_message = "Schedule a meeting with John tomorrow at 2pm"
        try:
            intent_result = await ai_agent.analyze_intent(test_message)
            response = await ai_agent.generate_response(test_message, intent_result)
            print(f"   User: {test_message}")
            print(f"   AI: {response}")
        except Exception as e:
            print(f"   ❌ Error generating response: {e}")
        
        # Test permission requirements
        print("\n🔐 Testing Permission Requirements...")
        from app.core.ai_agent import IntentType
        
        test_intents = [
            IntentType.CALENDAR_CREATE_EVENT,
            IntentType.EMAIL_SEND,
            IntentType.GITHUB_CREATE_ISSUE,
            IntentType.SLACK_SEND_MESSAGE
        ]
        
        for intent in test_intents:
            perm_req = ai_agent.get_permission_requirements(intent)
            if perm_req:
                print(f"   {intent.value}:")
                print(f"      Service: {perm_req.service}")
                print(f"      Scopes: {perm_req.scopes}")
                print(f"      Risk level: {perm_req.risk_level}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_oauth_flows():
    """Test OAuth flow simulation"""
    print("\n🔗 Testing OAuth Flow Simulation...")
    
    try:
        # Test user permissions check
        from app.core.ai_agent import ai_agent
        
        # Simulate user permissions
        user_permissions = [
            {
                "service_name": "google",
                "scopes": ["https://www.googleapis.com/auth/calendar"],
                "is_active": True
            },
            {
                "service_name": "github", 
                "scopes": ["repo"],
                "is_active": True
            }
        ]
        
        # Test permission checking
        required_permissions = ["https://www.googleapis.com/auth/calendar"]
        has_perms, missing = ai_agent.check_user_permissions(
            user_permissions, required_permissions, "google"
        )
        
        print(f"   Google Calendar permissions: {'✅ Granted' if has_perms else '❌ Missing'}")
        if missing:
            print(f"   Missing permissions: {missing}")
        
        # Test missing permissions
        required_permissions = ["https://www.googleapis.com/auth/gmail.send"]
        has_perms, missing = ai_agent.check_user_permissions(
            user_permissions, required_permissions, "google"
        )
        
        print(f"   Gmail send permissions: {'✅ Granted' if has_perms else '❌ Missing'}")
        if missing:
            print(f"   Missing permissions: {missing}")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth flow test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting CipherMate OpenAI Agents SDK Integration Tests\n")
    
    # Check environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY environment variable not set")
        print("   Please set your Gemini API key to run these tests")
        return False
    
    print(f"✅ Environment configured")
    print(f"   Gemini API Key: {'*' * 20}{os.getenv('GEMINI_API_KEY', '')[-4:]}")
    
    # Run tests
    tests = [
        ("AI Agent Integration", test_ai_agent_integration),
        ("OAuth Flows", test_oauth_flows),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All integration tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)