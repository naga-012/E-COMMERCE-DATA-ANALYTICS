"""
06_sales_analysis.py
====================
E-Commerce Sales, Customer & Profitability Analytics
Sales Performance, Seasonality & Growth Modeling

Calculates:
- Monthly & Quarterly revenue, profit, volume aggregations
- Month-over-Month (MoM) Growth %
- Year-over-Year (YoY) Growth %
- Day-of-week and monthly seasonal indices
- Highlights peak vs trough sales periods.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")


def main():
    print("=" * 65)
    print(" SALES ANALYSIS: TIME-SERIES, SEASONALITY & GROWTH")
    print("=" * 65)

    df_ord = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))
    df_ord["order_date"] = pd.to_datetime(df_ord["order_date"])
    df_ord["year"] = df_ord["order_date"].dt.year
    df_ord["month"] = df_ord["order_date"].dt.month
    df_ord["month_name"] = df_ord["order_date"].dt.strftime("%b")
    df_ord["year_month"] = df_ord["order_date"].dt.to_period("M").astype(str)
    df_ord["quarter"] = df_ord["order_date"].dt.to_period("Q").astype(str)
    df_ord["day_of_week"] = df_ord["order_date"].dt.day_name()

    # 1. Monthly Performance & MoM Growth
    monthly = df_ord.groupby(["year_month", "year", "month", "month_name"]).agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Units=("quantity", "sum")
    ).reset_index().sort_values(by=["year", "month"]).reset_index(drop=True)

    monthly["AOV"] = (monthly["Revenue"] / monthly["Orders"]).round(2)
    monthly["Profit_Margin_%"] = ((monthly["Profit"] / monthly["Revenue"]) * 100).round(2)

    # MoM Growth
    monthly["Revenue_MoM_%"] = (monthly["Revenue"].pct_change() * 100).round(2)
    monthly["Profit_MoM_%"] = (monthly["Profit"].pct_change() * 100).round(2)
    monthly["Orders_MoM_%"] = (monthly["Orders"].pct_change() * 100).round(2)

    # YoY Growth (shift by 12 months)
    monthly["Revenue_YoY_%"] = (monthly["Revenue"].pct_change(periods=12) * 100).round(2)
    monthly["Profit_YoY_%"] = (monthly["Profit"].pct_change(periods=12) * 100).round(2)

    # Export monthly trend
    out_monthly = os.path.join(DATA_DIR, "monthly_sales_summary.csv")
    monthly.to_csv(out_monthly, index=False)
    print(f"[OK] Monthly sales summary saved to {out_monthly}")

    # 2. Yearly Sales Aggregation
    yearly = df_ord.groupby("year").agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Units=("quantity", "sum")
    ).reset_index()
    yearly["AOV"] = (yearly["Revenue"] / yearly["Orders"]).round(2)
    yearly["Profit_Margin_%"] = ((yearly["Profit"] / yearly["Revenue"]) * 100).round(2)
    yearly["YoY_Revenue_Growth_%"] = (yearly["Revenue"].pct_change() * 100).round(2)
    yearly["YoY_Profit_Growth_%"] = (yearly["Profit"].pct_change() * 100).round(2)

    print("\n--- ANNUAL BUSINESS PERFORMANCE ---")
    print(yearly.to_string(index=False, formatters={
        "Revenue": lambda x: f"INR {x:,.2f}",
        "Profit": lambda x: f"INR {x:,.2f}",
        "AOV": lambda x: f"INR {x:,.2f}",
        "Profit_Margin_%": lambda x: f"{x:.2f}%",
        "YoY_Revenue_Growth_%": lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A",
        "YoY_Profit_Growth_%": lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A",
    }))

    # 3. Quarterly Performance
    quarterly = df_ord.groupby("quarter").agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum")
    ).reset_index()
    quarterly["QoQ_Growth_%"] = (quarterly["Revenue"].pct_change() * 100).round(2)
    print("\n--- QUARTERLY BUSINESS PERFORMANCE (SAMPLE) ---")
    print(quarterly.tail(6).to_string(index=False, formatters={
        "Revenue": lambda x: f"INR {x:,.2f}",
        "Profit": lambda x: f"INR {x:,.2f}",
        "QoQ_Growth_%": lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A"
    }))

    # 4. Seasonal Index by Month
    monthly_seasonality = df_ord.groupby("month_name")["sales_amount"].mean().reindex(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ).reset_index()
    overall_mean = monthly_seasonality["sales_amount"].mean()
    monthly_seasonality["Seasonality_Index"] = (monthly_seasonality["sales_amount"] / overall_mean).round(2)

    print("\n--- MONTHLY SEASONALITY INDEX ---")
    print(monthly_seasonality.to_string(index=False, formatters={
        "sales_amount": lambda x: f"INR {x:,.2f}"
    }))

    # Peak and Trough Months
    best_month = monthly.sort_values(by="Revenue", ascending=False).iloc[0]
    worst_month = monthly.sort_values(by="Revenue", ascending=True).iloc[0]
    print(f"\n[*] All-Time Peak Month:    {best_month['year_month']} with INR {best_month['Revenue']:,.2f} ({best_month['Orders']:,} orders)")
    print(f"[*] All-Time Trough Month:  {worst_month['year_month']} with INR {worst_month['Revenue']:,.2f} ({worst_month['Orders']:,} orders)")

    print("\nSales Analysis Completed Successfully.")


if __name__ == "__main__":
    main()
