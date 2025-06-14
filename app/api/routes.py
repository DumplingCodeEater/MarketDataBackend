from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.config import get_settings
from app.services.finnhub_provider import get_market_data_provider, MarketDataProvider
from app.schemas.prices import PollRequest, PollResponse, LatestPriceResponse

router = APIRouter()

@router.get("/latest", response_model=LatestPriceResponse)
def get_latest_price(
    symbol: str,
    provider: Optional[str] = "finnhub",
    settings=Depends(get_settings),
    market_data_provider: MarketDataProvider = Depends(get_market_data_provider)
) -> LatestPriceResponse:
    """
    Get the latest price for a given symbol from the selected provider.
    """
    price = market_data_provider.fetch_price(symbol.upper())
    if price is None:
        raise HTTPException(status_code=502, detail="Failed to fetch price from provider.")
    return LatestPriceResponse(
        symbol=symbol.upper(),
        price=price,
        timestamp=datetime.utcnow().isoformat(),
        provider=provider
    )

@router.post("/poll", response_model=PollResponse, status_code=status.HTTP_202_ACCEPTED)
def poll_prices(
    request: PollRequest,
    settings=Depends(get_settings)
) -> PollResponse:
    """
    Start a polling job for a list of symbols at a given interval.
    """
    job_id = f"poll_{uuid4().hex[:8]}"
    return PollResponse(
        job_id=job_id,
        status="accepted",
        config={
            "symbols": request.symbols,
            "interval": request.interval
        }
    )