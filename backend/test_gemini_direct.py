#!/usr/bin/env python3
"""Test Gemini API directly to see available models"""

import os
import sys
import requests
from app.core.config import settings

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_direct():
    """Test Gemini API directly"""
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not configured")
        return
    
    try:
        # List models using direct Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Available Gemini models:")
            for model in models.get('models', []):
                name = model.get('name', 'Unknown')
                methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    print(f"  - {name}")
        else:
            print(f"❌ Error listing models: {response.status_code} - {response.text}")
            
        # Test a simple generation request
        print("\n🧪 Testing direct generation:")
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": "Hello"}]
            }]
        }
        
        response = requests.post(gen_url, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No text')
            print(f"  ✅ Direct API: {text[:50]}...")
        else:
            print(f"  ❌ Direct API error: {response.status_code} - {response.text[:100]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_direct()