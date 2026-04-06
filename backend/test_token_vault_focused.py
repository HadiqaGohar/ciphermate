#!/usr/bin/env python3
"""
Focused test for Token Vault service functionality
Tests core functionality without external dependencies
"""

import asyncio
import sys
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, AsyncMock, patch

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.token_vault import (
    TokenVaultService,
    TokenVaultError,
    TokenNotFoundError,
    TokenExpiredError,
    AuthenticationError,
    ServiceError,
    TokenStatus
)


async def test_token_vault_initialization():
    """Test TokenVaultService initialization"""
    print("Testing TokenVaultService initialization...")
    
    service = TokenVaultService()
    
    # Check initialization values
    assert service._max_retries == 3, "Max retries should be 3"
    assert service._retry_delay == 1.0, "Retry delay should be 1.0 seconds"
    assert service._management_token_cache is None, "Token cache should be None initially"
    assert service._management_token_expires is None, "Token expiration should be None initially"
    
    print("✓ TokenVaultService initialized correctly")
    return True


async def test_input_validation():
    """Test input validation for all methods"""
    print("Testing input validation...")
    
    service = TokenVaultService()
    
    # Test store_token validation
    try:
        await service.store_token("", "service", {"token": "test"}, [])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id, service_name, and token_data are required" in str(e)
    
    try:
        await service.store_token("user", "", {"token": "test"}, [])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id, service_name, and token_data are required" in str(e)
    
    try:
        await service.store_token("user", "service", {}, [])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id, service_name, and token_data are required" in str(e)
    
    # Test retrieve_token validation
    try:
        await service.retrieve_token("", "service")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id and service_name are required" in str(e)
    
    try:
        await service.retrieve_token("user", "")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id and service_name are required" in str(e)
    
    # Test revoke_token validation
    try:
        await service.revoke_token("", "service")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id and service_name are required" in str(e)
    
    try:
        await service.revoke_token("user", "")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id and service_name are required" in str(e)
    
    print("✓ Input validation working correctly")
    return True


async def test_exception_hierarchy():
    """Test exception class hierarchy"""
    print("Testing exception hierarchy...")
    
    # Test inheritance
    assert issubclass(TokenNotFoundError, TokenVaultError), "TokenNotFoundError should inherit from TokenVaultError"
    assert issubclass(TokenExpiredError, TokenVaultError), "TokenExpiredError should inherit from TokenVaultError"
    assert issubclass(AuthenticationError, TokenVaultError), "AuthenticationError should inherit from TokenVaultError"
    assert issubclass(ServiceError, TokenVaultError), "ServiceError should inherit from TokenVaultError"
    
    # Test exception instantiation
    base_error = TokenVaultError("Base error")
    assert str(base_error) == "Base error"
    
    not_found_error = TokenNotFoundError("Token not found")
    assert str(not_found_error) == "Token not found"
    
    expired_error = TokenExpiredError("Token expired")
    assert str(expired_error) == "Token expired"
    
    auth_error = AuthenticationError("Auth failed")
    assert str(auth_error) == "Auth failed"
    
    service_error = ServiceError("Service error")
    assert str(service_error) == "Service error"
    
    print("✓ Exception hierarchy properly defined")
    return True


async def test_token_status_enum():
    """Test TokenStatus enum"""
    print("Testing TokenStatus enum...")
    
    assert TokenStatus.ACTIVE.value == "active"
    assert TokenStatus.EXPIRED.value == "expired"
    assert TokenStatus.REVOKED.value == "revoked"
    assert TokenStatus.REFRESH_FAILED.value == "refresh_failed"
    
    print("✓ TokenStatus enum values correct")
    return True


async def test_service_specific_refresh_routing():
    """Test that service-specific refresh methods exist"""
    print("Testing service-specific refresh method routing...")
    
    service = TokenVaultService()
    
    # Check that service-specific refresh methods exist
    refresh_methods = {
        "google_calendar": "_refresh_google_token",
        "github": "_refresh_github_token",
        "slack": "_refresh_slack_token"
    }
    
    for service_name, method_name in refresh_methods.items():
        has_method = hasattr(service, method_name)
        assert has_method, f"Method {method_name} should exist for {service_name}"
        
        # Check that method is callable
        method = getattr(service, method_name)
        assert callable(method), f"Method {method_name} should be callable"
    
    print("✓ Service-specific refresh methods available")
    return True


