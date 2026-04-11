#!/usr/bin/env python3
"""
Quick Slack Scopes Checker
"""

import asyncio
import os
import sys
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

async def check_scopes():
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not found in .env")
        return
    
    print("🔐 Checking Slack Bot Scopes...")
    print("=" * 40)
    
    headers = {
        'Authorization': f'Bearer {bot_token}',
        'Content-Type': 'application/json'
    }
    
    # Test different API endpoints to check scopes
    tests = [
        ("auth.test", "Basic bot info"),
        ("conversations.list", "List channels"),
        ("users.list", "List users"),
        ("conversations.join", "Join channels (POST test)"),
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint, description in tests:
            try:
                if endpoint == "conversations.join":
                    # Skip POST test for now
                    print(f"⏭️  {endpoint}: {description} (Skipped - requires channel ID)")
                    continue
                
                async with session.get(f"https://slack.com/api/{endpoint}", headers=headers) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        print(f"✅ {endpoint}: {description}")
                    else:
                        error = data.get('error', 'Unknown error')
                        print(f"❌ {endpoint}: {description} - {error}")
                        
            except Exception as e:
                print(f"❌ {endpoint}: Exception - {e}")
    
    print(f"\n📋 Required Scopes for Full Functionality:")
    print(f"   - chat:write (send messages)")
    print(f"   - channels:read (read channel info)")
    print(f"   - channels:history (read messages)")
    print(f"   - channels:join (join channels)")
    print(f"   - groups:read (private channels)")
    print(f"   - im:read (direct messages)")

if __name__ == "__main__":
    asyncio.run(check_scopes())