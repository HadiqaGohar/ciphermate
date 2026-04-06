"""Test script for permission management API endpoints"""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_user():
    """Create a mock authenticated user"""
    return {
        "sub": "auth0|test_user_123",
        "email": "test@example.com",
        "name": "Test User"
    }


def test_api_endpoints():
    """Test permission management API endpoints"""
    print("\n=== Testing Permission API Endpoints ===")
    
    try:
        client = TestClient(app)
        
        # Mock the authentication dependency
        from app.core.auth import get_current_user
        app.dependency_overrides[get_current_user] = lambda: create_mock_user()
        
        # Test 1: Get supported services
        print("Testing GET /api/v1/permissions/services...")
        response = client.get("/api/v1/permissions/services")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            services = data.get("services", {})
            print(f"✓ Found {len(services)} supported services: {list(services.keys())}")
        else:
            print(f"✗ Failed to get services: {response.text}")
            return False
        
        # Test 2: Get service scopes
        print("\nTesting GET /api/v1/permissions/scopes/google...")
        response = client.get("/api/v1/permissions/scopes/google")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            scopes = data.get("available_scopes", {})
            default_scopes = data.get("default_scopes", [])
            print(f"✓ Found {len(scopes)} available scopes, {len(default_scopes)} default scopes")
        else:
            print(f"✗ Failed to get Google scopes: {response.text}")
            return False
        
        # Test 3: Validate scopes
        print("\nTesting POST /api/v1/permissions/validate-scopes/google...")
        test_scopes = {
            "scopes": ["https://www.googleapis.com/auth/calendar.readonly"]
        }
        response = client.post("/api/v1/permissions/validate-scopes/google", json=test_scopes)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            validation = data.get("validation", {})
            print(f"✓ Scope validation completed: {validation.get('validation_passed', False)}")
        else:
            print(f"✗ Failed to validate scopes: {response.text}")
            return False
        
        # Test 4: List user permissions (should be empty initially)
        print("\nTesting GET /api/v1/permissions/list...")
        response = client.get("/api/v1/permissions/list")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            permissions = response.json()
            print(f"✓ Retrieved {len(permissions)} user permissions")
        else:
            print(f"✗ Failed to list permissions: {response.text}")
            return False
        
        # Test 5: Get permission status for a service
        print("\nTesting GET /api/v1/permissions/status/google...")
        response = client.get("/api/v1/permissions/status/google")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            has_permission = data.get("has_permission", False)
            print(f"✓ Google permission status: {status}, has_permission: {has_permission}")
        else:
            print(f"✗ Failed to get permission status: {response.text}")
            return False
        
        # Test 6: Get permission summary
        print("\nTesting GET /api/v1/permissions/summary...")
        response = client.get("/api/v1/permissions/summary")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            total_services = summary.get("total_services", 0)
            print(f"✓ Permission summary retrieved: {total_services} total services")
        else:
            print(f"✗ Failed to get permission summary: {response.text}")
            return False
        
        # Test 7: Initiate permission grant (should return authorization URL)
        print("\nTesting POST /api/v1/permissions/grant...")
        grant_request = {
            "service": "google"
        }
        response = client.post("/api/v1/permissions/grant", json=grant_request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            auth_url = data.get("authorization_url", "")
            state = data.get("state", "")
            print(f"✓ Authorization URL generated (length: {len(auth_url)})")
            print(f"✓ State parameter generated: {state[:20]}...")
        else:
            print(f"✗ Failed to initiate permission grant: {response.text}")
            return False
        
        # Test 8: Test invalid service
        print("\nTesting invalid service...")
        response = client.get("/api/v1/permissions/scopes/invalid_service")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✓ Invalid service properly rejected")
        else:
            print(f"✗ Invalid service should return 400, got {response.status_code}")
            return False
        
        print("\nAPI endpoints test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {e}")
        return False
    finally:
        # Clean up dependency overrides
        app.dependency_overrides.clear()


def test_error_handling():
    """Test error handling in API endpoints"""
    print("\n=== Testing Error Handling ===")
    
    try:
        client = TestClient(app)
        
        # Test without authentication (should fail)
        print("Testing unauthenticated request...")
        response = client.get("/api/v1/permissions/services")
        print(f"Status: {response.status_code}")
        
        if response.status_code in [401, 403]:
            print("✓ Unauthenticated request properly rejected")
        else:
            print(f"✗ Expected 401/403, got {response.status_code}")
            return False
        
        # Add mock authentication for remaining tests
        from app.core.auth import get_current_user
        app.dependency_overrides[get_current_user] = lambda: create_mock_user()
        
        # Test invalid JSON
        print("\nTesting invalid JSON in scope validation...")
        response = client.post("/api/v1/permissions/validate-scopes/google", json={"invalid": "data"})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✓ Invalid JSON properly handled")
        else:
            print(f"✗ Expected 400, got {response.status_code}")
            return False
        
        print("Error handling test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False
    finally:
        # Clean up dependency overrides
        app.dependency_overrides.clear()


def main():
    """Run all API tests"""
    print("Starting Permission Management API Tests...")
    print("=" * 50)
    
    tests = [
        ("API Endpoints", test_api_endpoints),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("API TEST SUMMARY")
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
        print("🎉 All API tests passed! Permission management API is ready.")
        return True
    else:
        print("⚠ Some API tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)