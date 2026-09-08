# Excel E-Commerce Analytics Guide & Modeling Reference

This guide provides step-by-step instructions for navigating, auditing, and extending the financial model and reporting dashboard in `excel/ecommerce_analysis.xlsx`.

---

## 1. Workbook Architecture

The workbook contains 8 structured, color-coded sheets designed for C-suite and analyst workflows:

| Sheet Name | Purpose | Primary Functions / Features |
|---|---|---|
| **Dashboard** | Executive overview with KPI cards, category contribution, and regional summary | Dynamic formulas, merged cards, styled summary tables |
| **KPI Summary** | Formal enterprise metric dictionary with benchmarks and targets | `SUM`, `AVERAGE`, `COUNTIF`, target benchmarks |
| **Sales Analysis** | 36-month time series breakdown (2022–2024) | MoM Growth %, Profit Margin %, formatted currency |
| **Product Analysis** | Top and bottom performers by revenue, margin, and returns | Portfolio segment tags, return rate calculations |
| **Customer Analysis** | RFM segment breakdown (Champions, At Risk, etc.) | Segment order frequency, average spend, revenue share |
| **Regional Analysis** | State-level and regional volume, revenue, profit, and AOV | Regional rollups, margin comparisons |
| **Returns Analysis** | Root-cause breakdown and payment channel performance | Share of returns, payment channel distribution |
| **Pivot Tables** | Source transaction data table (sample 10,000 transactions) | Structured records for custom pivot table exploration |

---

## 2. Core Excel Formulas Implemented

### 1. Dynamic Gross Sales Revenue
```excel
=SUM('Sales Analysis'!E4:E39)
```
Aggregates monthly revenue dynamically across the 36-month operating horizon.

### 2. Net Profit Margin Percentage
```excel
=Dashboard!D6 / Dashboard!B6
```
Calculates blended enterprise profit margin (`Total Net Profit / Total Gross Sales`).

### 3. Month-over-Month (MoM) Growth
```excel
=(E5 - E4) / E4
```
Calculates revenue acceleration from the previous month, formatted as `0.00%`.

### 4. Order Return Rate via Conditional Counting
```excel
=COUNTIF('Pivot Tables'!H4:H50000, "Returned") / Dashboard!F6
```
Measures the percentage of completed orders that resulted in return processing.

### 5. Multi-Condition Aggregations (`SUMIFS` / `COUNTIFS`)
```excel
=SUMIFS('Pivot Tables'!F4:F10000, 'Pivot Tables'!K4:K10000, "South", 'Pivot Tables'!H4:H10000, "Delivered")
```
Calculates total delivered sales volume restricted strictly to the Southern territory.

### 6. Dynamic Pricing & Product Lookup (`XLOOKUP`)
```excel
=XLOOKUP(A4, 'Product Analysis'!A4:A50, 'Product Analysis'!F4:F50, "Not Found", 0)
```
Retrieves the total lifetime revenue for any given `product_id`.

---

## 3. How to Build Native Excel Pivot Tables

Follow these steps in Microsoft Excel to create interactive pivots from the `Pivot Tables` sheet:

### Step 1: Regional Profitability Pivot Table
1. Navigate to sheet `Pivot Tables`.
2. Select range `A3:K10004` and click **Insert > PivotTable**.
3. Place on a **New Worksheet**.
4. Drag fields into areas:
   - **Rows**: `region`, `state`
   - **Values**: `sales_amount` (Summarize by Sum, Format as Currency `₹ #,##0`), `profit_amount` (Summarize by Sum)
   - **Calculated Field**: Name = `Profit Margin %`, Formula = `=profit_amount / sales_amount`.

### Step 2: Customer Status Matrix
1. Select transaction table and create a Pivot Table.
2. Drag `order_status` to **Rows**.
3. Drag `order_id` to **Values** (Summarize by Count).
4. Drag `sales_amount` to **Values** (Show Values As > **% of Grand Total**).

---

## 4. Conditional Formatting Rules Applied
- **Profit Margin Column**: Green-Yellow-Red color gradient highlighting high-margin (>40%) vs low-margin (<15%) categories.
- **Top 10 Performers**: Soft green highlight for the top 10% revenue-generating products.
- **High Return Alert**: Light red fill applied to return rates exceeding the 10.0% threshold.
