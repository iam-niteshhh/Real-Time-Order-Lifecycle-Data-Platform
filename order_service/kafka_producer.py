from kafka import KafkaProducer
import json
import uuid
from datetime import datetime


producer = KafkaProducer(
    value_serializer = lambda v: json.dumps(v).encode("utf-8"),
    bootstrap_server = "localhost:9092"
)

def send_event(event: dict):
    producer.send("order_events", value=event)
    producer.flush()
