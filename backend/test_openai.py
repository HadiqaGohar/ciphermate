#!/usr/bin/env python3
"""Test script for Gemini Agents SDK integration"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel

async def test_gemini_agents_sdk():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not configured in .env file")
        print("Please add your Gemini API key to backend/.env:")
        print("GEMINI_API_KEY=your-gemini-api-key-here")
        return
    
    print(f"✅ Gemini API Key found: {api_key[:15]}...")
    
    try:
        # Setup OpenAI-compatible client for Gemini API
        external_client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        
        # Setup model
        model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=external_client,
        )
        
        # Setup run configuration
        config = RunConfig(
            model=model,
            model_provider=external_client,
            tracing_disabled=True
        )
        
        # Create a simple test agent
        math_agent = Agent(
            name="math_agent",
            instructions="You are a math specialist. Calculate mathematical expressions and show the result clearly.",
            model=model
        )
        
        # Create triage agent
        triage_agent = Agent(
            name="triage_agent",
            instructions="You route math questions to the math specialist. Use the math tool for any calculations.",
            tools=[
                math_agent.as_tool(
                    tool_name="calculate",
                    tool_description="Handle mathematical calculations"
                )
            ],
            model=model
        )
        
        print("✅ Gemini Agents SDK configured successfully!")
        
        # Test with a simple math question
        test_messages = [
            {"role": "user", "content": "What is 2 + 3?"}
        ]
        
        result = await Runner.run(triage_agent, test_messages, run_config=config)
        response = result.final_output
        
        print(f"✅ Gemini Agents SDK working!")
        print(f"Question: What is 2 + 3?")
        print(f"Response: {response}")
        
        # Test with a calendar question
        calendar_messages = [
            {"role": "user", "content": "Schedule a meeting tomorrow at 3pm"}
        ]
        
        result2 = await Runner.run(triage_agent, calendar_messages, run_config=config)
        response2 = result2.final_output
        
        print(f"\n✅ Calendar test:")
        print(f"Question: Schedule a meeting tomorrow at 3pm")
        print(f"Response: {response2}")
        
    except Exception as e:
        print(f"❌ Gemini Agents SDK error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_agents_sdk())