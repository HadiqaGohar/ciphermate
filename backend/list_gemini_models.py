#!/usr/bin/env python3
"""
Script to list available Gemini models
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import google.generativeai as genai
from app.core.config import settings

def list_models():
    """List available Gemini models"""
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not configured")
        return
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        print("🔍 Listing available Gemini models...")
        
        models = genai.list_models()
        for model in models:
            print(f"   📋 {model.name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"      Methods: {model.supported_generation_methods}")
            print()
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_models()