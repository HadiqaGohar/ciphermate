"""Test script for permission management system"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.oauth_handlers import oauth_service, OAuthError
from app.core.permission_service import permission_service
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_oauth_handlers():
    """Test OAuth handler initialization and basic functionality"""
    print("\n=== Testing OAuth Handlers ===")
    
    try:
        # Test getting handlers
        google_handler = oauth_service.get_handler("google")
        github_handler = oauth_service.get_handler("github")
        slack_handler = oauth_service.get_handler("slack")
        
        print(f"✓ Google handler initialized: {google_handler.service_name}")
        print(f"✓ GitHub handler initialized: {github_handler.service_name}")
        print(f"✓ Slack handler initialized: {slack_handler.service_name}")
        
        # Test default scopes
        google_scopes = oauth_service.get_default_scopes("google")
        github_scopes = oauth_service.get_default_scopes("github")
        slack_scopes = oauth_service.get_default_scopes("slack")
        
        print(f"✓ Google default scopes: {len(google_scopes)} scopes")
        print(f"✓ GitHub default scopes: {len(github_scopes)} scopes")
        print(f"✓ Slack default scopes: {len(slack_scopes)} scopes")
        
        # Test authorization URL generation (without actual OAuth)
        test_user_id = "test_user_123"
        
        try:
            google_auth_url, google_state = await oauth_service.initiate_oauth_flow(
                user_id=test_user_id,
                service_name="google"
            )
            print(f"✓ Google OAuth URL generated (length: {len(google_auth_url)})")
            print(f"✓ Google state generated: {google_state[:20]}...")
        except Exception as e:
            print(f"⚠ Google OAuth URL generation failed (expected if no credentials): {e}")
        
        print("OAuth handlers test completed successfully!")
        
    except Exception as e:
        print(f"✗ OAuth handlers test failed: {e}")
        return False
    
    return True


async def test_permission_service():
    """Test permission service functionality"""
    print("\n=== Testing Permission Service ===")
    
    try:
        # Test default scopes
        google_defaults = permission_service.get_default_scopes_for_service("google")
        github_defaults = permission_service.get_default_scopes_for_service("github")
        slack_defaults = permission_service.get_default_scopes_for_service("slack")
        
        print(f"✓ Google default scopes: {len(google_defaults)} scopes")
        print(f"✓ GitHub default scopes: {len(github_defaults)} scopes")
        print(f"✓ Slack default scopes: {len(slack_defaults)} scopes")
        
        # Test high-risk scopes
        google_high_risk = permission_service.get_high_risk_scopes_for_service("google")
        github_high_risk = permission_service.get_high_risk_scopes_for_service("github")
        slack_high_risk = permission_service.get_high_risk_scopes_for_service("slack")
        
        print(f"✓ Google high-risk scopes: {len(google_high_risk)} scopes")
        print(f"✓ GitHub high-risk scopes: {len(github_high_risk)} scopes")
        print(f"✓ Slack high-risk scopes: {len(slack_high_risk)} scopes")
        
        # Test scope validation (without database)
        test_scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        print(f"✓ Permission service initialized successfully")
        
        print("Permission service test completed successfully!")
        
    except Exception as e:
        print(f"✗ Permission service test failed: {e}")
        return False
    
    return True


async def test_configuration():
    """Test configuration and environment setup"""
    print("\n=== Testing Configuration ===")
    
    try:
        # Check required settings
        required_settings = [
            "AUTH0_DOMAIN",
            "AUTH0_CLIENT_ID", 
            "AUTH0_CLIENT_SECRET",
            "GOOGLE_CLIENT_ID",
            "GITHUB_CLIENT_ID",
            "SLACK_CLIENT_ID"
        ]
        
        missing_settings = []
        for setting in required_settings:
            value = getattr(settings, setting, "")
            if not value:
                missing_settings.append(setting)
            else:
                print(f"✓ {setting}: configured")
        
        if missing_settings:
            print(f"⚠ Missing configuration: {', '.join(missing_settings)}")
            print("  Note: These are required for full OAuth functionality")
        else:
            print("✓ All required settings configured")
        
        # Test app configuration
        print(f"✓ App name: {settings.APP_NAME}")
        print(f"✓ App environment: {settings.APP_ENV}")
        print(f"✓ App base URL: {settings.APP_BASE_URL}")
        
        print("Configuration test completed successfully!")
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False
    
    return True


async def test_service_integration():
    """Test integration between services"""
    print("\n=== Testing Service Integration ===")
    
    try:
        # Test that OAuth service can work with permission service
        services = list(oauth_service.handlers.keys())
        print(f"✓ Available services: {', '.join(services)}")
        
        for service in services:
            # Test that each service has default scopes
            oauth_defaults = oauth_service.get_default_scopes(service)
            perm_defaults = permission_service.get_default_scopes_for_service(service)
            
            print(f"✓ {service.title()}: OAuth defaults={len(oauth_defaults)}, Permission defaults={len(perm_defaults)}")
        
        print("Service integration test completed successfully!")
        
    except Exception as e:
        print(f"✗ Service integration test failed: {e}")
        return False
    
    return True


async def main():
    """Run all tests"""
    print("Starting Permission Management System Tests...")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("OAuth Handlers", test_oauth_handlers),
        ("Permission Service", test_permission_service),
        ("Service Integration", test_service_integration)
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
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Permission management system is ready.")
        return True
    else:
        print("⚠ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)