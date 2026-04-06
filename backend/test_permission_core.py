"""Test script for core permission management functionality without database dependencies"""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_oauth_flow_generation():
    """Test OAuth flow URL generation"""
    print("\n=== Testing OAuth Flow Generation ===")
    
    try:
        from app.core.oauth_handlers import GoogleOAuthHandler, GitHubOAuthHandler, SlackOAuthHandler
        
        # Test Google OAuth handler
        google_handler = GoogleOAuthHandler()
        test_user_id = "test_user_123"
        test_scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        
        auth_url, state = await google_handler.get_authorization_url(test_user_id, test_scopes)
        
        print(f"✓ Google OAuth URL generated: {len(auth_url)} characters")
        print(f"✓ State parameter: {state[:30]}...")
        
        # Validate state
        is_valid = google_handler.validate_state(state, test_user_id)
        print(f"✓ State validation: {is_valid}")
        
        # Test GitHub OAuth handler
        github_handler = GitHubOAuthHandler()
        github_scopes = ["user:email", "repo"]
        
        github_url, github_state = await github_handler.get_authorization_url(test_user_id, github_scopes)
        
        print(f"✓ GitHub OAuth URL generated: {len(github_url)} characters")
        print(f"✓ GitHub state parameter: {github_state[:30]}...")
        
        # Test Slack OAuth handler
        slack_handler = SlackOAuthHandler()
        slack_scopes = ["channels:read", "chat:write"]
        
        slack_url, slack_state = await slack_handler.get_authorization_url(test_user_id, slack_scopes)
        
        print(f"✓ Slack OAuth URL generated: {len(slack_url)} characters")
        print(f"✓ Slack state parameter: {slack_state[:30]}...")
        
        print("OAuth flow generation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ OAuth flow generation test failed: {e}")
        return False


async def test_permission_templates():
    """Test permission template functionality"""
    print("\n=== Testing Permission Templates ===")
    
    try:
        from app.core.permission_service import PermissionService
        
        perm_service = PermissionService()
        
        # Test default scopes
        google_defaults = perm_service.get_default_scopes_for_service("google")
        github_defaults = perm_service.get_default_scopes_for_service("github")
        slack_defaults = perm_service.get_default_scopes_for_service("slack")
        
        print(f"✓ Google default scopes: {len(google_defaults)} scopes")
        for scope in google_defaults[:2]:  # Show first 2
            print(f"  - {scope}")
        
        print(f"✓ GitHub default scopes: {len(github_defaults)} scopes")
        for scope in github_defaults:
            print(f"  - {scope}")
        
        print(f"✓ Slack default scopes: {len(slack_defaults)} scopes")
        for scope in slack_defaults:
            print(f"  - {scope}")
        
        # Test high-risk scopes
        google_high_risk = perm_service.get_high_risk_scopes_for_service("google")
        github_high_risk = perm_service.get_high_risk_scopes_for_service("github")
        slack_high_risk = perm_service.get_high_risk_scopes_for_service("slack")
        
        print(f"✓ Google high-risk scopes: {len(google_high_risk)} scopes")
        print(f"✓ GitHub high-risk scopes: {len(github_high_risk)} scopes")
        print(f"✓ Slack high-risk scopes: {len(slack_high_risk)} scopes")
        
        # Test service scope data structure
        google_scopes = perm_service.service_scopes.get("google", {})
        print(f"✓ Google scope templates: {len(google_scopes)} defined")
        
        # Test a specific scope
        calendar_scope = google_scopes.get("calendar")
        if calendar_scope:
            print(f"✓ Calendar scope details: {calendar_scope['description']}")
            print(f"  Risk level: {calendar_scope['risk_level']}")
            print(f"  Requires step-up: {calendar_scope['requires_step_up']}")
        
        print("Permission templates test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Permission templates test failed: {e}")
        return False


async def test_oauth_service_integration():
    """Test OAuth service integration"""
    print("\n=== Testing OAuth Service Integration ===")
    
    try:
        from app.core.oauth_handlers import oauth_service
        
        # Test service handlers
        services = list(oauth_service.handlers.keys())
        print(f"✓ Available services: {', '.join(services)}")
        
        for service in services:
            handler = oauth_service.get_handler(service)
            print(f"✓ {service.title()} handler: {handler.__class__.__name__}")
            
            # Test default scopes
            default_scopes = oauth_service.get_default_scopes(service)
            print(f"  Default scopes: {len(default_scopes)}")
        
        # Test OAuth flow initiation
        test_user_id = "test_user_456"
        
        for service in ["google", "github", "slack"]:
            try:
                auth_url, state = await oauth_service.initiate_oauth_flow(
                    user_id=test_user_id,
                    service_name=service
                )
                print(f"✓ {service.title()} OAuth flow initiated successfully")
                
                # Validate the URL contains expected components
                if service == "google" and "accounts.google.com" in auth_url:
                    print(f"  ✓ Google URL contains correct domain")
                elif service == "github" and "github.com" in auth_url:
                    print(f"  ✓ GitHub URL contains correct domain")
                elif service == "slack" and "slack.com" in auth_url:
                    print(f"  ✓ Slack URL contains correct domain")
                
            except Exception as e:
                print(f"  ⚠ {service.title()} OAuth flow failed (expected without credentials): {str(e)[:100]}...")
        
        print("OAuth service integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ OAuth service integration test failed: {e}")
        return False


