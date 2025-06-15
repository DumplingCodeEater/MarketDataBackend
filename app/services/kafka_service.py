from confluent_kafka import Producer, Consumer, KafkaException
import json, time
from app.schemas.kafka_messages import PriceEventMessage
from typing import Callable

KAFKA_BROKER = "kafka:9092"
PRICE_TOPIC = "price-events"
AVG_TOPIC = "symbol-averages"

# Producer setup
_Producer = None
def get_kafka_producer() -> Producer:
    global _Producer
    if _Producer is None:
        _Producer = Producer({'bootstrap.servers': KAFKA_BROKER})
    return _Producer

def publish_price_event(event: PriceEventMessage):
    producer = get_kafka_producer()
    message = event.json()
    for _ in range(3):
        try:
            producer.produce(PRICE_TOPIC, message.encode())
            producer.flush()
            return
        except KafkaException:
            time.sleep(1)
    raise RuntimeError("Failed to publish price event after retries.")

# Consumer setup
def get_kafka_consumer(group_id: str = "ma-consumer") -> Consumer:
    return Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

def consume_price_events(process_fn: Callable[[PriceEventMessage], None]):
    consumer = get_kafka_consumer()
    consumer.subscribe([PRICE_TOPIC])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None or msg.error():
                continue
            try:
                data = json.loads(msg.value())
                event = PriceEventMessage.parse_obj(data)
                process_fn(event)
            except Exception as e:
                # Optionally log or handle malformed messages
                continue
    finally:
        consumer.close()
