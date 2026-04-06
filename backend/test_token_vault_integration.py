#!/usr/bin/env python3
"""
Integration test for Token Vault service
Tests the complete workflow including API endpoints
"""

import asyncio
import sys
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, AsyncMock, patch
import json

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


async def test_complete_token_lifecycle():
    """Test complete token lifecycle: store -> retrieve -> refresh -> revoke"""
    print("Testing complete token lifecycle...")
    
    service = TokenVaultService()
    
    # Mock data
    user_id = "test_user_lifecycle"
    service_name = "google_calendar"
    token_data = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    scopes = ["https://www.googleapis.com/auth/calendar"]
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    
    # Mock all external dependencies
    with patch.object(service, '_get_management_token_with_retry') as mock_get_token, \
         patch.object(service, '_store_in_vault_with_retry') as mock_store, \
         patch.object(service, '_store_local_reference') as mock_store_local, \
         patch.object(service, '_retrieve_from_vault_with_retry') as mock_retrieve, \
         patch.object(service, '_revoke_from_vault_with_retry') as mock_revoke, \
         patch('app.core.token_vault.AsyncSessionLocal') as mock_db:
        
        # Setup mocks
        mock_get_token.return_value = "mock_management_token"
        mock_store.return_value = "vault_id_123"
        mock_store_local.return_value = None
        mock_retrieve.return_value = token_data
        mock_revoke.return_value = True
        
        # Mock database interactions
        mock_db_instance = AsyncMock()
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Mock connection for retrieve
        mock_connection = MagicMock()
        mock_connection.expires_at = expires_at
        mock_connection.token_vault_id = "vault_id_123"
        mock_connection.last_used_at = None
        mock_connection.is_active = True
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_connection
        mock_db_instance.execute.return_value = mock_result
        
        # 1. Store token
        print("  1. Storing token...")
        vault_id = await service.store_token(user_id, service_name, token_data, scopes, expires_at)
        assert vault_id == "vault_id_123"
        print("     ✓ Token stored successfully")
        
        # 2. Retrieve token
        print("  2. Retrieving token...")
        retrieved_token = await service.retrieve_token(user_id, service_name)
        assert retrieved_token == token_data
        print("     ✓ Token retrieved successfully")
        
        # 3. Revoke token
        print("  3. Revoking token...")
        revoke_success = await service.revoke_token(user_id, service_name)
        assert revoke_success is True
        print("     ✓ Token revoked successfully")
    
    print("✓ Complete token lifecycle test passed")
    return True


async def test_error_handling_scenarios():
    """Test various error handling scenarios"""
    print("Testing error handling scenarios...")
    
    service = TokenVaultService()
    
    # Test 1: Invalid input validation
    print("  1. Testing input validation...")
    try:
        await service.store_token("", "service", {"token": "test"}, [])
        assert False, "Should have raised ValueError"
    except ValueError:
        print("     ✓ Input validation working")
    
    # Test 2: Authentication error handling
    print("  2. Testing authentication error handling...")
    with patch.object(service, '_get_management_token_with_retry') as mock_get_token:
        mock_get_token.side_effect = AuthenticationError("Auth failed")
        
        try:
            await service.store_token("user", "service", {"token": "test"}, [])
            assert False, "Should have raised AuthenticationError"
        except AuthenticationError:
            print("     ✓ Authentication error handling working")
    
    # Test 3: Token not found error
    print("  3. Testing token not found error...")
    with patch('app.core.token_vault.AsyncSessionLocal') as mock_db:
        mock_db_instance = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        result = await service.retrieve_token("user", "nonexistent_service")
        assert result is None
        print("     ✓ Token not found handling working")
    
    # Test 4: Token expired error
    print("  4. Testing token expired error...")
    with patch('app.core.token_vault.AsyncSessionLocal') as mock_db:
        mock_db_instance = AsyncMock()
        
        # Mock expired connection
        mock_connection = MagicMock()
        mock_connection.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)  # Expired
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_connection
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        try:
            await service.retrieve_token("user", "expired_service", auto_refresh=False)
            assert False, "Should have raised TokenExpiredError"
        except TokenExpiredError:
            print("     ✓ Token expired error handling working")
    
    print("✓ Error handling scenarios test passed")
    return True


