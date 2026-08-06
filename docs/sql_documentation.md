# Enterprise SQL Analytics & Database Documentation

**Database Name**: `BusinessGrowthDB`  
**Engine**: SQLite / ANSI-SQL Relational Standard  
**Total Queries**: 50 Real Business Analytics Queries  
**Location**: [data/BusinessGrowthDB.sqlite](file:///C:/Users/barun/.gemini/antigravity-ide/scratch/business-growth-analytics-suite/data/BusinessGrowthDB.sqlite)

---

## 1. Database Schema & Normalization (3NF)

To convert the flat enterprise CSV into a production-grade relational database, we applied Third Normal Form (3NF) normalization. This eliminates data redundancy, prevents update anomalies, and optimizes query execution speeds.

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

## 2. SQL Query Concepts & Explanations

### 🟢 Category 1: Basic SQL Queries (Q1 – Q12)
*Focus: Data Retrieval, Filtering, Aggregation, and Grouping.*

- **Q1 (Total Orders & Customers)**: Uses `COUNT()` and `COUNT(DISTINCT)` to find total sales orders and unique active buyers.
- **Q2 (City Filter)**: Demonstrates `WHERE city = 'Mumbai'` with `ORDER BY order_date DESC` to view recent transactions in specific hubs.
- **Q3 (Revenue & Profit Summary)**: Uses aggregate functions `SUM(sales_amount)` and `SUM(profit_amount)` to compute overall business financial numbers.
- **Q4 (Product Catalog Filtering)**: Filters tech items priced above ₹50,000 using standard logical comparison operators.
- **Q5 (Order Volume per State)**: Uses `GROUP BY state` combined with `COUNT()` to see which states place the most orders.
- **Q6 (Category Revenue Breakdown)**: Joins `Sales` and `Products` to group revenue by broad merchandise categories (`Technology`, `Furniture`, `Office Supplies`).
- **Q7 (High Discount Transactions)**: Filters orders where discount rates meet or exceed 20% (`discount >= 0.20`).
- **Q8 (Average Cart Items)**: Uses `AVG(quantity)` to measure average item basket size per purchase.
- **Q9 (High-Volume Cities with HAVING)**: Demonstrates `HAVING COUNT(order_id) > 3000` to filter aggregated city results after grouping.
- **Q10 (Payment Method Totals)**: Summarizes gross transaction values processed by payment channel.
- **Q11 (Yearly Date Filtering)**: Filters transactions occurring within the 2024 calendar year using string/datetime boundaries.
- **Q12 (Pricing Min/Max/Avg)**: Computes statistical boundaries for product selling prices across all orders.

---

### 🟡 Category 2: Intermediate SQL Queries (Q13 – Q25)
*Focus: Multi-table JOINs, Subqueries, Conditional Logic (`CASE WHEN`).*

- **Q13 (Customers & Orders INNER JOIN)**: Merges buyer names with order timestamps and shipping cities.
- **Q14 (3-Table Transaction Join)**: Joins `Sales`, `Orders`, and `Products` to create a complete detail record per line item.
- **Q15 (Order Tier Classification via CASE WHEN)**: Categorizes purchases into `Small Order (< 5K)`, `Medium Order (5K - 50K)`, or `Large Enterprise Order (> 50K)`.
- **Q16 (High Spenders Subquery)**: Uses a nested subquery to identify customers whose total spending exceeds the overall customer average.
- **Q17 (Low Profit Margin Detection)**: Calculates margin percentage `(profit / sales) * 100` and flags orders below 10% margin.
- **Q18 (Zero-Discount Items)**: Finds products sold exclusively at full list price without discounts.
- **Q19 (Unmatched Buyers via LEFT JOIN)**: Uses `LEFT JOIN` and `HAVING order_count = 0` to verify if any registered customer profile has 0 orders.
- **Q20 (State Average Order Value)**: Calculates the average cart spend per state to evaluate purchasing power.
- **Q21 (City Payment Preferences)**: Analyzes payment channel choices specifically for Bengaluru orders.
- **Q22 (Year-over-Year Annual Growth)**: Groups metrics by `strftime('%Y', order_date)` to compare 2023 vs 2024 performance.
- **Q23 (Category Payment Pivot)**: Uses conditional `CASE WHEN` aggregation inside `SUM()` to pivot sales across payment methods per category.
- **Q24 (High Discount Positive Profit Check)**: Identifies transactions where heavy discounts (>15%) still yielded positive net profits.
- **Q25 (Product Sales & Units Leaderboard)**: Aggregates total units sold and total revenue per individual product.

---

### 🔴 Category 3: Advanced SQL Queries (Q26 – Q38)
*Focus: Common Table Expressions (CTEs), Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), Running Totals, Moving Averages.*

