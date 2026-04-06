#!/usr/bin/env python3
"""
Basic setup test for CipherMate backend
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.core.config import settings
        print("✓ Config imported successfully")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from app.core.database import Base, engine
        print("✓ Database imported successfully")
    except Exception as e:
        print(f"✗ Database import failed: {e}")
        return False
    
    try:
        from app.models.user import User
        from app.models.service_connection import ServiceConnection
        print("✓ Models imported successfully")
    except Exception as e:
        print(f"✗ Models import failed: {e}")
        return False
    
    try:
        from app.core.session import session_manager
        print("✓ Session manager imported successfully")
    except Exception as e:
        print(f"✗ Session manager import failed: {e}")
        return False
    
    try:
        from app.core.auth import auth0_jwt_bearer
        print("✓ Auth module imported successfully")
    except Exception as e:
        print(f"✗ Auth module import failed: {e}")
        return False
    
    try:
        from app.core.token_vault import token_vault_service
        print("✓ Token vault service imported successfully")
    except Exception as e:
        print(f"✗ Token vault service import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration values"""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        
        # Test that settings object exists
        print(f"✓ Settings loaded")
        print(f"  - App name: {settings.APP_NAME}")
        print(f"  - Environment: {settings.APP_ENV}")
        print(f"  - Debug mode: {settings.DEBUG}")
        
        # Check Auth0 configuration structure
        if hasattr(settings, 'AUTH0_DOMAIN'):
            print("✓ Auth0 configuration structure exists")
        else:
            print("✗ Auth0 configuration missing")
            return False
        
        # Test URL generation
        try:
            issuer_url = settings.auth0_issuer_url
            jwks_url = settings.auth0_jwks_url
            print(f"✓ Auth0 URLs can be generated")
        except Exception as e:
            print(f"✗ Auth0 URL generation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run basic setup tests"""
    print("CipherMate Backend Basic Setup Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Basic setup is working!")
    else:
        print("⚠️  Some basic setup issues found.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)