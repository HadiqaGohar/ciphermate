#!/usr/bin/env python3
"""Debug script to check environment variables"""

import os
from app.core.config import settings

print("🔍 Environment Variables Debug:")
print(f"APP_ENV: {getattr(settings, 'APP_ENV', 'NOT_SET')}")
print(f"FRONTEND_URL: {getattr(settings, 'FRONTEND_URL', 'NOT_SET')}")
print(f"GOOGLE_CLIENT_ID: {getattr(settings, 'GOOGLE_CLIENT_ID', 'NOT_SET')[:20]}...")
print(f"GITHUB_CLIENT_ID: {getattr(settings, 'GITHUB_CLIENT_ID', 'NOT_SET')}")

print("\n🔍 Raw Environment Variables:")
print(f"APP_ENV (raw): {os.getenv('APP_ENV', 'NOT_SET')}")
print(f"FRONTEND_URL (raw): {os.getenv('FRONTEND_URL', 'NOT_SET')}")

# Test the logic
frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
if not frontend_url or frontend_url == 'http://localhost:3000':
    if hasattr(settings, 'APP_ENV') and settings.APP_ENV == 'production':
        frontend_url = 'https://ciphermate.vercel.app'
    else:
        frontend_url = 'http://localhost:3000'

print(f"\n🎯 Final Frontend URL: {frontend_url}")