- **Q26 (Category Top Products via DENSE_RANK)**: Ranks products within each product category using `DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC)`.
- **Q27 (Cumulative Running Revenue via SUM() OVER)**: Computes a running total of sales revenue month-over-month using `SUM() OVER (ORDER BY year_month)`.
- **Q28 (3-Month Moving Average)**: Calculates a rolling 3-month moving average of sales using `AVG() OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
- **Q29 (Customer Order Sequence via ROW_NUMBER)**: Assigns sequential order numbers (1st order, 2nd order, 3rd order) per customer using `ROW_NUMBER()`.
- **Q30 (State Profit Rankings via RANK)**: Ranks all 14 commercial states by net profit contribution.
- **Q31 (Month-over-Month MoM Growth via LAG)**: Uses `LAG(revenue, 1)` to fetch previous month sales and calculate percentage MoM growth.
- **Q32 (VIP Buyer CTE)**: Uses a Common Table Expression (`WITH CustomerOrderStats AS ...`) to isolate customers with >20 repeat purchases.
- **Q33 (Customer Quartile Segmentation via NTILE)**: Segments buyers into 4 spend quartiles (Top 25% VIPs to Bottom 25% Occasional Buyers) using `NTILE(4)`.
- **Q34 (First & Latest Order Dates via Window Functions)**: Uses `FIRST_VALUE()` and `LAST_VALUE()` to track customer acquisition and recent activity dates.
- **Q35 (Monthly Performance Metrics CTE)**: Constructs a clean summary matrix combining order volume, gross sales, net profit, and margin %.
- **Q36 (Top 5% Highest Sales Orders via PERCENT_RANK)**: Filters top 5th percentile order values using `PERCENT_RANK() >= 0.95`.
- **Q37 (Cumulative Product Units Sold)**: Tracks running sum of inventory volume sold per product over time.
- **Q38 (Category Profit Contribution %)**: Calculates each product's percentage contribution to its parent category profit pool using a CTE.

---

### 🔵 Category 4: Specialized Business Analytics Queries (Q39 – Q50)
*Focus: Executive Business KPIs, CLV, Retention, and Seasonal Analysis.*

- **Q39 & Q40 (Monthly Revenue & Profit Trends)**: Tracks month-by-month financial performance for executive reporting.
- **Q41 (Top 10 Customers Leaderboard)**: Ranks top 10 highest spending accounts.
- **Q42 (Customer Lifetime Value - CLV Tiering)**: Groups buyers into `Platinum (> 20L)`, `Gold (10L-20L)`, and `Silver (< 10L)` CLV brackets.
- **Q43 (Product Category Performance Matrix)**: Renders complete volume, revenue, profit, and margin stats by category.
- **Q44 & Q45 (State & City Leaderboards)**: Identifies top regional revenue generators across India.
- **Q46 (Discount Tier Impact Analysis)**: Evaluates trade-off between volume growth and margin compression across discount tiers.
- **Q47 (Payment Method Market Share)**: Analyzes average transaction size per payment method.
- **Q48 (Seasonal Quarterly Performance)**: Uses `CASE WHEN` month grouping to compare Q1, Q2, Q3, and Q4 revenue trends.
- **Q49 (Repeat Customer Purchase Frequency)**: Classifies buyers into single-order, 2-10 repeat, 11-25 loyal, and 25+ heavy buyers.
- **Q50 (Best vs. Worst Selling Products)**: Combines Top 5 and Bottom 5 revenue-generating products into a single executive dashboard comparison using `UNION ALL`.

---

## 3. SQL Performance Optimization (Indexes)

To ensure sub-second query performance across 100,000 transactions, 7 B-Tree indexes were created in [sql/indexes.sql](file:///C:/Users/barun/.gemini/antigravity-ide/scratch/business-growth-analytics-suite/sql/indexes.sql):
- `idx_orders_order_date`: Speeds up time-series filters & month grouping.
- `idx_orders_customer_id`: Accelerates customer joins & RFM analysis.
- `idx_orders_location`: Optimizes state & city aggregations.
- `idx_sales_order_id`: Fast foreign key joins between Orders & Sales.
- `idx_sales_product_id`: Fast joins between Sales & Products.
- `idx_products_category`: Accelerates category grouping.
- `idx_payments_order_method`: Speeds up payment channel analytics.

---
*Documentation generated for Step 3 of Business Growth Analytics Suite.*
