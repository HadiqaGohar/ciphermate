#!/usr/bin/env python3
"""
Slack App Setup Verification Script
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

def main():
    print("🔧 Slack App Setup Verification")
    print("=" * 50)
    
    client_id = os.getenv('SLACK_CLIENT_ID')
    client_secret = os.getenv('SLACK_CLIENT_SECRET')
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    
    print("📋 Current Configuration:")
    print(f"   ✅ Client ID: {client_id[:20]}..." if client_id else "   ❌ Client ID: Missing")
    print(f"   ✅ Client Secret: Configured" if client_secret else "   ❌ Client Secret: Missing")
    print(f"   ✅ Bot Token: Configured" if bot_token and bot_token != 'xoxb-your-bot-token-here' else "   ❌ Bot Token: Missing or placeholder")
    
    print(f"\n🤖 Bot User Setup Checklist:")
    print(f"□ 1. Go to https://api.slack.com/apps")
    print(f"□ 2. Select your CipherMate app")
    print(f"□ 3. Click 'Bot Users' → 'Add a Bot User'")
    print(f"□ 4. Set Display Name: 'CipherMate AI'")
    print(f"□ 5. Set Username: 'ciphermate'")
    print(f"□ 6. Click 'Add Bot User'")
    
    print(f"\n🔐 OAuth & Permissions Setup:")
    print(f"□ 1. Go to 'OAuth & Permissions'")
    print(f"□ 2. Add Bot Token Scopes:")
    print(f"     - channels:read")
    print(f"     - chat:write")
    print(f"□ 3. Add Redirect URL:")
    print(f"     https://cipheremate-31299921364.europe-west1.run.app/api/auth/slack/callback")
    print(f"□ 4. Click 'Install to Workspace'")
    print(f"□ 5. Copy 'Bot User OAuth Token' to .env as SLACK_BOT_TOKEN")
    
    if bot_token and bot_token != 'xoxb-your-bot-token-here':
        print(f"\n✅ Ready to test! Run: python3 test_slack_integration.py")
    else:
        print(f"\n⚠️  Complete the setup above, then update your .env file:")
        print(f"   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token-here")

if __name__ == "__main__":
    main()