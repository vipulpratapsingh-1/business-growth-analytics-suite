# Relational Database Design & Data Warehousing (3NF)

**Database**: `BusinessGrowthDB.sqlite`  
**Engine**: SQLite 3 / ANSI-SQL Relational Standard  
**Normal Form**: Third Normal Form (3NF)  
**Total Tables**: 5 Relational Tables  
**Total Records**: 100,000 Transactions  

---

## 1. Entity-Relationship (ER) Schema

```text
+-------------------+       +-------------------+       +-------------------+
|     Customers     |       |      Orders       |       |     Payments      |
+-------------------+       +-------------------+       +-------------------+
| customer_id (PK)  |<----->| order_id (PK)     |<----->| payment_id (PK)   |
| customer_name     |       | order_date        |       | order_id (FK)     |
+-------------------+       | customer_id (FK)  |       | payment_method    |
                            | city              |       | transaction_amount|
                            | state             |       +-------------------+
                            +-------------------+
                                      ^
                                      |
                                      v
                            +-------------------+       +-------------------+
                            |       Sales       |       |     Products      |
                            +-------------------+       +-------------------+
                            | sales_id (PK)     |       | product_id (PK)   |
                            | order_id (FK)     |<----->| product_name      |
                            | product_id (FK)   |       | category          |
                            | quantity          |       +-------------------+
                            | unit_price        |
                            | discount          |
                            | sales_amount      |
                            | profit_amount     |
                            +-------------------+
```

---

## 2. Table Specifications & Constraints

### 1. `Customers` Table
- `customer_id` (VARCHAR(20), PRIMARY KEY): Unique customer identifier (`CUST-10001` to `CUST-15000`).
- `customer_name` (VARCHAR(100), NOT NULL): Full name of buyer.

### 2. `Products` Table
- `product_id` (INTEGER, PRIMARY KEY AUTOINCREMENT): Unique surrogate product key.
- `product_name` (VARCHAR(150), UNIQUE, NOT NULL): Product title.
- `category` (VARCHAR(50), NOT NULL): Merchandise category (`Technology`, `Furniture`, `Office Supplies`).

### 3. `Orders` Table
- `order_id` (VARCHAR(30), PRIMARY KEY): Unique order transaction code (`ORD-2024-XXXXXX`).
- `order_date` (DATETIME, NOT NULL): Timestamp of sale.
- `customer_id` (VARCHAR(20), FOREIGN KEY -> `Customers.customer_id`).
- `city` (VARCHAR(50), NOT NULL): Commercial hub city.
- `state` (VARCHAR(50), NOT NULL): State location.

### 4. `Sales` Table
- `sales_id` (INTEGER, PRIMARY KEY AUTOINCREMENT): Line item surrogate key.
- `order_id` (VARCHAR(30), FOREIGN KEY -> `Orders.order_id`).
- `product_id` (INTEGER, FOREIGN KEY -> `Products.product_id`).
- `quantity` (INTEGER, CHECK(quantity > 0)): Units purchased.
- `unit_price` (DECIMAL(10,2), CHECK(unit_price > 0)): Base price per unit.
- `discount` (DECIMAL(4,2), CHECK(discount BETWEEN 0.0 AND 1.0)): Promotional discount rate.
- `sales_amount` (DECIMAL(12,2), NOT NULL): Final revenue after discount.
- `profit_amount` (DECIMAL(12,2), NOT NULL): Net profit contribution.

### 5. `Payments` Table
- `payment_id` (INTEGER, PRIMARY KEY AUTOINCREMENT): Transaction log key.
- `order_id` (VARCHAR(30), FOREIGN KEY -> `Orders.order_id`).
- `payment_method` (VARCHAR(50), NOT NULL): Channel (`UPI`, `Credit Card`, `Net Banking`, `Debit Card`, `Cash on Delivery`).
- `transaction_amount` (DECIMAL(12,2), NOT NULL): Settlement amount.

---

## 3. Performance Indexes & Reporting Views

### B-Tree Indexes
- `idx_orders_order_date`: Speeds up time-series queries.
- `idx_orders_customer_id`: Accelerates customer joins.
- `idx_orders_location`: Speeds up regional state/city aggregations.
- `idx_sales_order_id` & `idx_sales_product_id`: Accelerates line-item joins.
- `idx_products_category`: Speeds up category grouping.

### Reporting Views
1. `vw_monthly_executive_summary`: Monthly revenue, profit, orders, and margins.
2. `vw_customer_rfm_metrics`: Customer order frequency, lifetime spend, and acquisition dates.
3. `vw_product_performance_matrix`: Volume units sold, gross revenue, net profit per product item.
4. `vw_regional_sales_breakdown`: Regional performance per state and city.
5. `vw_discount_profitability_analysis`: Profit margin breakdown across discount tiers.
