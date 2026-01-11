import sys
import os
import random
from faker import Faker
import psycopg2
from psycopg2.extras import execute_values  # For high-speed batch inserts

# Ensure Python can find config.py in the root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import create_connection

fake = Faker()

def populate_database():
    conn = create_connection()
    if not conn:
        return
    
    cur = conn.cursor()

    try:
        # --- 1. GENERATE 10,000 USERS ---
        print("Inserting 10,000 users...")
        users_data = [
            (fake.name(), fake.unique.email(), fake.date_this_decade()) 
            for _ in range(10000)
        ]
        execute_values(cur, "INSERT INTO users (name, email, signup_date) VALUES %s", users_data)
        conn.commit()

        # --- 2. GENERATE 500 PRODUCTS ---
        print("Inserting 500 products...")
        categories = ['Electronics', 'Books', 'Clothing', 'Home']
        products_data = [
            (fake.catch_phrase(), random.choice(categories), round(random.uniform(10, 1000), 2))
            for _ in range(500)
        ]
        execute_values(cur, "INSERT INTO products (name, category, price) VALUES %s", products_data)
        conn.commit()

        # --- 3. GENERATE 500,000 ORDERS ---
        # First, fetch existing user IDs to ensure Referential Integrity
        cur.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cur.fetchall()]
        
        print("Generating 500,000 orders (Batch Processing)...")
        orders_data = []
        for _ in range(500000):
            user_id = random.choice(user_ids)
            order_date = fake.date_between(start_date='-2y', end_date='today')
            # Gauss: Mean=150, StdDev=50 (Most orders between $100-$200)
            amount = abs(round(random.gauss(150, 50), 2))
            
            orders_data.append((user_id, order_date, amount))

            # Insert in chunks of 10,000 to keep memory low
            if len(orders_data) >= 10000:
                execute_values(cur, "INSERT INTO orders (user_id, order_date, total_amount) VALUES %s", orders_data)
                orders_data = [] # Clear the list for next batch
        
        # Insert any remaining orders
        if orders_data:
            execute_values(cur, "INSERT INTO orders (user_id, order_date, total_amount) VALUES %s", orders_data)
        
        conn.commit()
        print("✅ Successfully inserted all data!")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    populate_database()