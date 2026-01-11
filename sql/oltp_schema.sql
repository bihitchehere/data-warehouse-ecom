-- Clean up existing tables if they exist (Run in reverse order of creation)

\c ecommerce_source;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- 1. Users Dimension
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    signup_date DATE DEFAULT CURRENT_DATE
);

-- 2. Products Dimension
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- 3. Orders (Fact Header)
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Order Items (The Grain / Fact Detail)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_order FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
);
create table test(
    id FLOAT NOT NULL 
) ; 
SELECT current_database();


