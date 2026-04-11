from typing import Optional, Dict, Any
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
    # // done hadiqa

class SessionManager:
    """Manage user sessions with Redis"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.session_prefix = "session:"
        self.user_prefix = "user:"
        self.default_ttl = 3600 * 24  # 24 hours
    
    async def get_redis_client(self) -> redis.Redis:
        """Get Redis client instance"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def create_session(
        self, 
        user_id: str, 
        user_data: Dict[str, Any],
        session_id: Optional[str] = None,
        ttl: Optional[int] = None
    ) -> str:
        """Create a new user session"""
        try:
            client = await self.get_redis_client()
            
            if session_id is None:
                session_id = f"{user_id}_{int(datetime.utcnow().timestamp())}"
            
            session_key = f"{self.session_prefix}{session_id}"
            user_key = f"{self.user_prefix}{user_id}"
            
            # Session data
            session_data = {
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "last_accessed": datetime.utcnow().isoformat(),
                "user_data": json.dumps(user_data)
            }
            
            # Store session
            await client.hset(session_key, mapping=session_data)
            await client.expire(session_key, ttl or self.default_ttl)
            
            # Store user reference to session
            await client.set(user_key, session_id, ex=ttl or self.default_ttl)
            
            logger.info(f"Created session {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            client = await self.get_redis_client()
            session_key = f"{self.session_prefix}{session_id}"
            
            session_data = await client.hgetall(session_key)
            if not session_data:
                return None
            
            # Update last accessed time
            await client.hset(
                session_key, 
                "last_accessed", 
                datetime.utcnow().isoformat()
            )
            
            # Parse user data
            if "user_data" in session_data:
                session_data["user_data"] = json.loads(session_data["user_data"])
            
            return session_data
            
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            return None
    
    async def update_session(
        self, 
        session_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """Update session data"""
        try:
            client = await self.get_redis_client()
            session_key = f"{self.session_prefix}{session_id}"
            
            # Check if session exists
            if not await client.exists(session_key):
                return False
            
            # Prepare updates
            update_data = {
                "last_accessed": datetime.utcnow().isoformat()
            }
            
            for key, value in updates.items():
                if key == "user_data":
                    update_data[key] = json.dumps(value)
                else:
                    update_data[key] = str(value)
            
            await client.hset(session_key, mapping=update_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}")
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            client = await self.get_redis_client()
            session_key = f"{self.session_prefix}{session_id}"
            
            # Get user_id before deleting
            session_data = await client.hgetall(session_key)
            user_id = session_data.get("user_id")
            
            # Delete session
            deleted = await client.delete(session_key)
            
            # Delete user reference if it matches this session
            if user_id:
                user_key = f"{self.user_prefix}{user_id}"
                current_session = await client.get(user_key)
                if current_session == session_id:
                    await client.delete(user_key)
            
            logger.info(f"Deleted session {session_id}")
            return bool(deleted)
            
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False
    
    async def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get active session for a user"""
        try:
            client = await self.get_redis_client()
            user_key = f"{self.user_prefix}{user_id}"
            
            session_id = await client.get(user_key)
            if not session_id:
                return None
            
            return await self.get_session(session_id)
            
        except Exception as e:
            logger.error(f"Failed to get user session for {user_id}: {e}")
            return None
    
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions (called by background task)"""
        try:
            client = await self.get_redis_client()
            
            # Get all session keys
            session_keys = await client.keys(f"{self.session_prefix}*")
            cleaned = 0
            
            for key in session_keys:
                # Check if key still exists (Redis auto-expires)
                if not await client.exists(key):
                    cleaned += 1
            
            logger.info(f"Cleaned up {cleaned} expired sessions")
            return cleaned
            
        except Exception as e:
            logger.error(f"Failed to cleanup sessions: {e}")
            return 0
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()

# Global session manager instance
session_manager = SessionManager()