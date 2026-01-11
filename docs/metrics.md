# E-commerce Data Warehouse: Metrics & Domain Definition

## 1. Business Domain
**Domain:** E-commerce Platform  
**Focus:** Sales performance, customer behavior, and inventory movement.

## 2. Business Questions
The warehouse must be able to answer:
* What is our **daily revenue trend**?
* Which **product categories** are driving the most profit?
* Who are our **top 10% of customers** by lifetime value?
* Are there specific times of day when **order volume spikes**?

## 3. Key Metrics
| Metric | Calculation | Frequency |
| :--- | :--- | :--- |
| **Total Revenue** | Sum of `price * quantity` | Daily |
| **Order Count** | Count of unique `order_id` | Daily |
| **AOV (Avg Order Value)** | Total Revenue / Order Count | Monthly |
| **DAU (Daily Active Users)** | Count of unique `user_id` with an order | Daily |
| **Top Products** | Products ranked by total quantity sold | Weekly |

## 4. Data Grain
**Definition:** **One row per order line item.**
* **Why?** This allows us to analyze individual product performance while still being able to aggregate upwards to the total order or total customer level.

## 5. Entities (The Schema)
* **Users:** Demographics and account info.
* **Products:** Catalog details, pricing, and categories.
* **Orders:** Header level info (timestamp, status).
* **Order_Items:** The grain level (which product, what price, what quantity).