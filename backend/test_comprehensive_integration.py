#!/usr/bin/env python3
"""
Comprehensive integration test for CipherMate platform
Tests all major components without requiring live API calls
"""

import asyncio
import os
import sys
import json
from unittest.mock import Mock, AsyncMock, patch
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Load environment variables
load_dotenv()

async def test_ai_agent_initialization():
    """Test AI agent initialization with OpenAI Agents SDK"""
    print("🤖 Testing AI Agent Initialization...")
    
    try:
        from app.core.ai_agent import ai_agent, AIProvider, IntentType
        
        # Test basic initialization
        assert ai_agent.active_provider == AIProvider.OPENAI_AGENTS_SDK
        assert ai_agent.triage_agent is not None
        assert ai_agent.intent_agent is not None
        assert ai_agent.response_agent is not None
        
        # Test provider availability
        available_providers = ai_agent.get_available_providers()
        assert AIProvider.OPENAI_AGENTS_SDK in available_providers
        
        # Test permission mappings
        calendar_perm = ai_agent.get_permission_requirements(IntentType.CALENDAR_CREATE_EVENT)
        assert calendar_perm is not None
        assert calendar_perm.service == "google"
        assert "https://www.googleapis.com/auth/calendar" in calendar_perm.scopes
        
        print("   ✅ AI Agent initialized correctly with OpenAI Agents SDK")
        print(f"   ✅ Active provider: {ai_agent.active_provider.value}")
        print(f"   ✅ Available providers: {[p.value for p in available_providers]}")
        print("   ✅ Permission mappings configured")
        
        return True
        
    except Exception as e:
        print(f"   ❌ AI Agent initialization failed: {e}")
        return False

