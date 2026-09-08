-- ==========================================================
-- 02_create_tables.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Relational DDL with Primary Keys, Foreign Keys & Indexes
-- ==========================================================

USE ecommerce_analytics;

-- Drop child tables first to respect referential integrity
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- ----------------------------------------------------------
-- 1. CUSTOMERS TABLE (Dimension)
-- ----------------------------------------------------------
CREATE TABLE customers (
    customer_id         VARCHAR(20)     NOT NULL,
    customer_name       VARCHAR(100)    NOT NULL,
    gender              VARCHAR(20)     NOT NULL,
    age                 INT             NOT NULL,
    city                VARCHAR(50)     NOT NULL,
    state               VARCHAR(50)     NOT NULL,
    region              VARCHAR(30)     NOT NULL,
    signup_date         DATE            NOT NULL,
    customer_segment    VARCHAR(50)     NOT NULL,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_customers PRIMARY KEY (customer_id),
    CONSTRAINT chk_customer_age CHECK (age >= 18 AND age <= 120)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes for customer queries
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_customers_state ON customers(state);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_customers_signup ON customers(signup_date);


-- ----------------------------------------------------------
-- 2. PRODUCTS TABLE (Dimension)
-- ----------------------------------------------------------
CREATE TABLE products (
    product_id          VARCHAR(20)     NOT NULL,
    product_name        VARCHAR(150)    NOT NULL,
    category            VARCHAR(50)     NOT NULL,
    subcategory         VARCHAR(50)     NOT NULL,
    brand               VARCHAR(50)     NOT NULL,
    cost_price          DECIMAL(10, 2)  NOT NULL,
    selling_price       DECIMAL(10, 2)  NOT NULL,
    supplier            VARCHAR(100)    NOT NULL,
    stock_quantity      INT             NOT NULL DEFAULT 0,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_products PRIMARY KEY (product_id),
    CONSTRAINT chk_product_prices CHECK (selling_price >= cost_price AND cost_price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes for product analytics
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_subcategory ON products(subcategory);
CREATE INDEX idx_products_brand ON products(brand);


-- ----------------------------------------------------------
-- 3. ORDERS TABLE (Fact)
-- ----------------------------------------------------------
CREATE TABLE orders (
    order_id            VARCHAR(20)     NOT NULL,
    customer_id         VARCHAR(20)     NOT NULL,
    product_id          VARCHAR(20)     NOT NULL,
    order_date          DATE            NOT NULL,
    quantity            INT             NOT NULL DEFAULT 1,
    unit_price          DECIMAL(10, 2)  NOT NULL,
    discount_percentage DECIMAL(5, 2)   NOT NULL DEFAULT 0.00,
    discount_amount     DECIMAL(10, 2)  NOT NULL DEFAULT 0.00,
    sales_amount        DECIMAL(10, 2)  NOT NULL,
    cost_amount         DECIMAL(10, 2)  NOT NULL,
    profit_amount       DECIMAL(10, 2)  NOT NULL,
    city                VARCHAR(50)     NOT NULL,
    state               VARCHAR(50)     NOT NULL,
    region              VARCHAR(30)     NOT NULL,
    order_status        VARCHAR(30)     NOT NULL,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    CONSTRAINT chk_order_quantity CHECK (quantity > 0),
    CONSTRAINT chk_order_status CHECK (order_status IN ('Delivered', 'Cancelled', 'Returned'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Highly optimized indexes for reporting & time-series
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_product ON orders(product_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_region ON orders(region);
CREATE INDEX idx_orders_date_status ON orders(order_date, order_status);


-- ----------------------------------------------------------
-- 4. PAYMENTS TABLE (Fact)
-- ----------------------------------------------------------
CREATE TABLE payments (
    payment_id          VARCHAR(20)     NOT NULL,
    order_id            VARCHAR(20)     NOT NULL,
    payment_date        DATE            NOT NULL,
    payment_method      VARCHAR(50)     NOT NULL,
    payment_status      VARCHAR(30)     NOT NULL,
    payment_amount      DECIMAL(10, 2)  NOT NULL,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_payments PRIMARY KEY (payment_id),
    CONSTRAINT fk_payments_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT chk_payment_status CHECK (payment_status IN ('Success', 'Failed', 'Refunded'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_method ON payments(payment_method);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_payments_date ON payments(payment_date);


-- ----------------------------------------------------------
-- 5. RETURNS TABLE (Fact)
-- ----------------------------------------------------------
CREATE TABLE returns (
    return_id           VARCHAR(20)     NOT NULL,
    order_id            VARCHAR(20)     NOT NULL,
    return_date         DATE            NOT NULL,
    return_reason       VARCHAR(100)    NOT NULL,
    return_quantity     INT             NOT NULL DEFAULT 1,
    refund_amount       DECIMAL(10, 2)  NOT NULL,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_returns PRIMARY KEY (return_id),
    CONSTRAINT fk_returns_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT chk_return_qty CHECK (return_quantity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_returns_order ON returns(order_id);
CREATE INDEX idx_returns_reason ON returns(return_reason);
CREATE INDEX idx_returns_date ON returns(return_date);
