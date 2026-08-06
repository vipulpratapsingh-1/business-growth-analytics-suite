-- ============================================================
-- Database Performance Optimization: Indexes for BusinessGrowthDB
-- Accelerates JOINs, Aggregations, Filtering, and Window Functions
-- ============================================================

-- 1. Index on Orders(order_date) for fast date-range filtering and time-series trends
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON Orders(order_date);

-- 2. Index on Orders(customer_id) for customer analysis & JOINs
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON Orders(customer_id);

-- 3. Index on Orders(city, state) for regional aggregation queries
CREATE INDEX IF NOT EXISTS idx_orders_location ON Orders(city, state);

-- 4. Index on Sales(order_id) for relational JOINs between Orders & Sales
CREATE INDEX IF NOT EXISTS idx_sales_order_id ON Sales(order_id);

-- 5. Index on Sales(product_id) for product performance JOINs
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON Sales(product_id);

-- 6. Index on Products(category) for category filtering & grouping
CREATE INDEX IF NOT EXISTS idx_products_category ON Products(category);

-- 7. Index on Payments(order_id, payment_method) for payment channel analysis
CREATE INDEX IF NOT EXISTS idx_payments_order_method ON Payments(order_id, payment_method);
