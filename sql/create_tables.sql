-- ============================================================
-- Database Creation & DDL Schema: BusinessGrowthDB
-- Normalized 3NF Relational Structure with Primary & Foreign Keys
-- ============================================================

-- 1. Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL
);

-- 2. Products Table
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(150) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL
);

-- 3. Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date DATETIME NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- 4. Sales Table
CREATE TABLE IF NOT EXISTS Sales (
    sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(30) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    discount DECIMAL(4, 2) NOT NULL CHECK (discount >= 0.0 AND discount <= 1.0),
    sales_amount DECIMAL(12, 2) NOT NULL,
    profit_amount DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- 5. Payments Table
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(30) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    transaction_amount DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
