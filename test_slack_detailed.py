#!/usr/bin/env python3
"""
Detailed Slack Integration Test with Better Error Handling
"""

import asyncio
import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append('./backend')

import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

class DetailedSlackTester:
    def __init__(self):
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.channel = os.getenv('SLACK_CHANNEL', '#general')
        self.base_url = "https://slack.com/api"
        
    async def test_bot_info(self):
        """Get detailed bot information"""
        print("🤖 Getting Bot Information...")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/auth.test", headers=headers) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        print(f"   ✅ Bot User: {data.get('user')}")
                        print(f"   🏢 Team: {data.get('team')}")
                        print(f"   🆔 User ID: {data.get('user_id')}")
                        print(f"   🔗 Team ID: {data.get('team_id')}")
                        return data
                    else:
                        print(f"   ❌ Error: {data.get('error')}")
                        return None
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                return None
    
    async def test_scopes(self):
        """Test what scopes the bot has"""
        print(f"\n🔐 Testing Bot Scopes...")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/auth.test", headers=headers) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        # Try different API calls to test scopes
                        scope_tests = [
                            ("conversations.list", "/conversations.list"),
                            ("channels.list", "/channels.list"),
                            ("users.list", "/users.list"),
                        ]
                        
                        for scope_name, endpoint in scope_tests:
                            try:
                                async with session.get(f"{self.base_url}{endpoint}", headers=headers) as test_response:
                                    test_data = await test_response.json()
                                    if test_data.get('ok'):
                                        print(f"   ✅ {scope_name}: Working")
                                    else:
                                        print(f"   ❌ {scope_name}: {test_data.get('error', 'Failed')}")
                            except Exception as e:
                                print(f"   ❌ {scope_name}: Exception - {e}")
                        
            except Exception as e:
                print(f"   ❌ Error testing scopes: {e}")
    
    async def list_all_conversations(self):
        """List all conversations the bot can see"""
        print(f"\n📋 Listing All Conversations...")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                # Try conversations.list first
                async with session.get(
                    f"{self.base_url}/conversations.list",
                    headers=headers,
                    params={'types': 'public_channel,private_channel'}
                ) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        channels = data.get('channels', [])
                        print(f"   ✅ Found {len(channels)} conversations")
                        
                        for channel in channels[:10]:  # Show first 10
                            is_member = channel.get('is_member', False)
                            member_status = "✅ Member" if is_member else "❌ Not Member"
                            print(f"   📺 #{channel['name']} (ID: {channel['id']}) - {member_status}")
                        
                        return channels
                    else:
                        print(f"   ❌ conversations.list failed: {data.get('error')}")
                        
                        # Fallback to channels.list
                        async with session.get(f"{self.base_url}/channels.list", headers=headers) as fallback_response:
                            fallback_data = await fallback_response.json()
                            if fallback_data.get('ok'):
                                channels = fallback_data.get('channels', [])
                                print(f"   ✅ Fallback: Found {len(channels)} channels")
                                for channel in channels[:5]:
                                    print(f"   📺 #{channel['name']} (ID: {channel['id']})")
                                return channels
                            else:
                                print(f"   ❌ channels.list also failed: {fallback_data.get('error')}")
                        
                        return []
                        
            except Exception as e:
                print(f"   ❌ Error listing conversations: {e}")
                return []
    
    async def try_join_channel(self, channel_name):
        """Try to join a channel"""
        print(f"\n🚪 Trying to Join Channel: {channel_name}")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        # First, find the channel ID
        channel_id = None
        if channel_name.startswith('#'):
            channel_name = channel_name[1:]  # Remove #
        
        async with aiohttp.ClientSession() as session:
            try:
                # Get channel info
                async with session.get(
                    f"{self.base_url}/conversations.list",
                    headers=headers,
                    params={'types': 'public_channel'}
                ) as response:
                    data = await response.json()
                    
                    if data.get('ok'):
                        for channel in data.get('channels', []):
                            if channel['name'] == channel_name:
                                channel_id = channel['id']
                                print(f"   📺 Found channel: #{channel_name} (ID: {channel_id})")
                                break
                
                if channel_id:
                    # Try to join
                    async with session.post(
                        f"{self.base_url}/conversations.join",
                        headers=headers,
                        json={'channel': channel_id}
                    ) as join_response:
                        join_data = await join_response.json()
                        
                        if join_data.get('ok'):
                            print(f"   ✅ Successfully joined #{channel_name}")
                            return True
                        else:
                            error = join_data.get('error')
                            if error == 'already_in_channel':
                                print(f"   ✅ Already in #{channel_name}")
                                return True
                            else:
                                print(f"   ❌ Failed to join: {error}")
                                return False
                else:
                    print(f"   ❌ Channel #{channel_name} not found")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Error joining channel: {e}")
                return False
    
    async def send_test_message_with_channel_id(self, channel_id, message):
        """Send message using channel ID instead of name"""
        print(f"\n💬 Sending Message to Channel ID: {channel_id}")
        
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'channel': channel_id,
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
                        return True
                    else:
                        print(f"   ❌ Error: {data.get('error')}")
                        return False
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                return False
    
    async def run_detailed_tests(self):
        """Run comprehensive Slack tests"""
        print("🔍 Detailed Slack Integration Analysis")
        print("=" * 60)
        
        # Test 1: Bot Info
        bot_info = await self.test_bot_info()
        if not bot_info:
            return False
        
        # Test 2: Scopes
        await self.test_scopes()
        
        # Test 3: List Conversations
        channels = await self.list_all_conversations()
        
        # Test 4: Try to join general channel
        await self.try_join_channel("general")
        
        # Test 5: Try sending message with channel ID if we found general
        general_channel = None
        for channel in channels:
            if channel['name'] == 'general':
                general_channel = channel
                break
        
        if general_channel:
            message = f"Hello from CipherMate AI! 🤖 Detailed test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.send_test_message_with_channel_id(general_channel['id'], message)
        
        print(f"\n" + "=" * 60)
        print(f"🎯 Next Steps:")
        print(f"1. Add missing scopes: conversations.list, channels:join")
        print(f"2. Reinstall app to workspace")
        print(f"3. Invite bot to #general: /invite @ciphermate")
        
        return True

async def main():
    tester = DetailedSlackTester()
    await tester.run_detailed_tests()

if __name__ == "__main__":
    asyncio.run(main())