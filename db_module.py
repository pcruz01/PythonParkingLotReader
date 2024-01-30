# db_module.py
import psycopg2

def connect_to_db():
    # Replace the following with your actual database connection details
    dbname = 'ParkingVerse_DB'
    user = 'postgres'
    password = 'IAmElonMuskrat'
    host = 'localhost'
    port = '5432'

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return conn

def perform_query(conn, lotID, available_spots):
    cursor = conn.cursor()

    try:
        # Example query: Update available_spots in 'lot_info' table
        cursor.execute("UPDATE lot_info SET available_spots = %s WHERE \"lotID\" = %s", (available_spots, lotID))
        conn.commit()
        print("Query executed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
