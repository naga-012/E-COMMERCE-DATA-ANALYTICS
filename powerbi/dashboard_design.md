# Power BI Executive Dashboard UI/UX Design Blueprint

This document details the layout, visual hierarchy, user experience architecture, and styling rules for the 4-page executive report in Power BI Desktop.

---

## 1. Global Visual Theme & Color Palette

- **Canvas Size**: 16:9 widescreen (1920 x 1080 px or 1280 x 720 px)
- **Background**: Soft Gray (`#F8FAFC`) with elevated White cards (`#FFFFFF`) featuring subtle shadow radii.
- **Header Accent**: Dark Slate Navy (`#1E293B`)
- **Brand Primary Accent**: Royal Indigo Blue (`#2563EB`)
- **Success / Profit Green**: Emerald (`#10B981`)
- **Warning / Alert**: Amber Gold (`#F59E0B`)
- **Critical / Returns**: Crimson Rose (`#EF4444`)
- **Typography**: Segoe UI (Standard Microsoft BI Typography) or Inter (Clean Modern Sans)

---

## 2. Global Slicer Panel (Header / Left Side Navigation)

Placed across the top banner or collapsible left pane on every page:
1. **Date Hierarchy Slicer**: Year (`2022`, `2023`, `2024`), Quarter, Month (Dropdown or Tile format)
2. **Region & State**: Hierarchy dropdown filter
3. **Category & Subcategory**: Slicer dropdown
4. **Customer Segment**: Multi-select pills (`Champions`, `Loyal`, `At Risk`, `New`)
5. **Clear All Slicers**: Reset bookmark button

---

## 3. Page 1: Executive Overview

**Target Audience:** CEO, CFO, VP of E-Commerce  
**Goal:** Deliver an instant health check on commercial performance, profit trajectory, and high-level mix.

```
+----------------------------------------------------------------------------------------------------+
|  [LOGO]  E-COMMERCE EXECUTIVE PERFORMANCE DASHBOARD             [Slicers: Date | Region | Cat]     |
+----------------------------------------------------------------------------------------------------+
| [ KPI 1: Revenue ]  [ KPI 2: Net Profit ]  [ KPI 3: Orders ]  [ KPI 4: Customers ]  [ KPI 5: Margin ]|
|   ₹ 13.48 Cr           ₹ 3.86 Cr              52,500             5,156                 28.6%       |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: Monthly Revenue & Profit Margin Trend |  VISUAL 2: Revenue & Margin by Category         |
|  (Combo: Clustered Column & Line Chart)          |  (Horizontal Bar Chart sorted by Revenue)       |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: Regional Sales & Profit Comparison    |  VISUAL 4: Top 10 Revenue-Generating SKUs       |
|  (Clustered Column Chart: Revenue vs Profit)     |  (Horizontal Bar Chart with data callouts)      |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications:
1. **Top KPI Cards Container**: 5 modern multi-row cards showing `[Total Revenue]`, `[Total Profit]`, `[Total Orders]`, `[Average Order Value]`, and `[Profit Margin %]` with small sparklines.
2. **Monthly Revenue & Profit Margin Trend**:
   - **X-axis**: `DimDate[YearMonth]`
   - **Column y-axis**: `[Total Revenue]` (Navy Blue bars)
   - **Line y-axis**: `[Profit Margin %]` (Emerald Green line with data markers)
3. **Revenue by Category**:
   - **Y-axis**: `DimProduct[category]`
   - **X-axis**: `[Total Revenue]`
   - **Tooltips**: `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]`
4. **Regional Sales Comparison**:
   - **X-axis**: `DimGeography[region]`
   - **Y-axis**: `[Total Revenue]`, `[Total Profit]`
5. **Top 10 Products**:
   - Filtered via Top N filter: `DimProduct[product_name]` by `[Total Revenue]` Top 10.

---

## 4. Page 2: Customer Analytics & RFM Segmentation

**Target Audience:** CMO, Head of CRM, Retention Strategist  
**Goal:** Deep-dive into customer retention, cohort health, repeat ordering, and high-value tier protection.

```
+----------------------------------------------------------------------------------------------------+
|  CUSTOMER LIFETIME VALUE & RFM COHORT ANALYTICS                 [Slicers: Segment | Region]        |
+----------------------------------------------------------------------------------------------------+
| [ Active Customers: 5,156 ] [ Repeat Rate: 99.0% ] [ ARPC: ₹ 26,138 ] [ Champions Share: 35.8% ]  |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: RFM Segment Contribution Matrix       |  VISUAL 2: Customer Spend Distribution          |
|  (Donut Chart: Revenue Share by RFM Segment)     |  (Histogram / Binned Spend Categories)          |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: New vs Returning Customers Over Time  |  VISUAL 4: Top 15 Customer Leaderboard Table    |
|  (Stacked Area Chart: Month x Customer Type)     |  (Table: Customer, City, Orders, Spend, Tier)   |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications:
1. **RFM Segment Donut Chart**:
   - **Legend**: `customer_rfm_profiles[RFM_Segment]` (`Champions`, `Loyal Customers`, `At Risk`, `Lost`, etc.)
   - **Values**: `[Total Revenue]`
   - **Data Label**: Category and percentage of total
