from fastapi import APIRouter, Depends, status, HTTPException, Query 
from typing import Optional, List
from uuid import uuid4
from datetime import datetime

from app.services.finnhub_provider import get_market_data_provider, MarketDataProvider
from app.schemas.prices import PollRequest, PollResponse, LatestPriceResponse
from app.services.redis_cache import get_or_set_cache
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/latest", 
    response_model=LatestPriceResponse,
    responses={
        200: {
            "description": "Successfully retrieved the latest price",
            "content": {
                "application/json": {
                    "example": {
                        "symbol": "AAPL",
                        "price": 150.25,
                        "timestamp": "2024-03-20T10:30:00Z",
                        "provider": "finnhub"
                    }
                }
            }
        },
        400: {"description": "Invalid provider specified"},
        429: {"description": "Rate limit exceeded"},
        502: {"description": "Failed to fetch price from provider"}
    }
)
async def get_latest_price(
    symbol: str = Query(..., description="Stock symbol to fetch price for", example="AAPL"),
    provider: Optional[str] = Query("finnhub", description="Data provider to use", example="finnhub"),
    db: Session = Depends(get_db)
) -> LatestPriceResponse:
    """
    Get the latest price for a given symbol from the selected provider.
    
    - **symbol**: Stock symbol to fetch price for (e.g., AAPL, MSFT)
    - **provider**: Data provider to use (default: finnhub)
    
    Returns the latest price with timestamp and provider information.
    """
    try:
        market_data_provider: MarketDataProvider = get_market_data_provider(provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Use cache with 5-minute expiration
    cache_key = f"price:{symbol}:{provider}"
    
    async def fetch_price():
        price = market_data_provider.fetch_price(symbol.upper())
        if price is None:
            raise HTTPException(status_code=502, detail="Failed to fetch price from provider.")
        return price

    price = await get_or_set_cache(cache_key, fetch_price, expire=300)
    
    return LatestPriceResponse(
        symbol=symbol.upper(),
        price=price,
        timestamp=datetime.utcnow().isoformat(),
        provider=provider
    )

@router.post("/poll", 
    response_model=PollResponse, 
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {
            "description": "Polling job accepted",
            "content": {
                "application/json": {
                    "example": {
                        "job_id": "poll_abc123",
                        "status": "accepted",
                        "config": {
                            "symbols": ["AAPL", "MSFT"],
                            "interval": 60
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid request parameters"},
        429: {"description": "Rate limit exceeded"}
    }
)
async def poll_prices(
    request: PollRequest,
    db: Session = Depends(get_db)
) -> PollResponse:
    """
    Start a polling job for a list of symbols at a given interval.
    
    - **symbols**: List of stock symbols to poll
    - **interval**: Polling interval in seconds (minimum: 60)
    
    Returns a job ID and configuration details.
    """
    if request.interval < 60:
        raise HTTPException(
            status_code=400,
            detail="Interval must be at least 60 seconds"
        )

    job_id = f"poll_{uuid4().hex[:8]}"

    return PollResponse(
        job_id=job_id,
        status="accepted",
        config={
            "symbols": request.symbols,
            "interval": request.interval
        }
    )