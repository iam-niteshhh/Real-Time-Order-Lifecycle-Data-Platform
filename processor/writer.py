import json
import psycopg2

# use to save raw events data to json file
def write_json(data):
    with open("data/raw_data.json", 'a') as f:
        f.write(json.dumps(data, indent=4) + "\n")



db_connection = psycopg2.connect(
    host="localhost",
    database="orders_db",
    user="admin",
    password="admin"
)

cursor = db_connection.cursor()
# use to save processed events data to postgres database
def write_to_db(data):
    insert_query = """
    INSERT INTO orders (event_id ,order_id, event_type, service, timestamp)
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
        data['current_status'],
        data['timestamp']
    ))
    db_connection.commit()