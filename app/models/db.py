from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True)
    price = Column(Float)
    provider = Column(String)
    raw_response = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PollingJobConfig(Base):
    __tablename__ = "polling_job_configs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    symbols = Column(JSON) # Or use Array(String) if your DB supports it well
    interval = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Add other models like PricePoint, MovingAverage here if they are part of Base