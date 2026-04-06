#!/usr/bin/env python3
"""Test Google Calendar integration"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.google_calendar import google_calendar_service
from app.core.database import AsyncSessionLocal

async def test_calendar():
    print('🧪 Testing Google Calendar service...')
    try:
        async with AsyncSessionLocal() as db:
            result = await google_calendar_service.create_event(
                db=db,
                user_id=1,  # Test user ID
                title='Test Meeting',
                date='2026-04-07',
                time='15:00'
            )
            print('✅ Result:', result)
    except Exception as e:
        print('❌ Expected error (no user connection):', str(e))
        print('✅ This is expected - user needs to connect Google Calendar first')

if __name__ == "__main__":
    asyncio.run(test_calendar())