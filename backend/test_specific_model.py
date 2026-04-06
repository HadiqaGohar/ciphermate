#!/usr/bin/env python3
"""Test specific Gemini model through OpenAI compatibility layer"""

import os
import sys
import openai
from app.core.config import settings

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_specific_model():
    """Test specific Gemini model"""
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
        
        # Test the specific model
        model_name = "gemini-2.5-flash"
        print(f"🧪 Testing {model_name}...")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello, respond with just 'Hi there!'"}],
            max_tokens=50,  # Increased token limit
            timeout=5.0
        )
        print(f"✅ Success: {response.choices[0].message.content}")
        print(f"📋 Full response: {response}")
        print(f"📋 Choice: {response.choices[0]}")
        print(f"📋 Message: {response.choices[0].message}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_specific_model()