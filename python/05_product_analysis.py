"""
05_product_analysis.py
======================
E-Commerce Sales, Customer & Profitability Analytics
Product Profitability & Portfolio Matrix Pipeline

Calculates:
- Revenue, Net Profit, Units Sold, Return Rate, and Profit Margin % per product
- Pareto 80/20 Analysis (identifies top products driving 80% of revenue)
- Portfolio Quadrants:
  1. Stars: High Revenue & High Profit Margin
  2. Cash Cows / Workhorses: High Revenue & Low Margin
  3. Margin Opportunities: Low Revenue & High Margin
  4. Dogs / Underperformers: Low Revenue & Low Margin
- Identifies products with high return rates (> 12%) for quality investigation.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")


def main():
    print("=" * 65)
    print(" PRODUCT PERFORMANCE, PROFITABILITY & PARETO ANALYSIS")
    print("=" * 65)

    df_prod = pd.read_csv(os.path.join(DATA_DIR, "products_cleaned.csv"))
    df_ord = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))

    # Aggregate orders per product
    prod_agg = df_ord.groupby("product_id").agg(
        Total_Orders=("order_id", "count"),
        Total_Quantity=("quantity", "sum"),
        Total_Revenue=("sales_amount", "sum"),
        Total_Cost=("cost_amount", "sum"),
        Total_Profit=("profit_amount", "sum"),
        Returned_Orders=("order_status", lambda s: (s == "Returned").sum()),
        Cancelled_Orders=("order_status", lambda s: (s == "Cancelled").sum())
    ).reset_index()

    prod_agg["Profit_Margin_%"] = ((prod_agg["Total_Profit"] / prod_agg["Total_Revenue"]) * 100).round(2)
    prod_agg["Return_Rate_%"] = ((prod_agg["Returned_Orders"] / prod_agg["Total_Orders"]) * 100).round(2)
    prod_agg["Cancellation_Rate_%"] = ((prod_agg["Cancelled_Orders"] / prod_agg["Total_Orders"]) * 100).round(2)

    # Merge product catalog details
    df_perf = prod_agg.merge(df_prod, on="product_id", how="left")

    # Pareto 80/20 Analysis
    df_perf = df_perf.sort_values(by="Total_Revenue", ascending=False).reset_index(drop=True)
    df_perf["Cum_Revenue"] = df_perf["Total_Revenue"].cumsum()
    total_rev = df_perf["Total_Revenue"].sum()
    df_perf["Cum_Revenue_Pct"] = ((df_perf["Cum_Revenue"] / total_rev) * 100).round(2)
    df_perf["Product_Rank"] = df_perf.index + 1
    df_perf["Cum_Product_Pct"] = ((df_perf["Product_Rank"] / len(df_perf)) * 100).round(2)

    # Threshold for 80% revenue
    pareto_cutoff = df_perf[df_perf["Cum_Revenue_Pct"] <= 80.0]
    pareto_prod_count = len(pareto_cutoff)
    pareto_pct = (pareto_prod_count / len(df_perf)) * 100
    print(f"[*] Pareto Insight: {pareto_prod_count} products ({pareto_pct:.1f}% of catalog) generate 80% of total revenue.")

    # BCG / Portfolio Matrix Classification
    median_rev = df_perf["Total_Revenue"].median()
    median_margin = df_perf["Profit_Margin_%"].median()

    def classify_portfolio(row):
        rev = row["Total_Revenue"]
        margin = row["Profit_Margin_%"]
        if rev >= median_rev and margin >= median_margin:
            return "Star (High Rev, High Margin)"
        elif rev >= median_rev and margin < median_margin:
            return "Volume Driver (High Rev, Low Margin)"
        elif rev < median_rev and margin >= median_margin:
            return "Niche Gem (Low Rev, High Margin)"
        else:
            return "Lagging (Low Rev, Low Margin)"

    df_perf["Portfolio_Segment"] = df_perf.apply(classify_portfolio, axis=1)

    # Save to cleaned
    out_file = os.path.join(DATA_DIR, "product_performance_metrics.csv")
    df_perf.to_csv(out_file, index=False)
    print(f"[OK] Product performance saved to {out_file}")

    # Top 5 Revenue Products
    print("\n--- TOP 5 PRODUCTS BY REVENUE ---")
    top_rev = df_perf.head(5)
    for _, r in top_rev.iterrows():
        print(f"[{r['product_id']}] {r['product_name']} ({r['category']}) | Revenue: INR {r['Total_Revenue']:,.2f} | Profit: INR {r['Total_Profit']:,.2f} | Margin: {r['Profit_Margin_%']:.1f}% | Return Rate: {r['Return_Rate_%']:.1f}%")

    # High Revenue but Low Margin Products
    print("\n--- HIGH REVENUE BUT LOW MARGIN PRODUCTS (Pricing Review Candidate) ---")
    high_rev_low_margin = df_perf[(df_perf["Total_Revenue"] > df_perf["Total_Revenue"].quantile(0.80)) &
                                  (df_perf["Profit_Margin_%"] < df_perf["Profit_Margin_%"].quantile(0.30))].head(5)
    for _, r in high_rev_low_margin.iterrows():
        print(f"[{r['product_id']}] {r['product_name']} ({r['category']}) | Revenue: INR {r['Total_Revenue']:,.2f} | Margin: {r['Profit_Margin_%']:.1f}% | Discount Avg: Check promos")

    # Low Revenue but High Margin Products
    print("\n--- LOW REVENUE BUT HIGH MARGIN PRODUCTS (Scale Up Candidates) ---")
    low_rev_high_margin = df_perf[(df_perf["Total_Revenue"] < df_perf["Total_Revenue"].quantile(0.40)) &
                                  (df_perf["Profit_Margin_%"] > df_perf["Profit_Margin_%"].quantile(0.80))].head(5)
    for _, r in low_rev_high_margin.iterrows():
        print(f"[{r['product_id']}] {r['product_name']} ({r['category']}) | Revenue: INR {r['Total_Revenue']:,.2f} | Margin: {r['Profit_Margin_%']:.1f}% | Units: {r['Total_Quantity']}")

    # High Return Products
    print("\n--- HIGH RETURN RATE PRODUCTS (> 12% returns) ---")
    high_ret = df_perf[df_perf["Return_Rate_%"] > 12.0].sort_values(by="Returned_Orders", ascending=False).head(5)
    for _, r in high_ret.iterrows():
        print(f"[{r['product_id']}] {r['product_name']} ({r['category']}) | Return Rate: {r['Return_Rate_%']:.1f}% | Returned Orders: {r['Returned_Orders']} | Total Orders: {r['Total_Orders']}")

    print("\nProduct Analysis Completed Successfully.")


if __name__ == "__main__":
    main()
