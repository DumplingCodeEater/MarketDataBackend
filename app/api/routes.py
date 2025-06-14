from fastapi import APIRouter, Depends, status
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.config import get_settings
from app.services.finnhub_provider import fetch_finnhub_price
from app.models.prices import PollRequest, PollResponse, LatestPriceResponse

router = APIRouter()

# Placeholder DB simulation
mock_prices = {
    "AAPL": 150.25,
    "MSFT": 310.75,
}

@router.get("/latest", response_model=LatestPriceResponse)
def get_latest_price(symbol: str, provider: Optional[str] = "finnhub", settings=Depends(get_settings)):
    price = fetch_finnhub_price(symbol.upper()) or 100.00
    return {
        "symbol": symbol.upper(),
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "provider": provider
    }

@router.post("/poll", response_model=PollResponse, status_code=status.HTTP_202_ACCEPTED)
def poll_prices(request: PollRequest, settings=Depends(get_settings)):
    job_id = f"poll_{uuid4().hex[:8]}"
    return {
        "job_id": job_id,
        "status": "accepted",
        "config": {
            "symbols": request.symbols,
            "interval": request.interval
        }
    }