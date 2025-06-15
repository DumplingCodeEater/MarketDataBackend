from abc import ABC, abstractmethod
from typing import Optional

class MarketDataProvider(ABC):
    @abstractmethod
    async def fetch_price(self, symbol: str) -> Optional[float]:
        """Fetch the latest price for a given symbol."""
        pass