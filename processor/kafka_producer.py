from kafka import KafkaProducer
import json

dlq_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_dlq(event):
    dlq_producer.send("dlq_events", event)
    print("Sent to DLQ:", event['order_id'])