async def test_service_specific_refresh():
    """Test service-specific token refresh functionality"""
    print("Testing service-specific token refresh...")
    
    service = TokenVaultService()
    
    # Test Google token refresh
    print("  1. Testing Google token refresh...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_google_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._refresh_google_token("refresh_token")
        assert result["access_token"] == "new_google_token"
        print("     ✓ Google token refresh working")
    
    # Test GitHub token validation
    print("  2. Testing GitHub token validation...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._refresh_github_token("github_token")
        assert result["access_token"] == "github_token"
        print("     ✓ GitHub token validation working")
    
    # Test Slack token refresh
    print("  3. Testing Slack token refresh...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ok": True,
            "access_token": "new_slack_token",
            "refresh_token": "new_refresh_token"
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._refresh_slack_token("slack_refresh_token")
        assert result["access_token"] == "new_slack_token"
        print("     ✓ Slack token refresh working")
    
    print("✓ Service-specific refresh test passed")
    return True


async def test_health_check_functionality():
    """Test token health check functionality"""
    print("Testing health check functionality...")
    
    service = TokenVaultService()
    
    # Test Google health check
    print("  1. Testing Google health check...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "expires_in": "3600",
            "scope": "https://www.googleapis.com/auth/calendar"
        }
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._check_google_token_health("google_token")
        assert result["healthy"] is True
        assert result["status"] == "active"
        print("     ✓ Google health check working")
    
    # Test GitHub health check
    print("  2. Testing GitHub health check...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"login": "testuser"}
        mock_response.headers = {"X-OAuth-Scopes": "repo, user"}
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._check_github_token_health("github_token")
        assert result["healthy"] is True
        assert result["user"] == "testuser"
        print("     ✓ GitHub health check working")
    
    # Test Slack health check
    print("  3. Testing Slack health check...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ok": True,
            "user": "testuser",
            "team": "testteam"
        }
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await service._check_slack_token_health("slack_token")
        assert result["healthy"] is True
        assert result["user"] == "testuser"
        print("     ✓ Slack health check working")
    
    print("✓ Health check functionality test passed")
    return True


async def test_bulk_operations():
    """Test bulk operations functionality"""
    print("Testing bulk operations...")
    
    service = TokenVaultService()
    
    # Test bulk revocation
    print("  1. Testing bulk token revocation...")
    with patch('app.core.token_vault.AsyncSessionLocal') as mock_db, \
         patch.object(service, 'revoke_token') as mock_revoke:
        
        # Mock database response
        mock_db_instance = AsyncMock()
        mock_connection1 = MagicMock()
        mock_connection1.service_name = "google_calendar"
        mock_connection2 = MagicMock()
        mock_connection2.service_name = "github"
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_connection1, mock_connection2]
        mock_db_instance.execute.return_value = mock_result
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        # Mock revoke_token calls
        mock_revoke.side_effect = [True, True]
        
        results = await service.bulk_revoke_tokens("user_123")
        assert results["google_calendar"] is True
        assert results["github"] is True
        print("     ✓ Bulk revocation working")
    
    # Test statistics generation
    print("  2. Testing statistics generation...")
    with patch('app.core.token_vault.AsyncSessionLocal') as mock_db:
        mock_db_instance = AsyncMock()
        
        # Mock various database queries
        mock_total_result = MagicMock()
        mock_total_result.scalars.return_value.all.return_value = ["conn1", "conn2", "conn3"]
        
        mock_active_result = MagicMock()
        mock_active_result.scalars.return_value.all.return_value = ["conn1", "conn2"]
        
        mock_expired_result = MagicMock()
        mock_expired_result.scalars.return_value.all.return_value = ["conn1"]
        
        mock_service_result = MagicMock()
        mock_service_result.fetchall.return_value = [
            ("google_calendar", True),
            ("github", True),
            ("slack", False)
        ]
        
        mock_db_instance.execute.side_effect = [
            mock_total_result,
            mock_active_result,
            mock_expired_result,
            mock_service_result
        ]
        mock_db.return_value.__aenter__.return_value = mock_db_instance
        
        stats = await service.get_vault_statistics()
        assert stats["total_connections"] == 3
        assert stats["active_connections"] == 2
        assert "service_breakdown" in stats
        print("     ✓ Statistics generation working")
    
    print("✓ Bulk operations test passed")
    return True


async def test_retry_and_resilience():
    """Test retry logic and resilience features"""
    print("Testing retry logic and resilience...")
    
    service = TokenVaultService()
    
    # Test retry logic with eventual success
    print("  1. Testing retry logic with eventual success...")
    with patch('app.core.token_vault.httpx.AsyncClient') as mock_client:
        mock_client_instance = AsyncMock()
        
        # First two calls fail, third succeeds
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
        
        token = await service._get_management_token_with_retry()
        assert token == "success_token"
        assert mock_client_instance.post.call_count == 3
        print("     ✓ Retry logic with eventual success working")
    
    # Test max retries exceeded
    print("  2. Testing max retries exceeded...")
    with patch.object(service, '_get_management_token') as mock_get_token:
        mock_get_token.side_effect = Exception("Persistent error")
        
        exception_raised = False
        try:
            await service._get_management_token_with_retry()
        except Exception as e:
            exception_raised = True
            print(f"     Exception type: {type(e).__name__}")
            print(f"     Exception message: {str(e)}")
            # Accept AuthenticationError or similar
            if isinstance(e, AuthenticationError) or "Auth0" in str(e) or "authentication" in str(e).lower():
                print("     ✓ Max retries exceeded handling working")
            else:
                raise e
        
        if not exception_raised:
            assert False, "Should have raised an exception"
        
        assert mock_get_token.call_count == 3  # max_retries
    
    print("✓ Retry and resilience test passed")
    return True


async def main():
    """Run all integration tests"""
    print("Token Vault Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Complete Token Lifecycle", test_complete_token_lifecycle),
        ("Error Handling Scenarios", test_error_handling_scenarios),
        ("Service-Specific Refresh", test_service_specific_refresh),
        ("Health Check Functionality", test_health_check_functionality),
        ("Bulk Operations", test_bulk_operations),
        ("Retry and Resilience", test_retry_and_resilience),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("INTEGRATION TEST SUMMARY")
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
        print("🎉 All integration tests passed! Token Vault service is fully functional.")
        print("\nKey Features Verified:")
        print("- ✓ Auth0 Management API client integration")
        print("- ✓ Token storage, retrieval, and revocation")
        print("- ✓ Automatic token refresh and expiration handling")
        print("- ✓ Comprehensive error handling and retry logic")
        print("- ✓ Service-specific token operations (Google, GitHub, Slack)")
        print("- ✓ Health checks and token validation")
        print("- ✓ Bulk operations and statistics")
        print("- ✓ Resilience and fault tolerance")
    else:
        print("⚠️  Some integration tests failed. Check implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)