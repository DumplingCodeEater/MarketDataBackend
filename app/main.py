from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.middleware import RateLimitMiddleware
from app.core.database import get_db
from sqlalchemy.orm import Session
import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Market Data Service",
    description="A service for fetching and processing market data from various providers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Include the main router
app.include_router(router, prefix="/prices")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    """Database health check endpoint."""
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@app.get("/health/redis")
async def redis_health_check():
    """Redis health check endpoint."""
    try:
        redis_client = redis.from_url(settings.redis_url)
        await redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": str(e)}

@app.on_event("shutdown")
async def shutdown_event():
    """Handle graceful shutdown."""
    # Close database connections
    db = next(get_db())
    db.close()
    
    # Close Redis connections
    redis_client = redis.from_url(settings.redis_url)
    await redis_client.close()
