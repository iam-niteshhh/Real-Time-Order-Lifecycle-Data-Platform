import random
import uuid
from datetime import datetime
from producer import send_event

def process_payment(event):
    order_id = event_id.get("order_id")

    # simulate success/failure
    success = random.choice([True, True, False, True])

    payment_event = {
        "event_id": str(uuid.uuid4())
        "order_id": order_id,
        "user_id": event.get("user_id"),
        "event_type": "payment_success" if success else "payment_failed",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "payment-service",
        "amount": event.get("amount"),
        "status": "success" if success else "failed"
    }

    send_event(payment_event)