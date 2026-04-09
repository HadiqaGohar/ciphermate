#!/usr/bin/env python3
"""
Test database connection to Neon.tech PostgreSQL
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print(f"🔗 Testing connection to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
    
    try:
        engine = create_async_engine(database_url)
        
        async with engine.begin() as conn:
            result = await conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"📊 PostgreSQL version: {version}")
            
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())