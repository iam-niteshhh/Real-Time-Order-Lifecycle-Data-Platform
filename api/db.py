import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="orders_db",
        user="admin",
        password="admin"
    )
    return conn
