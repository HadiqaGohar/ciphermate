#!/usr/bin/env python3
"""
Test Gmail authentication flow
"""

import requests
import json

def test_gmail_status():
    """Test Gmail configuration status"""
    print("🔍 Testing Gmail Status...")
    
    try:
        response = requests.get("http://localhost:8080/api/v1/gmail/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Gmail Status:")
            for key, value in data.items():
                status = "✅" if value else "❌"
                print(f"   {key}: {status} {value}")
            return data
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_auth_url():
    """Get Gmail authentication URL"""
    print("\n🔐 Getting Gmail Auth URL...")
    
    try:
        # This would normally redirect to Google, but we'll catch the redirect
        response = requests.get("http://localhost:8080/api/auth/gmail/login", allow_redirects=False)
        if response.status_code == 307:  # Redirect
            auth_url = response.headers.get('location')
            print(f"✅ Auth URL: {auth_url[:100]}...")
            return auth_url
        else:
            print(f"❌ Auth URL failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🧪 Gmail Authentication Test")
    print("=" * 50)
    
    # Test status
    status = test_gmail_status()
    if not status:
        print("❌ Gmail not configured properly")
        return
    
    if status.get('ready_to_send'):
        print("🎉 Gmail is ready to send emails!")
        return
    
    if not status.get('token_available'):
        print("\n⚠️ Gmail authentication required")
        print("To authenticate:")
        print("1. Open browser to: http://localhost:8080/api/auth/gmail/login")
        print("2. Complete Google OAuth flow")
        print("3. Grant permission to send emails")
        print("4. Return to test email sending")
        
        # Try to get auth URL
        auth_url = get_auth_url()
        if auth_url:
            print(f"\n🔗 Direct auth URL: {auth_url}")

if __name__ == "__main__":
    main()