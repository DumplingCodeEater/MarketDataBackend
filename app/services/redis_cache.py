import redis.asyncio as redis
from app.core.config import get_settings
from typing import Optional, Any
import json
from datetime import datetime

settings = get_settings()
REDIS_URL = settings.redis_url

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def set_cache(key: str, value: Any, expire: int = 300) -> None:
    """Set a value in the cache with expiration."""
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    await redis_client.set(key, value, ex=expire)

async def get_cache(key: str) -> Optional[Any]:
    """Get a value from the cache."""
    value = await redis_client.get(key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value

async def delete_cache(key: str) -> None:
    """Delete a value from the cache."""
    await redis_client.delete(key)

async def get_or_set_cache(key: str, fetch_func, expire: int = 300) -> Any:
    """Get from cache or fetch and set if not exists."""
    cached_value = await get_cache(key)
    if cached_value is not None:
        return cached_value
    
    value = await fetch_func()
    if value is not None:
        await set_cache(key, value, expire)
    return value
