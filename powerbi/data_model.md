# Power BI Dimensional Data Model (Star Schema)

This document specifies the enterprise Star Schema architecture implemented for the **E-Commerce Sales, Customer & Profitability Analytics** Power BI semantic model.

---

## 1. Architectural Architecture Overview

The semantic model follows Kimball dimensional modeling principles. It consists of **three Fact tables** sharing conforming **Dimension tables** in a high-performance Star/Constellation Schema.

```
       +-------------------+       +-------------------+
       |    DimCustomer    |       |    DimProduct     |
       +-------------------+       +-------------------+
                 \                       /
           1:*    \                     / 1:*
                   \                   /
             +-------------------------------+
             |          FactOrders           |
             +-------------------------------+
              /             |               \
        1:1  /        1:*   |         1:*    \  1:*
            /               |                 \
  +------------------+  +------------------+  +--------------------+
  |   FactPayments   |  |   FactReturns    |  |      DimDate       |
  +------------------+  +------------------+  +--------------------+
                            |
                      1:*   |
                      +-------------------+
                      |   DimGeography    |
                      +-------------------+
```

---

## 2. Table Specifications

### Dimension Tables

#### 1. `DimCustomer`
- **Primary Source**: `data/cleaned/customers_cleaned.csv`
- **Primary Key**: `customer_id`
- **Attributes**:
  - `customer_id` (Text) — Unique business identifier (e.g., `CUST-00001`)
  - `customer_name` (Text) — Full customer name
  - `gender` (Text) — Male, Female, Other
  - `age` (Whole Number) — Standardized age (18–70)
  - `signup_date` (Date) — Initial account creation date
  - `customer_segment` (Text) — New Customer, Regular Customer, Loyal Customer, VIP Customer

#### 2. `DimProduct`
- **Primary Source**: `data/cleaned/products_cleaned.csv`
- **Primary Key**: `product_id`
- **Attributes**:
  - `product_id` (Text) — Unique SKU identifier (e.g., `PROD-0001`)
  - `product_name` (Text) — Descriptive title
  - `category` (Text) — 8 primary divisions (Electronics, Fashion, etc.)
  - `subcategory` (Text) — Granular category classification
  - `brand` (Text) — Brand/Manufacturer name
  - `cost_price` (Decimal Currency) — Standard baseline purchase price
  - `selling_price` (Decimal Currency) — Retail selling price (MRP)
  - `supplier` (Text) — Direct vendor/distributor
  - `stock_quantity` (Whole Number) — Current warehouse inventory level

#### 3. `DimDate`
- **Generated via DAX**:
  ```dax
  DimDate = 
  VAR MinDate = MIN(FactOrders[order_date])
  VAR MaxDate = MAX(FactOrders[order_date])
  RETURN
  ADDCOLUMNS (
      CALENDAR(MinDate, MaxDate),
      "Year", YEAR([Date]),
      "YearMonth", FORMAT([Date], "YYYY-MM"),
      "MonthName", FORMAT([Date], "MMM"),
      "MonthNumber", MONTH([Date]),
      "Quarter", "Q" & FORMAT([Date], "Q"),
      "YearQuarter", FORMAT([Date], "YYYY") & " Q" & FORMAT([Date], "Q"),
      "DayOfWeek", FORMAT([Date], "dddd"),
      "DayOfWeekNumber", WEEKDAY([Date], 2),
      "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")
  )
  ```
- **Primary Key**: `Date`

#### 4. `DimGeography`
- **Normalized Geographic Dimension**:
  - `city` (Text) — City name
  - `state` (Text) — State jurisdiction
  - `region` (Text) — Geographic zone (North, South, East, West, Central)

---

### Fact Tables

#### 1. `FactOrders` (Grain: 1 Row per Order Line Item)
- **Primary Source**: `data/cleaned/orders_cleaned.csv`
- **Primary Key**: `order_id`
- **Foreign Keys**: `customer_id`, `product_id`, `order_date`, `city`
- **Measures & Metrics**:
  - `quantity` (Whole Number)
  - `unit_price` (Decimal)
  - `discount_percentage` (Decimal)
  - `discount_amount` (Decimal)
  - `sales_amount` (Decimal) — Net sales revenue realized
  - `cost_amount` (Decimal) — Realized COGS
  - `profit_amount` (Decimal) — Net gross profit contribution
  - `order_status` (Text) — `Delivered`, `Cancelled`, `Returned`

#### 2. `FactPayments` (Grain: 1 Row per Payment Attempt)
- **Primary Source**: `data/cleaned/payments_cleaned.csv`
- **Primary Key**: `payment_id`
- **Foreign Key**: `order_id`, `payment_date`
- **Attributes**: `payment_method`, `payment_status`, `payment_amount`

#### 3. `FactReturns` (Grain: 1 Row per Return Incident)
- **Primary Source**: `data/cleaned/returns_cleaned.csv`
- **Primary Key**: `return_id`
- **Foreign Key**: `order_id`, `return_date`
- **Attributes**: `return_reason`, `return_quantity`, `refund_amount`

---

## 3. Relational Schema & Cardinality Map

| From Table | To Table | Join Column | Cardinality | Filter Direction | Active |
|---|---|---|---|---|---|
| `FactOrders` | `DimCustomer` | `customer_id` | Many-to-One (*:1) | Single (`DimCustomer` filters `FactOrders`) | Yes |
| `FactOrders` | `DimProduct` | `product_id` | Many-to-One (*:1) | Single (`DimProduct` filters `FactOrders`) | Yes |
| `FactOrders` | `DimDate` | `order_date` -> `Date` | Many-to-One (*:1) | Single (`DimDate` filters `FactOrders`) | Yes |
| `FactPayments` | `FactOrders` | `order_id` | Many-to-One (*:1) | Both (Bi-directional or Single) | Yes |
| `FactReturns` | `FactOrders` | `order_id` | Many-to-One (*:1) | Both (Bi-directional) | Yes |
| `FactOrders` | `DimGeography` | `city` | Many-to-One (*:1) | Single (`DimGeography` filters `FactOrders`) | Yes |

---

## 4. Best Practice Modeling Principles
1. **Star Schema Dominance**: All slicing dimensions connect directly to facts to optimize VertiPaq compression.
2. **Hidden Foreign Keys**: Hide all FKs in Fact tables (`FactOrders[customer_id]`, etc.) to force end-users to slice using validated Dimension fields.
3. **Dedicated Measures Table**: Create an empty table `_Measures` to house all DAX business measures for clean discovery.
