-- =============================================================================
-- 07_business_questions.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Comprehensive Master Reference: 50 Production SQL Business Queries
-- =============================================================================

USE ecommerce_analytics;

/*
INDEX OF 50 BUSINESS QUESTIONS:
01. Total revenue
02. Total profit
03. Total orders
04. Total customers
05. Average order value (AOV)
06. Revenue by month
07. Profit by month
08. Top 10 products
09. Top 10 customers
10. Revenue by category
11. Profit by category
12. Revenue by region
13. Monthly growth
14. Yearly growth
15. Repeat customers
16. New customers
17. Customer retention
18. Customer ranking
19. Product ranking
20. Category ranking
21. Highest-profit product
22. Lowest-profit product
23. Highest-margin product
24. Return rate
25. Return reasons
26. Payment-method analysis
27. Customers with more than 5 orders
28. Customers whose spending is above average
29. Products whose revenue is above category average
30. Monthly revenue ranking
31. Running revenue total
32. Month-over-month growth
33. Top 3 products per category
34. Customer RFM preparation
35. Regional performance
36. High-revenue low-profit products
37. High-return products
38. Revenue contribution percentage
39. Pareto/80-20 analysis
40. Customer lifetime value approximation
41. First purchase date
42. Last purchase date
43. Days between purchases
44. Churn-risk customers
45. Most profitable customer segment
46. Average order value by region
47. Profit margin by category
48. Return rate by category
49. Revenue share by payment method
50. Year-over-year growth
*/

-- -----------------------------------------------------------------------------
-- Q01: Total Revenue
-- Business Purpose: Measure overall gross and net delivered top-line turnover.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(sales_amount), 2) AS total_gross_revenue,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN sales_amount ELSE 0 END), 2) AS total_delivered_revenue
FROM orders;


-- -----------------------------------------------------------------------------
-- Q02: Total Profit & Margin
-- Business Purpose: Quantify enterprise bottom-line cash generation and margin.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(profit_amount), 2) AS total_gross_profit,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN profit_amount ELSE 0 END), 2) AS delivered_profit,
    ROUND((SUM(profit_amount) / SUM(sales_amount)) * 100, 2) AS overall_profit_margin_pct
FROM orders;


-- -----------------------------------------------------------------------------
-- Q03: Total Orders by Fulfillment Status
-- Business Purpose: Monitor order volume split across Delivered, Returned, and Cancelled.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM orders;


-- -----------------------------------------------------------------------------
-- Q04: Total Active vs Registered Customers
-- Business Purpose: Assess marketplace customer conversion efficiency.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT customer_id) AS total_active_purchasers,
    (SELECT COUNT(*) FROM customers) AS total_registered_customers
FROM orders;


-- -----------------------------------------------------------------------------
-- Q05: Average Order Value (AOV)
-- Business Purpose: Track average basket monetary size across all transactions.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(AVG(sales_amount), 2) AS overall_aov,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' THEN sales_amount END), 2) AS delivered_aov
FROM orders;


-- -----------------------------------------------------------------------------
-- Q06: Monthly Revenue Trajectory
-- Business Purpose: Review chronological monthly sales to spot seasonal fluctuations.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS monthly_revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- -----------------------------------------------------------------------------
-- Q07: Monthly Profit & Margin Performance
-- Business Purpose: Determine if higher monthly revenue yields healthy profitability.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(profit_amount), 2) AS monthly_profit,
    ROUND((SUM(profit_amount) / SUM(sales_amount)) * 100, 2) AS monthly_margin_pct
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- -----------------------------------------------------------------------------
-- Q08: Top 10 Products by Gross Revenue
-- Business Purpose: Identify the commercial volume drivers of the catalog.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q09: Top 10 Customers by Spending
-- Business Purpose: Surface high-net-worth accounts for loyalty concierge perks.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q10: Revenue by Category & Market Share
-- Business Purpose: Assess catalog mix and category revenue dependencies.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q11: Profit & Margin by Category
-- Business Purpose: Uncover discrepancies between sales volume and bottom-line margin.
-- -----------------------------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS total_revenue,
    ROUND(SUM(o.profit_amount), 2) AS total_profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_profit DESC;


-- -----------------------------------------------------------------------------
-- Q12: Regional Geographic Revenue Distribution
-- Business Purpose: Allocate regional marketing spend and fulfillment capacity.
-- -----------------------------------------------------------------------------
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS regional_revenue,
    ROUND(AVG(sales_amount), 2) AS regional_aov
