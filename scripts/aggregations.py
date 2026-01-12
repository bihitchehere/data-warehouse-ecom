import duckdb
import pandas as pd
import os

def run_analytics_pipeline():
    """
    Connects to the DuckDB warehouse and generates 
    key business metric reports.
    """
    db_path = 'olap.duckdb'
    output_dir = 'reports'

    # Check if warehouse exists
    if not os.path.exists(db_path):
        print(f"⚠️ Error: {db_path} not found. Did you run the ETL script first?")
        return

    # Create reports folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize connection
    con = duckdb.connect(db_path)
    print("🚀 Connected to Warehouse. Generating reports...")

    try:
        # 1. DAILY REVENUE & ORDER VOLUME
        print("📊 Processing Daily Revenue and Order counts...")
        daily_stats_sql = """
            SELECT 
                order_date, 
                COUNT(DISTINCT order_id) AS total_orders,
                ROUND(SUM(revenue), 2) AS gross_revenue
            FROM fact_orders
            GROUP BY 1
            ORDER BY 1 ASC
        """
        con.execute(daily_stats_sql).df().to_csv(f"{output_dir}/daily_performance.csv", index=False)

        # 2. TOP 10 PRODUCTS BY REVENUE
        # Using a JOIN to get the human-readable product name
        print("🔝 Identifying Top 10 Best-Selling Products...")
        top_products_sql = """
            SELECT 
                p.name AS product_name, 
                ROUND(SUM(f.revenue), 2) AS total_revenue,
                SUM(f.quantity) AS total_units_sold
            FROM fact_orders f
            JOIN dim_products p ON f.product_id = p.id
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 10
        """
        con.execute(top_products_sql).df().to_csv(f"{output_dir}/top_products.csv", index=False)

        # 3. CUSTOMER ENGAGEMENT (Active Users)
        print("👥 Calculating Daily Active Users (DAU)...")
        dau_sql = """
            SELECT 
                order_date, 
                COUNT(DISTINCT user_id) AS unique_customers
            FROM fact_orders
            GROUP BY 1
            ORDER BY 1
        """
        con.execute(dau_sql).df().to_csv(f"{output_dir}/active_users.csv", index=False)

        print(f"\n✅ All reports exported successfully to the '/{output_dir}' folder!")

    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
    
    finally:
        con.close()
        print("🔌 Warehouse connection closed.")

if __name__ == "__main__":
    run_analytics_pipeline()