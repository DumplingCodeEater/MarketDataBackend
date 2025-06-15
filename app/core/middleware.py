from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from app.services.redis_cache import redis_client
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Create a key for this IP
        key = f"rate_limit:{client_ip}"
        
        # Get current count and timestamp
        current = await redis_client.get(key)
        
        if current is None:
            # First request from this IP
            await redis_client.set(key, 1, ex=60)
        else:
            current = int(current)
            if current >= self.requests_per_minute:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )
            await redis_client.incr(key)
        
        response = await call_next(request)
        return response 