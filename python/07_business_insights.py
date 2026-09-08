"""
07_business_insights.py
=======================
E-Commerce Sales, Customer & Profitability Analytics
Automated Business Insights & Numerical Fact Generator

Extracts all core business insights and exact numerical findings directly from
the cleaned datasets. Outputs verifiable figures for executive reports,
dashboards, and interview talking points.
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
REPORT_DIR = os.path.join(BASE_DIR, "reports")


def main():
    print("=" * 65)
    print(" GENERATING VERIFIABLE BUSINESS INSIGHTS & FACT SHEET")
    print("=" * 65)

    df_cust = pd.read_csv(os.path.join(DATA_DIR, "customers_cleaned.csv"))
    df_prod = pd.read_csv(os.path.join(DATA_DIR, "products_cleaned.csv"))
    df_ord = pd.read_csv(os.path.join(DATA_DIR, "orders_cleaned.csv"))
    df_pay = pd.read_csv(os.path.join(DATA_DIR, "payments_cleaned.csv"))
    df_ret = pd.read_csv(os.path.join(DATA_DIR, "returns_cleaned.csv"))
    df_rfm = pd.read_csv(os.path.join(DATA_DIR, "customer_rfm_profiles.csv"))

    df_ord["order_date"] = pd.to_datetime(df_ord["order_date"])
    df_ord["year"] = df_ord["order_date"].dt.year
    df_ord_prod = df_ord.merge(df_prod, on="product_id", how="left")

    facts = {}

    # 1. Macro KPIs
    total_rev = float(df_ord["sales_amount"].sum())
    total_prof = float(df_ord["profit_amount"].sum())
    total_cost = float(df_ord["cost_amount"].sum())
    total_orders = int(len(df_ord))
    total_cust = int(df_ord["customer_id"].nunique())
    aov = total_rev / total_orders
    overall_margin = (total_prof / total_rev) * 100

    delivered = df_ord[df_ord["order_status"] == "Delivered"]
    returned = df_ord[df_ord["order_status"] == "Returned"]
    cancelled = df_ord[df_ord["order_status"] == "Cancelled"]

    facts["macro"] = {
        "total_revenue_inr": total_rev,
        "total_profit_inr": total_prof,
        "total_cost_inr": total_cost,
        "delivered_revenue_inr": float(delivered["sales_amount"].sum()),
        "delivered_profit_inr": float(delivered["profit_amount"].sum()),
        "total_orders": total_orders,
        "total_customers": total_cust,
        "aov_inr": aov,
        "profit_margin_pct": overall_margin,
        "return_rate_pct": (len(returned) / total_orders) * 100,
        "returned_orders_count": len(returned),
        "returned_value_inr": float(returned["sales_amount"].sum()),
        "cancelled_orders_count": len(cancelled),
        "cancellation_rate_pct": (len(cancelled) / total_orders) * 100,
    }

    # 2. Category Performance
    cat_summary = df_ord_prod.groupby("category").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Orders=("order_id", "count")
    ).reset_index()
    cat_summary["Margin_Pct"] = (cat_summary["Profit"] / cat_summary["Revenue"]) * 100
    cat_summary["Revenue_Share_%"] = (cat_summary["Revenue"] / total_rev) * 100
    cat_sorted_rev = cat_summary.sort_values(by="Revenue", ascending=False)
    cat_sorted_margin = cat_summary.sort_values(by="Margin_Pct", ascending=False)

    top_rev_cat = cat_sorted_rev.iloc[0]
    top_margin_cat = cat_sorted_margin.iloc[0]
    lowest_margin_cat = cat_sorted_margin.iloc[-1]

    facts["categories"] = {
        "highest_revenue": {
            "name": top_rev_cat["category"],
            "revenue_inr": float(top_rev_cat["Revenue"]),
            "share_pct": float(top_rev_cat["Revenue_Share_%"]),
            "margin_pct": float(top_rev_cat["Margin_Pct"])
        },
        "highest_margin": {
            "name": top_margin_cat["category"],
            "margin_pct": float(top_margin_cat["Margin_Pct"]),
            "revenue_inr": float(top_margin_cat["Revenue"])
        },
        "lowest_margin": {
            "name": lowest_margin_cat["category"],
            "margin_pct": float(lowest_margin_cat["Margin_Pct"]),
            "revenue_inr": float(lowest_margin_cat["Revenue"])
        }
    }

    # 3. Regional Performance
    reg_summary = df_ord.groupby("region").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Orders=("order_id", "count")
    ).reset_index()
    reg_summary["Margin_Pct"] = (reg_summary["Profit"] / reg_summary["Revenue"]) * 100
    reg_summary["Revenue_Share_%"] = (reg_summary["Revenue"] / total_rev) * 100
    reg_sorted = reg_summary.sort_values(by="Revenue", ascending=False)
    
    top_reg = reg_sorted.iloc[0]
    lowest_reg = reg_sorted.iloc[-1]

    facts["regions"] = {
        "top_region": {
            "name": top_reg["region"],
            "revenue_inr": float(top_reg["Revenue"]),
            "share_pct": float(top_reg["Revenue_Share_%"]),
            "margin_pct": float(top_reg["Margin_Pct"])
        },
        "lowest_region": {
            "name": lowest_reg["region"],
            "revenue_inr": float(lowest_reg["Revenue"]),
            "share_pct": float(lowest_reg["Revenue_Share_%"]),
            "margin_pct": float(lowest_reg["Margin_Pct"])
        }
    }

    # Top State
    state_summary = df_ord.groupby("state").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Orders=("order_id", "count")
    ).reset_index().sort_values(by="Revenue", ascending=False)
    top_state = state_summary.iloc[0]
    lowest_state = state_summary.iloc[-1]

    facts["states"] = {
        "top_state": {
            "name": top_state["state"],
            "revenue_inr": float(top_state["Revenue"]),
            "profit_inr": float(top_state["Profit"]),
            "share_pct": float((top_state["Revenue"] / total_rev) * 100)
        },
        "lowest_state": {
            "name": lowest_state["state"],
            "revenue_inr": float(lowest_state["Revenue"]),
            "share_pct": float((lowest_state["Revenue"] / total_rev) * 100)
        }
    }

    # 4. Customer RFM Segments
    rfm_summary = df_rfm.groupby("RFM_Segment").agg(
        Customers=("customer_id", "count"),
        Revenue=("Total_Spend", "sum"),
        Profit=("Total_Profit", "sum")
    ).reset_index()
    rfm_summary["Revenue_Share_%"] = (rfm_summary["Revenue"] / total_rev) * 100

    champions = rfm_summary[rfm_summary["RFM_Segment"] == "Champions"].iloc[0]
    at_risk = rfm_summary[rfm_summary["RFM_Segment"] == "At Risk"].iloc[0]

    facts["rfm"] = {
        "champions": {
            "count": int(champions["Customers"]),
            "revenue_inr": float(champions["Revenue"]),
            "revenue_share_pct": float(champions["Revenue_Share_%"])
        },
        "at_risk": {
            "count": int(at_risk["Customers"]),
            "revenue_inr": float(at_risk["Revenue"]),
            "revenue_share_pct": float(at_risk["Revenue_Share_%"])
        }
    }

    # 5. Returns Root Cause
    ret_summary = df_ret.groupby("return_reason").agg(
        Count=("return_id", "count"),
        Refund=("refund_amount", "sum")
    ).reset_index().sort_values(by="Count", ascending=False)
    top_reason = ret_summary.iloc[0]

    facts["returns"] = {
        "top_reason": {
            "reason": top_reason["return_reason"],
            "count": int(top_reason["Count"]),
            "pct_of_returns": float((top_reason["Count"] / len(df_ret)) * 100),
            "refund_inr": float(top_reason["Refund"])
        }
    }

    # 6. Payment Methods
    pay_summary = df_pay.groupby("payment_method").agg(
        Transactions=("payment_id", "count"),
        Amount=("payment_amount", "sum")
    ).reset_index().sort_values(by="Amount", ascending=False)
    top_pay = pay_summary.iloc[0]

    facts["payments"] = {
        "top_method": {
            "method": top_pay["payment_method"],
            "volume_inr": float(top_pay["Amount"]),
            "share_pct": float((top_pay["Amount"] / total_rev) * 100)
        }
    }

    # Save to JSON
    json_path = os.path.join(REPORT_DIR, "business_facts.json")
    with open(json_path, "w") as f:
        json.dump(facts, f, indent=4)

    print(f"[OK] Saved Business Facts JSON to {json_path}")
    print("\n--- EXECUTIVE FACT SUMMARY ---")
    print(f"Total Marketplace Revenue:  INR {facts['macro']['total_revenue_inr']:,.2f}")
    print(f"Delivered Revenue:          INR {facts['macro']['delivered_revenue_inr']:,.2f}")
    print(f"Total Net Profit:           INR {facts['macro']['total_profit_inr']:,.2f}")
    print(f"Blended Profit Margin:      {facts['macro']['profit_margin_pct']:.2f}%")
    print(f"Leading Revenue Category:   {facts['categories']['highest_revenue']['name']} (INR {facts['categories']['highest_revenue']['revenue_inr']:,.2f} / {facts['categories']['highest_revenue']['share_pct']:.1f}% share)")
    print(f"Highest Margin Category:    {facts['categories']['highest_margin']['name']} ({facts['categories']['highest_margin']['margin_pct']:.1f}%)")
    print(f"Lowest Margin Category:     {facts['categories']['lowest_margin']['name']} ({facts['categories']['lowest_margin']['margin_pct']:.1f}%)")
    print(f"Leading Region:             {facts['regions']['top_region']['name']} (INR {facts['regions']['top_region']['revenue_inr']:,.2f} / {facts['regions']['top_region']['share_pct']:.1f}% share)")
    print(f"Champions Contribution:     {facts['rfm']['champions']['count']:,} customers generate INR {facts['rfm']['champions']['revenue_inr']:,.2f} ({facts['rfm']['champions']['revenue_share_pct']:.1f}% of total sales)")
    print(f"At-Risk Revenue Exposure:   {facts['rfm']['at_risk']['count']:,} customers account for INR {facts['rfm']['at_risk']['revenue_inr']:,.2f} ({facts['rfm']['at_risk']['revenue_share_pct']:.1f}% of total sales)")
    print(f"Leading Return Reason:      {facts['returns']['top_reason']['reason']} ({facts['returns']['top_reason']['count']:,} returns, {facts['returns']['top_reason']['pct_of_returns']:.1f}% of all returns)")
    print(f"Leading Payment Channel:    {facts['payments']['top_method']['method']} (INR {facts['payments']['top_method']['volume_inr']:,.2f} / {facts['payments']['top_method']['share_pct']:.1f}% volume)")
    print("=" * 65)


if __name__ == "__main__":
    main()
