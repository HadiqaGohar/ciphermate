#!/usr/bin/env python3
"""Test Gemini API through OpenAI compatibility layer"""

import os
import sys
import openai
from app.core.config import settings

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_openai():
    """Test Gemini API through OpenAI compatibility layer"""
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not configured")
        return
    
    try:
        client = openai.OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            timeout=5.0,
            max_retries=0
        )
        print("✅ OpenAI client configured for Gemini API")
        
        # Test different model names
        test_models = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-002',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        print("\n🧪 Testing model names:")
        for model_name in test_models:
            try:
                print(f"  Testing {model_name}...")
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10,
                    timeout=3.0
                )
                print(f"  ✅ {model_name}: {response.choices[0].message.content}")
                break  # Use the first working model
            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:100]}...")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_openai()