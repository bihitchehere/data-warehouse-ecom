import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# Load environment variables from .env file
load_dotenv()

def get_db_config():
    """
    Retrieves database credentials from the .env file.
    Provides defaults for localhost development.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "ecommerce_source"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASS"),
        "port": os.getenv("DB_PORT", "5432")
    }

def create_connection():
    """
    Creates and returns a connection object to the PostgreSQL database.
    """
    config = get_db_config()
    try:
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"]
        )
        return conn
    except OperationalError as e:
        print(f"❌ Error: Could not connect to the database.\nDetails: {e}")
        return None

# --- Self-Test Block ---
# This part only runs if you execute 'python config.py' directly
if __name__ == "__main__":
    print("--- Testing Database Connection Configuration ---")
    connection = create_connection()
    if connection:
        print("✅ SUCCESS: Python successfully connected to 'ecommerce_source'!")
        connection.close()
    else:
        print("💡 TIP: Check if your PostgreSQL service is running and your .env password is correct.")