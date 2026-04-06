#!/usr/bin/env python3
"""Database management CLI for CipherMate"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.init_db import init_database, seed_database, reset_database
from app.db.seed_data import seed_sample_data
from app.core.database import AsyncSessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_migrations():
    """Run Alembic migrations"""
    import subprocess
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Migrations completed successfully")
            print(result.stdout)
        else:
            logger.error("Migration failed")
            print(result.stderr)
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        sys.exit(1)


async def create_sample_data():
    """Create sample data for development"""
    try:
        async with AsyncSessionLocal() as session:
            await seed_sample_data(session)
            await session.commit()
        logger.info("Sample data created successfully")
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        raise


def print_help():
    """Print help information"""
    print("""
CipherMate Database Management CLI

Usage: python manage_db.py <command>

Commands:
    init        Initialize database (create tables)
    migrate     Run Alembic migrations
    seed        Seed database with initial data
    sample      Create sample data for development
    reset       Reset database (drop and recreate all tables)
    help        Show this help message

Examples:
    python manage_db.py migrate
    python manage_db.py seed
    python manage_db.py reset
    """)


async def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "init":
            await init_database()
            print("✅ Database initialized successfully")
            
        elif command == "migrate":
            await run_migrations()
            print("✅ Migrations completed successfully")
            
        elif command == "seed":
            await seed_database()
            print("✅ Database seeded successfully")
            
        elif command == "sample":
            await create_sample_data()
            print("✅ Sample data created successfully")
            
        elif command == "reset":
            confirm = input("⚠️  This will delete all data. Are you sure? (y/N): ")
            if confirm.lower() == 'y':
                await reset_database()
                print("✅ Database reset successfully")
            else:
                print("❌ Operation cancelled")
                
        elif command == "help":
            print_help()
            
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Command failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())