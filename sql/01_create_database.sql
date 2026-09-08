-- ==========================================================
-- 01_create_database.sql
-- E-Commerce Sales, Customer & Profitability Analytics
-- Database Initialization & Character Set Setup
-- ==========================================================

-- Drop database if already exists to ensure fresh deployment
DROP DATABASE IF EXISTS ecommerce_analytics;

-- Create production database with UTF-8 character encoding and collation
CREATE DATABASE ecommerce_analytics
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Switch to the active database context
USE ecommerce_analytics;

-- Display verification
SELECT 
    DATABASE() AS current_database,
    @@character_set_database AS default_charset,
    @@collation_database AS default_collation;
