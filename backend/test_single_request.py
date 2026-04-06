#!/usr/bin/env python3
"""
Test script for a single AI agent request to avoid rate limiting
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.ai_agent import AIAgentEngine, AIProvider


async def test_single_request():
    """Test a single AI agent request"""
    print("🤖 Testing AI Agent Engine with Gemini 3 Flash...")
    
    # Initialize the AI agent
    agent = AIAgentEngine(preferred_provider=AIProvider.AUTO)
    
    print(f"✅ AI Agent initialized with provider: {agent.active_provider.value}")
    
    # Test a single message
    message = "Schedule a meeting with John tomorrow at 2pm about the project review"
    print(f"\n📝 Testing message: '{message}'")
    
    try:
        # Analyze intent
        result = await agent.analyze_intent(message)
        
        print(f"   🎯 Intent: {result.intent_type.value}")
        print(f"   📊 Confidence: {result.confidence.value}")
        print(f"   🔧 Service: {result.service_name or 'None'}")
        print(f"   📋 Parameters: {result.parameters}")
        print(f"   🔐 Required permissions: {result.required_permissions}")
        
        if result.clarification_needed:
            print(f"   ❓ Clarification needed: {result.clarification_questions}")
        
        # Generate response
        response = await agent.generate_response(message, result)
        print(f"   💬 Response: {response}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Single request test completed!")


if __name__ == "__main__":
    asyncio.run(test_single_request())