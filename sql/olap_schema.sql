-- 1. Create a dedicated schema for the Warehouse
CREATE SCHEMA IF NOT EXISTS warehouse;

-- 2. dim_users (Dimension Table)
-- We keep the same basic info, but add an insertion_timestamp
CREATE TABLE IF NOT EXISTS warehouse.dim_users (
    user_key SERIAL PRIMARY KEY,      -- Surrogate Key for the Warehouse
    user_id INT UNIQUE,               -- Natural Key (ID from the Source)
    name VARCHAR(100),
    email VARCHAR(100),
    signup_date DATE,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. dim_products (Dimension Table)
CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    product_key SERIAL PRIMARY KEY,   -- Surrogate Key
    product_id INT UNIQUE,            -- Natural Key from Source
    name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. fact_sales (The Central Fact Table)
-- Note: We "flatten" the orders and order_items logic here.
-- One row here = One item sold.
CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    sale_key SERIAL PRIMARY KEY,
    order_id INT,                     -- Source Order ID
    user_id INT,                      -- Reference to dim_users
    product_id INT,                   -- Reference to dim_products
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),       -- Quantity * Unit Price
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


#change git ignore 