from fastapi import APIRouter
from api.db import get_db_connection
from order_service.service import create_order

router = APIRouter()

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT order_id, user_id, current_status, updated_at FROM orders WHERE order_id = %s",
        (order_id,)
    )

    order = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if order:
        return {
                "order_id": order[0],
                "user_id": order[1],
                "status": order[2],
                "updated_at": order[3]
            }    
    else:
        return {"error": "Order not found"}
    

@router.get("/orders/{order_id}/history")
def get_order_history(order_id: int):
    conn = get_db_connection()
    cusror = conn.cursor()

    cusror.execute(
        """
        SELECT event_type, service, timestamp
        FROM order_events
        WHERE order_id = %s
        ORDER BY timestamp
        """,
        (order_id,)
    )

    rows = cusror.fetchall()
    cusror.close()

    if rows:
        history = []
        for row in rows:
            history.append({
                "event_type": row[0],
                "service": row[1],
                "timestamp": row[2]
            })
        return {"order_id": order_id, "history": history}
    else:
        return {"error": "No history found for this order"}

@router.post("/order")
def order_endpoint(payload: dict):
    return create_order(payload)