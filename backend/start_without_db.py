#!/usr/bin/env python3
"""
Start CipherMate backend without database dependencies
Useful for testing AI agent functionality and API endpoints
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variable to disable database
os.environ["DISABLE_DATABASE"] = "true"
os.environ["DISABLE_REDIS"] = "true"

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting CipherMate Backend (No Database Mode)")
    print("=" * 50)
    print("✅ AI Agent with OpenAI Agents SDK: Enabled")
    print("✅ API Endpoints: Enabled")
    print("⚠️  Database: Disabled")
    print("⚠️  Redis: Disabled")
    print("⚠️  Token Vault: Mock Mode")
    print("=" * 50)
    print("Server will be available at: http://localhost:8080")
    print("API Documentation: http://localhost:8080/docs")
    print("Press Ctrl+C to stop")
    print()
    
    uvicorn.run(
        "app.main_no_db:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )