#!/usr/bin/env python3
"""Test script to list available Gemini models"""

import os
import sys
import google.generativeai as genai
from app.core.config import settings

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_models():
    """Test available Gemini models"""
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not configured")
        return
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        print("✅ Gemini API configured successfully")
        
        # List available models
        print("\n📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Test a few common model names
        test_models = [
            'gemini-pro',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'models/gemini-pro',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash'
        ]
        
        print("\n🧪 Testing model names:")
        for model_name in test_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello")
                print(f"  ✅ {model_name}: {response.text[:50]}...")
                break  # Use the first working model
            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:100]}...")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_models()