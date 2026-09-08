-- ==========================================================
-- 06_advanced_analysis.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Section 3: Advanced Analytical Queries (Questions 34 to 50)
-- ==========================================================

USE ecommerce_analytics;

-- ----------------------------------------------------------
-- Question 34: Customer RFM Preparation Metrics
-- Explanation: Computes Recency (relative to 2025-01-01), Frequency, and Monetary raw values per customer.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    DATEDIFF('2025-01-01', MAX(o.order_date)) AS recency_days,
    COUNT(o.order_id) AS frequency,
    ROUND(SUM(o.sales_amount), 2) AS monetary_total,
    ROUND(AVG(o.sales_amount), 2) AS monetary_aov
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;


-- ----------------------------------------------------------
-- Question 35: Regional Performance & Profit Matrix
-- Explanation: Multi-dimensional regional comparison of orders, revenue, profit, margin, and AOV.
-- ----------------------------------------------------------
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(order_id) AS order_volume,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit_amount), 2) AS total_profit,
    ROUND((SUM(profit_amount) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales_amount), 2) AS aov
FROM orders
GROUP BY region
ORDER BY total_revenue DESC;


-- ----------------------------------------------------------
-- Question 36: High-Revenue Low-Profit Products (Pricing Alert)
-- Explanation: Identifies products generating top 25% revenue but bottom 25% profit margin.
-- ----------------------------------------------------------
WITH ProductMetrics AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(o.sales_amount), 2) AS revenue,
        ROUND(SUM(o.profit_amount), 2) AS profit,
        ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS margin_pct,
        NTILE(4) OVER (ORDER BY SUM(o.sales_amount) DESC) AS revenue_quartile,
        NTILE(4) OVER (ORDER BY (SUM(o.profit_amount) / SUM(o.sales_amount)) ASC) AS margin_quartile
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id,
    product_name,
    category,
    revenue,
    profit,
    margin_pct
FROM ProductMetrics
WHERE revenue_quartile = 1 AND margin_quartile = 1
ORDER BY revenue DESC;


-- ----------------------------------------------------------
-- Question 37: High-Return Products (> 10% Return Rate with Minimum 50 Orders)
-- Explanation: Flags merchandise with disproportionate return frequencies for QA audit.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND((SUM(CASE WHEN o.order_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(o.order_id)) * 100, 2) AS return_rate_pct,
    ROUND(SUM(CASE WHEN o.order_status = 'Returned' THEN o.sales_amount ELSE 0 END), 2) AS returned_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING COUNT(o.order_id) >= 50 AND return_rate_pct > 10.00
ORDER BY return_rate_pct DESC;


-- ----------------------------------------------------------
-- Question 38: Revenue Contribution Percentage by Category
-- Explanation: Calculates each category's exact share of grand total marketplace revenue.
-- ----------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS category_revenue,
    ROUND((SUM(o.sales_amount) / SUM(SUM(o.sales_amount)) OVER ()) * 100, 2) AS pct_of_total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;


-- ----------------------------------------------------------
-- Question 39: Pareto / 80-20 Analysis on Product Catalog
-- Explanation: Uses cumulative window aggregation to identify the top catalog products accounting for 80% of revenue.
-- ----------------------------------------------------------
WITH RankedProducts AS (
    SELECT 
        p.product_id,
        p.product_name,
        ROUND(SUM(o.sales_amount), 2) AS product_revenue,
        SUM(SUM(o.sales_amount)) OVER () AS grand_total_revenue,
        SUM(SUM(o.sales_amount)) OVER (ORDER BY SUM(o.sales_amount) DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_cumulative_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT 
    product_id,
    product_name,
    product_revenue,
    running_cumulative_revenue,
    ROUND((running_cumulative_revenue / grand_total_revenue) * 100, 2) AS cumulative_revenue_pct
FROM RankedProducts
WHERE (running_cumulative_revenue / grand_total_revenue) <= 0.80
ORDER BY product_revenue DESC;


-- ----------------------------------------------------------
-- Question 40: Customer Lifetime Value (CLV) Approximation
-- Explanation: Calculates historic CLV as Total Revenue minus Direct Product Cost per customer.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.sales_amount), 2) AS lifetime_revenue,
    ROUND(SUM(o.profit_amount), 2) AS customer_lifetime_value,
    ROUND(AVG(o.sales_amount), 2) AS average_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.customer_segment
ORDER BY customer_lifetime_value DESC
LIMIT 20;


-- ----------------------------------------------------------
-- Question 41: First Purchase Date per Customer
-- Explanation: Surfaces initial acquisition timestamp for cohort analysis.
-- ----------------------------------------------------------
SELECT 
    customer_id,
    MIN(order_date) AS first_order_date,
    COUNT(order_id) AS lifetime_orders
FROM orders
GROUP BY customer_id
ORDER BY first_order_date ASC
LIMIT 20;


-- ----------------------------------------------------------
-- Question 42: Last Purchase Date per Customer (Recency Audit)
-- Explanation: Identifies the most recent transaction date to monitor active churn.
-- ----------------------------------------------------------
SELECT 
    customer_id,
    MAX(order_date) AS last_order_date,
    DATEDIFF('2025-01-01', MAX(order_date)) AS days_since_last_order
FROM orders
GROUP BY customer_id
ORDER BY days_since_last_order ASC
LIMIT 20;


-- ----------------------------------------------------------
-- Question 43: Average Days Between Purchases (Inter-Purchase Time)
-- Explanation: Calculates customer purchase frequency cadence using MIN, MAX dates and order count.
-- ----------------------------------------------------------
SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order,
    DATEDIFF(MAX(order_date), MIN(order_date)) AS customer_lifecycle_days,
    ROUND(DATEDIFF(MAX(order_date), MIN(order_date)) / NULLIF(COUNT(order_id) - 1, 0), 1) AS avg_days_between_purchases
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) >= 3
ORDER BY avg_days_between_purchases ASC
LIMIT 20;