FROM orders
GROUP BY region
ORDER BY regional_revenue DESC;


-- -----------------------------------------------------------------------------
-- Q13: Monthly Revenue Growth (Self-Join Methodology)
-- Business Purpose: Calculate MoM growth without window functions.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q14: Annual Sales & YoY Growth
-- Business Purpose: Multi-year macro expansion tracking.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q15: Repeat Customers Count & Repeat Purchase Rate
-- Business Purpose: Measure customer stickiness and repeat ordering propensity.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers,
    COUNT(*) AS total_purchasing_customers,
    ROUND((COUNT(CASE WHEN order_count > 1 THEN 1 END) / COUNT(*)) * 100, 2) AS repeat_purchase_rate_pct
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) cust_orders;


-- -----------------------------------------------------------------------------
-- Q16: New Customers Acquired by Cohort Month
-- Business Purpose: Track monthly new customer influx.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q17: Customer Retention Rate (Cohort-Based)
-- Business Purpose: Measure percentage of customer base retaining active repeat status.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q18: Customer Ranking by Lifetime Revenue (DENSE_RANK)
-- Business Purpose: Accurately tier customers without rank gaps.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q19: Product Ranking by Profit Contribution
-- Business Purpose: Rank catalog products by net profit generated.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q20: Category Ranking by Profit Margin %
-- Business Purpose: Rank product categories by percentage margin efficiency.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q21: Highest-Profit Product
-- Business Purpose: Highlight the company's single most profitable SKU.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q22: Lowest-Profit Product
-- Business Purpose: Flag negative/lowest profit products for supplier renegotiation.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q23: Highest-Margin Product (Min 30 Orders)
-- Business Purpose: Identify high-margin niche SKUs that warrant ad spend.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q24: Overall Order Return Rate
-- Business Purpose: Benchmark return incidence rate and reverse logistics value.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND((SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS return_rate_pct,
    ROUND(SUM(CASE WHEN order_status = 'Returned' THEN sales_amount ELSE 0 END), 2) AS returned_merchandise_value
FROM orders;


-- -----------------------------------------------------------------------------
-- Q25: Return Reasons Breakdown
-- Business Purpose: Pinpoint operational root causes for merchandise returns.
-- -----------------------------------------------------------------------------
SELECT 
    return_reason,
    COUNT(return_id) AS return_count,
    ROUND(SUM(refund_amount), 2) AS total_refunded,
    ROUND((COUNT(return_id) / (SELECT COUNT(*) FROM returns)) * 100, 2) AS return_share_pct
FROM returns
GROUP BY return_reason
ORDER BY return_count DESC;


-- -----------------------------------------------------------------------------
-- Q26: Payment Method Processing Volume & Success Rate
-- Business Purpose: Evaluate payment gateway transaction costs and reliability.
-- -----------------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(payment_id) AS transaction_count,
    ROUND(SUM(payment_amount), 2) AS total_volume,
    ROUND(AVG(payment_amount), 2) AS avg_ticket_size,
    ROUND((SUM(CASE WHEN payment_status = 'Success' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS success_rate_pct
FROM payments
GROUP BY payment_method
ORDER BY total_volume DESC;


-- -----------------------------------------------------------------------------
-- Q27: Customers with More than 5 Orders
-- Business Purpose: Identify the high-frequency shopper core.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q28: Customers Spending Above Overall Population Average
-- Business Purpose: Segment premium shoppers outperforming average customer spend.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q29: Products Outperforming Their Category Average Revenue
-- Business Purpose: Identify standout SKUs beating category baselines.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q30: Monthly Revenue Ranking (DENSE_RANK)
-- Business Purpose: Rank peak calendar months across multi-year timeline.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(sales_amount), 2) AS monthly_revenue,
    DENSE_RANK() OVER(ORDER BY SUM(sales_amount) DESC) AS revenue_rank
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY revenue_rank ASC;


-- -----------------------------------------------------------------------------
-- Q31: Running Cumulative Revenue Total
-- Business Purpose: Track company cumulative milestone progression.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    ROUND(SUM(sales_amount), 2) AS month_revenue,
    ROUND(SUM(SUM(sales_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')), 2) AS cumulative_running_revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;


-- -----------------------------------------------------------------------------
-- Q32: Month-over-Month (MoM) Growth via Window Function LAG()
-- Business Purpose: Calculate month-on-month revenue acceleration rate.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q33: Top 3 Products Per Category (Window Partition)
-- Business Purpose: Identify the top 3 revenue anchors within each category.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q34: Customer RFM Metric Preparation
-- Business Purpose: Extract base Recency, Frequency, and Monetary figures.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q35: Regional Performance & Profit Matrix
-- Business Purpose: Multi-dimensional review of regional volume, margin, and AOV.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q36: High-Revenue Low-Profit Products (Quartile Analysis)
-- Business Purpose: Isolate top revenue products suffering from bottom quartile margins.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q37: High-Return Products (> 10% Return Rate, Min 50 Orders)
-- Business Purpose: Alert merchandise quality inspection teams to problematic items.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q38: Revenue Contribution Percentage by Category (SUM OVER ())
-- Business Purpose: Calculate precise share of total company sales per category.
-- -----------------------------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS category_revenue,
    ROUND((SUM(o.sales_amount) / SUM(SUM(o.sales_amount)) OVER ()) * 100, 2) AS pct_of_total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;


-- -----------------------------------------------------------------------------
-- Q39: Pareto / 80-20 Analysis on Product Catalog
-- Business Purpose: Identify the vital minority of SKUs driving 80% of sales.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q40: Customer Lifetime Value (CLV) Approximation
-- Business Purpose: Measure historic cumulative net profit per customer.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q41: Customer First Purchase Date (Acquisition Timing)
-- Business Purpose: Cohort analysis anchor for retention tracking.
-- -----------------------------------------------------------------------------
SELECT 
    customer_id,
    MIN(order_date) AS first_order_date,
    COUNT(order_id) AS lifetime_orders
FROM orders
GROUP BY customer_id
ORDER BY first_order_date ASC
LIMIT 20;


-- -----------------------------------------------------------------------------
-- Q42: Customer Last Purchase Date (Inactivity Metric)
-- Business Purpose: Measure days elapsed since last purchase to detect churn.
-- -----------------------------------------------------------------------------
SELECT 
    customer_id,
    MAX(order_date) AS last_order_date,
    DATEDIFF('2025-01-01', MAX(order_date)) AS days_since_last_order
FROM orders
GROUP BY customer_id
ORDER BY days_since_last_order ASC
LIMIT 20;


-- -----------------------------------------------------------------------------
-- Q43: Days Between Purchases (Purchase Frequency Cadence)
-- Business Purpose: Average inter-order purchase cycle in days.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q44: Churn-Risk Customers (High Spend, Inactive > 120 Days)
-- Business Purpose: Automated targeting list for win-back discount campaigns.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q45: Most Profitable Customer Segment
-- Business Purpose: Compare value generated per customer across customer tiers.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q46: Average Order Value (AOV) by Region
-- Business Purpose: Evaluate regional consumer willingness to pay.
-- -----------------------------------------------------------------------------
SELECT 
    region,
    COUNT(order_id) AS orders_count,
    ROUND(SUM(sales_amount), 2) AS regional_sales,
    ROUND(AVG(sales_amount), 2) AS regional_aov
FROM orders
GROUP BY region
ORDER BY regional_aov DESC;


-- -----------------------------------------------------------------------------
-- Q47: Profit Margin % by Category
-- Business Purpose: Rank categories strictly by net margin percentage.
-- -----------------------------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(o.sales_amount), 2) AS revenue,
    ROUND(SUM(o.profit_amount), 2) AS profit,
    ROUND((SUM(o.profit_amount) / SUM(o.sales_amount)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY profit_margin_pct DESC;


-- -----------------------------------------------------------------------------
-- Q48: Return Rate by Category
-- Business Purpose: Determine return vulnerability across product divisions.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- Q49: Revenue Share by Payment Method
-- Business Purpose: Identify customer payment preferences to negotiate gateway rates.
-- -----------------------------------------------------------------------------
SELECT 
    p.payment_method,
    COUNT(p.payment_id) AS transaction_count,
    ROUND(SUM(p.payment_amount), 2) AS processed_amount,
    ROUND((SUM(p.payment_amount) / SUM(SUM(p.payment_amount)) OVER ()) * 100, 2) AS payment_share_pct
FROM payments p
GROUP BY p.payment_method
ORDER BY processed_amount DESC;


-- -----------------------------------------------------------------------------
-- Q50: Year-over-Year (YoY) Growth by Month (LAG Window Function)
-- Business Purpose: Perform seasonal YoY growth benchmarking matching exact months across years.
-- -----------------------------------------------------------------------------
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
