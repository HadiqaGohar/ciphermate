#!/usr/bin/env python3
"""
Slack OAuth Configuration Test for CipherMate AI

This script helps you test and configure Slack OAuth integration.
"""

import os
import sys
from urllib.parse import urlencode

# Add backend to path
sys.path.append('./backend')

from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

def main():
    print("🔧 Slack OAuth Configuration Helper")
    print("=" * 50)
    
    # Get configuration
    client_id = os.getenv('SLACK_CLIENT_ID')
    client_secret = os.getenv('SLACK_CLIENT_SECRET')
    app_env = os.getenv('APP_ENV', 'development')
    app_base_url = os.getenv('APP_BASE_URL', 'http://localhost:8080')
    
    print(f"📋 Current Configuration:")
    print(f"   Environment: {app_env}")
    print(f"   Base URL: {app_base_url}")
    print(f"   Client ID: {client_id[:20]}..." if client_id else "   Client ID: Not configured")
    print(f"   Client Secret: {'✅ Configured' if client_secret else '❌ Not configured'}")
    
    # Determine redirect URI
    if app_env == "production":
        redirect_uri = f"{app_base_url}/api/auth/slack/callback"
    else:
        redirect_uri = "https://localhost:3000/api/auth/slack/callback"
    
    print(f"\n🔗 Required Redirect URI for Slack App:")
    print(f"   {redirect_uri}")
    
    print(f"\n📋 Slack App Configuration Steps:")
    print(f"1. Go to: https://api.slack.com/apps")
    print(f"2. Select your CipherMate app")
    print(f"3. Go to 'OAuth & Permissions'")
    print(f"4. Add this Redirect URL:")
    print(f"   {redirect_uri}")
    print(f"5. Make sure Bot Token Scopes include:")
    print(f"   - chat:write")
    print(f"   - channels:read")
    print(f"6. Install/Reinstall to Workspace")
    
    # Generate test OAuth URL
    if client_id:
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "chat:write,channels:read",
            "state": "test_state_123"
        }
        oauth_url = f"https://slack.com/oauth/v2/authorize?{urlencode(params)}"
        
        print(f"\n🧪 Test OAuth URL:")
        print(f"   {oauth_url}")
        print(f"\n   Copy this URL to test the OAuth flow!")
    else:
        print(f"\n❌ Cannot generate test URL - SLACK_CLIENT_ID not configured")
    
    print(f"\n✨ After configuration, test with:")
    print(f"   python3 test_slack_integration.py")

if __name__ == "__main__":
    main()