-- ----------------------------------------------------------
-- Question 44: Churn-Risk Customers (High Value Inactive > 120 Days)
-- Explanation: Flags high-spend customers who haven't transacted in 120+ days relative to benchmark.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.sales_amount), 2) AS lifetime_spend,
    MAX(o.order_date) AS last_purchase_date,
    DATEDIFF('2025-01-01', MAX(o.order_date)) AS days_inactive
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.customer_segment
HAVING DATEDIFF('2025-01-01', MAX(o.order_date)) >= 120 AND SUM(o.sales_amount) > 25000
ORDER BY lifetime_spend DESC
LIMIT 25;


-- ----------------------------------------------------------
-- Question 45: Most Profitable Customer Segment
-- Explanation: Evaluates customer tiers (Champions, Regular, etc.) by net profit contribution.
-- ----------------------------------------------------------
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(o.order_id) AS order_volume,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(o.profit_amount) / COUNT(DISTINCT c.customer_id), 2) AS avg_profit_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY total_profit DESC;


-- ----------------------------------------------------------
-- Question 46: Average Order Value (AOV) by Region
-- Explanation: Evaluates regional basket sizes to optimize localized shipping and promotions.
-- ----------------------------------------------------------
SELECT 
    region,
    COUNT(order_id) AS orders_count,
    ROUND(SUM(sales_amount), 2) AS regional_sales,
    ROUND(AVG(sales_amount), 2) AS regional_aov
FROM orders
GROUP BY region
ORDER BY regional_aov DESC;


-- ----------------------------------------------------------
-- Question 47: Profit Margin % by Category
-- Explanation: Ranks merchandise categories from highest to lowest margin profitability.
-- ----------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS revenue,
    ROUND(SUM(o.profit_amount), 2) AS profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY profit_margin_pct DESC;


-- ----------------------------------------------------------
-- Question 48: Return Rate by Category
-- Explanation: Quantifies return friction across different merchandise divisions.
-- ----------------------------------------------------------
SELECT 
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND((SUM(CASE WHEN o.order_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(o.order_id)) * 100, 2) AS return_rate_pct,
    ROUND(SUM(CASE WHEN o.order_status = 'Returned' THEN o.sales_amount ELSE 0 END), 2) AS refund_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC;


-- ----------------------------------------------------------
-- Question 49: Revenue Share by Payment Method
-- Explanation: Determines volume share and gateway dependency per payment tender.
-- ----------------------------------------------------------
SELECT 
    p.payment_method,
    COUNT(p.payment_id) AS transaction_count,
    ROUND(SUM(p.payment_amount), 2) AS processed_amount,
    ROUND((SUM(p.payment_amount) / SUM(SUM(p.payment_amount)) OVER ()) * 100, 2) AS payment_share_pct
FROM payments p
GROUP BY p.payment_method
ORDER BY processed_amount DESC;


-- ----------------------------------------------------------
-- Question 50: Year-over-Year (YoY) Growth by Month (LAG Window Function)
-- Explanation: Matches each calendar month with the exact corresponding month in the prior year (12-period lag).
-- ----------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS year_month,
        YEAR(order_date) AS yr,
        MONTH(order_date) AS mo,
        ROUND(SUM(sales_amount), 2) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m'), YEAR(order_date), MONTH(order_date)
)
SELECT 
    cur.year_month,
    cur.revenue AS current_revenue,
    prev.revenue AS prior_year_revenue,
    ROUND(((cur.revenue - prev.revenue) / prev.revenue) * 100, 2) AS yoy_growth_pct
FROM MonthlySales cur
LEFT JOIN MonthlySales prev 
    ON cur.mo = prev.mo AND cur.yr = prev.yr + 1
ORDER BY cur.year_month;
