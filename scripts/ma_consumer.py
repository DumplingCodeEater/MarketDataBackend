from app.services.kafka_service import consume_price_events
from app.core.database import get_db
from app.models.db import PricePoint, MovingAverage
from sqlalchemy.orm import Session

def calculate_moving_average(prices):
    return sum(prices) / len(prices) if prices else None

def process_event(event):
    db: Session = next(get_db())
    symbol = event["symbol"]
    price = event["price"]
    timestamp = event["timestamp"]
    provider = event["source"]
    # Store price point
    db.add(PricePoint(symbol=symbol, price=price, timestamp=timestamp, provider=provider))
    db.commit()
    # Calculate MA
    last_5 = db.query(PricePoint).filter_by(symbol=symbol).order_by(PricePoint.timestamp.desc()).limit(5).all()
    if len(last_5) == 5:
        ma = calculate_moving_average([p.price for p in last_5])
        db.add(MovingAverage(symbol=symbol, average=ma, timestamp=timestamp, provider=provider))
        db.commit()

if __name__ == "__main__":
    consume_price_events(process_event)
