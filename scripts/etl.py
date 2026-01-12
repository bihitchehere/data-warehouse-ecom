import pandas as pd
import duckdb
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_etl():
    # --- PHASE 10: EXTRACT ---
    try:
        # Create connection to PostgreSQL
        conn_pg = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Connected to PostgreSQL (Source)")

        print("📥 Extracting data...")
        df_users = pd.read_sql("SELECT * FROM users", conn_pg)
        df_products = pd.read_sql("SELECT * FROM products", conn_pg)
        df_orders = pd.read_sql("SELECT * FROM orders", conn_pg)
        df_order_items = pd.read_sql("SELECT * FROM order_items", conn_pg)

        # --- PHASE 11: TRANSFORM ---
        print("🔄 Transforming data...")
        
        # Merge orders and items to create the base for the Fact table
        df_fact = pd.merge(df_orders, df_order_items, left_on='id', right_on='order_id', suffixes=('_ord', '_itm'))
        
        # Calculate revenue: quantity * price
        df_fact['revenue'] = df_fact['quantity'] * df_fact['price']
        
        # Transform date columns to proper datetime format
        df_fact['order_date'] = pd.to_datetime(df_fact['order_date'])
        
        # Clean up columns for the final fact table
        df_fact = df_fact[['id_itm', 'id_ord', 'user_id', 'product_id', 'order_date', 'quantity', 'price', 'revenue']]
        df_fact.columns = ['line_item_id', 'order_id', 'user_id', 'product_id', 'order_date', 'quantity', 'unit_price', 'revenue']

        # --- PHASE 12: LOAD ---
        print("🚀 Loading into DuckDB Warehouse...")
        
        # Create connection to DuckDB (creates olap.duckdb file)
        con_olap = duckdb.connect('olap.duckdb')

        # Load dim_users and dim_products
        con_olap.execute("CREATE TABLE IF NOT EXISTS dim_users AS SELECT * FROM df_users")
        con_olap.execute("CREATE TABLE IF NOT EXISTS dim_products AS SELECT * FROM df_products")
        
        # Load fact_orders
        con_olap.execute("CREATE TABLE IF NOT EXISTS fact_orders AS SELECT * FROM df_fact")

        # Create dim_date by extracting unique dates
        con_olap.execute("""
            CREATE TABLE IF NOT EXISTS dim_date AS
            SELECT 
                DISTINCT order_date AS date,
                EXTRACT(year FROM order_date) AS year,
                EXTRACT(month FROM order_date) AS month,
                EXTRACT(day FROM order_date) AS day,
                EXTRACT(dayofweek FROM order_date) AS day_of_week
            FROM fact_orders
        """)

        print("✅ ETL Process Finished Successfully!")

    except Exception as e:
        print(f"❌ ETL Error: {e}")
    
    finally:
        if 'conn_pg' in locals():
            conn_pg.close()
        if 'con_olap' in locals():
            con_olap.close()

if __name__ == "__main__":
    run_etl()