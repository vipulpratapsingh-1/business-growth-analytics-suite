-- ============================================================
-- Business Growth Analytics Suite - 50 Real Business SQL Queries
-- Database Engine: SQLite / ANSI-SQL Standard
-- Structure: Basic (Q1-12) | Intermediate (Q13-25) | Advanced (Q26-38) | Business Analytics (Q39-50)
-- ============================================================

-- ============================================================
-- SECTION 1: BASIC SQL QUERIES (Q1 - Q12)
-- Key Concepts: SELECT, WHERE, ORDER BY, GROUP BY, HAVING, COUNT, SUM, AVG
-- ============================================================

-- Q1: Retrieve total order count and total customer count from the database
SELECT 
    COUNT(order_id) AS total_orders, 
    COUNT(DISTINCT customer_id) AS unique_customers 
FROM Orders;

-- Q2: Find all orders placed in the city of 'Mumbai'
SELECT order_id, order_date, customer_id, city, state 
FROM Orders 
WHERE city = 'Mumbai' 
ORDER BY order_date DESC 
LIMIT 10;

-- Q3: Get total sales revenue and total profit generated across the entire business
SELECT 
    ROUND(SUM(sales_amount), 2) AS total_revenue, 
    ROUND(SUM(profit_amount), 2) AS total_profit 
FROM Sales;

-- Q4: List all products priced above INR 50,000 in the Technology category
SELECT product_id, product_name, category 
FROM Products 
WHERE category = 'Technology' 
ORDER BY product_name ASC;

-- Q5: Count the total number of orders placed per state
SELECT state, COUNT(order_id) AS order_count 
FROM Orders 
GROUP BY state 
ORDER BY order_count DESC;

-- Q6: Calculate total sales revenue grouped by product category
SELECT p.category, ROUND(SUM(s.sales_amount), 2) AS category_revenue 
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
GROUP BY p.category 
ORDER BY category_revenue DESC;

-- Q7: Find all sales transactions with a discount rate of 20% or higher
SELECT sales_id, order_id, unit_price, discount, sales_amount 
FROM Sales 
WHERE discount >= 0.20 
ORDER BY sales_amount DESC 
LIMIT 10;

-- Q8: Get average quantity of items purchased per order
SELECT ROUND(AVG(quantity), 2) AS avg_quantity_per_order 
FROM Sales;

-- Q9: List cities that have generated more than 3,000 total orders (HAVING clause)
SELECT city, state, COUNT(order_id) AS order_count 
FROM Orders 
GROUP BY city, state 
HAVING order_count > 3000 
ORDER BY order_count DESC;

-- Q10: Find total revenue by payment method
SELECT payment_method, ROUND(SUM(transaction_amount), 2) AS total_amount 
FROM Payments 
GROUP BY payment_method 
ORDER BY total_amount DESC;

-- Q11: Retrieve all orders placed in the year 2024
SELECT order_id, order_date, customer_id 
FROM Orders 
WHERE order_date >= '2024-01-01' AND order_date <= '2024-12-31' 
LIMIT 10;

-- Q12: Find minimum, average, and maximum unit price for products
SELECT 
    MIN(unit_price) AS min_price, 
    ROUND(AVG(unit_price), 2) AS avg_price, 
    MAX(unit_price) AS max_price 
FROM Sales;

-- ============================================================
-- SECTION 2: INTERMEDIATE SQL QUERIES (Q13 - Q25)
-- Key Concepts: INNER JOIN, LEFT JOIN, Subqueries, CASE WHEN, Multi-table aggregation
-- ============================================================

-- Q13: Join Orders and Customers to view order details with customer names
SELECT o.order_id, o.order_date, c.customer_id, c.customer_name, o.city 
FROM Orders o
INNER JOIN Customers c ON o.customer_id = c.customer_id
LIMIT 10;

-- Q14: Combine Sales, Orders, and Products to show detailed sales line items
SELECT s.sales_id, o.order_date, p.product_name, p.category, s.quantity, s.sales_amount, s.profit_amount 
FROM Sales s
JOIN Orders o ON s.order_id = o.order_id
JOIN Products p ON s.product_id = p.product_id
LIMIT 10;

