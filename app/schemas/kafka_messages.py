from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from uuid import UUID

class PriceEventMessage(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    source: Literal["finnhub", "alpha_vantage", "yahoo"]
    raw_response_id: UUID