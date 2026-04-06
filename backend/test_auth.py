"""
Simple test script to verify Auth0 authentication setup
"""
import asyncio
import httpx
from app.core.config import settings
from app.core.auth import auth0_jwt_bearer
from app.core.session import session_manager
from app.core.token_vault import token_vault_service

async def test_auth0_config():
    """Test Auth0 configuration"""
    print("Testing Auth0 Configuration...")
    
    # Check if Auth0 settings are configured
    if not settings.AUTH0_DOMAIN:
        print("❌ AUTH0_DOMAIN not configured")
        return False
    
    if not settings.AUTH0_CLIENT_ID:
        print("❌ AUTH0_CLIENT_ID not configured")
        return False
    
    if not settings.AUTH0_CLIENT_SECRET:
        print("❌ AUTH0_CLIENT_SECRET not configured")
        return False
    
    print(f"✅ Auth0 Domain: {settings.AUTH0_DOMAIN}")
    print(f"✅ Auth0 Client ID: {settings.AUTH0_CLIENT_ID[:8]}...")
    print(f"✅ Auth0 Audience: {settings.AUTH0_AUDIENCE}")
    
    return True

async def test_jwks_endpoint():
    """Test JWKS endpoint accessibility"""
    print("\nTesting JWKS Endpoint...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.auth0_jwks_url)
            response.raise_for_status()
            jwks = response.json()
            
            if "keys" in jwks and len(jwks["keys"]) > 0:
                print(f"✅ JWKS endpoint accessible with {len(jwks['keys'])} keys")
                return True
            else:
                print("❌ JWKS endpoint returned no keys")
                return False
                
    except Exception as e:
        print(f"❌ JWKS endpoint error: {e}")
        return False

async def test_redis_connection():
    """Test Redis connection"""
    print("\nTesting Redis Connection...")
    
    try:
        client = await session_manager.get_redis_client()
        await client.ping()
        print("✅ Redis connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        return False

async def test_management_api():
    """Test Auth0 Management API token acquisition"""
    print("\nTesting Auth0 Management API...")
    
    try:
        token = await token_vault_service.get_management_token()
        if token:
            print("✅ Management API token acquired successfully")
            return True
        else:
            print("❌ Failed to acquire Management API token")
            return False
            
    except Exception as e:
        print(f"❌ Management API error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔐 CipherMate Auth0 Integration Test\n")
    
    tests = [
        test_auth0_config,
        test_jwks_endpoint,
        test_redis_connection,
        test_management_api
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Auth0 integration is ready.")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        print("\nNext steps:")
        print("1. Set up your Auth0 tenant and configure Token Vault")
        print("2. Update your .env file with correct Auth0 credentials")
        print("3. Ensure Redis is running")
        print("4. Verify your Auth0 application settings")

if __name__ == "__main__":
    asyncio.run(main())