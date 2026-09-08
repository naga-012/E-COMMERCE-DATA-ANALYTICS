-- ==========================================================
-- 05_intermediate_analysis.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Section 2: Intermediate Analytical Queries (Questions 16 to 33)
-- ==========================================================

USE ecommerce_analytics;

-- ----------------------------------------------------------
-- Question 16: New Customers Acquired by Month
-- Explanation: Identifies customer acquisition velocity based on their first order date.
-- ----------------------------------------------------------
WITH FirstOrders AS (
    SELECT 
        customer_id, 
        DATE_FORMAT(MIN(order_date), '%Y-%m') AS cohort_month
    FROM orders
    GROUP BY customer_id
)
SELECT 
    cohort_month,
    COUNT(customer_id) AS new_customers_acquired
FROM FirstOrders
GROUP BY cohort_month
ORDER BY cohort_month;


-- ----------------------------------------------------------
-- Question 17: Customer Retention Rate (Cohort-Based)
-- Explanation: Percentage of acquired customers who returned to make a subsequent purchase.
-- ----------------------------------------------------------
WITH CustomerActivity AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS retained_customers,
    ROUND((SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS retention_rate_pct
FROM CustomerActivity;


-- ----------------------------------------------------------
-- Question 18: Customer Ranking by Lifetime Revenue
-- Explanation: Employs DENSE_RANK() window function to rank customers by total expenditure.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    ROUND(SUM(o.sales_amount), 2) AS total_spend,
    DENSE_RANK() OVER(ORDER BY SUM(o.sales_amount) DESC) AS customer_rank
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY customer_rank
LIMIT 20;


-- ----------------------------------------------------------
-- Question 19: Product Ranking by Profit Contribution
-- Explanation: Ranks catalog products based on cumulative net profit generated.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    DENSE_RANK() OVER(ORDER BY SUM(o.profit_amount) DESC) AS profit_rank
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY profit_rank
LIMIT 20;


-- ----------------------------------------------------------
-- Question 20: Category Ranking by Profit Margin
-- Explanation: Ranks merchandise categories by blended profit margin percentage.
-- ----------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS margin_pct,
    RANK() OVER(ORDER BY (SUM(o.profit_amount) / SUM(o.sales_amount)) DESC) AS margin_rank
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY margin_rank;


-- ----------------------------------------------------------
-- Question 21: Highest-Profit Product
-- Explanation: Identifies the single most lucrative product in catalog history.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_profit DESC
LIMIT 1;


-- ----------------------------------------------------------
-- Question 22: Lowest-Profit Product
-- Explanation: Identifies the worst-performing product by net profit generated.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_profit ASC
LIMIT 1;


-- ----------------------------------------------------------
-- Question 23: Highest-Margin Product (with Minimum 30 Orders)
-- Explanation: Surfaces niche high-margin products with validated customer traction.
-- ----------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING COUNT(o.order_id) >= 30
ORDER BY profit_margin_pct DESC
LIMIT 5;


-- ----------------------------------------------------------
-- Question 24: Order Return Rate
-- Explanation: Ratio of returned orders relative to total transactions.
-- ----------------------------------------------------------
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND((SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS return_rate_pct,
    ROUND(SUM(CASE WHEN order_status = 'Returned' THEN sales_amount ELSE 0 END), 2) AS returned_merchandise_value
FROM orders;


-- ----------------------------------------------------------
-- Question 25: Return Reasons Breakdown
-- Explanation: Frequency and refund value per customer return root cause.
-- ----------------------------------------------------------
SELECT 
    return_reason,
    COUNT(return_id) AS return_count,
    ROUND(SUM(refund_amount), 2) AS total_refunded,
    ROUND((COUNT(return_id) / (SELECT COUNT(*) FROM returns)) * 100, 2) AS return_share_pct
FROM returns
GROUP BY return_reason
ORDER BY return_count DESC;


-- ----------------------------------------------------------
-- Question 26: Payment-Method Analysis
-- Explanation: Analyzes payment channel transaction counts, volume, and success rates.
-- ----------------------------------------------------------
SELECT 
    payment_method,
    COUNT(payment_id) AS transaction_count,
    ROUND(SUM(payment_amount), 2) AS total_volume,
    ROUND(AVG(payment_amount), 2) AS avg_ticket_size,
    ROUND((SUM(CASE WHEN payment_status = 'Success' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS success_rate_pct
FROM payments
GROUP BY payment_method
ORDER BY total_volume DESC;


-- ----------------------------------------------------------
-- Question 27: Customers with More than 5 Orders
-- Explanation: Identifies high-frequency loyal customer base.
-- ----------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.sales_amount), 2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.customer_segment
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;


-- ----------------------------------------------------------
-- Question 28: Customers Whose Spending is Above Average
-- Explanation: Uses subquery to filter customers exceeding population average spend.
-- ----------------------------------------------------------
WITH CustomerSpend AS (
    SELECT 
        customer_id,
        ROUND(SUM(sales_amount), 2) AS total_spend
    FROM orders
    GROUP BY customer_id
)
SELECT 
    cs.customer_id,
    c.customer_name,
    c.city,
    cs.total_spend
FROM CustomerSpend cs
JOIN customers c ON cs.customer_id = c.customer_id
WHERE cs.total_spend > (SELECT AVG(total_spend) FROM CustomerSpend)
ORDER BY cs.total_spend DESC;


-- ----------------------------------------------------------
-- Question 29: Products Whose Revenue is Above Category Average
-- Explanation: Correlated subquery / CTE comparing product revenue to category benchmark.
-- ----------------------------------------------------------
WITH ProductRev AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(o.sales_amount), 2) AS product_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
),
CategoryAvg AS (
    SELECT 
        category,
        AVG(product_revenue) AS avg_cat_revenue
    FROM ProductRev
    GROUP BY category
)
SELECT 
    pr.product_id,
    pr.product_name,
    pr.category,
    pr.product_revenue,
    ROUND(ca.avg_cat_revenue, 2) AS category_avg_revenue
FROM ProductRev pr
JOIN CategoryAvg ca ON pr.category = ca.category
WHERE pr.product_revenue > ca.avg_cat_revenue
ORDER BY pr.category, pr.product_revenue DESC;


-- ----------------------------------------------------------
-- Question 30: Monthly Revenue Ranking
-- Explanation: Uses DENSE_RANK() to determine historically best sales months.
-- ----------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(sales_amount), 2) AS monthly_revenue,
    DENSE_RANK() OVER(ORDER BY SUM(sales_amount) DESC) AS revenue_rank
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY revenue_rank ASC;


-- ----------------------------------------------------------
-- Question 31: Running Revenue Total (Cumulative Revenue)
-- Explanation: Window function SUM() OVER(ORDER BY ...) to track running total revenue.
-- ----------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(sales_amount), 2) AS month_revenue,
    ROUND(SUM(SUM(sales_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')), 2) AS cumulative_running_revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- ----------------------------------------------------------
-- Question 32: Month-over-Month Growth (LAG Window Function)
-- Explanation: Computes MoM growth % using the LAG() analytical window function.
-- ----------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS year_month,
        ROUND(SUM(sales_amount), 2) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    year_month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY year_month) AS prior_month_revenue,
    ROUND(((revenue - LAG(revenue, 1) OVER (ORDER BY year_month)) / 
           LAG(revenue, 1) OVER (ORDER BY year_month)) * 100, 2) AS mom_growth_pct
FROM MonthlySales;


-- ----------------------------------------------------------
-- Question 33: Top 3 Products Per Category (DENSE_RANK Partitioned)
-- Explanation: Window function partitioned by category to surface category leaders.
-- ----------------------------------------------------------
WITH RankedCategoryProducts AS (
    SELECT 
        p.category,
        p.product_id,
        p.product_name,
        ROUND(SUM(o.sales_amount), 2) AS product_revenue,
        DENSE_RANK() OVER (
            PARTITION BY p.category 
            ORDER BY SUM(o.sales_amount) DESC
        ) AS rank_in_category
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT 
    category,
    rank_in_category,
    product_id,
    product_name,
    product_revenue
FROM RankedCategoryProducts
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;
