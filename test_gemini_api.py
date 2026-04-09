#!/usr/bin/env python3
"""
Test Gemini API key with both REST API and Agents SDK
"""

import os
import sys
import asyncio
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_rest_api(api_key: str) -> dict:
    """Test using direct REST API (more reliable for debugging)"""
    
    print("\n🔍 TEST 1: Direct REST API Call")
    print("-" * 40)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Say exactly 'API is working' and nothing else."
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and data['candidates']:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ REST API SUCCESS")
                print(f"Response: {text}")
                return {"success": True, "response": text}
            else:
                print(f"❌ Invalid response structure")
                print(json.dumps(data, indent=2))
                return {"success": False, "error": "Invalid response"}
        
        elif response.status_code == 429:
            print(f"❌ QUOTA EXCEEDED - Your API key has no remaining quota")
            print(f"Response: {response.text}")
            return {"success": False, "error": "quota_exceeded"}
        
        elif response.status_code == 403:
            print(f"❌ INVALID API KEY")
            print(f"Response: {response.text}")
            return {"success": False, "error": "invalid_key"}
        
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {"success": False, "error": f"http_{response.status_code}"}
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"success": False, "error": str(e)}


def test_gemini_agents_sdk(api_key: str) -> dict:
    """Test using Agents SDK"""
    
    print("\n🔍 TEST 2: Agents SDK Call")
    print("-" * 40)
    
    try:
        from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
        
        client = AsyncOpenAI(
            api_key=api_key,  # Use actual key variable
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            timeout=30.0
        )
        
        model = OpenAIChatCompletionsModel(
            model="gemini-3-flash-preview", 
            openai_client=client
        )
        
        agent = Agent(
            name="test", 
            instructions="Say exactly 'Agents SDK is working' and nothing else.", 
            model=model
        )
        
        async def run_test():
            result = await Runner.run(agent, "Say the phrase")
            return result.final_output
        
        response = asyncio.run(run_test())
        print(f"✅ Agents SDK SUCCESS")
        print(f"Response: {response}")
        return {"success": True, "response": response}
        
    except ImportError:
        print(f"❌ Agents SDK not installed")
        print(f"   Install with: pip install openai-agents")
        return {"success": False, "error": "agents_sdk_not_installed"}
        
    except Exception as e:
        print(f"❌ Agents SDK Error: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    print("🚀 Gemini API Diagnostic Tool")
    print("=" * 50)
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("\n❌ GEMINI_API_KEY not found in environment!")
        print("\n💡 Fix: Create a .env file with:")
        print("   GEMINI_API_KEY=your_actual_api_key_here")
        print("\n   Or set environment variable:")
        print("   export GEMINI_API_KEY='your_key'")
        sys.exit(1)
    
    print(f"\n✅ Found API Key: {api_key[:10]}...{api_key[-4:]}")
    
    # Test REST API first
    rest_result = test_gemini_rest_api(api_key)
    
    # Test Agents SDK
    agents_result = test_gemini_agents_sdk(api_key)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if rest_result["success"]:
        print("✅ REST API: Working")
    else:
        print(f"❌ REST API: {rest_result.get('error', 'Failed')}")
    
    if agents_result["success"]:
        print("✅ Agents SDK: Working")
    else:
        print(f"❌ Agents SDK: {agents_result.get('error', 'Failed')}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if rest_result.get("error") == "quota_exceeded":
        print("   ⚠️ Your API key has EXCEEDED QUOTA!")
        print("   → Get a new API key from: https://aistudio.google.com/apikey")
        print("   → Or enable billing on your Google Cloud project")
        
    elif not rest_result["success"]:
        print("   ⚠️ Your API key is INVALID or NOT WORKING!")
        print("   → Generate a new key at: https://aistudio.google.com/apikey")
        print("   → Make sure Gemini API is enabled")
        
    elif rest_result["success"] and not agents_result["success"]:
        print("   ⚠️ REST API works but Agents SDK fails")
        print("   → Install agents SDK: pip install openai-agents")
        print("   → Check agents SDK version compatibility")
        
    else:
        print("   ✅ Everything is working correctly!")
        print("   → Your CipherMate AI should work now")


if __name__ == "__main__":
    main()