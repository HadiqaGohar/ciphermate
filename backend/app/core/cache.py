"""Redis caching service for performance optimization"""

import json
import pickle
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Redis-based caching service for frequently accessed data"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.default_ttl = 3600  # 1 hour default TTL
        
        # Cache key prefixes for different data types
        self.prefixes = {
            "user": "user:",
            "service_connection": "conn:",
            "permission_template": "perm:",
            "audit_stats": "audit_stats:",
            "token_health": "token_health:",
            "api_response": "api:",
            "rate_limit": "rate:",
            "session": "session:",
        }
    
    async def get_redis_client(self) -> Optional[redis.Redis]:
        """Get Redis client instance"""
        if self.redis_client is None:
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=False,  # Handle binary data
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
                # Test connection
                await self.redis_client.ping()
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Running without cache.")
                self.redis_client = None
                return None
        return self.redis_client
    
    def _make_key(self, prefix: str, identifier: str) -> str:
        """Create a cache key with prefix"""
        return f"{self.prefixes.get(prefix, prefix)}{identifier}"
    
    async def get(self, key: str, prefix: str = "") -> Optional[Any]:
        """Get value from cache"""
        try:
            client = await self.get_redis_client()
            if client is None:
                return None
                
            cache_key = self._make_key(prefix, key) if prefix else key
            
            data = await client.get(cache_key)
            if data is None:
                return None
            
            # Try JSON first, then pickle for complex objects
            try:
                return json.loads(data)
            except (json.JSONDecodeError, TypeError):
                return pickle.loads(data)
                
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None, 
        prefix: str = ""
    ) -> bool:
        """Set value in cache"""
        try:
            client = await self.get_redis_client()
            if client is None:
                return False
                
            cache_key = self._make_key(prefix, key) if prefix else key
            ttl = ttl or self.default_ttl
            
            # Try JSON first, then pickle for complex objects
            try:
                data = json.dumps(value, default=str)
            except (TypeError, ValueError):
                data = pickle.dumps(value)
            
            await client.setex(cache_key, ttl, data)
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str, prefix: str = "") -> bool:
        """Delete value from cache"""
        try:
            client = await self.get_redis_client()
            cache_key = self._make_key(prefix, key) if prefix else key
            
            result = await client.delete(cache_key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str, prefix: str = "") -> bool:
        """Check if key exists in cache"""
        try:
            client = await self.get_redis_client()
            cache_key = self._make_key(prefix, key) if prefix else key
            
            result = await client.exists(cache_key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def get_many(self, keys: List[str], prefix: str = "") -> Dict[str, Any]:
        """Get multiple values from cache"""
        try:
            client = await self.get_redis_client()
            cache_keys = [self._make_key(prefix, key) if prefix else key for key in keys]
            
            values = await client.mget(cache_keys)
            result = {}
            
            for i, (original_key, data) in enumerate(zip(keys, values)):
                if data is not None:
                    try:
                        result[original_key] = json.loads(data)
                    except (json.JSONDecodeError, TypeError):
                        result[original_key] = pickle.loads(data)
            
            return result
            
        except Exception as e:
            logger.error(f"Cache get_many error: {e}")
            return {}
    
    async def set_many(
        self, 
        data: Dict[str, Any], 
        ttl: Optional[int] = None, 
        prefix: str = ""
    ) -> bool:
        """Set multiple values in cache"""
        try:
            client = await self.get_redis_client()
            ttl = ttl or self.default_ttl
            
            pipe = client.pipeline()
            
            for key, value in data.items():
                cache_key = self._make_key(prefix, key) if prefix else key
                
                try:
                    serialized_value = json.dumps(value, default=str)
                except (TypeError, ValueError):
                    serialized_value = pickle.dumps(value)
                
                pipe.setex(cache_key, ttl, serialized_value)
            
            await pipe.execute()
            return True
            
        except Exception as e:
            logger.error(f"Cache set_many error: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1, prefix: str = "") -> Optional[int]:
        """Increment a numeric value in cache"""
        try:
            client = await self.get_redis_client()
            cache_key = self._make_key(prefix, key) if prefix else key
            
            result = await client.incrby(cache_key, amount)
            return result
            
        except Exception as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None
    
    async def expire(self, key: str, ttl: int, prefix: str = "") -> bool:
        """Set expiration time for a key"""
        try:
            client = await self.get_redis_client()
            cache_key = self._make_key(prefix, key) if prefix else key
            
            result = await client.expire(cache_key, ttl)
            return result
            
        except Exception as e:
            logger.error(f"Cache expire error for key {key}: {e}")
            return False
    
    async def get_ttl(self, key: str, prefix: str = "") -> Optional[int]:
        """Get time to live for a key"""
        try:
            client = await self.get_redis_client()
            cache_key = self._make_key(prefix, key) if prefix else key
            
            ttl = await client.ttl(cache_key)
            return ttl if ttl >= 0 else None
            
        except Exception as e:
            logger.error(f"Cache get_ttl error for key {key}: {e}")
            return None
    
    async def flush_prefix(self, prefix: str) -> int:
        """Delete all keys with a specific prefix"""
        try:
            client = await self.get_redis_client()
            pattern = f"{self.prefixes.get(prefix, prefix)}*"
            
            keys = await client.keys(pattern)
            if keys:
                return await client.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache flush_prefix error for prefix {prefix}: {e}")
            return 0
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            client = await self.get_redis_client()
            info = await client.info()
            
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                ),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0),
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {}
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage"""
        total = hits + misses
        return (hits / total * 100) if total > 0 else 0.0
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Redis health"""
        try:
            client = await self.get_redis_client()
            if client is None:
                return {
                    "status": "unavailable",
                    "connected": False,
                    "message": "Redis not available, running without cache"
                }
            
            # Test basic operations
            test_key = "health_check_test"
            test_value = {"timestamp": datetime.utcnow().isoformat()}
            
            # Set test value
            await client.setex(test_key, 10, json.dumps(test_value))
            
            # Get test value
            retrieved = await client.get(test_key)
            if retrieved:
                retrieved_data = json.loads(retrieved)
                
            # Clean up
            await client.delete(test_key)
            
            # Get basic info
            info = await client.info()
            
            return {
                "status": "healthy",
                "connected": True,
                "test_passed": retrieved is not None,
                "uptime_seconds": info.get("uptime_in_seconds", 0),
                "memory_usage": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
            }
            
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "connected": False,
                "error": str(e),
                "test_passed": False,
            }
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            try:
                await self.redis_client.close()
            except Exception as e:
                logger.error(f"Error closing Redis connection: {e}")
            finally:
                self.redis_client = None


# Global cache service instance
cache_service = CacheService()


# Decorator for caching function results
def cached(ttl: int = 3600, prefix: str = "func"):
    """Decorator to cache function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key, prefix)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, ttl, prefix)
            
            return result
        return wrapper
    return decorator