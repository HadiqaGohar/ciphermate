"""
Redis handler with graceful fallback for Cloud Run deployment
"""

import logging
import redis
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisHandler:
    """Redis handler that gracefully handles connection failures"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.redis_available = False
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection if not disabled"""
        if settings.DISABLE_REDIS:
            logger.info("Redis is disabled via DISABLE_REDIS setting")
            return

        # Use validated Redis URL
        redis_url = settings.redis_url_validated
        
        if not redis_url:
            logger.info("Redis URL not configured or invalid, running without cache")
            return

        try:
            # Upstash requires rediss:// (TLS) or redis:// with ssl_cert_reqs=None
            if "upstash.io" in redis_url:
                # Ensure URL uses rediss:// for TLS
                if redis_url.startswith("redis://"):
                    redis_url = redis_url.replace("redis://", "rediss://", 1)
                    logger.info(f"🔒 Converting to TLS: {redis_url[:30]}...")
                
                self.redis_client = redis.from_url(
                    redis_url,
                    ssl_cert_reqs=None,  # Disable SSL certificate verification
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_keepalive=True
                )
                logger.info("Connecting to Upstash Redis with TLS...")
            else:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                logger.info(f"Connecting to Redis at {redis_url}...")

            # Test connection with ping
            self.redis_client.ping()
            self.redis_available = True
            logger.info("✅ Redis connection established successfully")

        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Running without cache.")
            self.redis_client = None
            self.redis_available = False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis with fallback"""
        if not self.redis_available or not self.redis_client:
            return None
        
        try:
            return self.redis_client.get(key)
        except Exception as e:
            logger.warning(f"Redis GET failed for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Set value in Redis with fallback"""
        if not self.redis_available or not self.redis_client:
            return False
        
        try:
            return self.redis_client.set(key, value, ex=ex)
        except Exception as e:
            logger.warning(f"Redis SET failed for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis with fallback"""
        if not self.redis_available or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.warning(f"Redis DELETE failed for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis with fallback"""
        if not self.redis_available or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.warning(f"Redis EXISTS failed for key {key}: {e}")
            return False
    
    def info(self) -> dict:
        """Get Redis info with fallback"""
        if not self.redis_available or not self.redis_client:
            return {"status": "disabled", "available": False}
        
        try:
            info = self.redis_client.info()
            return {"status": "connected", "available": True, "info": info}
        except Exception as e:
            logger.warning(f"Redis INFO failed: {e}")
            return {"status": "error", "available": False, "error": str(e)}

# Global Redis handler instance
redis_handler = RedisHandler()