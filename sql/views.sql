-- ============================================================
-- SQL Reporting Views: BusinessGrowthDB
-- Re-usable analytical views for executive dashboards & reporting
-- ============================================================

-- View 1: Monthly Executive Summary View
CREATE VIEW IF NOT EXISTS vw_monthly_executive_summary AS
SELECT 
    strftime('%Y-%m', o.order_date) AS Year_Month,
    COUNT(DISTINCT o.order_id) AS Total_Orders,
    COUNT(DISTINCT o.customer_id) AS Active_Customers,
    SUM(s.sales_amount) AS Total_Revenue,
    SUM(s.profit_amount) AS Total_Profit,
    ROUND((SUM(s.profit_amount) / SUM(s.sales_amount)) * 100, 2) AS Overall_Profit_Margin_Pct,
    ROUND(AVG(s.sales_amount), 2) AS Average_Order_Value
FROM Orders o
JOIN Sales s ON o.order_id = s.order_id
GROUP BY strftime('%Y-%m', o.order_date);

-- View 2: Customer RFM & Lifetime Value Metrics View
CREATE VIEW IF NOT EXISTS vw_customer_rfm_metrics AS
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS Total_Orders_Placed,
    SUM(s.sales_amount) AS Lifetime_Value,
    SUM(s.profit_amount) AS Total_Profit_Generated,
    ROUND(AVG(s.sales_amount), 2) AS Avg_Transaction_Value,
    MIN(o.order_date) AS First_Order_Date,
    MAX(o.order_date) AS Last_Order_Date
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Sales s ON o.order_id = s.order_id
GROUP BY c.customer_id, c.customer_name;

-- View 3: Product Performance Matrix View
CREATE VIEW IF NOT EXISTS vw_product_performance_matrix AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(s.quantity) AS Total_Units_Sold,
    SUM(s.sales_amount) AS Total_Revenue,
    SUM(s.profit_amount) AS Total_Profit,
    ROUND(AVG(s.discount) * 100, 2) AS Avg_Discount_Pct,
    ROUND((SUM(s.profit_amount) / SUM(s.sales_amount)) * 100, 2) AS Category_Profit_Margin_Pct
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category;

-- View 4: Regional Sales Breakdown View
CREATE VIEW IF NOT EXISTS vw_regional_sales_breakdown AS
SELECT 
    o.state,
    o.city,
    COUNT(DISTINCT o.order_id) AS Total_Orders,
    COUNT(DISTINCT o.customer_id) AS Unique_Customers,
    SUM(s.sales_amount) AS Regional_Revenue,
    SUM(s.profit_amount) AS Regional_Profit,
    ROUND(AVG(s.sales_amount), 2) AS Avg_Order_Value
FROM Orders o
JOIN Sales s ON o.order_id = s.order_id
GROUP BY o.state, o.city;

-- View 5: Discount Profitability Analysis View
CREATE VIEW IF NOT EXISTS vw_discount_profitability_analysis AS
SELECT 
    s.discount AS Discount_Rate,
    CASE 
        WHEN s.discount = 0.0 THEN 'No Discount (0%)'
        WHEN s.discount <= 0.10 THEN 'Low Discount (1-10%)'
        WHEN s.discount <= 0.20 THEN 'Medium Discount (11-20%)'
        ELSE 'High Discount (>20%)'
    END AS Discount_Tier,
    COUNT(s.sales_id) AS Order_Volume,
    SUM(s.sales_amount) AS Total_Sales,
    SUM(s.profit_amount) AS Total_Profit,
    ROUND((SUM(s.profit_amount) / SUM(s.sales_amount)) * 100, 2) AS Profit_Margin_Pct
FROM Sales s
GROUP BY s.discount;
