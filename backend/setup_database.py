#!/usr/bin/env python3
"""
Database setup script for CipherMate
Creates PostgreSQL database and user if they don't exist
"""

import asyncio
import asyncpg
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def setup_database():
    """Setup PostgreSQL database for CipherMate"""
    
    print("🗄️  Setting up CipherMate Database...")
    print("=" * 40)
    
    # Database configuration
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "ciphermate"
    DB_USER = "postgres"
    DB_PASSWORD = "password"
    
    try:
        # Connect to PostgreSQL as superuser
        print("1. Connecting to PostgreSQL...")
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"  # Connect to default database first
        )
        
        # Check if database exists
        print("2. Checking if database exists...")
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", DB_NAME
        )
        
        if not db_exists:
            print(f"3. Creating database '{DB_NAME}'...")
            await conn.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"   ✅ Database '{DB_NAME}' created successfully")
        else:
            print(f"   ✅ Database '{DB_NAME}' already exists")
        
        await conn.close()
        
        # Connect to the CipherMate database
        print("4. Connecting to CipherMate database...")
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        # Test the connection
        result = await conn.fetchval("SELECT version()")
        print(f"   ✅ Connected successfully")
        print(f"   PostgreSQL version: {result.split(',')[0]}")
        
        await conn.close()
        
        print("\n🎉 Database setup completed successfully!")
        print(f"   Database URL: postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print("\nYou can now start the backend with:")
        print("   python -m uvicorn app.main:app --reload --port 8000")
        
        return True
        
    except asyncpg.InvalidPasswordError:
        print("❌ Error: Invalid password for PostgreSQL user 'postgres'")
        print("\nTo fix this:")
        print("1. Make sure PostgreSQL is running")
        print("2. Update the password in this script or reset PostgreSQL password")
        print("3. Or use the no-database mode: python start_without_db.py")
        return False
        
    except asyncpg.CannotConnectNowError:
        print("❌ Error: Cannot connect to PostgreSQL")
        print("\nTo fix this:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Check if PostgreSQL service is started")
        print("3. Or use the no-database mode: python start_without_db.py")
        return False
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\nAlternative: Use no-database mode for development:")
        print("   python start_without_db.py")
        return False

def check_postgresql_running():
    """Check if PostgreSQL is running"""
    import subprocess
    try:
        # Try to check if PostgreSQL is running
        result = subprocess.run(
            ["pg_isready", "-h", "localhost", "-p", "5432"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        # pg_isready not found, PostgreSQL might not be installed
        return False

async def main():
    """Main function"""
    print("🚀 CipherMate Database Setup")
    print("=" * 30)
    
    # Check if PostgreSQL is running
    if not check_postgresql_running():
        print("⚠️  PostgreSQL doesn't seem to be running or installed")
        print("\nOptions:")
        print("1. Install and start PostgreSQL")
        print("2. Use no-database mode: python start_without_db.py")
        print("\nFor Ubuntu/Debian:")
        print("   sudo apt update")
        print("   sudo apt install postgresql postgresql-contrib")
        print("   sudo systemctl start postgresql")
        print("\nFor macOS:")
        print("   brew install postgresql")
        print("   brew services start postgresql")
        return
    
    success = await setup_database()
    
    if not success:
        print("\n💡 Alternative: Start without database")
        print("   python start_without_db.py")

if __name__ == "__main__":
    asyncio.run(main())