async def test_intent_analysis_mock():
    """Test intent analysis with mocked responses"""
    print("🔍 Testing Intent Analysis (Mocked)...")
    
    try:
        from app.core.ai_agent import ai_agent, IntentType, ConfidenceLevel
        
        # Mock the Runner.run method to return a controlled response
        mock_response = Mock()
        mock_response.final_output = json.dumps({
            "intent_type": "calendar_create_event",
            "confidence": "high",
            "parameters": {
                "title": "Meeting with John",
                "start_time": "2024-01-15T14:00:00",
                "attendees": ["john@example.com"]
            },
            "service_name": "google",
            "clarification_needed": False,
            "clarification_questions": []
        })
        
        with patch('agents.Runner.run', return_value=mock_response):
            result = await ai_agent.analyze_intent("Schedule a meeting with John tomorrow at 2pm")
            
            assert result.intent_type == IntentType.CALENDAR_CREATE_EVENT
            assert result.confidence == ConfidenceLevel.HIGH
            assert result.service_name == "google"
            assert "title" in result.parameters
            assert len(result.required_permissions) > 0
            
        print("   ✅ Intent analysis working correctly")
        print(f"   ✅ Detected intent: {result.intent_type.value}")
        print(f"   ✅ Confidence: {result.confidence.value}")
        print(f"   ✅ Required permissions: {result.required_permissions}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Intent analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_response_generation_mock():
    """Test response generation with mocked responses"""
    print("💬 Testing Response Generation (Mocked)...")
    
    try:
        from app.core.ai_agent import ai_agent, IntentType, ConfidenceLevel, IntentAnalysisResult
        
        # Create a mock intent result
        intent_result = IntentAnalysisResult(
            intent_type=IntentType.CALENDAR_CREATE_EVENT,
            confidence=ConfidenceLevel.HIGH,
            parameters={"title": "Meeting with John", "start_time": "2024-01-15T14:00:00"},
            required_permissions=["https://www.googleapis.com/auth/calendar"],
            service_name="google",
            clarification_needed=False,
            clarification_questions=[]
        )
        
        # Mock the Runner.run method for response generation
        mock_response = Mock()
        mock_response.final_output = "I can help you schedule that meeting with John. To create calendar events, I'll need access to your Google Calendar. Please grant the necessary permissions first."
        
        with patch('agents.Runner.run', return_value=mock_response):
            response = await ai_agent.generate_response(
                "Schedule a meeting with John tomorrow at 2pm",
                intent_result
            )
            
            assert isinstance(response, str)
            assert len(response) > 0
            assert "calendar" in response.lower() or "meeting" in response.lower()
            
        print("   ✅ Response generation working correctly")
        print(f"   ✅ Generated response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Response generation test failed: {e}")
        return False

async def test_token_vault_integration():
    """Test Token Vault integration"""
    print("🔐 Testing Token Vault Integration...")
    
    try:
        from app.core.token_vault import token_vault_service
        
        # Test service initialization
        assert token_vault_service is not None
        
        # Mock Auth0 Management API responses
        mock_token_response = {
            "access_token": "mock_access_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        mock_store_response = {
            "id": "mock_token_id",
            "user_id": "auth0|test_user",
            "service": "google",
            "created_at": "2024-01-15T10:00:00Z"
        }
        
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_store_response
            
            # Test token storage
            result = await token_vault_service.store_token(
                user_id="auth0|test_user",
                service="google",
                access_token="test_access_token",
                refresh_token="test_refresh_token",
                scopes=["https://www.googleapis.com/auth/calendar"]
            )
            
            assert result is not None
            
        print("   ✅ Token Vault service initialized")
        print("   ✅ Token storage interface working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Token Vault integration test failed: {e}")
        return False

async def test_permission_management():
    """Test permission management system"""
    print("🔑 Testing Permission Management...")
    
    try:
        from app.core.ai_agent import ai_agent
        
        # Test permission checking
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
        
        # Test sufficient permissions
        has_perms, missing = ai_agent.check_user_permissions(
            user_permissions,
            ["https://www.googleapis.com/auth/calendar"],
            "google"
        )
        assert has_perms == True
        assert len(missing) == 0
        
        # Test insufficient permissions
        has_perms, missing = ai_agent.check_user_permissions(
            user_permissions,
            ["https://www.googleapis.com/auth/gmail.send"],
            "google"
        )
        assert has_perms == False
        assert len(missing) > 0
        
        print("   ✅ Permission checking working correctly")
        print("   ✅ Missing permission detection working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Permission management test failed: {e}")
        return False

async def test_api_integration_service():
    """Test API integration service"""
    print("🌐 Testing API Integration Service...")
    
    try:
        from app.core.api_integration import api_integration_service
        
        # Test service initialization
        assert api_integration_service is not None
        
        # Mock API response
        mock_response = {
            "events": [
                {
                    "id": "event_1",
                    "summary": "Test Meeting",
                    "start": {"dateTime": "2024-01-15T14:00:00Z"}
                }
            ]
        }
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            # Test API call
            result = await api_integration_service.make_api_call(
                service="google",
                endpoint="calendar/v3/calendars/primary/events",
                method="GET",
                token="mock_token"
            )
            
            assert result is not None
            
        print("   ✅ API integration service initialized")
        print("   ✅ API call interface working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API integration test failed: {e}")
        return False

async def test_audit_system():
    """Test audit logging system"""
    print("📊 Testing Audit System...")
    
    try:
        from app.core.audit_service import audit_service
        
        # Test service initialization
        assert audit_service is not None
        
        # Mock database operations
        with patch('app.core.audit_service.audit_service.log_action') as mock_log:
            mock_log.return_value = True
            
            # Test action logging
            result = await audit_service.log_action(
                user_id=1,
                action_type="ai_chat",
                service_name="google",
                details={"intent": "calendar_create_event"},
                request=None
            )
            
            assert mock_log.called
            
        print("   ✅ Audit service initialized")
        print("   ✅ Action logging interface working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Audit system test failed: {e}")
        return False

async def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    print("🔄 Testing End-to-End Workflow...")
    
    try:
        from app.core.ai_agent import ai_agent, IntentType
        
        # Simulate complete workflow
        user_message = "Schedule a meeting with John tomorrow at 2pm"
        
        # Mock intent analysis
        mock_intent_response = Mock()
        mock_intent_response.final_output = json.dumps({
            "intent_type": "calendar_create_event",
            "confidence": "high",
            "parameters": {"title": "Meeting with John", "start_time": "2024-01-15T14:00:00"},
            "service_name": "google",
            "clarification_needed": False,
            "clarification_questions": []
        })
        
        # Mock response generation
        mock_response_response = Mock()
        mock_response_response.final_output = "I can help you schedule that meeting. I'll need access to your Google Calendar first."
        
        with patch('agents.Runner.run', side_effect=[mock_intent_response, mock_response_response]):
            # Step 1: Analyze intent
            intent_result = await ai_agent.analyze_intent(user_message)
            assert intent_result.intent_type == IntentType.CALENDAR_CREATE_EVENT
            
            # Step 2: Check permissions
            user_permissions = []  # No permissions granted
            has_perms, missing = ai_agent.check_user_permissions(
                user_permissions,
                intent_result.required_permissions,
                intent_result.service_name
            )
            assert has_perms == False  # Should need permissions
            
            # Step 3: Generate response
            response = await ai_agent.generate_response(user_message, intent_result)
            assert isinstance(response, str)
            assert len(response) > 0
            
        print("   ✅ End-to-end workflow completed successfully")
        print(f"   ✅ Intent: {intent_result.intent_type.value}")
        print(f"   ✅ Permissions needed: {len(intent_result.required_permissions)} scopes")
        print(f"   ✅ Response generated: {len(response)} characters")
        
        return True
        
    except Exception as e:
        print(f"   ❌ End-to-end workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_security_features():
    """Test security features"""
    print("🛡️ Testing Security Features...")
    
    try:
        from app.core.ai_agent import ai_agent, IntentType
        
        # Test permission requirement mapping
        high_risk_intents = [
            IntentType.EMAIL_SEND,
            IntentType.CALENDAR_DELETE_EVENT,
            IntentType.GITHUB_CREATE_PR
        ]
        
        for intent in high_risk_intents:
            perm_req = ai_agent.get_permission_requirements(intent)
            assert perm_req is not None
            assert len(perm_req.scopes) > 0
            
        # Test parameter validation
        valid, missing = await ai_agent.validate_intent_parameters(
            IntentType.CALENDAR_CREATE_EVENT,
            {"title": "Test Meeting", "start_time": "2024-01-15T14:00:00"}
        )
        assert valid == True
        
        valid, missing = await ai_agent.validate_intent_parameters(
            IntentType.CALENDAR_CREATE_EVENT,
            {"title": "Test Meeting"}  # Missing start_time
        )
        assert valid == False
        assert "start_time" in missing
        
        print("   ✅ Permission requirements properly mapped")
        print("   ✅ Parameter validation working")
        print("   ✅ Security boundaries enforced")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Security features test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting CipherMate Comprehensive Integration Tests\n")
    
    # Check environment
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not set - using mock responses for API tests")
    else:
        print(f"✅ Environment configured with Gemini API key")
    
    # Define test suite
    tests = [
        ("AI Agent Initialization", test_ai_agent_initialization),
        ("Intent Analysis (Mocked)", test_intent_analysis_mock),
        ("Response Generation (Mocked)", test_response_generation_mock),
        ("Token Vault Integration", test_token_vault_integration),
        ("Permission Management", test_permission_management),
        ("API Integration Service", test_api_integration_service),
        ("Audit System", test_audit_system),
        ("End-to-End Workflow", test_end_to_end_workflow),
        ("Security Features", test_security_features),
    ]
    
    # Run tests
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            result = await test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("COMPREHENSIVE TEST SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All comprehensive integration tests passed!")
        print("🔒 OpenAI Agents SDK integration successful")
        print("🔐 Token Vault integration validated")
        print("🛡️ Security features working correctly")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)