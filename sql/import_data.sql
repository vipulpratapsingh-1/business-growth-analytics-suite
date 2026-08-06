-- ============================================================
-- ETL Data Import Strategy & SQL Schema Documentation
-- BusinessGrowthDB Data Loading Guide
-- ============================================================

-- Note: In production enterprise environments, data is loaded from staging CSVs
-- using Python ETL pipelines or database bulk loaders (.import / COPY command).

-- Example Batch Insertion Structure for Reference:

-- 1. Populating Customers
-- INSERT OR IGNORE INTO Customers (customer_id, customer_name) VALUES ('CUST-10001', 'Aarav Sharma');

-- 2. Populating Products
-- INSERT OR IGNORE INTO Products (product_name, category) VALUES ('MacBook Pro 16-inch', 'Technology');

-- 3. Populating Orders
-- INSERT OR IGNORE INTO Orders (order_id, order_date, customer_id, city, state) 
-- VALUES ('ORD-2024-100001', '2023-01-01 00:00:38', 'CUST-10001', 'Mumbai', 'Maharashtra');

-- 4. Populating Sales
-- INSERT INTO Sales (order_id, product_id, quantity, unit_price, discount, sales_amount, profit_amount)
-- VALUES ('ORD-2024-100001', 1, 2, 219900.00, 0.10, 395820.00, 75205.80);

-- 5. Populating Payments
-- INSERT INTO Payments (order_id, payment_method, transaction_amount)
-- VALUES ('ORD-2024-100001', 'UPI', 395820.00);

-- The automated Python ETL runner (scripts/sql_integration.py) executes batch normalization
-- and population directly from data/clean_sales_data.csv into BusinessGrowthDB.sqlite.
