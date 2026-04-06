#!/usr/bin/env python3
"""Test script to check if agents SDK can be imported"""

import sys
import os
sys.path.append('.')

print("🧪 Testing Agents SDK import...")

try:
    from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
    print("✅ Agents SDK imported successfully!")
    
    # Test basic functionality
    print("✅ Agent class available")
    print("✅ Runner class available") 
    print("✅ RunConfig class available")
    print("✅ AsyncOpenAI class available")
    print("✅ OpenAIChatCompletionsModel class available")
    
except ImportError as e:
    print(f"❌ Failed to import Agents SDK: {e}")
    print("Please install the agents SDK:")
    print("pip install agents")
    
except Exception as e:
    print(f"❌ Error importing Agents SDK: {e}")

print("\n🧪 Testing OpenAI import...")

try:
    from openai import AsyncOpenAI
    print("✅ OpenAI imported successfully!")
    
except ImportError as e:
    print(f"❌ Failed to import OpenAI: {e}")
    print("Please install OpenAI:")
    print("pip install openai")
    
except Exception as e:
    print(f"❌ Error importing OpenAI: {e}")

print("\n🧪 Testing environment variables...")

from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"✅ GEMINI_API_KEY found: {gemini_key[:15]}...")
else:
    print("❌ GEMINI_API_KEY not found")

print("\n✅ Import test completed!")