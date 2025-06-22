from abc import ABC, abstractmethod
from typing import Optional

class MarketDataProvider(ABC):
    @abstractmethod # type: ignore
    async def fetch_price(self, symbol: str) -> Optional[float]:
        """Fetch the latest price for a symbol."""
        pass

    @abstractmethod # type: ignore
    async def fetch_historical_prices(self, symbol: str, start_date: str, end_date: str) -> Optional[list]:
        """Fetch historical prices for a symbol between start_date and end_date."""
        pass
    @abstractmethod # type: ignore
    async def fetch_company_info(self, symbol: str) -> Optional[dict]:
        """Fetch company information for a given symbol."""
        pass