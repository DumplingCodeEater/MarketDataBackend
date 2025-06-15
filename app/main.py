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
