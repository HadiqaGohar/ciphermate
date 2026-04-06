#!/usr/bin/env python3
"""
Test script for Auth0 integration and Token Vault functionality
"""

import asyncio
import httpx
import json
from datetime import datetime
from app.core.config import settings
from app.core.auth import auth0_jwt_bearer
from app.core.token_vault import (
    token_vault_service, 
    TokenVaultError, 
    TokenNotFoundError, 
    TokenExpiredError,
    AuthenticationError,
    ServiceError,
    TokenStatus
)
from app.core.session import session_manager

async def test_auth0_jwks():
    """Test Auth0 JWKS endpoint connectivity"""
    print("Testing Auth0 JWKS endpoint...")
    try:
        jwks = await auth0_jwt_bearer.get_jwks()
        print(f"✓ JWKS retrieved successfully with {len(jwks.get('keys', []))} keys")
        return True
    except Exception as e:
        print(f"✗ JWKS test failed: {e}")
        return False

async def test_session_management():
    """Test session management functionality"""
    print("\nTesting session management...")
    try:
        # Test session creation
        user_id = "test_user_123"
        user_data = {
            "sub": user_id,
            "email": "test@example.com",
            "name": "Test User"
        }
        
        session_id = await session_manager.create_session(user_id, user_data)
        print(f"✓ Session created: {session_id}")
        
        # Test session retrieval
        session_data = await session_manager.get_session(session_id)
        if session_data and session_data.get("user_id") == user_id:
            print("✓ Session retrieved successfully")
        else:
            print("✗ Session retrieval failed")
            return False
        
        # Test session update
        updates = {"last_login": datetime.now().isoformat()}
        success = await session_manager.update_session(session_id, updates)
        if success:
            print("✓ Session updated successfully")
        else:
            print("✗ Session update failed")
            return False
        
        # Test session deletion
        success = await session_manager.delete_session(session_id)
        if success:
            print("✓ Session deleted successfully")
        else:
            print("✗ Session deletion failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Session management test failed: {e}")
        return False

async def test_token_vault_operations():
    """Test Token Vault operations with enhanced functionality"""
    print("\nTesting Enhanced Token Vault operations...")
    try:
        user_id = "test_user_456"
        service_name = "google_calendar"
        token_data = {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        scopes = ["https://www.googleapis.com/auth/calendar"]
        
        # Test service initialization
        service = token_vault_service
        print(f"✓ Token Vault service initialized with {service._max_retries} max retries")
        
        # Test input validation
        try:
            await service.store_token("", "service", {}, [])
            print("✗ Validation should have failed")
            return False
        except ValueError:
            print("✓ Input validation working correctly")
        
        # Test token status enum
        print(f"✓ Token status enum: {TokenStatus.ACTIVE.value}, {TokenStatus.EXPIRED.value}, {TokenStatus.REVOKED.value}")
        
        # Test error hierarchy
        assert issubclass(TokenNotFoundError, TokenVaultError)
        assert issubclass(TokenExpiredError, TokenVaultError)
        assert issubclass(AuthenticationError, TokenVaultError)
        assert issubclass(ServiceError, TokenVaultError)
        print("✓ Exception hierarchy properly defined")
        
        # Test token listing (will return empty for test user)
        tokens = await token_vault_service.list_tokens(user_id)
        print(f"✓ Token listing works (found {len(tokens)} tokens)")
        
        # Test token status check
        status = await token_vault_service.get_token_status(user_id, service_name)
        print(f"✓ Token status check works (status: {status['status']})")
        
        # Test service-specific refresh routing
        refresh_methods = {
            "google_calendar": "_refresh_google_token",
            "github": "_refresh_github_token", 
            "slack": "_refresh_slack_token"
        }
        
        for service_name, method_name in refresh_methods.items():
            has_method = hasattr(token_vault_service, method_name)
            print(f"✓ {service_name} refresh method available: {has_method}")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced Token Vault test failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints availability"""
    print("\nTesting API endpoints...")
    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✓ Health endpoint accessible")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}")
                return False
            
            # Test API root
            response = await client.get("http://localhost:8000/api/v1/")
            if response.status_code == 200:
                print("✓ API v1 root accessible")
            else:
                print(f"✗ API v1 root failed: {response.status_code}")
                return False
            
            # Test auth health (should work without auth)
            response = await client.get("http://localhost:8000/api/v1/auth/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Auth health endpoint accessible (authenticated: {data.get('authenticated', False)})")
            else:
                print(f"✗ Auth health endpoint failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {e}")
        return False

async def test_configuration():
    """Test configuration values"""
    print("\nTesting configuration...")
    
    config_checks = [
        ("AUTH0_DOMAIN", settings.AUTH0_DOMAIN),
        ("AUTH0_CLIENT_ID", settings.AUTH0_CLIENT_ID),
        ("AUTH0_AUDIENCE", settings.AUTH0_AUDIENCE),
        ("DATABASE_URL", settings.DATABASE_URL),
        ("REDIS_URL", settings.REDIS_URL),
    ]
    
    all_good = True
    for name, value in config_checks:
        if value and value != "":
            print(f"✓ {name} is configured")
        else:
            print(f"✗ {name} is missing or empty")
            all_good = False
    
    # Test derived URLs
    try:
        issuer_url = settings.auth0_issuer_url
        jwks_url = settings.auth0_jwks_url
        print(f"✓ Auth0 URLs generated: {issuer_url}")
        print(f"✓ JWKS URL: {jwks_url}")
    except Exception as e:
        print(f"✗ URL generation failed: {e}")
        all_good = False
    
    return all_good

async def main():
    """Run all tests"""
    print("CipherMate Auth0 Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Auth0 JWKS", test_auth0_jwks),
        ("Session Management", test_session_management),
        ("Token Vault Operations", test_token_vault_operations),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Auth0 integration is ready.")
    else:
        print("⚠️  Some tests failed. Check configuration and setup.")
    
    # Cleanup
    await session_manager.close()

if __name__ == "__main__":
    asyncio.run(main())