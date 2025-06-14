import requests
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

def fetch_finnhub_price(symbol: str) -> Optional[float]:
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={settings.finnhub_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("c")  # Current price
    return None