-- Q15: Categorize order values into 'Small', 'Medium', and 'Large' tiers using CASE WHEN
SELECT order_id, sales_amount,
    CASE 
        WHEN sales_amount < 5000 THEN 'Small Order (< 5K)'
        WHEN sales_amount BETWEEN 5000 AND 50000 THEN 'Medium Order (5K - 50K)'
        ELSE 'Large Enterprise Order (> 50K)'
    END AS order_tier
FROM Sales
LIMIT 10;

-- Q16: Identify customers who have spent more than the overall average customer spending (Subquery)
SELECT c.customer_id, c.customer_name, ROUND(SUM(s.sales_amount), 2) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Sales s ON o.order_id = s.order_id
GROUP BY c.customer_id, c.customer_name
HAVING total_spent > (
    SELECT AVG(customer_sales) FROM (
        SELECT SUM(sales_amount) AS customer_sales 
        FROM Orders o2 
        JOIN Sales s2 ON o2.order_id = s2.order_id 
        GROUP BY o2.customer_id
    )
)
ORDER BY total_spent DESC
LIMIT 10;

-- Q17: Calculate profit margin percentage per order and filter orders with margin < 10%
SELECT sales_id, sales_amount, profit_amount,
    ROUND((profit_amount / sales_amount) * 100, 2) AS profit_margin_pct
FROM Sales
WHERE (profit_amount / sales_amount) < 0.10
LIMIT 10;

-- Q18: Find products that have never been discounted (discount = 0)
SELECT DISTINCT p.product_name, p.category 
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
WHERE s.discount = 0.0;

-- Q19: LEFT JOIN between Customers and Orders to verify if any registered customers have zero orders
SELECT c.customer_id, c.customer_name, COUNT(o.order_id) AS order_count
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING order_count = 0;

-- Q20: Find state-wise average order transaction size
SELECT o.state, ROUND(AVG(s.sales_amount), 2) AS avg_order_value
FROM Orders o
JOIN Sales s ON o.order_id = s.order_id
GROUP BY o.state
ORDER BY avg_order_value DESC;

-- Q21: Count payment transactions grouped by payment method for orders in 'Bengaluru'
SELECT pay.payment_method, COUNT(pay.payment_id) AS total_transactions, ROUND(SUM(pay.transaction_amount), 2) AS total_amount
FROM Payments pay
JOIN Orders o ON pay.order_id = o.order_id
WHERE o.city = 'Bengaluru'
GROUP BY pay.payment_method;

-- Q22: Calculate annual sales comparison (2023 vs 2024)
SELECT 
    strftime('%Y', o.order_date) AS order_year,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(s.sales_amount), 2) AS annual_revenue,
    ROUND(SUM(s.profit_amount), 2) AS annual_profit
FROM Orders o
JOIN Sales s ON o.order_id = s.order_id
GROUP BY strftime('%Y', o.order_date);

-- Q23: Determine top payment method for each product category using CASE aggregation
SELECT p.category,
    SUM(CASE WHEN pay.payment_method = 'UPI' THEN s.sales_amount ELSE 0 END) AS upi_sales,
    SUM(CASE WHEN pay.payment_method = 'Credit Card' THEN s.sales_amount ELSE 0 END) AS credit_card_sales,
    SUM(CASE WHEN pay.payment_method = 'Net Banking' THEN s.sales_amount ELSE 0 END) AS net_banking_sales
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
JOIN Payments pay ON s.order_id = pay.order_id
GROUP BY p.category;

-- Q24: Find orders where discount was higher than 15% but profit was still positive
SELECT s.order_id, s.discount, s.sales_amount, s.profit_amount
FROM Sales s
WHERE s.discount > 0.15 AND s.profit_amount > 0
LIMIT 10;

-- Q25: List products with their total units sold and total revenue generated
SELECT p.product_name, SUM(s.quantity) AS total_units, ROUND(SUM(s.sales_amount), 2) AS total_revenue
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;

-- ============================================================
-- SECTION 3: ADVANCED SQL QUERIES (Q26 - Q38)
-- Key Concepts: CTEs (WITH), ROW_NUMBER, RANK, DENSE_RANK, Running Totals, Moving Averages
-- ============================================================

