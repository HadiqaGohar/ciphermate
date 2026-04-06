#!/usr/bin/env python3
"""
Simple startup script for OpenAI Agents SDK Demo
"""

import os
import sys
import subprocess
from pathlib import Path


def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["GEMINI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment")
        return False
    
    return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements-demo.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def run_server():
    """Run the demo server"""
    print("🚀 Starting OpenAI Agents SDK Demo server...")
    print("   Server will be available at: http://localhost:8000")
    print("   API docs available at: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "demo_openai_agents.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")


def main():
    """Main function"""
    print("🤖 OpenAI Agents SDK Demo Launcher\n")
    
    # Check if we're in the right directory
    if not Path("demo_openai_agents.py").exists():
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies if needed
    if "--install" in sys.argv or not Path("requirements-demo.txt").exists():
        if not install_dependencies():
            sys.exit(1)
    
    # Run the server
    run_server()


if __name__ == "__main__":
    main()