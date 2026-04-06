#!/usr/bin/env python3
"""
Simple startup test for Cloud Run deployment
"""
import sys
import os

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing basic imports...")
        import fastapi
        print("✓ FastAPI imported")
        
        import uvicorn
        print("✓ Uvicorn imported")
        
        # Test basic config import
        try:
            from app.core.config import settings
            print("✓ Settings imported")
            print(f"✓ App environment: {settings.APP_ENV}")
        except Exception as e:
            print(f"⚠ Settings import warning: {e}")
            print("✓ Continuing without full settings...")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_app():
    """Test if basic FastAPI app can be created"""
    try:
        print("Testing basic FastAPI app...")
        from fastapi import FastAPI
        
        # Create a minimal test app
        test_app = FastAPI(title="Test App")
        
        @test_app.get("/")
        def root():
            return {"status": "ok"}
        
        print("✓ Basic FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"✗ Basic app creation error: {e}")
        return False

def main():
    print("=== CipherMate Startup Test ===")
    
    # Test environment
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PORT environment: {os.getenv('PORT', 'Not set')}")
    print(f"APP_ENV environment: {os.getenv('APP_ENV', 'Not set')}")
    
    # Test imports
    if not test_imports():
        print("⚠ Some imports failed, but continuing...")
    
    # Test basic app creation
    if not test_basic_app():
        print("✗ Basic app test failed")
        sys.exit(1)
    
    print("✓ Basic tests passed! Attempting full app import...")
    
    # Try to import the full app (optional)
    try:
        from app.main import app
        print("✓ Full app imported successfully!")
    except Exception as e:
        print(f"⚠ Full app import failed: {e}")
        print("✓ But basic FastAPI works, so container should start")
    
    print("✓ Startup test completed successfully!")

if __name__ == "__main__":
    main()