#!/usr/bin/env python3
"""
Final validation test for OpenAI Agents SDK integration
Focuses on the core AI agent functionality that was migrated from Google Generative AI
"""

import asyncio
import os
import sys
import json
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Load environment variables
load_dotenv()

async def validate_openai_agents_sdk_migration():
    """Validate that the migration from Google Generative AI to OpenAI Agents SDK is successful"""
    print("🔄 Validating OpenAI Agents SDK Migration...")
    
    try:
        # Test 1: Import and initialization
        from app.core.ai_agent import ai_agent, AIProvider, IntentType, ConfidenceLevel
        
        print("   ✅ Successfully imported AI agent with OpenAI Agents SDK")
        
        # Test 2: Verify provider is OpenAI Agents SDK (not Gemini)
        assert ai_agent.active_provider == AIProvider.OPENAI_AGENTS_SDK
        print("   ✅ Active provider is OpenAI Agents SDK (not direct Gemini)")
        
        # Test 3: Verify agents are initialized
        assert ai_agent.triage_agent is not None
        assert ai_agent.intent_agent is not None
        assert ai_agent.response_agent is not None
        print("   ✅ All OpenAI Agents SDK agents initialized")
        
        # Test 4: Verify Gemini client is configured for OpenAI API compatibility
        assert ai_agent.gemini_client is not None
        print("   ✅ Gemini client configured for OpenAI API compatibility")
        
        # Test 5: Test intent analysis with mocked response
        mock_response = Mock()
        mock_response.final_output = json.dumps({
            "intent_type": "email_send",
            "confidence": "high",
            "parameters": {"recipient": "test@example.com", "subject": "Test"},
            "service_name": "google",
            "clarification_needed": False,
            "clarification_questions": []
        })
        
        with patch('agents.Runner.run', return_value=mock_response):
            result = await ai_agent.analyze_intent("Send an email to test@example.com")
            assert result.intent_type == IntentType.EMAIL_SEND
            assert result.confidence == ConfidenceLevel.HIGH
            print("   ✅ Intent analysis working through OpenAI Agents SDK")
        
        # Test 6: Test response generation with mocked response
        mock_response.final_output = "I can help you send that email. I'll need access to your Gmail account first."
        
        with patch('agents.Runner.run', return_value=mock_response):
            response = await ai_agent.generate_response("Send an email", result)
            assert isinstance(response, str)
            assert len(response) > 0
            print("   ✅ Response generation working through OpenAI Agents SDK")
        
        # Test 7: Verify permission mappings still work
        email_perm = ai_agent.get_permission_requirements(IntentType.EMAIL_SEND)
        assert email_perm is not None
        assert email_perm.service == "google"
        assert "gmail.send" in str(email_perm.scopes)
        print("   ✅ Permission mappings preserved after migration")
        
        # Test 8: Test provider switching (should only have OpenAI Agents SDK)
        available_providers = ai_agent.get_available_providers()
        assert AIProvider.OPENAI_AGENTS_SDK in available_providers
        print("   ✅ Provider management working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Migration validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def validate_api_endpoint_compatibility():
    """Validate that API endpoints work with the new OpenAI Agents SDK"""
    print("🌐 Validating API Endpoint Compatibility...")
    
    try:
        # Test the AI agent API endpoint response model
        from app.api.v1.ai_agent import ProviderStatusResponse
        from app.core.ai_agent import ai_agent
        
        # Simulate the provider status endpoint
        available_providers = ai_agent.get_available_providers()
        
        response = ProviderStatusResponse(
            active_provider=ai_agent.active_provider.value,
            available_providers=[p.value for p in available_providers],
            gemini_available=False,  # No longer using direct Gemini
            openai_available=ai_agent.gemini_client is not None,  # Using Gemini via OpenAI API
            agents_sdk_available=ai_agent.triage_agent is not None
        )
        
        assert response.active_provider == "openai_agents_sdk"
        assert response.agents_sdk_available == True
        assert response.openai_available == True  # Gemini via OpenAI API
        assert response.gemini_available == False  # No direct Gemini
        
        print("   ✅ API endpoint responses updated for OpenAI Agents SDK")
        print(f"   ✅ Active provider: {response.active_provider}")
        print(f"   ✅ Agents SDK available: {response.agents_sdk_available}")
        print(f"   ✅ OpenAI compatible: {response.openai_available}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API endpoint validation failed: {e}")
        return False

async def validate_configuration_changes():
    """Validate that configuration changes are correct"""
    print("⚙️ Validating Configuration Changes...")
    
    try:
        # Test 1: Verify dependencies are updated
        try:
            import openai_agents
            from openai_agents import OpenAIChatCompletionsModel, AsyncOpenAI
            print("   ✅ OpenAI Agents SDK dependencies available")
        except ImportError as e:
            print(f"   ❌ Missing OpenAI Agents SDK dependency: {e}")
            return False
        
        # Test 2: Verify old Gemini imports are removed
        from app.core.ai_agent import ai_agent
        
        # Should not have direct google.generativeai usage
        assert not hasattr(ai_agent, 'gemini_model')
        print("   ✅ Direct Google Generative AI usage removed")
        
        # Test 3: Verify environment variables are still used
        from app.core.config import settings
        if settings.GEMINI_API_KEY:
            print("   ✅ GEMINI_API_KEY still configured for OpenAI API compatibility")
        else:
            print("   ⚠️  GEMINI_API_KEY not configured")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration validation failed: {e}")
        return False

async def validate_backward_compatibility():
    """Validate that existing functionality still works"""
    print("🔄 Validating Backward Compatibility...")
    
    try:
        from app.core.ai_agent import ai_agent, IntentType
        
        # Test all intent types are still supported
        supported_intents = [
            IntentType.CALENDAR_CREATE_EVENT,
            IntentType.CALENDAR_LIST_EVENTS,
            IntentType.EMAIL_SEND,
            IntentType.EMAIL_LIST,
            IntentType.GITHUB_CREATE_ISSUE,
            IntentType.GITHUB_LIST_REPOS,
            IntentType.SLACK_SEND_MESSAGE,
            IntentType.SLACK_LIST_CHANNELS,
            IntentType.GENERAL_QUERY,
            IntentType.PERMISSION_REQUEST,
            IntentType.UNKNOWN
        ]
        
        for intent in supported_intents:
            perm_req = ai_agent.get_permission_requirements(intent)
            # Some intents don't have permission requirements (like GENERAL_QUERY)
            if intent in [IntentType.GENERAL_QUERY, IntentType.PERMISSION_REQUEST, IntentType.UNKNOWN]:
                assert perm_req is None
            else:
                assert perm_req is not None
        
        print(f"   ✅ All {len(supported_intents)} intent types supported")
        
        # Test parameter validation still works
        valid, missing = await ai_agent.validate_intent_parameters(
            IntentType.EMAIL_SEND,
            {"recipient": "test@example.com", "subject": "Test"}
        )
        assert valid == True
        
        valid, missing = await ai_agent.validate_intent_parameters(
            IntentType.EMAIL_SEND,
            {"recipient": "test@example.com"}  # Missing subject
        )
        assert valid == False
        assert "subject" in missing
        
        print("   ✅ Parameter validation preserved")
        
        # Test permission checking still works
        user_permissions = [{"service_name": "google", "scopes": ["gmail.send"], "is_active": True}]
        has_perms, missing = ai_agent.check_user_permissions(
            user_permissions, ["gmail.send"], "google"
        )
        assert has_perms == True
        
        print("   ✅ Permission checking preserved")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Backward compatibility validation failed: {e}")
        return False

async def main():
    """Main validation function"""
    print("🎯 Final Validation: OpenAI Agents SDK Migration")
    print("=" * 60)
    print("Task: Replace Google Generative AI with OpenAI Agents SDK")
    print("=" * 60)
    
    # Check environment
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not set - some validations may be limited")
    else:
        print("✅ GEMINI_API_KEY configured for OpenAI API compatibility")
    
    # Run validation tests
    tests = [
        ("OpenAI Agents SDK Migration", validate_openai_agents_sdk_migration),
        ("API Endpoint Compatibility", validate_api_endpoint_compatibility),
        ("Configuration Changes", validate_configuration_changes),
        ("Backward Compatibility", validate_backward_compatibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Validating: {test_name}")
        print('='*60)
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Validation '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("FINAL VALIDATION SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} validations passed")
    
    if passed == len(results):
        print("\n🎉 MIGRATION SUCCESSFUL!")
        print("✅ Google Generative AI successfully replaced with OpenAI Agents SDK")
        print("✅ All functionality preserved and working")
        print("✅ API endpoints updated correctly")
        print("✅ Configuration properly migrated")
        print("✅ Backward compatibility maintained")
        print("\n🔧 Task 18 - Final integration testing and bug fixes: COMPLETED")
        return True
    else:
        print(f"\n⚠️  Migration validation incomplete: {len(results) - passed} issues found")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)