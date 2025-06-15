import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.db import Base, RawMarketData
from app.services.market_data_service import MarketDataService

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_store_and_get_price(db):
    service = MarketDataService(db)
    service.store_raw_market_data("AAPL", 123.45, "finnhub", {"raw": "data"})
    result = service.get_latest_price("AAPL")
    assert result is not None
    assert result.symbol == "AAPL"
    assert result.price == 123.45