2. **New vs Returning Monthly Orders**:
   - **X-axis**: `DimDate[YearMonth]`
   - **Y-axis**: Order counts stacked by customer type
3. **Top 15 High-Value Customer Leaderboard**:
   - Table visual: `customer_id`, `customer_name`, `city`, `Total Orders`, `Total Spend`, `RFM_Segment`, Conditional data bars on Spend.

---

## 5. Page 3: Product Profitability & Portfolio Matrix

**Target Audience:** Head of Merchandising, Supply Chain Director  
**Goal:** Isolate high-turnover/low-margin SKUs, identify margin scale-up opportunities, and audit return rates.

```
+----------------------------------------------------------------------------------------------------+
|  PRODUCT PERFORMANCE & PROFITABILITY MATRIX                     [Slicers: Category | Brand]       |
+----------------------------------------------------------------------------------------------------+
| [ Total SKUs: 550 ]  [ Star SKUs: 142 ]  [ Avg Margin: 28.6% ]  [ Low-Margin Volume: ₹ 2.1 Cr ]    |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: Product BCG Profitability Scatterplot |  VISUAL 2: Pareto 80/20 Cumulative Revenue Curve|
|  (X: Sales Volume, Y: Profit Margin %, Size: Qty)|  (Line & Clustered Column: Product Rank x Cum %)|
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: Top 10 High-Revenue Low-Margin Alert  |  VISUAL 4: High-Return Risk Products (>10%)     |
|  (Table: SKU, Category, Sales, Margin % < 15%)   |  (Bar Chart: Products with high return rates)   |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications:
1. **Product Profitability Scatter Plot**:
   - **X-axis**: `[Total Revenue]`
   - **Y-axis**: `[Profit Margin %]`
   - **Size**: `[Total Quantity]`
   - **Legend**: `DimProduct[category]`
   - Quadrant reference lines at median revenue and median margin.
2. **Pareto 80/20 Chart**:
   - Column showing individual SKU revenue, line showing running cumulative percentage hitting the 80% reference mark.

---

## 6. Page 4: Regional & Reverse Logistics (Returns)

**Target Audience:** VP of Logistics, Customer Experience Director  
**Goal:** Track geographical growth corridors and systematically reduce return friction.

```
+----------------------------------------------------------------------------------------------------+
|  REGIONAL SALES & REVERSE LOGISTICS ANALYTICS                   [Slicers: Year | State]            |
+----------------------------------------------------------------------------------------------------+
| [ Return Rate: 7.00% ] [ Returned Value: ₹ 94.2 L ] [ Top Reason: Size Issue (20.9%) ] [ UPI: 42% ]|
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 1: India Regional Sales Bubble Map       |  VISUAL 2: Return Reasons Breakdown             |
|  (Filled / Bubble Map by Indian State & City)    |  (Horizontal Bar Chart: Count by Reason)        |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
|                                                  |                                                 |
|  VISUAL 3: Return Rate % by Product Category     |  VISUAL 4: Payment Tender Processing Volume     |
|  (Bar Chart comparing category return rates)     |  (Treemap: Transaction Share by Payment Method) |
|                                                  |                                                 |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications:
1. **India State Geographic Map**:
   - **Location**: `DimGeography[state]`
   - **Size / Bubble**: `[Total Revenue]`
   - **Color saturation**: `[Profit Margin %]`
2. **Return Reasons Breakdown**:
   - Bar chart showing return incident counts for `Size Issue`, `Damaged Product`, `Quality Issue`, `Wrong Product`, `Changed Mind`, `Late Delivery`.
3. **Category Return Rate Comparison**:
   - Clearly highlights Fashion (~14%) vs Electronics (~8%) vs Grocery (~2%).
4. **Payment Method Treemap**:
   - Tenders: `UPI`, `Credit Card`, `Debit Card`, `Net Banking`, `Cash on Delivery`, `Wallet`.
