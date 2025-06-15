from abc import ABC, abstractmethod
from typing import Optional
import requests
from app.core.config import get_settings
from app.services.base_provider import MarketDataProvider
import os

class FinnhubProvider(MarketDataProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY") or getattr(self.settings, "finnhub_api_key", None)
        if not self.api_key:
            raise ValueError("Finnhub API key is missing. Set FINNHUB_API_KEY in your environment or .env file.")

    def fetch_price(self, symbol: str) -> Optional[float]:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("c")  # Current price
        except Exception:
            return None

def get_market_data_provider(provider: Optional[str] = "finnhub") -> MarketDataProvider:
    provider = (provider or "finnhub").strip().lower()
    if provider == "finnhub":
        return FinnhubProvider()
    
    # Add more providers here as needed
    else:
        raise ValueError(f"Unknown provider: {provider}")
