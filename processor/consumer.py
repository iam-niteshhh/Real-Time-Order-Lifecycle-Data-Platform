from kafka import KafkaConsumer
import json
from writer import write_json, write_to_db, upsert_order

consumer = KafkaConsumer(
    'order_events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='processor_group',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

for message in consumer:
    event_data = message.value
    print(f"Received event for event: {event_data.get('event_type')} - order_id: {event_data.get('order_id')}")

    # store raw data to json file
    write_json(event_data)


    # store structured data to postgres database
    write_to_db(event_data)

    # update order status in orders table
    print(f"event {event_data}")
    upsert_order(event_data)