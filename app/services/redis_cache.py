import redis.asyncio as redis
from app.core.config import get_settings
from typing import Optional, Any, Callable
import json
from datetime import datetime

settings = get_settings()
REDIS_URL = settings.redis_url

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def set_cache(key: str, value: Any, expire: int = 300) -> None:
    """Set a value in the cache with expiration."""
    await redis_client.set(key, json.dumps(value), ex=expire)

async def get_cache(key: str) -> Optional[Any]:
    """Get a value from the cache."""
    value = await redis_client.get(key)
    if value is not None:
        return json.loads(value)
    return None

async def delete_cache(key: str) -> None:
    """Delete a value from the cache."""
    await redis_client.delete(key)

async def get_or_set_cache(key: str, fetch_func: Callable, expire: int = 300) -> Any:
    """
    Get a value from cache or fetch and cache it if not present.
    
    Args:
        key: Cache key
        fetch_func: Async function to fetch the value if not in cache
        expire: Cache expiration time in seconds (default: 300)
    
    Returns:
        The cached or freshly fetched value
    """
    # Try to get from cache first
    cached_value = await get_cache(key)
    if cached_value is not None:
        return cached_value
    
    # If not in cache, fetch the value
    value = await fetch_func()
    
    # Cache the value
    await set_cache(key, value, expire)
    
    return value
