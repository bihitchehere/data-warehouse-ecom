import sys
import os
import random
from faker import Faker
from psycopg2.extras import execute_values

# Setup paths to import your config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import create_connection

fake = Faker()

def is_table_empty(cursor, table_name):
    """DRY Helper: Checks if a table has 0 rows."""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] == 0

def populate_database():
    conn = create_connection()
    if not conn: return
    cur = conn.cursor()

    try:
        # --- 1. USERS (10,000) ---
        if is_table_empty(cur, "users"):
            print("Populating Users...")
            users = [(fake.name(), fake.unique.email(), fake.date_this_decade()) for _ in range(10000)]
            execute_values(cur, "INSERT INTO users (name, email, signup_date) VALUES %s", users)
            conn.commit()
        else:
            print("✅ Users exist. Skipping.")

        # --- 2. PRODUCTS (500) ---
        if is_table_empty(cur, "products"):
            print("Populating Products...")
            categories = ['Electronics', 'Books', 'Clothing', 'Home']
            products = [(fake.catch_phrase(), random.choice(categories), round(random.uniform(10, 1000), 2)) for _ in range(500)]
            execute_values(cur, "INSERT INTO products (name, category, price) VALUES %s", products)
            conn.commit()
        else:
            print("✅ Products exist. Skipping.")

        # --- 3. ORDERS (100,000) ---
        if is_table_empty(cur, "orders"):
            print("Populating Orders...")
            cur.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cur.fetchall()]
            orders = [(random.choice(user_ids), fake.date_this_decade(), abs(round(random.gauss(150, 50), 2))) for _ in range(100000)]
            execute_values(cur, "INSERT INTO orders (user_id, order_date, total_amount) VALUES %s", orders)
            conn.commit()
        else:
            print("✅ Orders exist. Skipping.")

        # --- 4. ORDER ITEMS (The Child Table) ---
        if is_table_empty(cur, "order_items"):
            print("Generating 1-5 items per order...")
            # Fetch parents and product prices
            cur.execute("SELECT id FROM orders")
            order_ids = [row[0] for row in cur.fetchall()]
            cur.execute("SELECT id, price FROM products")
            product_info = cur.fetchall() # List of tuples (id, price)

            items_to_insert = []
            for o_id in order_ids:
                # Generate 1 to 5 items for this specific order
                for _ in range(random.randint(1, 5)):
                    p_id, p_price = random.choice(product_info)
                    qty = random.randint(1, 10)
                    items_to_insert.append((o_id, p_id, qty, p_price))
                
                # Batch insert every 20,000 items to keep RAM clean
                if len(items_to_insert) >= 20000:
                    execute_values(cur, "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES %s", items_to_insert)
                    items_to_insert = []

            if items_to_insert:
                execute_values(cur, "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES %s", items_to_insert)
            
            conn.commit()
            print("✅ Order Items populated successfully!")
        else:
            print("✅ Order Items exist. Skipping.")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_database()