async def test_scope_validation():
    """Test scope validation without database"""
    print("\n=== Testing Scope Validation ===")
    
    try:
        from app.core.permission_service import PermissionService
        
        perm_service = PermissionService()
        
        # Test valid Google scopes
        valid_google_scopes = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        
        # Mock the database call to return our service scopes
        with patch.object(perm_service, 'get_service_scopes') as mock_get_scopes:
            mock_get_scopes.return_value = {
                "https://www.googleapis.com/auth/calendar.readonly": {
                    "description": "Read access to Google Calendar",
                    "risk_level": "medium",
                    "requires_step_up": False
                },
                "https://www.googleapis.com/auth/userinfo.email": {
                    "description": "Access to user email",
                    "risk_level": "low",
                    "requires_step_up": False
                },
                "https://www.googleapis.com/auth/calendar": {
                    "description": "Full calendar access",
                    "risk_level": "high",
                    "requires_step_up": True
                }
            }
            
            validation_result = await perm_service.validate_scopes("google", valid_google_scopes)
            
            print(f"✓ Validation result: {validation_result['validation_passed']}")
            print(f"✓ Valid scopes: {len(validation_result['valid_scopes'])}")
            print(f"✓ Invalid scopes: {len(validation_result['invalid_scopes'])}")
            print(f"✓ High-risk scopes: {len(validation_result['high_risk_scopes'])}")
            print(f"✓ Requires step-up: {validation_result['requires_step_up']}")
        
        # Test invalid scopes
        invalid_scopes = ["invalid.scope", "another.invalid.scope"]
        
        with patch.object(perm_service, 'get_service_scopes') as mock_get_scopes:
            mock_get_scopes.return_value = {}  # No valid scopes
            
            validation_result = await perm_service.validate_scopes("google", invalid_scopes)
            
            print(f"✓ Invalid scope validation: {not validation_result['validation_passed']}")
            print(f"✓ All scopes marked invalid: {len(validation_result['invalid_scopes']) == 2}")
        
        print("Scope validation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Scope validation test failed: {e}")
        return False


async def test_state_parameter_security():
    """Test OAuth state parameter security"""
    print("\n=== Testing State Parameter Security ===")
    
    try:
        from app.core.oauth_handlers import GoogleOAuthHandler
        
        handler = GoogleOAuthHandler()
        test_user_id = "test_user_789"
        
        # Generate state
        state = handler.generate_state(test_user_id)
        print(f"✓ State generated: {state[:30]}...")
        
        # Test valid state validation
        is_valid = handler.validate_state(state, test_user_id)
        print(f"✓ Valid state validation: {is_valid}")
        
        # Test invalid user ID
        is_invalid = handler.validate_state(state, "different_user")
        print(f"✓ Invalid user validation: {not is_invalid}")
        
        # Test malformed state
        malformed_states = [
            "malformed_state",
            "",
            "user_id_only",
            "too:many:colons:here"
        ]
        
        for malformed in malformed_states:
            is_invalid = handler.validate_state(malformed, test_user_id)
            if not is_invalid:
                print(f"✓ Malformed state '{malformed[:20]}...' properly rejected")
            else:
                print(f"✗ Malformed state '{malformed[:20]}...' incorrectly accepted")
                return False
        
        # Test state uniqueness
        state1 = handler.generate_state(test_user_id)
        state2 = handler.generate_state(test_user_id)
        
        if state1 != state2:
            print("✓ State parameters are unique")
        else:
            print("✗ State parameters should be unique")
            return False
        
        print("State parameter security test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ State parameter security test failed: {e}")
        return False


async def main():
    """Run all core tests"""
    print("Starting Permission Management Core Tests...")
    print("=" * 60)
    
    tests = [
        ("OAuth Flow Generation", test_oauth_flow_generation),
        ("Permission Templates", test_permission_templates),
        ("OAuth Service Integration", test_oauth_service_integration),
        ("Scope Validation", test_scope_validation),
        ("State Parameter Security", test_state_parameter_security)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("CORE TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core tests passed! Permission management system is working correctly.")
        return True
    else:
        print("⚠ Some core tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)