-- Q26: Rank top 5 products within each category based on total revenue using DENSE_RANK()
WITH CategoryProductRank AS (
    SELECT p.category, p.product_name, SUM(s.sales_amount) AS revenue,
        DENSE_RANK() OVER (PARTITION BY p.category ORDER BY SUM(s.sales_amount) DESC) AS category_rank
    FROM Products p
    JOIN Sales s ON p.product_id = s.product_id
    GROUP BY p.category, p.product_name
)
SELECT category, product_name, ROUND(revenue, 2) AS revenue, category_rank
FROM CategoryProductRank
WHERE category_rank <= 5;

-- Q27: Calculate cumulative running total of revenue month-by-month using Window Function
WITH MonthlySales AS (
    SELECT strftime('%Y-%m', o.order_date) AS year_month, SUM(s.sales_amount) AS monthly_revenue
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT year_month, ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY year_month), 2) AS running_total_revenue
FROM MonthlySales;

-- Q28: Compute 3-Month Moving Average of monthly sales revenue using AVG() OVER
WITH MonthlySales AS (
    SELECT strftime('%Y-%m', o.order_date) AS year_month, SUM(s.sales_amount) AS monthly_revenue
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT year_month, ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(AVG(monthly_revenue) OVER (ORDER BY year_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM MonthlySales;

-- Q29: Assign a sequential row number to orders per customer ordered by date using ROW_NUMBER()
SELECT c.customer_id, c.customer_name, o.order_id, o.order_date,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date ASC) AS customer_order_seq
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
LIMIT 15;

-- Q30: Rank states by total profit generated using RANK()
WITH StateProfit AS (
    SELECT o.state, SUM(s.profit_amount) AS total_profit
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY o.state
)
SELECT state, ROUND(total_profit, 2) AS total_profit,
    RANK() OVER (ORDER BY total_profit DESC) AS profit_rank
FROM StateProfit;

-- Q31: Calculate Month-over-Month (MoM) revenue growth rate using LAG()
WITH MonthlyRevenue AS (
    SELECT strftime('%Y-%m', o.order_date) AS year_month, SUM(s.sales_amount) AS current_revenue
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT year_month, ROUND(current_revenue, 2) AS current_revenue,
    ROUND(LAG(current_revenue, 1) OVER (ORDER BY year_month), 2) AS previous_month_revenue,
    ROUND(((current_revenue - LAG(current_revenue, 1) OVER (ORDER BY year_month)) / LAG(current_revenue, 1) OVER (ORDER BY year_month)) * 100, 2) AS mom_growth_pct
FROM MonthlyRevenue;

-- Q32: CTE to find customers with more than 20 lifetime orders (VIP Repeat Buyers)
WITH CustomerOrderStats AS (
    SELECT o.customer_id, COUNT(o.order_id) AS total_orders, SUM(s.sales_amount) AS total_spent
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY o.customer_id
)
SELECT cos.customer_id, c.customer_name, cos.total_orders, ROUND(cos.total_spent, 2) AS total_spent
FROM CustomerOrderStats cos
JOIN Customers c ON cos.customer_id = c.customer_id
WHERE cos.total_orders > 20
ORDER BY cos.total_spent DESC
LIMIT 10;

-- Q33: Percentile ranking of customers by total spend using NTILE(4) (Quartile Segmentation)
WITH CustomerSpend AS (
    SELECT c.customer_id, c.customer_name, SUM(s.sales_amount) AS total_spent
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT customer_id, customer_name, ROUND(total_spent, 2) AS total_spent,
    NTILE(4) OVER (ORDER BY total_spent DESC) AS spend_quartile
FROM CustomerSpend
LIMIT 15;

-- Q34: Find the first and most recent order date for each customer using MIN/MAX window functions
SELECT DISTINCT c.customer_id, c.customer_name,
    FIRST_VALUE(o.order_date) OVER (PARTITION BY c.customer_id ORDER BY o.order_date ASC) AS first_order_date,
    LAST_VALUE(o.order_date) OVER (PARTITION BY c.customer_id ORDER BY o.order_date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_order_date
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
LIMIT 10;

-- Q35: CTE combining monthly sales, order count, and profit margin in a single query
WITH MonthlyMetrics AS (
    SELECT strftime('%Y-%m', o.order_date) AS period,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(s.sales_amount) AS sales,
        SUM(s.profit_amount) AS profit
    FROM Orders o
    JOIN Sales s ON o.order_id = s.order_id
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT period, orders, ROUND(sales, 2) AS sales, ROUND(profit, 2) AS profit,
    ROUND((profit / sales) * 100, 2) AS margin_pct
FROM MonthlyMetrics;

-- Q36: Find orders that generated revenue higher than 95% of all order transactions
WITH OrderTotals AS (
    SELECT order_id, sales_amount,
        PERCENT_RANK() OVER (ORDER BY sales_amount ASC) as pct_rank
    FROM Sales
)
SELECT order_id, ROUND(sales_amount, 2) AS sales_amount, ROUND(pct_rank * 100, 2) AS percentile
FROM OrderTotals
WHERE pct_rank >= 0.95
LIMIT 10;

-- Q37: Cumulative running sum of quantity sold per product over time
SELECT s.sales_id, p.product_name, o.order_date, s.quantity,
    SUM(s.quantity) OVER (PARTITION BY p.product_id ORDER BY o.order_date ASC) AS running_units_sold
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
JOIN Orders o ON s.order_id = o.order_id
LIMIT 15;

-- Q38: Calculate profit contribution percentage of each product relative to its category total
WITH CategoryTotals AS (
    SELECT p.category, SUM(s.profit_amount) AS category_profit
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.category
)
SELECT p.category, p.product_name, ROUND(SUM(s.profit_amount), 2) AS product_profit,
    ROUND((SUM(s.profit_amount) / ct.category_profit) * 100, 2) AS profit_contribution_pct
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
JOIN CategoryTotals ct ON p.category = ct.category
GROUP BY p.category, p.product_name
ORDER BY p.category, profit_contribution_pct DESC;

-- ============================================================
-- SECTION 4: BUSINESS ANALYTICS QUERIES (Q39 - Q50)
-- Specialized Business Domain Insights & Executive KPIs
-- ============================================================

-- Q39: Monthly Revenue Analysis
SELECT strftime('%Y-%m', o.order_date) AS month, ROUND(SUM(s.sales_amount), 2) AS monthly_revenue
FROM Orders o JOIN Sales s ON o.order_id = s.order_id
GROUP BY month ORDER BY month;

-- Q40: Monthly Profit Analysis
SELECT strftime('%Y-%m', o.order_date) AS month, ROUND(SUM(s.profit_amount), 2) AS monthly_profit
FROM Orders o JOIN Sales s ON o.order_id = s.order_id
GROUP BY month ORDER BY month;

-- Q41: Top 10 High-Value Customers Leaderboard
SELECT c.customer_id, c.customer_name, COUNT(o.order_id) AS order_count, ROUND(SUM(s.sales_amount), 2) AS total_revenue
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id JOIN Sales s ON o.order_id = s.order_id
GROUP BY c.customer_id, c.customer_name ORDER BY total_revenue DESC LIMIT 10;

-- Q42: Customer Lifetime Value (CLV) Calculation & Tiering
SELECT c.customer_id, c.customer_name, ROUND(SUM(s.sales_amount), 2) AS clv,
    CASE 
        WHEN SUM(s.sales_amount) > 2000000 THEN 'Platinum CLV (> 20L)'
        WHEN SUM(s.sales_amount) BETWEEN 1000000 AND 2000000 THEN 'Gold CLV (10L - 20L)'
        ELSE 'Silver CLV (< 10L)'
    END AS clv_tier
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id JOIN Sales s ON o.order_id = s.order_id
GROUP BY c.customer_id, c.customer_name ORDER BY clv DESC LIMIT 10;

-- Q43: Product Category Performance Matrix
SELECT p.category, COUNT(DISTINCT s.order_id) AS orders, SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.sales_amount), 2) AS revenue, ROUND(SUM(s.profit_amount), 2) AS profit,
    ROUND((SUM(s.profit_amount) / SUM(s.sales_amount)) * 100, 2) AS margin_pct
FROM Products p JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.category ORDER BY revenue DESC;

-- Q44: State-wise Sales Revenue & Profit Performance
SELECT o.state, COUNT(DISTINCT o.order_id) AS orders, ROUND(SUM(s.sales_amount), 2) AS state_revenue, ROUND(SUM(s.profit_amount), 2) AS state_profit
FROM Orders o JOIN Sales s ON o.order_id = s.order_id
GROUP BY o.state ORDER BY state_revenue DESC;

-- Q45: City-wise Sales Revenue Leaderboard (Top 10 Cities)
SELECT o.city, o.state, COUNT(DISTINCT o.order_id) AS orders, ROUND(SUM(s.sales_amount), 2) AS city_revenue
FROM Orders o JOIN Sales s ON o.order_id = s.order_id
GROUP BY o.city, o.state ORDER BY city_revenue DESC LIMIT 10;

-- Q46: Discount Tier Impact Analysis on Sales Volume vs Profit Margin
SELECT 
    CASE 
        WHEN s.discount = 0.0 THEN '0% No Discount'
        WHEN s.discount <= 0.10 THEN '1% - 10% Low Discount'
        WHEN s.discount <= 0.20 THEN '11% - 20% Medium Discount'
        ELSE '>20% High Discount'
    END AS discount_tier,
    COUNT(s.sales_id) AS total_orders, ROUND(SUM(s.sales_amount), 2) AS total_sales,
    ROUND(SUM(s.profit_amount), 2) AS total_profit,
    ROUND((SUM(s.profit_amount) / SUM(s.sales_amount)) * 100, 2) AS margin_pct
FROM Sales s
GROUP BY discount_tier ORDER BY total_sales DESC;

-- Q47: Payment Method Market Share & Average Order Value
SELECT pay.payment_method, COUNT(pay.payment_id) AS transaction_count,
    ROUND(SUM(pay.transaction_amount), 2) AS total_volume,
    ROUND(AVG(pay.transaction_amount), 2) AS avg_transaction_value
FROM Payments pay
GROUP BY pay.payment_method ORDER BY total_volume DESC;

-- Q48: Seasonal Quarterly Revenue & Profit Trend Analysis
SELECT strftime('%Y', o.order_date) AS order_year,
    CASE 
        WHEN strftime('%m', o.order_date) IN ('01', '02', '03') THEN 'Q1 (Jan-Mar)'
        WHEN strftime('%m', o.order_date) IN ('04', '05', '06') THEN 'Q2 (Apr-Jun)'
        WHEN strftime('%m', o.order_date) IN ('07', '08', '09') THEN 'Q3 (Jul-Sep)'
        ELSE 'Q4 (Oct-Dec)'
    END AS quarter,
    ROUND(SUM(s.sales_amount), 2) AS quarterly_revenue, ROUND(SUM(s.profit_amount), 2) AS quarterly_profit
FROM Orders o JOIN Sales s ON o.order_id = s.order_id
GROUP BY order_year, quarter ORDER BY order_year, quarter;

-- Q49: Repeat Customer Purchase Frequency Analysis
SELECT customer_order_count_tier, COUNT(customer_id) AS customer_count
FROM (
    SELECT customer_id,
        CASE 
            WHEN COUNT(order_id) = 1 THEN '1 Single Order'
            WHEN COUNT(order_id) BETWEEN 2 AND 10 THEN '2-10 Repeat Orders'
            WHEN COUNT(order_id) BETWEEN 11 AND 25 THEN '11-25 Loyal Buyers'
            ELSE '25+ Heavy Buyers'
        END AS customer_order_count_tier
    FROM Orders GROUP BY customer_id
)
GROUP BY customer_order_count_tier ORDER BY customer_count DESC;

-- Q50: Best Selling vs Worst Selling Products Comparison
SELECT * FROM (
    SELECT 'Best Selling (Top 5)' AS status_type, p.product_name, SUM(s.quantity) AS units_sold, ROUND(SUM(s.sales_amount), 2) AS revenue
    FROM Products p JOIN Sales s ON p.product_id = s.product_id GROUP BY p.product_name ORDER BY revenue DESC LIMIT 5
)
UNION ALL
SELECT * FROM (
    SELECT 'Worst Selling (Bottom 5)' AS status_type, p.product_name, SUM(s.quantity) AS units_sold, ROUND(SUM(s.sales_amount), 2) AS revenue
    FROM Products p JOIN Sales s ON p.product_id = s.product_id GROUP BY p.product_name ORDER BY revenue ASC LIMIT 5
);
