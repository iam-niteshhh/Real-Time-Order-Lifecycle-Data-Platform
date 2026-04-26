from kafka import KafkaProducer
import json


producer = KafkaProducer(
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
    bootstrap_server = "localhost:9092"
)

def send_event(event):
    producer.send("order-events", value=event)
    producer.flush()