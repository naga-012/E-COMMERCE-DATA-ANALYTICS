# Power BI Desktop Implementation & Setup Guide

This guide walks through loading the cleaned dataset into Microsoft Power BI Desktop, establishing the Star Schema relationships, creating calculated date tables and measures, and building the interactive 4-page dashboard.

---

## 1. Prerequisites
- **Power BI Desktop** (Free download from Microsoft Store or official website)
- Cleaned CSV dataset files located in `data/cleaned/`:
  - `customers_cleaned.csv`
  - `products_cleaned.csv`
  - `orders_cleaned.csv`
  - `payments_cleaned.csv`
  - `returns_cleaned.csv`
  - `customer_rfm_profiles.csv`

---

## 2. Step-by-Step Data Ingestion

### Step 1: Ingest Cleaned Data
1. Launch **Power BI Desktop**.
2. Click **Get Data > Text/CSV**.
3. Select `data/cleaned/customers_cleaned.csv` and click **Transform Data** to open the Power Query Editor.
4. In Power Query, repeat for the other CSV files (`products_cleaned.csv`, `orders_cleaned.csv`, `payments_cleaned.csv`, `returns_cleaned.csv`, `customer_rfm_profiles.csv`).
5. Verify column data types:
   - `order_date`, `signup_date`, `payment_date`, `return_date` -> **Date**
   - `sales_amount`, `cost_amount`, `profit_amount`, `unit_price`, `refund_amount` -> **Fixed Decimal Number** (Currency)
   - `quantity`, `age`, `stock_quantity` -> **Whole Number**
6. Click **Close & Apply**.

---

## 3. Creating the Dimension Date Table

In the **Modeling** tab, click **New Table** and paste the following DAX formula:

```dax
DimDate = 
VAR MinDate = MIN('orders_cleaned'[order_date])
VAR MaxDate = MAX('orders_cleaned'[order_date])
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

> **Important**: Select column `MonthName`, go to **Column Tools**, click **Sort by Column**, and select `MonthNumber`.

---

## 4. Establishing Model Relationships

Switch to the **Model View** tab in Power BI Desktop and configure the relationships:

1. **`orders_cleaned` to `customers_cleaned`**:
   - Drag `orders_cleaned[customer_id]` to `customers_cleaned[customer_id]`.
   - Cardinality: **Many to One (*:1)** | Cross filter: **Single**.
2. **`orders_cleaned` to `products_cleaned`**:
   - Drag `orders_cleaned[product_id]` to `products_cleaned[product_id]`.
   - Cardinality: **Many to One (*:1)** | Cross filter: **Single**.
3. **`orders_cleaned` to `DimDate`**:
   - Drag `orders_cleaned[order_date]` to `DimDate[Date]`.
   - Cardinality: **Many to One (*:1)** | Cross filter: **Single**.
4. **`payments_cleaned` to `orders_cleaned`**:
   - Drag `payments_cleaned[order_id]` to `orders_cleaned[order_id]`.
   - Cardinality: **Many to One (*:1)** | Cross filter: **Both**.
5. **`returns_cleaned` to `orders_cleaned`**:
   - Drag `returns_cleaned[order_id]` to `orders_cleaned[order_id]`.
   - Cardinality: **Many to One (*:1)** | Cross filter: **Both**.

---

## 5. Creating the Measures Table

1. On the **Home** tab, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` and select **New Measure**.
4. Copy and paste the DAX measures from [dax_measures.md](file:///c:/Users/myaka/OneDrive/Desktop/E-commerce/powerbi/dax_measures.md).
5. Delete the blank `Column1` from `_Measures` so the table turns into a calculator icon at the top of the Fields pane.

---

## 6. Building the 4-Page Dashboard Visuals

Follow the layout specifications defined in [dashboard_design.md](file:///c:/Users/myaka/OneDrive/Desktop/E-commerce/powerbi/dashboard_design.md):

- **Page 1**: Executive Overview (KPI cards, Monthly Trend combo chart, Category breakdown, Regional comparison).
- **Page 2**: Customer Analytics (RFM Segment donut chart, New vs Returning area chart, Top customer leaderboard).
- **Page 3**: Product Analytics (BCG scatterplot, Pareto 80/20 curve, High-margin scale-up opportunities).
- **Page 4**: Regional & Returns (India state map, Return reasons horizontal bar chart, Payment method treemap).

---

## 7. Publishing & Sharing
1. Save the file locally as `E-Commerce_Analytics_Dashboard.pbix`.
2. Click **Publish** on the **Home** tab to deploy to your Power BI Service workspace.
3. Configure scheduled refresh if connected to an automated cloud database or OneDrive folder.
