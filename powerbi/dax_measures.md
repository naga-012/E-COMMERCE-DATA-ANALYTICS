# Power BI DAX Measures Reference Manual

This catalog contains the complete collection of production-grade DAX measures designed for the **E-Commerce Sales, Customer & Profitability Analytics** dashboard. All measures are grouped into an isolated `_Measures` table.

---

## 1. Core Financial & Volume Measures

### 1. Total Revenue
```dax
Total Revenue = 
SUM ( FactOrders[sales_amount] )
```
*Business Purpose:* Measures total realized top-line revenue after discounting across all transactions. Format as Currency (`₹ #,##0`).

---

### 2. Total Cost (COGS)
```dax
Total Cost = 
SUM ( FactOrders[cost_amount] )
```
*Business Purpose:* Measures direct cost of goods sold based on supplier unit cost multiplied by order quantity.

---

### 3. Total Profit
```dax
Total Profit = 
[Total Revenue] - [Total Cost]
```
*Business Purpose:* Quantifies net gross profit contribution across the marketplace.

---

### 4. Profit Margin %
```dax
Profit Margin % = 
DIVIDE ( [Total Profit], [Total Revenue], 0 )
```
*Business Purpose:* Computes the percentage of revenue retained as profit. Uses `DIVIDE` to protect against division-by-zero errors. Format as Percentage (`0.0%`).

---

### 5. Total Orders
```dax
Total Orders = 
DISTINCTCOUNT ( FactOrders[order_id] )
```
*Business Purpose:* Counts unique orders placed by customers. Format as Whole Number (`#,##0`).

---

### 6. Total Quantity Sold
```dax
Total Quantity = 
SUM ( FactOrders[quantity] )
```
*Business Purpose:* Measures physical unit sales volume moved through logistics hubs.

---

### 7. Total Customers
```dax
Total Customers = 
DISTINCTCOUNT ( FactOrders[customer_id] )
```
*Business Purpose:* Distinct count of purchasing customer accounts within the selected filter context.

---

### 8. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE ( [Total Revenue], [Total Orders], 0 )
```
*Business Purpose:* Measures the average monetary spend per transaction. Format as Currency (`₹ #,##0.00`).

---

### 9. Average Revenue Per Customer (ARPC)
```dax
Avg Revenue per Customer = 
DIVIDE ( [Total Revenue], [Total Customers], 0 )
```
*Business Purpose:* Evaluates average customer monetization across selected cohorts or territories.

---

## 2. Order Status & Fulfillment Measures

### 10. Delivered Orders
```dax
Delivered Orders = 
CALCULATE (
    [Total Orders],
    FactOrders[order_status] = "Delivered"
)
```
*Business Purpose:* Measures successful, completed customer deliveries.

---

### 11. Returned Orders
```dax
Returned Orders = 
CALCULATE (
    [Total Orders],
    FactOrders[order_status] = "Returned"
)
```
*Business Purpose:* Counts all orders resulting in merchandise returns and reverse logistics.

---

### 12. Return Rate %
```dax
Return Rate % = 
DIVIDE ( [Returned Orders], [Total Orders], 0 )
```
*Business Purpose:* Proportion of orders returned. Key operational metric (Target < 8.0%). Format as Percentage (`0.0%`).

---

### 13. Cancelled Orders
```dax
Cancelled Orders = 
CALCULATE (
    [Total Orders],
    FactOrders[order_status] = "Cancelled"
)
```
*Business Purpose:* Measures pre-dispatch customer or operational cancellations.

---

### 14. Cancellation Rate %
```dax
Cancellation Rate % = 
DIVIDE ( [Cancelled Orders], [Total Orders], 0 )
```
*Business Purpose:* Evaluates friction in payment authorization and stock stockouts. Format as Percentage (`0.0%`).

---

## 3. Customer Cohort & Retention Measures

### 15. New Customers
```dax
New Customers = 
VAR CurrentCustomers = VALUES ( FactOrders[customer_id] )
VAR FirstPurchaseDates = 
    ADDCOLUMNS (
        CurrentCustomers,
        "FirstDate", CALCULATE ( MIN ( FactOrders[order_date] ), ALL ( DimDate ) )
    )
RETURN
COUNTROWS (
    FILTER (
        FirstPurchaseDates,
        [FirstDate] IN VALUES ( DimDate[Date] )
    )
)
```
*Business Purpose:* Identifies first-time purchasers acquired within the selected date window.

---

### 16. Returning Customers
```dax
Returning Customers = 
[Total Customers] - [New Customers]
```
*Business Purpose:* Counts existing accounts placing recurring purchases.

---

## 4. Time Intelligence & Growth Calculations

### 17. Revenue LY (Last Year)
```dax
Revenue LY = 
CALCULATE (
    [Total Revenue],
    SAMEPERIODLASTYEAR ( DimDate[Date] )
)
```
*Business Purpose:* Retrieves total revenue for the identical period in the previous year.

---

### 18. Revenue YoY % (Year-over-Year Growth)
```dax
Revenue YoY % = 
VAR PrevRev = [Revenue LY]
RETURN
IF (
    NOT ISBLANK ( PrevRev ),
    DIVIDE ( [Total Revenue] - PrevRev, PrevRev, 0 )
)
```
*Business Purpose:* Evaluates annual growth acceleration rate. Format as Percentage (`0.0%`).

---

### 19. Profit YoY %
```dax
Profit YoY % = 
VAR ProfitLY = CALCULATE ( [Total Profit], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
RETURN
IF (
    NOT ISBLANK ( ProfitLY ),
    DIVIDE ( [Total Profit] - ProfitLY, ProfitLY, 0 )
)
```
*Business Purpose:* Tracks bottom-line net profit growth rate year-over-year.

---

### 20. Revenue MoM % (Month-over-Month Growth)
```dax
Revenue MoM % = 
VAR CurrentMonthRev = [Total Revenue]
VAR PreviousMonthRev = 
    CALCULATE (
        [Total Revenue],
        PREVIOUSMONTH ( DimDate[Date] )
    )
RETURN
IF (
    NOT ISBLANK ( PreviousMonthRev ),
    DIVIDE ( CurrentMonthRev - PreviousMonthRev, PreviousMonthRev, 0 )
)
```
*Business Purpose:* Measures monthly trajectory and seasonality momentum.

---

### 21. Running Cumulative Revenue
```dax
Running Revenue = 
CALCULATE (
    [Total Revenue],
    FILTER (
        ALLSELECTED ( DimDate[Date] ),
        DimDate[Date] <= MAX ( DimDate[Date] )
    )
)
```
*Business Purpose:* Visualizes cumulative financial progress toward annual corporate revenue milestones.

---

### 22. Revenue % of Total
```dax
Revenue % of Total = 
DIVIDE (
    [Total Revenue],
    CALCULATE ( [Total Revenue], ALLSELECTED () ),
    0
)
```
*Business Purpose:* Measures category or regional percentage contribution to overall business performance.
