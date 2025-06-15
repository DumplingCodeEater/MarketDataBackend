from sqlalchemy.orm import Session
from app.models.db import RawMarketData, PricePoint
from datetime import datetime

class MarketDataService:
    def __init__(self, db: Session):
        self.db = db

    def store_raw_market_data(self, symbol: str, price: float, provider: str, raw_response: dict):
        data = RawMarketData(
            symbol=symbol,
            price=price,
            provider=provider,
            raw_response=raw_response,
            timestamp=datetime.utcnow()
        )
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def get_latest_price(self, symbol: str):
        return self.db.query(RawMarketData).filter_by(symbol=symbol).order_by(RawMarketData.timestamp.desc()).first()
