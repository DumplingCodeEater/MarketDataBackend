from abc import ABC, abstractmethod
from typing import Optional
import requests
from app.core.config import get_settings

class MarketDataProvider(ABC):
    @abstractmethod
    def fetch_price(self, symbol: str) -> Optional[float]:
        """Fetch the latest price for a symbol."""
        pass

class FinnhubProvider(MarketDataProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.finnhub_api_key

    def fetch_price(self, symbol: str) -> Optional[float]:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("c")  # Current price
        except Exception:
            return None

# Dependency for FastAPI
finnhub_provider = FinnhubProvider()
def get_market_data_provider():
    return finnhub_provider
