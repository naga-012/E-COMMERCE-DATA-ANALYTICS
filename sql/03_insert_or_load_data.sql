-- ==========================================================
-- 03_insert_or_load_data.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Bulk Ingestion Script via LOAD DATA INFILE
-- ==========================================================

USE ecommerce_analytics;

-- Enable local file loading in MySQL session
SET GLOBAL local_infile = 1;

-- ----------------------------------------------------------
-- 1. LOAD CLEANED CUSTOMERS
-- ----------------------------------------------------------
LOAD DATA LOCAL INFILE '../data/cleaned/customers_cleaned.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, customer_name, gender, age, city, state, region, signup_date, customer_segment);

SELECT COUNT(*) AS total_customers_loaded FROM customers;


-- ----------------------------------------------------------
-- 2. LOAD CLEANED PRODUCTS
-- ----------------------------------------------------------
LOAD DATA LOCAL INFILE '../data/cleaned/products_cleaned.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, subcategory, brand, cost_price, selling_price, supplier, stock_quantity, @dummy_margin);

SELECT COUNT(*) AS total_products_loaded FROM products;


-- ----------------------------------------------------------
-- 3. LOAD CLEANED ORDERS
-- ----------------------------------------------------------
LOAD DATA LOCAL INFILE '../data/cleaned/orders_cleaned.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, product_id, order_date, quantity, unit_price, discount_percentage, discount_amount, sales_amount, cost_amount, profit_amount, city, state, region, order_status, @dummy_margin);

SELECT COUNT(*) AS total_orders_loaded FROM orders;


-- ----------------------------------------------------------
-- 4. LOAD CLEANED PAYMENTS
-- ----------------------------------------------------------
LOAD DATA LOCAL INFILE '../data/cleaned/payments_cleaned.csv'
INTO TABLE payments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(payment_id, order_id, payment_date, payment_method, payment_status, payment_amount);

SELECT COUNT(*) AS total_payments_loaded FROM payments;


-- ----------------------------------------------------------
-- 5. LOAD CLEANED RETURNS
-- ----------------------------------------------------------
LOAD DATA LOCAL INFILE '../data/cleaned/returns_cleaned.csv'
INTO TABLE returns
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(return_id, order_id, return_date, return_reason, return_quantity, refund_amount);

SELECT COUNT(*) AS total_returns_loaded FROM returns;

-- ----------------------------------------------------------
-- INGESTION INTEGRITY CHECK
-- ----------------------------------------------------------
SELECT 
    'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 
    'products', COUNT(*) FROM products
UNION ALL
SELECT 
    'orders', COUNT(*) FROM orders
UNION ALL
SELECT 
    'payments', COUNT(*) FROM payments
UNION ALL
SELECT 
    'returns', COUNT(*) FROM returns;