async def test_health_check_methods():
    """Test that health check methods exist"""
    print("Testing health check methods...")
    
    service = TokenVaultService()
    
    # Check that health check methods exist
    health_methods = [
        "_check_google_token_health",
        "_check_github_token_health", 
        "_check_slack_token_health",
        "_perform_health_check",
        "validate_token_health"
    ]
    
    for method_name in health_methods:
        has_method = hasattr(service, method_name)
        assert has_method, f"Method {method_name} should exist"
        
        # Check that method is callable
        method = getattr(service, method_name)
        assert callable(method), f"Method {method_name} should be callable"
    
    print("✓ Health check methods available")
    return True


async def test_bulk_operations():
    """Test that bulk operation methods exist"""
    print("Testing bulk operation methods...")
    
    service = TokenVaultService()
    
    # Check that bulk operation methods exist
    bulk_methods = [
        "bulk_revoke_tokens",
        "cleanup_expired_tokens",
        "get_vault_statistics"
    ]
    
    for method_name in bulk_methods:
        has_method = hasattr(service, method_name)
        assert has_method, f"Method {method_name} should exist"
        
        # Check that method is callable
        method = getattr(service, method_name)
        assert callable(method), f"Method {method_name} should be callable"
    
    print("✓ Bulk operation methods available")
    return True


@patch('app.core.token_vault.httpx.AsyncClient')
async def test_management_token_caching(mock_client):
    """Test management token caching mechanism"""
    print("Testing management token caching...")
    
    service = TokenVaultService()
    
    # Mock successful token response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "mock_management_token",
        "expires_in": 3600
    }
    mock_response.raise_for_status = MagicMock()
    
    mock_client_instance = AsyncMock()
    mock_client_instance.post.return_value = mock_response
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    # First call should make HTTP request
    token1 = await service._get_management_token()
    assert token1 == "mock_management_token"
    assert mock_client_instance.post.call_count == 1
    
    # Second call should use cache
    token2 = await service._get_management_token()
    assert token2 == "mock_management_token"
    assert mock_client_instance.post.call_count == 1  # No additional calls
    
    # Verify cache is set
    assert service._management_token_cache == "mock_management_token"
    assert service._management_token_expires is not None
    
    print("✓ Management token caching working correctly")
    return True


@patch('app.core.token_vault.httpx.AsyncClient')
async def test_retry_logic(mock_client):
    """Test retry logic for management token acquisition"""
    print("Testing retry logic...")
    
    service = TokenVaultService()
    
    # Mock client that fails twice then succeeds
    mock_client_instance = AsyncMock()
    mock_client_instance.post.side_effect = [
        Exception("Network error"),
        Exception("Timeout error"),
        MagicMock(
            status_code=200,
            json=lambda: {"access_token": "success_token", "expires_in": 3600},
            raise_for_status=MagicMock()
        )
    ]
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    # Should succeed after retries
    token = await service._get_management_token_with_retry()
    assert token == "success_token"
    assert mock_client_instance.post.call_count == 3
    
    print("✓ Retry logic working correctly")
    return True


@patch('app.core.token_vault.httpx.AsyncClient')
async def test_max_retries_exceeded(mock_client):
    """Test behavior when max retries are exceeded"""
    print("Testing max retries exceeded...")
    
    service = TokenVaultService()
    
    # Mock client that always fails
    mock_client_instance = AsyncMock()
    mock_client_instance.post.side_effect = Exception("Persistent error")
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    # Should raise AuthenticationError after max retries
    try:
        await service._get_management_token_with_retry()
        assert False, "Should have raised AuthenticationError"
    except AuthenticationError as e:
        assert "Unable to authenticate with Auth0" in str(e)
    
    assert mock_client_instance.post.call_count == 3  # max_retries
    
    print("✓ Max retries exceeded handling working correctly")
    return True


async def main():
    """Run all focused tests"""
    print("Token Vault Service Focused Test Suite")
    print("=" * 50)
    
    tests = [
        ("Initialization", test_token_vault_initialization),
        ("Input Validation", test_input_validation),
        ("Exception Hierarchy", test_exception_hierarchy),
        ("Token Status Enum", test_token_status_enum),
        ("Service-Specific Refresh Routing", test_service_specific_refresh_routing),
        ("Health Check Methods", test_health_check_methods),
        ("Bulk Operations", test_bulk_operations),
        ("Management Token Caching", test_management_token_caching),
        ("Retry Logic", test_retry_logic),
        ("Max Retries Exceeded", test_max_retries_exceeded),
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
        print("🎉 All focused tests passed! Token Vault service is properly implemented.")
    else:
        print("⚠️  Some tests failed. Check implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)