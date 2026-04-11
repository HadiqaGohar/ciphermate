#!/usr/bin/env python3
"""
Slack Integration Test Script for CipherMate AI

This script tests the Slack integration functionality including:
1. Bot token validation
2. Channel access
3. Message sending
4. API endpoint testing

Prerequisites:
1. Slack Bot Token (SLACK_BOT_TOKEN in .env)
2. Slack app with proper scopes: chat:write, channels:read
3. Bot installed in workspace
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any

# Add backend to path
sys.path.append('./backend')

import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

class SlackTester:
    def __init__(self):
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.channel = os.getenv('SLACK_CHANNEL', '#general')
        self.base_url = "https://slack.com/api"
        
        if not self.bot_token or self.bot_token == 'xoxb-your-bot-token-here':
            print("❌ SLACK_BOT_TOKEN not configured in .env file")
            print("\n📋 Setup Instructions:")
            print("1. Go to https://api.slack.com/apps")
            print("2. Create new app or select existing")
            print("3. Go to 'OAuth & Permissions'")
            print("4. Add bot token scopes: chat:write, channels:read")
            print("5. Install to workspace")
            print("6. Copy 'Bot User OAuth Token' to .env as SLACK_BOT_TOKEN")
            sys.exit(1)
    
    async def test_bot_token(self) -> bool:
        """Test if the bot token is valid"""
        print("🔐 Testing Bot Token...")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/auth.test", headers=headers) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        print(f"   ✅ Bot token valid")
                        print(f"   📱 Bot User: {data.get('user')}")
                        print(f"   🏢 Team: {data.get('team')}")
                        print(f"   🆔 User ID: {data.get('user_id')}")
                        return True
                    else:
                        print(f"   ❌ Bot token invalid: {data.get('error')}")
                        return False
                        
            except Exception as e:
                print(f"   ❌ Error testing bot token: {e}")
                return False
    
    async def list_channels(self) -> Dict[str, Any]:
        """List available channels"""
        print(f"\n📋 Listing Channels...")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/conversations.list",
                    headers=headers,
                    params={'types': 'public_channel,private_channel'}
                ) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        channels = data.get('channels', [])
                        print(f"   ✅ Found {len(channels)} channels")
                        
                        for channel in channels[:5]:  # Show first 5 channels
                            print(f"   📺 #{channel['name']} (ID: {channel['id']})")
                        
                        return data
                    else:
                        print(f"   ❌ Error listing channels: {data.get('error')}")
                        return {}
                        
            except Exception as e:
                print(f"   ❌ Error listing channels: {e}")
                return {}
    
    async def send_test_message(self, message: str = None) -> bool:
        """Send a test message to the configured channel"""
        if not message:
            message = f"Hello everyone from CipherMate AI! 🤖 Test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print(f"\n💬 Sending Test Message...")
        print(f"   📺 Channel: {self.channel}")
        print(f"   📝 Message: {message}")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'channel': self.channel,
            'text': message
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat.postMessage",
                    headers=headers,
                    json=payload
                ) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        print(f"   ✅ Message sent successfully!")
                        print(f"   🕐 Timestamp: {data.get('ts')}")
                        print(f"   📺 Channel: {data.get('channel')}")
                        return True
                    else:
                        print(f"   ❌ Error sending message: {data.get('error')}")
                        return False
                        
            except Exception as e:
                print(f"   ❌ Error sending message: {e}")
                return False
    
    async def test_ciphermate_api_endpoint(self) -> bool:
        """Test the CipherMate API Slack endpoint"""
        print(f"\n🔌 Testing CipherMate API Endpoint...")
        
        # This would require authentication with your backend
        # For now, just show the endpoint structure
        print("   📋 API Endpoint: POST /api/v1/integrations/slack/messages")
        print("   📝 Payload structure:")
        print("   {")
        print(f'     "channel": "{self.channel}",')
        print('     "text": "Hello from CipherMate API!"')
        print("   }")
        print("   ℹ️  Note: This requires user authentication with your backend")
        return True
    
    async def run_all_tests(self):
        """Run all Slack integration tests"""
        print("🚀 Starting Slack Integration Tests for CipherMate AI")
        print("=" * 60)
        
        # Test 1: Bot Token
        token_valid = await self.test_bot_token()
        if not token_valid:
            print("\n❌ Bot token test failed. Please check your configuration.")
            return False
        
        # Test 2: List Channels
        await self.list_channels()
        
        # Test 3: Send Test Message
        message_sent = await self.send_test_message()
        
        # Test 4: API Endpoint Info
        await self.test_ciphermate_api_endpoint()
        
        print("\n" + "=" * 60)
        if token_valid and message_sent:
            print("✅ All Slack tests completed successfully!")
            print(f"💬 Check your Slack workspace → {self.channel} for the test message")
        else:
            print("❌ Some tests failed. Please check the configuration.")
        
        return token_valid and message_sent

async def main():
    """Main test function"""
    tester = SlackTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())