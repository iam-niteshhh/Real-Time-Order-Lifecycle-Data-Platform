from fastapi import APIRouter
from api.db import get_db_connection

router = APIRouter()

@router.get("/metrics/orders/count")
def get_order_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    print("connected to database for metrics")
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    metrics = {
        "total_orders": total_orders,
    }
    
    return metrics

@router.get("/metrics/orders/status")
def get_order_status_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT current_status, COUNT(*)
        FROM orders
        GROUP BY current_status
        """
    )
    status_counts = cursor.fetchall()

    cursor.close()
    conn.close()

    metrics = {status: count for status, count in status_counts}
    
    return metrics