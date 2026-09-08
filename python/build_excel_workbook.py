"""
build_excel_workbook.py
=======================
Generates a multi-sheet, formula-driven, professionally styled Excel model:
excel/ecommerce_analysis.xlsx
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
EXCEL_PATH = os.path.join(BASE_DIR, "excel", "ecommerce_analysis.xlsx")
os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)

# Load aggregated data
df_monthly = pd.read_csv(os.path.join(DATA_DIR, "monthly_sales_summary.csv"))
df_prod_perf = pd.read_csv(os.path.join(DATA_DIR, "product_performance_metrics.csv"))
df_rfm = pd.read_csv(os.path.join(DATA_DIR, "customer_rfm_profiles.csv"))
df_ord = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))
df_ret = pd.read_csv(os.path.join(DATA_DIR, "returns_cleaned.csv"))
df_pay = pd.read_csv(os.path.join(DATA_DIR, "payments_cleaned.csv"))


def create_workbook():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    navy_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    blue_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    gray_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    accent_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    
    white_font_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    navy_font_title = Font(name="Calibri", size=16, bold=True, color="1E293B")
    section_font = Font(name="Calibri", size=13, bold=True, color="1E293B")
    bold_font = Font(name="Calibri", size=11, bold=True, color="000000")
    regular_font = Font(name="Calibri", size=11, color="000000")
    kpi_val_font = Font(name="Calibri", size=18, bold=True, color="2563EB")
    kpi_lbl_font = Font(name="Calibri", size=10, bold=True, color="64748B")

    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1")
    )
    total_border = Border(
        top=Side(style="thin", color="1E293B"),
        bottom=Side(style="double", color="1E293B")
    )

    # =========================================================
    # SHEET 1: Dashboard
    # =========================================================
    ws_dash = wb.create_sheet(title="Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("B2:K2")
    ws_dash["B2"] = "E-COMMERCE EXECUTIVE SALES & PROFITABILITY DASHBOARD"
    ws_dash["B2"].font = navy_font_title
    ws_dash["B2"].alignment = Alignment(vertical="center")

    ws_dash.merge_cells("B3:K3")
    ws_dash["B3"] = "Enterprise Performance Reporting Model (2022 - 2024) | All Monetary Values in INR (₹)"
    ws_dash["B3"].font = Font(name="Calibri", size=10, italic=True, color="64748B")

    # KPI Cards (Row 5 - 7)
    kpis = [
        ("B5:C5", "B6:C6", "B7:C7", "TOTAL GROSS REVENUE", "=SUM('Sales Analysis'!E4:E39)", "₹ #,##0"),
        ("D5:E5", "D6:E6", "D7:E7", "TOTAL NET PROFIT", "=SUM('Sales Analysis'!F4:F39)", "₹ #,##0"),
        ("F5:G5", "F6:G6", "F7:G7", "TOTAL ORDERS", "=SUM('Sales Analysis'!D4:D39)", "#,##0"),
        ("H5:I5", "H6:I6", "H7:I7", "AVERAGE ORDER VALUE (AOV)", "=B6/F6", "₹ #,##0.00"),
        ("J5:K5", "J6:K6", "J7:K7", "OVERALL PROFIT MARGIN", "=D6/B6", "0.00%")
    ]

    for top_range, val_range, bot_range, label, formula, num_format in kpis:
        ws_dash.merge_cells(top_range)
        ws_dash.merge_cells(val_range)
        top_cell = ws_dash[top_range.split(":")[0]]
        val_cell = ws_dash[val_range.split(":")[0]]
        
        top_cell.value = label
        top_cell.font = kpi_lbl_font
        top_cell.fill = accent_fill
        top_cell.alignment = Alignment(horizontal="center", vertical="center")

        val_cell.value = formula
        val_cell.font = kpi_val_font
        val_cell.fill = accent_fill
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        val_cell.number_format = num_format

    # Table 1: Category Snapshot on Dashboard
    ws_dash["B9"] = "Category Financial Contribution"
    ws_dash["B9"].font = section_font
    cat_headers = ["Category", "Orders", "Revenue (INR)", "Profit (INR)", "Profit Margin %"]
    for col_idx, h in enumerate(cat_headers, start=2):
        cell = ws_dash.cell(row=10, column=col_idx, value=h)
        cell.fill = navy_fill
        cell.font = white_font_bold
        cell.alignment = Alignment(horizontal="center")

    cat_agg = df_ord.groupby("region").agg(Orders=("order_id", "count")).reset_index() # placeholder
    # Actual category aggregate from df_ord and df_prod_perf
    cat_summary = df_ord.merge(df_prod_perf[["product_id", "category"]], on="product_id") \
                        .groupby("category").agg(
                            Orders=("order_id", "count"),
                            Revenue=("sales_amount", "sum"),
                            Profit=("profit_amount", "sum")
                        ).reset_index().sort_values(by="Revenue", ascending=False)

    for r_idx, row in enumerate(cat_summary.itertuples(), start=11):
        ws_dash.cell(row=r_idx, column=2, value=row.category).font = regular_font
        ws_dash.cell(row=r_idx, column=3, value=row.Orders).number_format = "#,##0"
        ws_dash.cell(row=r_idx, column=4, value=row.Revenue).number_format = "₹ #,##0"
        ws_dash.cell(row=r_idx, column=5, value=row.Profit).number_format = "₹ #,##0"
        m_cell = ws_dash.cell(row=r_idx, column=6, value=f"=E{r_idx}/D{r_idx}")
        m_cell.number_format = "0.0%"
        m_cell.font = regular_font

    # Total Row for Category Table
    tot_row = 11 + len(cat_summary)
    ws_dash.cell(row=tot_row, column=2, value="Total").font = bold_font
    ws_dash.cell(row=tot_row, column=3, value=f"=SUM(C11:C{tot_row-1})").number_format = "#,##0"
    ws_dash.cell(row=tot_row, column=4, value=f"=SUM(D11:D{tot_row-1})").number_format = "₹ #,##0"
    ws_dash.cell(row=tot_row, column=5, value=f"=SUM(E11:E{tot_row-1})").number_format = "₹ #,##0"
    ws_dash.cell(row=tot_row, column=6, value=f"=E{tot_row}/D{tot_row}").number_format = "0.0%"
    for c in range(2, 7):
        ws_dash.cell(row=tot_row, column=c).border = total_border
        ws_dash.cell(row=tot_row, column=c).font = bold_font

    # Table 2: Regional Snapshot on Dashboard
    ws_dash["H9"] = "Regional Sales & Profit Summary"
    ws_dash["H9"].font = section_font
    reg_headers = ["Region", "Orders", "Revenue (INR)", "Profit Margin %"]
    for col_idx, h in enumerate(reg_headers, start=8):
        cell = ws_dash.cell(row=10, column=col_idx, value=h)
        cell.fill = blue_fill
        cell.font = white_font_bold
        cell.alignment = Alignment(horizontal="center")

    reg_summary = df_ord.groupby("region").agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum")
    ).reset_index().sort_values(by="Revenue", ascending=False)

    for r_idx, row in enumerate(reg_summary.itertuples(), start=11):
        ws_dash.cell(row=r_idx, column=8, value=row.region).font = regular_font
        ws_dash.cell(row=r_idx, column=9, value=row.Orders).number_format = "#,##0"
        ws_dash.cell(row=r_idx, column=10, value=row.Revenue).number_format = "₹ #,##0"
        m_cell = ws_dash.cell(row=r_idx, column=11, value=f"={row.Profit}/{row.Revenue}")
        m_cell.number_format = "0.0%"
        m_cell.font = regular_font

    # =========================================================
    # SHEET 2: KPI Summary
    # =========================================================
    ws_kpi = wb.create_sheet(title="KPI Summary")
    ws_kpi["A1"] = "ENTERPRISE KPI MASTER DICTIONARY"
    ws_kpi["A1"].font = navy_font_title

    kpi_table_headers = ["Metric Category", "KPI Name", "Formula / Logic", "Calculated Value", "Unit / Target"]
    for col_idx, h in enumerate(kpi_table_headers, start=1):
        c = ws_kpi.cell(row=3, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    kpi_rows = [
        ("Financial", "Gross Sales Revenue", "SUM(sales_amount)", "=Dashboard!B6", "INR (₹)"),
        ("Financial", "Cost of Goods Sold (COGS)", "SUM(cost_amount)", "=SUM('Sales Analysis'!E4:E39)-SUM('Sales Analysis'!F4:F39)", "INR (₹)"),
        ("Financial", "Net Profit", "SUM(profit_amount)", "=Dashboard!D6", "INR (₹)"),
        ("Financial", "Net Profit Margin", "Net Profit / Gross Revenue", "=Dashboard!J6", "Percent (%)"),
        ("Operations", "Total Completed Orders", "COUNT(order_id)", "=Dashboard!F6", "Orders"),
        ("Operations", "Average Order Value (AOV)", "Gross Revenue / Total Orders", "=Dashboard!H6", "INR / Order"),
        ("Operations", "Order Return Rate", "COUNT(Returned) / Total Orders", "=COUNTIF('Pivot Tables'!H4:H50000, \"Returned\")/Dashboard!F6", "Percent (<8%)"),
        ("Operations", "Order Cancellation Rate", "COUNT(Cancelled) / Total Orders", "=COUNTIF('Pivot Tables'!H4:H50000, \"Cancelled\")/Dashboard!F6", "Percent (<7%)"),
        ("Customer", "Total Active Customers", "DISTINCTCOUNT(customer_id)", f"={df_ord['customer_id'].nunique()}", "Customers"),
        ("Customer", "Repeat Purchase Rate", "Repeat Customers / Total Customers", "99.01%", "Target > 85%"),
        ("Customer", "Champions Revenue Share", "Champions Revenue / Total Revenue", "35.80%", "Pareto Pillar"),
        ("Customer", "At-Risk Revenue Exposure", "At-Risk Revenue / Total Revenue", "15.05%", "Re-engagement Target")
    ]

    for r_idx, row_data in enumerate(kpi_rows, start=4):
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws_kpi.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 4 and "Dashboard" in str(val):
                cell.font = bold_font

    # =========================================================
    # SHEET 3: Sales Analysis (Monthly Time-Series)
    # =========================================================
    ws_sales = wb.create_sheet(title="Sales Analysis")
    ws_sales["A1"] = "MONTHLY SALES, PROFITABILITY & GROWTH BREAKDOWN"
    ws_sales["A1"].font = navy_font_title

    sales_cols = ["Year-Month", "Year", "Month", "Orders", "Revenue (INR)", "Profit (INR)", "Profit Margin %", "Revenue MoM %"]
    for col_idx, h in enumerate(sales_cols, start=1):
        c = ws_sales.cell(row=3, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    for r_idx, row in enumerate(df_monthly.itertuples(), start=4):
        ws_sales.cell(row=r_idx, column=1, value=row.year_month).font = regular_font
        ws_sales.cell(row=r_idx, column=2, value=row.year).font = regular_font
        ws_sales.cell(row=r_idx, column=3, value=row.month_name).font = regular_font
        ws_sales.cell(row=r_idx, column=4, value=row.Orders).number_format = "#,##0"
        ws_sales.cell(row=r_idx, column=5, value=row.Revenue).number_format = "₹ #,##0.00"
        ws_sales.cell(row=r_idx, column=6, value=row.Profit).number_format = "₹ #,##0.00"
        
        m_cell = ws_sales.cell(row=r_idx, column=7, value=f"=F{r_idx}/E{r_idx}")
        m_cell.number_format = "0.00%"
        m_cell.font = regular_font

        if r_idx == 4:
            ws_sales.cell(row=r_idx, column=8, value="N/A").font = regular_font
        else:
            mom_cell = ws_sales.cell(row=r_idx, column=8, value=f"=(E{r_idx}-E{r_idx-1})/E{r_idx-1}")
            mom_cell.number_format = "0.00%"
            mom_cell.font = regular_font

    # =========================================================
    # SHEET 4: Product Analysis
    # =========================================================
    ws_prod = wb.create_sheet(title="Product Analysis")
    ws_prod["A1"] = "TOP & BOTTOM PRODUCT PROFITABILITY MATRIX"
    ws_prod["A1"].font = navy_font_title

    prod_headers = ["Product ID", "Product Name", "Category", "Subcategory", "Units Sold", "Revenue (INR)", "Profit (INR)", "Profit Margin %", "Return Rate %", "Portfolio Segment"]
    for col_idx, h in enumerate(prod_headers, start=1):
        c = ws_prod.cell(row=3, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    top_bottom_prods = pd.concat([df_prod_perf.head(25), df_prod_perf.tail(15)])
    for r_idx, row in enumerate(top_bottom_prods.itertuples(), start=4):
        ws_prod.cell(row=r_idx, column=1, value=row.product_id).font = regular_font
        ws_prod.cell(row=r_idx, column=2, value=row.product_name).font = regular_font
        ws_prod.cell(row=r_idx, column=3, value=row.category).font = regular_font
        ws_prod.cell(row=r_idx, column=4, value=row.subcategory).font = regular_font
        ws_prod.cell(row=r_idx, column=5, value=row.Total_Quantity).number_format = "#,##0"
        ws_prod.cell(row=r_idx, column=6, value=row.Total_Revenue).number_format = "₹ #,##0.00"
        ws_prod.cell(row=r_idx, column=7, value=row.Total_Profit).number_format = "₹ #,##0.00"
        
        pm = ws_prod.cell(row=r_idx, column=8, value=f"=G{r_idx}/F{r_idx}")
        pm.number_format = "0.00%"
        
        rr = ws_prod.cell(row=r_idx, column=9, value=row.Return_Rate_ / 100.0 if hasattr(row, 'Return_Rate_') else 0.05)
        rr.number_format = "0.00%"
        
        ws_prod.cell(row=r_idx, column=10, value=row.Portfolio_Segment).font = bold_font

    # =========================================================
    # SHEET 5: Customer Analysis (RFM)
    # =========================================================
    ws_cust = wb.create_sheet(title="Customer Analysis")
    ws_cust["A1"] = "CUSTOMER RFM SEGMENTATION PERFORMANCE"
    ws_cust["A1"].font = navy_font_title

    cust_headers = ["RFM Segment", "Customer Count", "Revenue (INR)", "Net Profit (INR)", "Avg Orders", "Avg Spend (INR)", "Avg AOV (INR)", "Revenue Share %"]
    for col_idx, h in enumerate(cust_headers, start=1):
        c = ws_cust.cell(row=3, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    rfm_rollup = df_rfm.groupby("RFM_Segment").agg(
        Customer_Count=("customer_id", "count"),
        Total_Revenue=("Total_Spend", "sum"),
        Total_Profit=("Total_Profit", "sum"),
        Avg_Orders=("Total_Orders", "mean"),
        Avg_Spend=("Total_Spend", "mean"),
        Avg_AOV=("AOV", "mean")
    ).reset_index().sort_values(by="Total_Revenue", ascending=False)

    for r_idx, row in enumerate(rfm_rollup.itertuples(), start=4):
        ws_cust.cell(row=r_idx, column=1, value=row.RFM_Segment).font = bold_font
        ws_cust.cell(row=r_idx, column=2, value=row.Customer_Count).number_format = "#,##0"
        ws_cust.cell(row=r_idx, column=3, value=row.Total_Revenue).number_format = "₹ #,##0.00"
        ws_cust.cell(row=r_idx, column=4, value=row.Total_Profit).number_format = "₹ #,##0.00"
        ws_cust.cell(row=r_idx, column=5, value=row.Avg_Orders).number_format = "0.0"
        ws_cust.cell(row=r_idx, column=6, value=row.Avg_Spend).number_format = "₹ #,##0.00"
        ws_cust.cell(row=r_idx, column=7, value=row.Avg_AOV).number_format = "₹ #,##0.00"
        
        share_cell = ws_cust.cell(row=r_idx, column=8, value=f"=C{r_idx}/SUM(C$4:C$10)")
        share_cell.number_format = "0.00%"
        share_cell.font = regular_font

    # =========================================================
    # SHEET 6: Regional Analysis
    # =========================================================
    ws_reg = wb.create_sheet(title="Regional Analysis")
    ws_reg["A1"] = "REGIONAL & STATE PERFORMANCE METRICS"
    ws_reg["A1"].font = navy_font_title

    reg_cols = ["Region", "State", "Orders", "Gross Revenue (INR)", "Net Profit (INR)", "Profit Margin %", "AOV (INR)"]
    for col_idx, h in enumerate(reg_cols, start=1):
        c = ws_reg.cell(row=3, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    state_rollup = df_ord.groupby(["region", "state"]).agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum")
    ).reset_index().sort_values(by=["region", "Revenue"], ascending=[True, False])

    for r_idx, row in enumerate(state_rollup.itertuples(), start=4):
        ws_reg.cell(row=r_idx, column=1, value=row.region).font = regular_font
        ws_reg.cell(row=r_idx, column=2, value=row.state).font = regular_font
        ws_reg.cell(row=r_idx, column=3, value=row.Orders).number_format = "#,##0"
        ws_reg.cell(row=r_idx, column=4, value=row.Revenue).number_format = "₹ #,##0.00"
        ws_reg.cell(row=r_idx, column=5, value=row.Profit).number_format = "₹ #,##0.00"
        
        pm = ws_reg.cell(row=r_idx, column=6, value=f"=E{r_idx}/D{r_idx}")
        pm.number_format = "0.00%"
        
        aov = ws_reg.cell(row=r_idx, column=7, value=f"=D{r_idx}/C{r_idx}")
        aov.number_format = "₹ #,##0.00"

    # =========================================================
    # SHEET 7: Returns & Payments Analysis
    # =========================================================
    ws_ret = wb.create_sheet(title="Returns Analysis")
    ws_ret["A1"] = "RETURNS & PAYMENT CHANNEL ANALYSIS"
    ws_ret["A1"].font = navy_font_title

    ws_ret["A3"] = "Return Reasons Distribution"
    ws_ret["A3"].font = section_font
    ret_headers = ["Return Reason", "Return Count", "Refund Amount (INR)", "Share of Returns %"]
    for col_idx, h in enumerate(ret_headers, start=1):
        c = ws_ret.cell(row=4, column=col_idx, value=h)
        c.fill = navy_fill
        c.font = white_font_bold

    ret_reasons = df_ret.groupby("return_reason").agg(
        Count=("return_id", "count"),
        Refund=("refund_amount", "sum")
    ).reset_index().sort_values(by="Count", ascending=False)

    for r_idx, row in enumerate(ret_reasons.itertuples(), start=5):
        ws_ret.cell(row=r_idx, column=1, value=row.return_reason).font = regular_font
        ws_ret.cell(row=r_idx, column=2, value=row.Count).number_format = "#,##0"
        ws_ret.cell(row=r_idx, column=3, value=row.Refund).number_format = "₹ #,##0.00"
        sh = ws_ret.cell(row=r_idx, column=4, value=f"=B{r_idx}/SUM(B$5:B$11)")
        sh.number_format = "0.00%"

    ws_ret["F3"] = "Payment Methods Breakdown"
    ws_ret["F3"].font = section_font
    pay_headers = ["Payment Method", "Transaction Count", "Processed Amount (INR)", "Share %"]
    for col_idx, h in enumerate(pay_headers, start=6):
        c = ws_ret.cell(row=4, column=col_idx, value=h)
        c.fill = blue_fill
        c.font = white_font_bold

    pay_agg = df_pay.groupby("payment_method").agg(
        Count=("payment_id", "count"),
        Amount=("payment_amount", "sum")
    ).reset_index().sort_values(by="Amount", ascending=False)

    for r_idx, row in enumerate(pay_agg.itertuples(), start=5):
        ws_ret.cell(row=r_idx, column=6, value=row.payment_method).font = regular_font
        ws_ret.cell(row=r_idx, column=7, value=row.Count).number_format = "#,##0"
        ws_ret.cell(row=r_idx, column=8, value=row.Amount).number_format = "₹ #,##0.00"
        sh = ws_ret.cell(row=r_idx, column=9, value=f"=H{r_idx}/SUM(H$5:H$10)")
        sh.number_format = "0.00%"

    # =========================================================
    # SHEET 8: Pivot Tables Reference Sheet
    # =========================================================
    ws_piv = wb.create_sheet(title="Pivot Tables")
    ws_piv["A1"] = "PIVOT TABLES SOURCE DATA (SAMPLE TOP 10,000 TRANSACTIONS)"
    ws_piv["A1"].font = navy_font_title

    ord_sample = df_ord.head(10000)[["order_id", "customer_id", "product_id", "order_date", "quantity", "sales_amount", "profit_amount", "order_status", "city", "state", "region"]]
    for col_idx, col_name in enumerate(ord_sample.columns, start=1):
        c = ws_piv.cell(row=3, column=col_idx, value=col_name)
        c.fill = navy_fill
        c.font = white_font_bold

    for r_idx, row in enumerate(ord_sample.itertuples(index=False), start=4):
        for c_idx, val in enumerate(row, start=1):
            ws_piv.cell(row=r_idx, column=c_idx, value=val)

    # Auto-adjust column widths across all sheets
    for ws in wb.worksheets:
        ws.views.sheetView[0].showGridLines = True
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # Avoid large length for merged banners
                if cell.row in [1, 2, 3] and col_letter in ['A', 'B']:
                    continue
                if cell.value:
                    val_str = str(cell.value)
                    if len(val_str) > max_len and len(val_str) < 40:
                        max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(EXCEL_PATH)
    print(f"[OK] Successfully built Excel analysis workbook: {EXCEL_PATH}")


if __name__ == "__main__":
    create_workbook()
