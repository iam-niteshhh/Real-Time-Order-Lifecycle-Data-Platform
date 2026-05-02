import json
import psycopg2
import os
import time

MAX_ATTEMPTS = 3
# use to save raw events data to json file
def write_json(data):
    order_id = data.get("order_id")
    if not order_id:
        raise ValueError("order_id is required")

    dir_path = "data/orders"
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{order_id}.jsonl")

    with open(file_path, "a") as f:
        f.write(json.dumps(data) + "\n")



db_connection = psycopg2.connect(
    host="localhost",
    database="orders_db",
    user="admin",
    password="admin"
)

cursor = db_connection.cursor()
# use to save processed events data to postgres database
def write_to_db(data):
    for attempt in range(MAX_ATTEMPTS):
        try:
            insert_query = """
            INSERT INTO order_events (event_id ,order_id, event_type, service, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (event_id) DO NOTHING;
            """
            cursor.execute(insert_query, (
                data['event_id'],
                data['order_id'],
                data['event_type'],
                data['service'],
                data['timestamp']
            ))
            db_connection.commit()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            db_connection.rollback()
            time.sleep(2 ** attempt)  # Exponential backoff
    print("All attempts to write to database failed.")
    return False

def upsert_order(data):
    update_query = """
    INSERT INTO orders (order_id, user_id, current_status, updated_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (order_id)
    DO UPDATE SET
        current_status = EXCLUDED.current_status,
        updated_at = EXCLUDED.updated_at;
    """
    cursor.execute(update_query, (
        data['order_id'],
        data['user_id'],
        data['status'],
        data['timestamp']
    ))
    db_connection.commit()