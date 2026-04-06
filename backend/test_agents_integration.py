#!/usr/bin/env python3
"""Test script for complete Agents SDK integration"""

import os
import asyncio
import sys
sys.path.append('.')

from dotenv import load_dotenv
from app.core.ai_agent_simple import simple_ai_agent

async def test_agents_integration():
    """Test the complete Agents SDK integration"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OPENAI_API_KEY not configured in .env file")
        print("Please add your OpenAI API key to backend/.env:")
        print("OPENAI_API_KEY=sk-your-actual-key-here")
        return
    
    print(f"✅ OpenAI API Key found: {api_key[:15]}...")
    print(f"✅ Agents SDK available: {simple_ai_agent.available}")
    
    if not simple_ai_agent.available:
        print("❌ Agents SDK not available")
        return
    
    # Test cases
    test_cases = [
        "Hello, how are you?",
        "What is 2 + 3?",
        "Schedule a meeting tomorrow at 3pm",
        "Send an email to john@example.com about the project",
        "Create a GitHub issue for the login bug",
        "Write a Python hello world program"
    ]
    
    print("\n🧪 Testing Agents SDK integration...")
    
    for i, test_message in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_message} ---")
        
        try:
            result = await simple_ai_agent.process_message(
                user_message=test_message,
                user_context={}
            )
            
            print(f"✅ Response: {result.get('response', 'No response')[:100]}...")
            print(f"   Intent: {result.get('intent_type', 'unknown')}")
            print(f"   Confidence: {result.get('confidence', 'low')}")
            print(f"   Service: {result.get('service_name', 'none')}")
            
            if result.get('parameters'):
                print(f"   Parameters: {result.get('parameters')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Agents SDK integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_agents_integration())