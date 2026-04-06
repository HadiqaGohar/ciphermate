"""
Test script for OpenAI Agents SDK Demo
"""

import asyncio
import httpx
import json


async def test_demo():
    """Test the demo endpoints"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing OpenAI Agents SDK Demo\n")
        
        # Test health endpoint
        print("1. Testing health endpoint...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test root endpoint
        print("2. Testing root endpoint...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test chat endpoint - single translation
        print("3. Testing single translation...")
        try:
            response = await client.post(
                f"{base_url}/chat",
                json={"message": "Translate 'Hello World' to Spanish"}
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Response: {result.get('response', 'No response')}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test chat endpoint - multiple translations
        print("4. Testing multiple translations...")
        try:
            response = await client.post(
                f"{base_url}/chat",
                json={"message": "Translate 'Good morning' to Spanish, French, and Italian"}
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Response: {result.get('response', 'No response')}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test general conversation
        print("5. Testing general conversation...")
        try:
            response = await client.post(
                f"{base_url}/chat",
                json={"message": "What languages can you translate to?"}
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Response: {result.get('response', 'No response')}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test reset endpoint
        print("6. Testing conversation reset...")
        try:
            response = await client.post(f"{base_url}/reset")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")


def run_interactive_test():
    """Run interactive test session"""
    import requests
    
    base_url = "http://localhost:8000"
    
    print("🎯 Interactive OpenAI Agents SDK Demo Test")
    print("Type 'quit' to exit, 'reset' to clear conversation\n")
    
    while True:
        try:
            message = input("You: ").strip()
            
            if message.lower() == 'quit':
                break
            elif message.lower() == 'reset':
                response = requests.post(f"{base_url}/reset")
                print("🔄 Conversation reset\n")
                continue
            elif not message:
                continue
            
            response = requests.post(
                f"{base_url}/chat",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Agent: {result.get('response', 'No response')}\n")
            else:
                print(f"Error: {response.status_code} - {response.text}\n")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")
    
    print("👋 Goodbye!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive_test()
    else:
        asyncio.run(test_demo())