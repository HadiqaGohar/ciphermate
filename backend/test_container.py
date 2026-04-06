#!/usr/bin/env python3
"""
Quick test to verify container startup
"""

import sys
import os

def test_imports():
    """Test critical imports"""
    try:
        print("Testing pydantic_settings...")
        from pydantic_settings import BaseSettings
        print("✅ pydantic_settings imported successfully")
        
        print("Testing app.main_no_db...")
        from app.main_no_db import app
        print("✅ app.main_no_db imported successfully")
        
        print("Testing FastAPI app...")
        assert app is not None
        print("✅ FastAPI app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print(f"PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"DISABLE_DATABASE: {os.environ.get('DISABLE_DATABASE', 'Not set')}")
    print(f"DISABLE_REDIS: {os.environ.get('DISABLE_REDIS', 'Not set')}")
    print(f"Working directory: {os.getcwd()}")
    
    # List app directory
    if os.path.exists('app'):
        print("App directory contents:")
        for item in os.listdir('app'):
            print(f"  - {item}")
    else:
        print("❌ App directory not found")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing container startup...")
    
    env_ok = test_environment()
    imports_ok = test_imports()
    
    if env_ok and imports_ok:
        print("✅ All tests passed - container should start successfully")
        sys.exit(0)
    else:
        print("❌ Tests failed - container will not start")
        sys.exit(1)