import uuid
from datetime import datetime
from order_service.kafka_producer import send_event


def create_order(data):
    order_id = f"ORD_{uuid.uuid4().hex[:8]}"

    event = {
        "event_id": str(uuid.uuid4()),
        "order_id": order_id,
        "user_id": data["user_id"],
        "event_type": "order_created",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "order-service",
        "amount": data["amount"],
        "status": "created"
    }
    
    send_event(event)

    return {
        "order_id":order_id,
        "status": "created"
    }