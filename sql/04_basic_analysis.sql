-- ==========================================================
-- 04_basic_analysis.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Section 1: Basic Analytical Queries (Questions 1 to 15)
-- ==========================================================

USE ecommerce_analytics;

-- ----------------------------------------------------------
-- Question 1: Total Revenue
-- Explanation: Sum of all realized sales amounts across the marketplace.
-- ----------------------------------------------------------
SELECT 
    ROUND(SUM(sales_amount), 2) AS total_gross_revenue,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN sales_amount ELSE 0 END), 2) AS total_delivered_revenue
FROM orders;


-- ----------------------------------------------------------
-- Question 2: Total Profit
-- Explanation: Net financial profit after deducting supplier product cost from sales amount.
-- ----------------------------------------------------------
SELECT 
    ROUND(SUM(profit_amount), 2) AS total_gross_profit,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN profit_amount ELSE 0 END), 2) AS delivered_profit,
    ROUND((SUM(profit_amount) / SUM(sales_amount)) * 100, 2) AS overall_profit_margin_pct
FROM orders;


-- ----------------------------------------------------------
-- Question 3: Total Orders
-- Explanation: Count of total transactional records segmented by status.
-- ----------------------------------------------------------
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM orders;


-- ----------------------------------------------------------
-- Question 4: Total Customers
-- Explanation: Distinct count of registered and purchasing customer accounts.
-- ----------------------------------------------------------
SELECT 
    COUNT(DISTINCT customer_id) AS total_active_purchasers,
    (SELECT COUNT(*) FROM customers) AS total_registered_customers
FROM orders;


-- ----------------------------------------------------------
-- Question 5: Average Order Value (AOV)
-- Explanation: Average gross expenditure per placed customer transaction.
-- ----------------------------------------------------------
SELECT 
    ROUND(AVG(sales_amount), 2) AS overall_aov,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' THEN sales_amount END), 2) AS delivered_aov
FROM orders;


-- ----------------------------------------------------------
-- Question 6: Revenue by Month
-- Explanation: Aggregates revenue by Year-Month to track sales trajectories.
-- ----------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS monthly_revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- ----------------------------------------------------------
-- Question 7: Profit by Month
-- Explanation: Tracks profitability and profit margin variations over time.
-- ----------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(profit_amount), 2) AS monthly_profit,
    ROUND((SUM(profit_amount) / SUM(sales_amount)) * 100, 2) AS monthly_margin_pct
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- ----------------------------------------------------------
-- Question 8: Top 10 Products by Revenue
-- Explanation: Identifies flagship products driving the highest gross turnover.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- ----------------------------------------------------------
-- Question 9: Top 10 Customers by Spending
-- Explanation: Highlights the highest-spending accounts for VIP clienteling.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    c.customer_segment,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.sales_amount), 2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city, c.customer_segment
ORDER BY total_spent DESC
LIMIT 10;


-- ----------------------------------------------------------
-- Question 10: Revenue by Category
-- Explanation: Compares category-level sales volumes and revenue contributions.
-- ----------------------------------------------------------
SELECT 
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS total_units_sold,
    ROUND(SUM(o.sales_amount), 2) AS category_revenue,
    ROUND((SUM(o.sales_amount) / (SELECT SUM(sales_amount) FROM orders)) * 100, 2) AS revenue_share_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;


-- ----------------------------------------------------------
-- Question 11: Profit by Category
-- Explanation: Evaluates net margin generation across product categories.
-- ----------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_profit DESC;


-- ----------------------------------------------------------
-- Question 12: Revenue by Region
-- Explanation: Geographical performance across North, South, East, West, Central.
-- ----------------------------------------------------------
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS regional_revenue,
    ROUND(AVG(sales_amount), 2) AS regional_aov
FROM orders
GROUP BY region
ORDER BY regional_revenue DESC;


-- ----------------------------------------------------------
-- Question 13: Monthly Growth (Basic Lag/Self-Join)
-- Explanation: Month-over-month revenue growth using a self-join.
-- ----------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS ym,
        ROUND(SUM(sales_amount), 2) AS rev
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    cur.ym AS current_month,
    cur.rev AS current_revenue,
    prev.rev AS previous_revenue,
    ROUND(((cur.rev - prev.rev) / prev.rev) * 100, 2) AS mom_growth_pct
FROM MonthlySales cur
LEFT JOIN MonthlySales prev 
    ON DATE_FORMAT(STR_TO_DATE(CONCAT(cur.ym, '-01'), '%Y-%m-%d') - INTERVAL 1 MONTH, '%Y-%m') = prev.ym
ORDER BY cur.ym;


-- ----------------------------------------------------------
-- Question 14: Yearly Growth
-- Explanation: Annual sales volume and YoY growth comparisons.
-- ----------------------------------------------------------
WITH AnnualSales AS (
    SELECT 
        YEAR(order_date) AS order_year,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(sales_amount), 2) AS annual_revenue,
        ROUND(SUM(profit_amount), 2) AS annual_profit
    FROM orders
    GROUP BY YEAR(order_date)
)
SELECT 
    cur.order_year,
    cur.total_orders,
    cur.annual_revenue,
    prev.annual_revenue AS prev_year_revenue,
    ROUND(((cur.annual_revenue - prev.annual_revenue) / prev.annual_revenue) * 100, 2) AS yoy_growth_pct
FROM AnnualSales cur
LEFT JOIN AnnualSales prev ON cur.order_year = prev.order_year + 1
ORDER BY cur.order_year;


-- ----------------------------------------------------------
-- Question 15: Repeat Customers Count & Rate
-- Explanation: Analyzes customers who placed more than 1 order.
-- ----------------------------------------------------------
SELECT 
    COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers,
    COUNT(*) AS total_purchasing_customers,
    ROUND((COUNT(CASE WHEN order_count > 1 THEN 1 END) / COUNT(*)) * 100, 2) AS repeat_purchase_rate_pct
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) cust_orders;
