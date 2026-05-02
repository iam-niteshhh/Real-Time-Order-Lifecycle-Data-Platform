from kafka import KafkaConsumer
import json
from service import process_payment

consumer = KafkaConsumer(
    "order_events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="payment-group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

for message in consumer:

    event = message.value
    print(f"Received event for event: {event.get('event_type')} - order_id: {event.get('order_id')}")
    if event.get("event_type") == "order_created":
        print(f"Processing payment for order: {event.get('order_id')}")
        process_payment(event)