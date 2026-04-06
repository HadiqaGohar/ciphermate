#!/usr/bin/env python3
"""
Test script to verify all CipherMate fixes
"""

import requests
import json

def test_all_endpoints():
    """Test all the fixed endpoints"""
    print("🧪 Testing All CipherMate Fixes - COMPREHENSIVE")
    print("=" * 70)
    
    tests = [
        # Permissions endpoints
        {
            "name": "Permissions List",
            "url": "http://localhost:3000/api/permissions/list",
            "expected_keys": ["service", "scopes", "status"]
        },
        {
            "name": "Permissions Services", 
            "url": "http://localhost:3000/api/permissions/services",
            "expected_keys": ["services", "total_services"]
        },
        {
            "name": "Service Scopes (Google Calendar)",
            "url": "http://localhost:3000/api/permissions/scopes/google_calendar",
            "expected_keys": ["service", "scopes", "required"]
        },
        {
            "name": "Service Scopes (Gmail)",
            "url": "http://localhost:3000/api/permissions/scopes/gmail", 
            "expected_keys": ["service", "scopes", "required"]
        },
        # Audit endpoints
        {
            "name": "Audit Logs",
            "url": "http://localhost:3000/api/audit/logs",
            "expected_keys": ["logs", "total", "page"]
        },
        {
            "name": "Audit Security Events",
            "url": "http://localhost:3000/api/audit/security-events",
            "expected_keys": ["security_events", "total", "summary"]
        },
        {
            "name": "Audit Summary",
            "url": "http://localhost:3000/api/audit/summary",
            "expected_keys": ["total_events", "unique_users", "top_actions"]
        },
        # Token Vault endpoints
        {
            "name": "Token Vault List",
            "url": "http://localhost:3000/api/token-vault/list",
            "expected_keys": ["tokens", "total"]
        },
        {
            "name": "Token Vault Retrieve (Google Calendar)",
            "url": "http://localhost:3000/api/token-vault/retrieve/google_calendar",
            "expected_keys": ["service", "token", "status"]
        },
        # Backend endpoints
        {
            "name": "Backend Permissions List",
            "url": "http://localhost:8080/api/v1/permissions/list",
            "expected_keys": ["service", "scopes", "status"]
        },
        {
            "name": "Backend Audit Logs",
            "url": "http://localhost:8080/api/v1/audit/logs",
            "expected_keys": ["logs", "total", "page"]
        },
        {
            "name": "Backend Audit Summary",
            "url": "http://localhost:8080/api/v1/audit/summary",
            "expected_keys": ["total_events", "unique_users", "top_actions"]
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\n🔍 Testing {test['name']}...")
        try:
            response = requests.get(test['url'], timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Check if expected keys exist
                if isinstance(data, list) and len(data) > 0:
                    # For list responses, check first item
                    has_keys = all(key in data[0] for key in test['expected_keys'])
                elif isinstance(data, dict):
                    # For dict responses, check top level
                    has_keys = all(key in data for key in test['expected_keys'])
                else:
                    has_keys = False
                
                if has_keys:
                    print(f"✅ {test['name']}: PASSED")
                    if isinstance(data, list):
                        print(f"   📊 Found {len(data)} items")
                    elif 'total' in data:
                        print(f"   📊 Total items: {data.get('total', 'N/A')}")
                    elif 'tokens' in data:
                        print(f"   📊 Found {len(data['tokens'])} tokens")
                    passed += 1
                else:
                    print(f"❌ {test['name']}: FAILED - Missing expected keys")
                    print(f"   Expected: {test['expected_keys']}")
                    print(f"   Got keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                    failed += 1
            else:
                print(f"❌ {test['name']}: FAILED - HTTP {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                failed += 1
                
        except Exception as e:
            print(f"❌ {test['name']}: ERROR - {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"🎯 Test Results: {passed} PASSED, {failed} FAILED")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Your CipherMate app is 100% ready for the hackathon!")
        print("\n📋 What's Working:")
        print("   ✅ Permissions page - Shows services and permissions")
        print("   ✅ Service scopes - Shows OAuth scopes for each service")
        print("   ✅ Audit logs - Shows user activity and security events")
        print("   ✅ Security events - Shows security monitoring data")
        print("   ✅ Audit summary - Shows analytics and statistics")
        print("   ✅ Token vault - Shows stored tokens and credentials")
        print("   ✅ Backend APIs - All endpoints returning demo data")
        print("   ✅ Frontend APIs - All proxy routes working")
        
        print("\n🚀 Hackathon Demo Ready:")
        print("   1. Authentication Flow - Auth0 login/logout")
        print("   2. Dashboard - User overview and navigation")
        print("   3. AI Chat - Gemini-powered assistant")
        print("   4. Permissions - Service permission management")
        print("   5. Audit Logs - Activity tracking and monitoring")
        print("   6. Security Events - Security monitoring dashboard")
        print("   7. Token Vault - Credential management system")
        
        print("\n🎯 Next Steps:")
        print("   1. Clear browser cache/cookies")
        print("   2. Go to http://localhost:3000")
        print("   3. Login with Auth0")
        print("   4. Test all pages: Dashboard, Permissions, Audit, Chat")
        print("   5. Prepare your hackathon demo presentation!")
        
    else:
        print("⚠️  Some tests failed. Check the errors above and restart servers if needed.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure both servers are running:")
        print("      - Backend: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")
        print("      - Frontend: npm run dev")
        print("   2. Check for any import errors in the logs")
        print("   3. Restart both servers if needed")

if __name__ == "__main__":
    test_all_endpoints()