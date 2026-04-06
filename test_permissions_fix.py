#!/usr/bin/env python3
"""
Test script to verify the permissions API fix
"""

import requests
import json

def test_permissions_api():
    """Test the permissions API endpoints"""
    base_url = "http://localhost:8080/api/v1/permissions"
    
    print("🧪 Testing CipherMate Permissions API Fix")
    print("=" * 50)
    
    # Test services endpoint
    print("\n1. Testing /services endpoint...")
    try:
        response = requests.get(f"{base_url}/services")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Services endpoint working! Found {data['total_services']} services")
            for service_id, service_info in data['services'].items():
                print(f"   - {service_info['name']}: {len(service_info['default_scopes'])} scopes")
        else:
            print(f"❌ Services endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Services endpoint error: {e}")
    
    # Test list endpoint
    print("\n2. Testing /list endpoint...")
    try:
        response = requests.get(f"{base_url}/list")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ List endpoint working! Found {len(data)} permissions")
            for perm in data:
                print(f"   - {perm['service']}: {perm['status']} ({len(perm['scopes'])} scopes)")
        else:
            print(f"❌ List endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ List endpoint error: {e}")
    
    # Test frontend API route
    print("\n3. Testing frontend API route...")
    try:
        response = requests.get("http://localhost:3000/api/permissions/list")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Frontend API route working! Data received successfully")
        else:
            print(f"❌ Frontend API route failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Frontend API route error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed! If all endpoints show ✅, the fix is working!")
    print("\nNext steps:")
    print("1. Clear your browser cache/cookies")
    print("2. Go to http://localhost:3000")
    print("3. Login and navigate to permissions page")
    print("4. You should see the permissions data instead of errors!")

if __name__ == "__main__":
    test_permissions_api()