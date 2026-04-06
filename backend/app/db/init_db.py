"""Database initialization and setup utilities"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine, Base
from app.db.seed_data import create_permission_templates
import logging

logger = logging.getLogger(__name__)


async def init_database() -> None:
    """Initialize the database by creating all tables"""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


async def seed_database() -> None:
    """Seed the database with initial data"""
    try:
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            # Create permission templates
            await create_permission_templates(session)
            await session.commit()
            
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise


async def reset_database() -> None:
    """Reset the database by dropping and recreating all tables"""
    try:
        async with engine.begin() as conn:
            # Drop all tables
            await conn.run_sync(Base.metadata.drop_all)
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        # Seed with initial data
        await seed_database()
        
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise


if __name__ == "__main__":
    # Allow running this script directly for database initialization
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            asyncio.run(init_database())
        elif command == "seed":
            asyncio.run(seed_database())
        elif command == "reset":
            asyncio.run(reset_database())
        else:
            print("Usage: python init_db.py [init|seed|reset]")
    else:
        print("Usage: python init_db.py [init|seed|reset]")