#!/usr/bin/env python3
"""
Full integration test for CipherMate platform
Tests both frontend and backend integration
"""

import asyncio
import httpx
import subprocess
import time
import sys
import os
from pathlib import Path

async def test_backend_health():
    """Test backend health endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend health: {data.get('status', 'unknown')}")
                print(f"   ✅ AI Agent: {data.get('ai_agent', {}).get('available', False)}")
                return True
            else:
                print(f"   ❌ Backend health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ Backend not accessible: {e}")
        return False

async def test_ai_agent_api():
    """Test AI agent API endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            # Test the chat endpoint
            response = await client.post(
                "http://localhost:8000/api/v1/ai-agent/chat",
                json={
                    "message": "Schedule a meeting with John tomorrow at 2pm",
                    "context": {}
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ AI Agent API working")
                print(f"   ✅ Intent detected: {data.get('intent_type', 'unknown')}")
                print(f"   ✅ Response generated: {len(data.get('response', ''))} chars")
                return True
            else:
                print(f"   ❌ AI Agent API failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
    except Exception as e:
        print(f"   ❌ AI Agent API error: {e}")
        return False

async def test_frontend_health():
    """Test frontend accessibility"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:3000", timeout=10.0)
            if response.status_code == 200:
                print(f"   ✅ Frontend accessible")
                return True
            else:
                print(f"   ❌ Frontend returned: {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ Frontend not accessible: {e}")
        return False

def check_process_running(port):
    """Check if a process is running on a specific port"""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and result.stdout.strip()
    except:
        return False

async def main():
    """Main test function"""
    print("🧪 CipherMate Full Integration Test")
    print("=" * 40)
    
    # Check if backend is running
    print("\n1. Checking Backend (Port 8000)...")
    if not check_process_running(8000):
        print("   ⚠️  Backend not running on port 8000")
        print("   Start with: cd backend && python start_without_db.py")
        backend_running = False
    else:
        print("   ✅ Backend process detected")
        backend_running = True
    
    # Check if frontend is running
    print("\n2. Checking Frontend (Port 3000)...")
    if not check_process_running(3000):
        print("   ⚠️  Frontend not running on port 3000")
        print("   Start with: cd frontend && npm run dev")
        frontend_running = False
    else:
        print("   ✅ Frontend process detected")
        frontend_running = True
    
    # Test backend health
    if backend_running:
        print("\n3. Testing Backend Health...")
        backend_healthy = await test_backend_health()
    else:
        backend_healthy = False
    
    # Test AI agent
    if backend_healthy:
        print("\n4. Testing AI Agent API...")
        ai_working = await test_ai_agent_api()
    else:
        ai_working = False
    
    # Test frontend
    if frontend_running:
        print("\n5. Testing Frontend...")
        frontend_healthy = await test_frontend_health()
    else:
        frontend_healthy = False
    
    # Summary
    print("\n" + "=" * 40)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 40)
    
    results = [
        ("Backend Running", backend_running),
        ("Backend Healthy", backend_healthy),
        ("AI Agent Working", ai_working),
        ("Frontend Running", frontend_running),
        ("Frontend Accessible", frontend_healthy),
    ]
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 Full integration test PASSED!")
        print("🔗 Frontend: http://localhost:3000")
        print("🔗 Backend: http://localhost:8000")
        print("🔗 API Docs: http://localhost:8000/docs")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed")
        print("\nQuick start commands:")
        print("Backend: cd backend && python start_without_db.py")
        print("Frontend: cd frontend && npm run dev")
    
    return passed == len(results)

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)