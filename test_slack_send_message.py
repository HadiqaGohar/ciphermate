#!/usr/bin/env python3
"""
Test sending Slack message to available channels
"""

import asyncio
import os
import sys
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')

async def test_send_message():
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    
    print("💬 Testing Slack Message Sending")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {bot_token}',
        'Content-Type': 'application/json'
    }
    
    async with aiohttp.ClientSession() as session:
        # First, get list of channels
        print("📋 Getting available channels...")
        async with session.get(
            "https://slack.com/api/conversations.list",
            headers=headers,
            params={'types': 'public_channel,private_channel'}
        ) as response:
            data = await response.json()
            
            if not data.get('ok'):
                print(f"❌ Failed to get channels: {data.get('error')}")
                return
            
            channels = data.get('channels', [])
            print(f"Found {len(channels)} channels:")
            
            for i, channel in enumerate(channels):
                is_member = channel.get('is_member', False)
                member_status = "✅ Member" if is_member else "❌ Not Member"
                print(f"  {i+1}. #{channel['name']} - {member_status}")
            
            # Try to join the first public channel
            if channels:
                target_channel = channels[0]  # Use first channel
                channel_id = target_channel['id']
                channel_name = target_channel['name']
                
                print(f"\n🚪 Trying to join #{channel_name}...")
                
                # Try to join the channel
                async with session.post(
                    "https://slack.com/api/conversations.join",
                    headers=headers,
                    json={'channel': channel_id}
                ) as join_response:
                    join_data = await join_response.json()
                    
                    if join_data.get('ok'):
                        print(f"   ✅ Successfully joined #{channel_name}")
                    elif join_data.get('error') == 'already_in_channel':
                        print(f"   ✅ Already in #{channel_name}")
                    else:
                        print(f"   ❌ Failed to join: {join_data.get('error')}")
                        print(f"   💡 You may need to manually invite the bot: /invite @ciphermate")
                
                # Try to send message regardless
                print(f"\n💬 Sending test message to #{channel_name}...")
                
                message = f"Hello from CipherMate AI! 🤖 Test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                async with session.post(
                    "https://slack.com/api/chat.postMessage",
                    headers=headers,
                    json={
                        'channel': channel_id,
                        'text': message
                    }
                ) as msg_response:
                    msg_data = await msg_response.json()
                    
                    if msg_data.get('ok'):
                        print(f"   ✅ Message sent successfully!")
                        print(f"   🕐 Timestamp: {msg_data.get('ts')}")
                        print(f"   📺 Channel: #{channel_name}")
                        print(f"   📝 Message: {message}")
                        
                        print(f"\n🎉 SUCCESS! Check your Slack workspace → #{channel_name}")
                        return True
                    else:
                        error = msg_data.get('error')
                        print(f"   ❌ Failed to send message: {error}")
                        
                        if error == 'not_in_channel':
                            print(f"   💡 Bot needs to be invited to #{channel_name}")
                            print(f"   💡 In Slack, go to #{channel_name} and type: /invite @ciphermate")
                        
                        return False
            else:
                print("❌ No channels found")
                return False

async def main():
    await test_send_message()

if __name__ == "__main__":
    asyncio.run(main())