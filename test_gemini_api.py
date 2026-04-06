#!/usr/bin/env python3
"""
Test script to verify if a Gemini API key is working correctly.
"""

import os
import sys
import requests
import json
from typing import Optional


def test_gemini_api_key(api_key: Optional[str] = None) -> bool:
    """
    Test if the Gemini API key is valid and working.
    
    Args:
        api_key: The API key to test. If None, will try to get from environment.
        
    Returns:
        bool: True if API key is working, False otherwise.
    """
    
    # Get API key from parameter or environment
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key provided. Set GEMINI_API_KEY environment variable or pass as argument.")
        return False
    
    # Gemini API endpoint for text generation (using the correct model name)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Simple test payload
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello, this is a test. Please respond with 'API key is working'."
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Testing Gemini API key...")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we got a valid response
            if 'candidates' in data and len(data['candidates']) > 0:
                content = data['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                
                if parts and len(parts) > 0:
                    response_text = parts[0].get('text', '')
                    print("✅ API key is working!")
                    print(f"📝 Response: {response_text.strip()}")
                    return True
                else:
                    print("❌ API returned empty response")
                    return False
            else:
                print("❌ API returned invalid response structure")
                print(f"Response: {json.dumps(data, indent=2)}")
                return False
                
        elif response.status_code == 400:
            print("❌ Bad request - API key might be invalid or request malformed")
            print(f"Error: {response.text}")
            return False
            
        elif response.status_code == 403:
            print("❌ Forbidden - API key is invalid or doesn't have permission")
            print(f"Error: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("❌ Rate limit exceeded - API key is valid but quota exceeded")
            print(f"Error: {response.text}")
            return False
            
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - check your internet connection")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check your internet connection")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def main():
    """Main function to run the API key test."""
    
    print("🚀 Gemini API Key Tester")
    print("=" * 40)
    
    # Check if API key is provided as command line argument
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    # Test the API key
    success = test_gemini_api_key(api_key)
    
    if success:
        print("\n🎉 Your Gemini API key is working correctly!")
        sys.exit(0)
    else:
        print("\n💡 Tips:")
        print("   - Make sure your API key is correct")
        print("   - Check if the API key has the necessary permissions")
        print("   - Verify your internet connection")
        print("   - Check if you have remaining quota")
        sys.exit(1)


if __name__ == "__main__":
    main()