#!/usr/bin/env python3
"""Test script to directly test the backend AI agent"""

import asyncio
import sys
import os
sys.path.append('.')

from app.core.ai_agent_simple import simple_ai_agent

async def test_backend_direct():
    """Test the backend AI agent directly"""
    
    print("🧪 Testing backend AI agent directly...")
    print(f"✅ Agent available: {simple_ai_agent.available}")
    print(f"✅ Triage agent: {simple_ai_agent.triage_agent is not None}")
    print(f"✅ Config: {simple_ai_agent.config is not None}")
    
    # Test simple message
    test_messages = [
        "Hello, how are you?",
        "What do you do?",
        "2 + 3 = ?",
        "Schedule a meeting tomorrow at 3pm"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i}: {message} ---")
        
        try:
            result = await simple_ai_agent.process_message(
                user_message=message,
                user_context={}
            )
            
            print(f"✅ Response: {result.get('response', 'No response')[:100]}...")
            print(f"   Intent: {result.get('intent_type', 'unknown')}")
            print(f"   Confidence: {result.get('confidence', 'low')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n✅ Backend direct test completed!")

if __name__ == "__main__":
    asyncio.run(test_backend_direct())