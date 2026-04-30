import random
import uuid
import time
from datetime import datetime
from kafka_producer import send_event

def process_delivery(event):
    order_id = event.get("order_id")
    
    # Step 1: shipped
    shipped_event = {
        "event_id": str(uuid.uuid4()),
        "order_id": order_id,
        "user_id": event["user_id"],
        "event_type": "order_shipped",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "delivery-service",
        "status": "shipped"
    }

    send_event(shipped_event)

     # simulate delay (real-world async gap)
    time.sleep(2)

    # Step 2: delivered
    delivered_event = {
        "event_id": str(uuid.uuid4()),
        "order_id": order_id,
        "user_id": event["user_id"],
        "event_type": "order_delivered",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "delivery-service",
        "status": "delivered"
    }

    send_event(delivered_event)