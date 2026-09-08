"""
03_eda.py
=========
E-Commerce Sales, Customer & Profitability Analytics
Exploratory Data Analysis & Production Visualizations

Calculates enterprise-level KPIs, performs deep cohort & financial trend analyses,
and generates 14 publication-grade visualizations saved to visuals/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
os.makedirs(VISUALS_DIR, exist_ok=True)

# Visual styling setup
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["figure.titlesize"] = 14

# Palette
PRIMARY_COLOR = "#3B82F6"   # Vibrant Blue
SECONDARY_COLOR = "#10B981" # Emerald Green
ACCENT_COLOR = "#F59E0B"    # Amber
DANGER_COLOR = "#EF4444"    # Rose Red
DARK_COLOR = "#1E293B"      # Slate Dark
PURPLE_COLOR = "#8B5CF6"    # Indigo/Violet


def format_inr(x, pos):
    """Format large numbers into Lakhs (L) and Crores (Cr)."""
    if abs(x) >= 1e7:
        return f"Rs {x*1e-7:.2f} Cr"
    elif abs(x) >= 1e5:
        return f"Rs {x*1e-5:.1f} L"
    elif abs(x) >= 1e3:
        return f"Rs {x*1e-3:.0f} K"
    else:
        return f"Rs {x:.0f}"


def load_data():
    df_cust = pd.read_csv(os.path.join(CLEANED_DIR, "customers_cleaned.csv"))
    df_prod = pd.read_csv(os.path.join(CLEANED_DIR, "products_cleaned.csv"))
    df_ord = pd.read_csv(os.path.join(CLEANED_DIR, "orders_cleaned.csv"))
    df_pay = pd.read_csv(os.path.join(CLEANED_DIR, "payments_cleaned.csv"))
    df_ret = pd.read_csv(os.path.join(CLEANED_DIR, "returns_cleaned.csv"))
    
    df_ord["order_date"] = pd.to_datetime(df_ord["order_date"])
    df_ord["year_month"] = df_ord["order_date"].dt.to_period("M").astype(str)
    df_ord["year"] = df_ord["order_date"].dt.year
    df_ord["quarter"] = df_ord["order_date"].dt.to_period("Q").astype(str)
    
    return df_cust, df_prod, df_ord, df_pay, df_ret


def generate_visualizations(df_cust, df_prod, df_ord, df_pay, df_ret):
    print("\n--- Generating Visualizations ---")
    inr_formatter = ticker.FuncFormatter(format_inr)
    
    # Merge orders with products
    df_ord_prod = df_ord.merge(
        df_prod[["product_id", "category", "subcategory", "brand"]],
        on="product_id",
        how="left"
    )

    # -------------------------------------------------------------
    # 1. Monthly Revenue Trend
    # -------------------------------------------------------------
    monthly_rev = df_ord.groupby("year_month")["sales_amount"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(monthly_rev["year_month"], monthly_rev["sales_amount"], marker="o", color=PRIMARY_COLOR, linewidth=2.5, markersize=6)
    ax.fill_between(monthly_rev["year_month"], monthly_rev["sales_amount"], color=PRIMARY_COLOR, alpha=0.15)
    ax.set_title("Monthly Revenue Trend (2022 - 2024)", pad=15)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Total Revenue (INR)")
    ax.yaxis.set_major_formatter(inr_formatter)
    plt.xticks(rotation=45, ha="right")
    
    # Peak annotation
    peak_idx = monthly_rev["sales_amount"].idxmax()
    peak_val = monthly_rev.loc[peak_idx, "sales_amount"]
    peak_month = monthly_rev.loc[peak_idx, "year_month"]
    ax.annotate(f"Festive Peak ({peak_month}):\n{format_inr(peak_val, None)}",
                xy=(peak_idx, peak_val),
                xytext=(peak_idx - 3, peak_val * 0.92),
                arrowprops=dict(facecolor=DARK_COLOR, shrink=0.08, width=1, headwidth=6),
                fontweight="bold", color=DARK_COLOR)
    
    plt.tight_layout()
    p1 = os.path.join(VISUALS_DIR, "monthly_sales.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"[OK] Saved {p1}")

    # -------------------------------------------------------------
    # 2. Monthly Profit Trend & Margin
    # -------------------------------------------------------------
    monthly_prof = df_ord.groupby("year_month").agg(
        Profit=("profit_amount", "sum"),
        Revenue=("sales_amount", "sum")
    ).reset_index()
    monthly_prof["Margin"] = (monthly_prof["Profit"] / monthly_prof["Revenue"]) * 100

    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()

    ax1.bar(monthly_prof["year_month"], monthly_prof["Profit"], color=SECONDARY_COLOR, alpha=0.8, width=0.6, label="Total Profit (INR)")
    ax2.plot(monthly_prof["year_month"], monthly_prof["Margin"], color=ACCENT_COLOR, marker="s", linewidth=2, label="Profit Margin %")

    ax1.set_title("Monthly Profit Volume & Profit Margin Trend", pad=15)
    ax1.set_xlabel("Year-Month")
    ax1.set_ylabel("Total Profit (INR)", color=SECONDARY_COLOR)
    ax2.set_ylabel("Profit Margin (%)", color=ACCENT_COLOR)
    ax1.yaxis.set_major_formatter(inr_formatter)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(axis="x")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    p2 = os.path.join(VISUALS_DIR, "monthly_profit.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"[OK] Saved {p2}")

    # -------------------------------------------------------------
    # 3. Revenue by Category
    # -------------------------------------------------------------
    cat_rev = df_ord_prod.groupby("category")["sales_amount"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(cat_rev.index, cat_rev.values, color=PRIMARY_COLOR, alpha=0.85, height=0.65)
    ax.set_title("Total Revenue by Product Category", pad=15)
    ax.set_xlabel("Total Revenue (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + (cat_rev.max() * 0.01), bar.get_y() + bar.get_height()/2, format_inr(w, None),
                va="center", ha="left", fontsize=9, fontweight="bold", color=DARK_COLOR)
    
    ax.set_xlim(0, cat_rev.max() * 1.18)
    plt.tight_layout()
    p3 = os.path.join(VISUALS_DIR, "category_sales.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"[OK] Saved {p3}")

    # -------------------------------------------------------------
    # 4. Profit by Category
    # -------------------------------------------------------------
    cat_prof = df_ord_prod.groupby("category")["profit_amount"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(cat_prof.index, cat_prof.values, color=SECONDARY_COLOR, alpha=0.85, height=0.65)
    ax.set_title("Total Profit by Product Category", pad=15)
    ax.set_xlabel("Total Profit (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + (cat_prof.max() * 0.01), bar.get_y() + bar.get_height()/2, format_inr(w, None),
                va="center", ha="left", fontsize=9, fontweight="bold", color=DARK_COLOR)

    ax.set_xlim(0, cat_prof.max() * 1.18)
    plt.tight_layout()
    p4 = os.path.join(VISUALS_DIR, "category_profit.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"[OK] Saved {p4}")

    # -------------------------------------------------------------
    # 5. Top 10 Products by Revenue
    # -------------------------------------------------------------
    prod_perf = df_ord.groupby("product_id").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum"),
        Quantity=("quantity", "sum")
    ).merge(df_prod[["product_id", "product_name", "category"]], on="product_id")

    top10_rev = prod_perf.sort_values(by="Revenue", ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(top10_rev["product_name"], top10_rev["Revenue"], color=PRIMARY_COLOR, alpha=0.85, height=0.6)
    ax.set_title("Top 10 Products by Revenue Generation", pad=15)
    ax.set_xlabel("Revenue (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + (top10_rev["Revenue"].max() * 0.01), bar.get_y() + bar.get_height()/2, format_inr(w, None),
                va="center", ha="left", fontsize=8.5, fontweight="bold")

    ax.set_xlim(0, top10_rev["Revenue"].max() * 1.20)
    plt.tight_layout()
    p5 = os.path.join(VISUALS_DIR, "top_products.png")
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"[OK] Saved {p5}")

    # -------------------------------------------------------------
    # 6. Top 10 Products by Profit
    # -------------------------------------------------------------
    top10_prof = prod_perf.sort_values(by="Profit", ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(top10_prof["product_name"], top10_prof["Profit"], color=SECONDARY_COLOR, alpha=0.85, height=0.6)
    ax.set_title("Top 10 Products by Net Profit Contribution", pad=15)
    ax.set_xlabel("Profit (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + (top10_prof["Profit"].max() * 0.01), bar.get_y() + bar.get_height()/2, format_inr(w, None),
                va="center", ha="left", fontsize=8.5, fontweight="bold")

    ax.set_xlim(0, top10_prof["Profit"].max() * 1.20)
    plt.tight_layout()
    p6 = os.path.join(VISUALS_DIR, "top_profit_products.png")
    plt.savefig(p6, dpi=300)
    plt.close()
    print(f"[OK] Saved {p6}")

    # -------------------------------------------------------------
    # 7. Sales by Region
    # -------------------------------------------------------------
    reg_perf = df_ord.groupby("region").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum")
    ).reset_index()

    x = np.arange(len(reg_perf))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 5.5))
    rects1 = ax.bar(x - width/2, reg_perf["Revenue"], width, label="Revenue", color=PRIMARY_COLOR)
    rects2 = ax.bar(x + width/2, reg_perf["Profit"], width, label="Profit", color=SECONDARY_COLOR)

    ax.set_title("Regional Performance: Revenue vs Profit Comparison", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(reg_perf["region"])
    ax.set_ylabel("Amount (INR)")
    ax.yaxis.set_major_formatter(inr_formatter)
    ax.legend()

    plt.tight_layout()
    p7 = os.path.join(VISUALS_DIR, "regional_sales.png")
    plt.savefig(p7, dpi=300)
    plt.close()
    print(f"[OK] Saved {p7}")

    # -------------------------------------------------------------
    # 8. Sales by State (Top 10)
    # -------------------------------------------------------------
    state_perf = df_ord.groupby("state")["sales_amount"].sum().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(state_perf.index, state_perf.values, color=PURPLE_COLOR, alpha=0.85, height=0.6)
    ax.set_title("Top 10 Indian States by Sales Revenue", pad=15)
    ax.set_xlabel("Revenue (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + (state_perf.max() * 0.01), bar.get_y() + bar.get_height()/2, format_inr(w, None),
                va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlim(0, state_perf.max() * 1.18)
    plt.tight_layout()
    p8 = os.path.join(VISUALS_DIR, "state_sales.png")
    plt.savefig(p8, dpi=300)
    plt.close()
    print(f"[OK] Saved {p8}")

    # -------------------------------------------------------------
    # 9. Customer Segment Revenue
    # -------------------------------------------------------------
    cust_seg_rev = df_ord.merge(df_cust[["customer_id", "customer_segment"]], on="customer_id") \
                         .groupby("customer_segment")["sales_amount"].sum()
    
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    colors = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, PURPLE_COLOR]
    wedges, texts, autotexts = ax.pie(
        cust_seg_rev.values,
        labels=cust_seg_rev.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops=dict(color=DARK_COLOR, fontweight="bold"),
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)
    ax.set_title("Revenue Contribution by Customer Segment", pad=20)

    plt.tight_layout()
    p9 = os.path.join(VISUALS_DIR, "customer_segments.png")
    plt.savefig(p9, dpi=300)
    plt.close()
    print(f"[OK] Saved {p9}")

    # -------------------------------------------------------------
    # 10. New vs. Returning Customers Over Time
    # -------------------------------------------------------------
    # Determine customer's first order date
    cust_first_order = df_ord.groupby("customer_id")["order_date"].min().reset_index()
    cust_first_order.rename(columns={"order_date": "first_order_date"}, inplace=True)
    df_ord_cohort = df_ord.merge(cust_first_order, on="customer_id")
    df_ord_cohort["is_new"] = df_ord_cohort["order_date"] == df_ord_cohort["first_order_date"]
    
    cohort_monthly = df_ord_cohort.groupby(["year_month", "is_new"])["order_id"].count().unstack().fillna(0)
    cohort_monthly.columns = ["Returning Customers", "New Customers"]

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.bar(cohort_monthly.index, cohort_monthly["Returning Customers"], label="Returning Orders", color=PRIMARY_COLOR, alpha=0.85)
    ax.bar(cohort_monthly.index, cohort_monthly["New Customers"], bottom=cohort_monthly["Returning Customers"],
           label="New Customer Orders", color=ACCENT_COLOR, alpha=0.85)
    
    ax.set_title("Monthly Order Volume: New vs Returning Customers", pad=15)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Number of Orders")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper left")

    plt.tight_layout()
    p10 = os.path.join(VISUALS_DIR, "new_vs_returning.png")
    plt.savefig(p10, dpi=300)
    plt.close()
    print(f"[OK] Saved {p10}")

    # -------------------------------------------------------------
    # 11. Payment Method Distribution
    # -------------------------------------------------------------
    pay_dist = df_pay.groupby("payment_method")["payment_amount"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(pay_dist.index, pay_dist.values, color=PRIMARY_COLOR, alpha=0.8, height=0.6)
    ax.set_title("Gross Transaction Volume by Payment Method", pad=15)
    ax.set_xlabel("Total Processed Volume (INR)")
    ax.xaxis.set_major_formatter(inr_formatter)

    for bar in bars:
        w = bar.get_width()
        pct = (w / pay_dist.sum()) * 100
        ax.text(w + (pay_dist.max() * 0.01), bar.get_y() + bar.get_height()/2,
                f"{format_inr(w, None)} ({pct:.1f}%)", va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlim(0, pay_dist.max() * 1.25)
    plt.tight_layout()
    p11 = os.path.join(VISUALS_DIR, "payment_distribution.png")
    plt.savefig(p11, dpi=300)
    plt.close()
    print(f"[OK] Saved {p11}")

    # -------------------------------------------------------------
    # 12. Return Analysis (Reasons & Volume)
    # -------------------------------------------------------------
    ret_reasons = df_ret.groupby("return_reason").agg(
        Count=("return_id", "count"),
        Refund=("refund_amount", "sum")
    ).sort_values(by="Count", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(ret_reasons.index, ret_reasons["Count"], color=DANGER_COLOR, alpha=0.8, height=0.6)
    ax.set_title("Return Incident Count by Primary Root Cause", pad=15)
    ax.set_xlabel("Number of Return Incidents")

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 15, bar.get_y() + bar.get_height()/2, f"{int(w):,} returns",
                va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlim(0, ret_reasons["Count"].max() * 1.2)
    plt.tight_layout()
    p12 = os.path.join(VISUALS_DIR, "return_analysis.png")
    plt.savefig(p12, dpi=300)
    plt.close()
    print(f"[OK] Saved {p12}")

    # -------------------------------------------------------------
    # 13. Monthly Order Volume & AOV
    # -------------------------------------------------------------
    monthly_orders = df_ord.groupby("year_month").agg(
        Orders=("order_id", "count"),
        Revenue=("sales_amount", "sum")
    ).reset_index()
    monthly_orders["AOV"] = monthly_orders["Revenue"] / monthly_orders["Orders"]

    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()

    ax1.plot(monthly_orders["year_month"], monthly_orders["Orders"], marker="o", color=PRIMARY_COLOR, linewidth=2, label="Order Count")
    ax2.plot(monthly_orders["year_month"], monthly_orders["AOV"], marker="^", color=ACCENT_COLOR, linewidth=2, linestyle="--", label="Average Order Value (INR)")

    ax1.set_title("Monthly Order Volume & Average Order Value (AOV)", pad=15)
    ax1.set_xlabel("Year-Month")
    ax1.set_ylabel("Order Count", color=PRIMARY_COLOR)
    ax2.set_ylabel("AOV (INR)", color=ACCENT_COLOR)
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("Rs {x:,.0f}"))
    ax1.tick_params(axis="x", rotation=45)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    p13 = os.path.join(VISUALS_DIR, "monthly_orders.png")
    plt.savefig(p13, dpi=300)
    plt.close()
    print(f"[OK] Saved {p13}")

    # -------------------------------------------------------------
    # 14. Profit Margin by Category
    # -------------------------------------------------------------
    cat_margin = df_ord_prod.groupby("category").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit_amount", "sum")
    ).reset_index()
    cat_margin["Margin_Pct"] = (cat_margin["Profit"] / cat_margin["Revenue"]) * 100
    cat_margin = cat_margin.sort_values(by="Margin_Pct", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(cat_margin["category"], cat_margin["Margin_Pct"], color=SECONDARY_COLOR, alpha=0.85, height=0.6)
    ax.set_title("Net Profit Margin (%) by Product Category", pad=15)
    ax.set_xlabel("Profit Margin (%)")
    ax.xaxis.set_major_formatter(ticker.PercentFormatter())

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{w:.1f}%",
                va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlim(0, cat_margin["Margin_Pct"].max() * 1.15)
    plt.tight_layout()
    p14 = os.path.join(VISUALS_DIR, "profit_margin_category.png")
    plt.savefig(p14, dpi=300)
    plt.close()
    print(f"[OK] Saved {p14}")


def compute_core_metrics(df_cust, df_prod, df_ord, df_pay, df_ret):
    print("\n" + "=" * 65)
    print(" CORE BUSINESS & FINANCIAL METRICS")
    print("=" * 65)
    
    total_rev = df_ord["sales_amount"].sum()
    total_cost = df_ord["cost_amount"].sum()
    total_prof = df_ord["profit_amount"].sum()
    total_orders = len(df_ord)
    total_customers = df_ord["customer_id"].nunique()
    aov = total_rev / total_orders
    overall_margin = (total_prof / total_rev) * 100

    delivered_orders = df_ord[df_ord["order_status"] == "Delivered"]
    returned_orders = df_ord[df_ord["order_status"] == "Returned"]
    cancelled_orders = df_ord[df_ord["order_status"] == "Cancelled"]

    delivered_rev = delivered_orders["sales_amount"].sum()
    delivered_prof = delivered_orders["profit_amount"].sum()

    return_rate = (len(returned_orders) / total_orders) * 100
    cancellation_rate = (len(cancelled_orders) / total_orders) * 100

    cust_freq = df_ord.groupby("customer_id").size()
    repeat_customers = (cust_freq > 1).sum()
    retention_rate = (repeat_customers / total_customers) * 100

    print(f"Total Gross Revenue:      INR {total_rev:,.2f}")
    print(f"Delivered Revenue:        INR {delivered_rev:,.2f}")
    print(f"Total COGS (Cost):        INR {total_cost:,.2f}")
    print(f"Total Net Profit:         INR {total_prof:,.2f}")
    print(f"Delivered Net Profit:     INR {delivered_prof:,.2f}")
    print(f"Overall Profit Margin:    {overall_margin:.2f}%")
    print(f"Total Orders:             {total_orders:,}")
    print(f"Total Active Customers:   {total_customers:,}")
    print(f"Average Order Value:      INR {aov:,.2f}")
    print(f"Return Rate:              {return_rate:.2f}% ({len(returned_orders):,} orders)")
    print(f"Cancellation Rate:        {cancellation_rate:.2f}% ({len(cancelled_orders):,} orders)")
    print(f"Repeat Purchase Rate:     {retention_rate:.2f}% ({repeat_customers:,} repeat customers)")
    print("=" * 65)


def main():
    df_cust, df_prod, df_ord, df_pay, df_ret = load_data()
    compute_core_metrics(df_cust, df_prod, df_ord, df_pay, df_ret)
    generate_visualizations(df_cust, df_prod, df_ord, df_pay, df_ret)
    print("\nEDA and Visualizations generation completed successfully!")


if __name__ == "__main__":
    main()
