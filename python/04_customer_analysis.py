"""
04_customer_analysis.py
=======================
E-Commerce Sales, Customer & Profitability Analytics
Customer Lifetime Value & RFM Segmentation Pipeline

Performs:
- Customer order frequency, cumulative spend, lifetime profit, AOV
- Recency, Frequency, Monetary (RFM) quintile calculation
- Rule-based algorithmic customer segmentation:
  * Champions
  * Loyal Customers
  * Potential Loyalists
  * New Customers
  * At Risk
  * Lost Customers
- Analyzes segment revenue contribution and churn vulnerability.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("=" * 65)
    print(" CUSTOMER ANALYTICS & RFM SEGMENTATION")
    print("=" * 65)

    df_cust = pd.read_csv(os.path.join(DATA_DIR, "customers_cleaned.csv"))
    df_ord = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))
    df_ord["order_date"] = pd.to_datetime(df_ord["order_date"])

    # Reference snapshot date: 2024-12-31 (end of dataset)
    snapshot_date = df_ord["order_date"].max() + pd.Timedelta(days=1)
    print(f"[*] RFM Snapshot Reference Date: {snapshot_date.strftime('%Y-%m-%d')}")

    # Aggregate customer order performance
    cust_agg = df_ord.groupby("customer_id").agg(
        Total_Orders=("order_id", "count"),
        Total_Spend=("sales_amount", "sum"),
        Total_Profit=("profit_amount", "sum"),
        First_Purchase_Date=("order_date", "min"),
        Last_Purchase_Date=("order_date", "max"),
        Unique_Products=("product_id", "nunique"),
        Total_Quantity=("quantity", "sum")
    ).reset_index()

    cust_agg["AOV"] = (cust_agg["Total_Spend"] / cust_agg["Total_Orders"]).round(2)
    cust_agg["Profit_Margin_%"] = ((cust_agg["Total_Profit"] / cust_agg["Total_Spend"]) * 100).round(2)

    # Recency: days between last purchase and snapshot date
    cust_agg["Recency_Days"] = (snapshot_date - cust_agg["Last_Purchase_Date"]).dt.days
    cust_agg["Tenure_Days"] = (snapshot_date - cust_agg["First_Purchase_Date"]).dt.days

    # RFM Scoring using quantiles (1 to 5)
    # Higher recency days = lower score (1 is worst, 5 is best)
    cust_agg["R_Score"] = pd.qcut(cust_agg["Recency_Days"], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    
    # Frequency: rank with method='first' to break ties
    cust_agg["F_Score"] = pd.qcut(cust_agg["Total_Orders"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Monetary: spend rank
    cust_agg["M_Score"] = pd.qcut(cust_agg["Total_Spend"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    cust_agg["RFM_Score"] = (
        cust_agg["R_Score"].astype(str) +
        cust_agg["F_Score"].astype(str) +
        cust_agg["M_Score"].astype(str)
    )

    # Business rule mapping for customer segmentation
    def assign_rfm_segment(row):
        r = row["R_Score"]
        f = row["F_Score"]
        m = row["M_Score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 3 and m >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 3:
            if f == 1:
                return "New Customers"
            return "Potential Loyalists"
        elif r <= 2 and f >= 3 and m >= 3:
            return "At Risk"
        elif r <= 2 and f <= 2:
            return "Lost Customers"
        else:
            return "Regular Customers"

    cust_agg["RFM_Segment"] = cust_agg.apply(assign_rfm_segment, axis=1)

    # Join with demographic attributes
    cust_full = cust_agg.merge(
        df_cust[["customer_id", "customer_name", "gender", "age", "city", "state", "region"]],
        on="customer_id",
        how="left"
    )

    # Export customer profile
    cust_profile_path = os.path.join(DATA_DIR, "customer_rfm_profiles.csv")
    cust_full.to_csv(cust_profile_path, index=False)
    print(f"[OK] Saved RFM profiles to {cust_profile_path}")

    # Summary table by RFM segment
    seg_summary = cust_full.groupby("RFM_Segment").agg(
        Customer_Count=("customer_id", "count"),
        Total_Revenue=("Total_Spend", "sum"),
        Total_Profit=("Total_Profit", "sum"),
        Avg_Recency_Days=("Recency_Days", "mean"),
        Avg_Orders=("Total_Orders", "mean"),
        Avg_Spend=("Total_Spend", "mean"),
        Avg_AOV=("AOV", "mean")
    ).reset_index()

    total_rev = seg_summary["Total_Revenue"].sum()
    total_cust = seg_summary["Customer_Count"].sum()
    seg_summary["Customer_Share_%"] = (seg_summary["Customer_Count"] / total_cust) * 100
    seg_summary["Revenue_Share_%"] = (seg_summary["Total_Revenue"] / total_rev) * 100
    seg_summary = seg_summary.sort_values(by="Total_Revenue", ascending=False)

    print("\n--- RFM SEGMENT PERFORMANCE MATRIX ---")
    print(seg_summary.to_string(index=False, formatters={
        "Total_Revenue": lambda x: f"INR {x:,.0f}",
        "Total_Profit": lambda x: f"INR {x:,.0f}",
        "Avg_Recency_Days": lambda x: f"{x:.1f} d",
        "Avg_Orders": lambda x: f"{x:.1f}",
        "Avg_Spend": lambda x: f"INR {x:,.0f}",
        "Avg_AOV": lambda x: f"INR {x:,.0f}",
        "Customer_Share_%": lambda x: f"{x:.1f}%",
        "Revenue_Share_%": lambda x: f"{x:.1f}%",
    }))

    # Top 5 most valuable customers
    print("\n--- TOP 5 HIGHEST VALUE CUSTOMERS ---")
    top5 = cust_full.sort_values(by="Total_Spend", ascending=False).head(5)
    for _, row in top5.iterrows():
        print(f"[{row['customer_id']}] {row['customer_name']} ({row['city']}, {row['region']}) | "
              f"Orders: {row['Total_Orders']} | Spend: INR {row['Total_Spend']:,.2f} | "
              f"Profit: INR {row['Total_Profit']:,.2f} | Segment: {row['RFM_Segment']}")

    print("\nCustomer Analysis Completed Successfully.")


if __name__ == "__main__":
    main()
