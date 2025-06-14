from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid

Base = declarative_base()

class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    provider = Column(String, nullable=False)
    raw_response = Column(JSON, nullable=False)

class PricePoint(Base):
    __tablename__ = "price_points"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    provider = Column(String, nullable=False)

class MovingAverage(Base):
    __tablename__ = "moving_averages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, index=True, nullable=False)
    average = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    provider = Column(String, nullable=False)

class PollingJobConfig(Base):
    __tablename__ = "polling_job_configs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, unique=True, nullable=False)
    symbols = Column(JSON, nullable=False)
    interval = Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Index('ix_price_points_symbol_timestamp', PricePoint.symbol, PricePoint.timestamp)
Index('ix_moving_averages_symbol_timestamp', MovingAverage.symbol, MovingAverage.timestamp)
