# 5-Minute Portfolio Project Presentation Script

**Project:** E-Commerce Sales, Customer & Profitability Analytics  
**Format:** Structured 5-Minute Verbal Pitch for Data Analyst & BI Developer Interviews  
**Pacing:** ~130 words per minute (Clear, confident, business-oriented delivery)

---

### [0:00 - 0:30] 1. The Business Problem
> "Good morning/afternoon. Today I'm excited to present my project on **E-Commerce Sales, Customer & Profitability Analytics**. 
> 
> As e-commerce marketplaces scale, executive leadership often faces a common blind spot: top-line revenue expands rapidly, but bottom-line net profit stagnates due to hidden product-line inefficiencies, aggressive promotional discounting, high reverse-logistics return costs, and silent customer churn. 
> 
> The objective of this project was to analyze 3 years of commercial transactions for an Indian e-commerce enterprise to pinpoint exactly where the company makes money, where it leaks profit, and how to engineer sustainable margin expansion."

---

### [0:30 - 1:00] 2. The Dataset Overview
> "The project analyzed five relational tables covering **52,500 orders, 5,156 customers, and 550 products** spanning **January 2022 to December 2024**. 
> 
> The dataset simulated a realistic multi-region marketplace across Tier-1, 2, and 3 Indian cities with seasonal festival spikes like Diwali, multi-tender payments like UPI and Credit Cards, and realistic return rates. 
> 
> In total, the business generated **INR 134.77 Million (approx. ₹ 13.5 Crore)** in gross revenue with an overall profit margin of **28.63%**."

---

### [1:00 - 1:30] 3. Data Cleaning & Engineering Pipeline
> "In a real data environment, raw data is never clean. The raw CSV feeds arrived with duplicate customer IDs, missing geographic cities, mixed date formats (such as DD/MM/YYYY mixed with ISO dates), and out-of-bounds age outliers.
> 
> I engineered a Python cleaning pipeline using Pandas. I deduplicated 85+ records across tables, imputed missing cities using regional hub hierarchies, resolved age anomalies using median imputation, and programmatically recalculated accounting metrics to guarantee that gross sales, discounts, net sales, COGS, and profit margins reconciled perfectly across all 52,500 orders. 
> 
> The output was exported to clean, validated datasets with zero broken foreign keys."

---

### [1:30 - 2:00] 4. Exploratory & Customer RFM Analytics
> "Next, I conducted exploratory data analysis and built a customer RFM segmentation framework. By calculating Recency, Frequency, and Monetary scores across quintiles, I grouped our customer base into 7 strategic cohorts.
> 
> The analysis revealed extreme revenue concentration: our top cohort, **Champions (945 customers or 18.3% of users)**, drove **35.8% of total marketplace revenue**—spending over ₹ 51,000 on average across 18 orders. 
> 
> Crucially, I detected that **584 high-value customers were 'At Risk'**. Although they historically spent over **₹ 2.03 Crore**, they had been inactive for an average of 144 days, exposing the company to severe churn risk."

---

### [2:00 - 2:45] 5. Production SQL Deep-Dive (50 Business Queries)
> "To demonstrate enterprise data querying, I loaded the data into a normalized MySQL relational schema and wrote **50 production SQL queries** answering granular business questions. 
> 
> I leveraged advanced SQL concepts:
> - **Window functions** like `ROW_NUMBER()`, `DENSE_RANK()`, and `RANK()` to build customer and product leaderboards without rank gaps.
> - `LAG()` to calculate Month-over-Month and Year-over-Year revenue expansion.
> - Running cumulative totals using `SUM() OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` to perform a Pareto 80/20 analysis—discovering that 293 SKUs generate 80% of total revenue.
> - Partitioned window functions to surface the top 3 highest-earning products within each merchandise category."

---

### [2:45 - 3:30] 6. Power BI Star Schema & Financial Modeling
> "To empower non-technical decision-makers, I architected a high-performance **Power BI Star Schema** comprising three Fact tables—`FactOrders`, `FactPayments`, and `FactReturns`—connected to conforming Dimension tables via 1-to-many relationships. 
> 
> I authored **22 DAX measures** covering core financials, fulfillment rates, and time intelligence. 
> 
> I structured the report into an executive 4-page dashboard:
> - **Page 1: Executive Overview** with KPI cards and monthly trends.
> - **Page 2: Customer Analytics** with RFM breakdown and cohort area charts.
> - **Page 3: Product Profitability** featuring a BCG scatterplot and low-margin alerts.
> - **Page 4: Regional & Returns** tracking state sales maps and return root causes.
> 
> I also created a formula-driven Excel model in `ecommerce_analysis.xlsx` with KPI summary sheets and dynamic formulas."

---

### [3:30 - 4:00] 7. Key Business Findings
> "Three major findings stood out from the data:
> 1. **The Electronics Paradox**: Electronics accounts for **40.2% of all marketplace sales (₹ 5.41 Crore)**, but operates on a thin **17.5% margin**. In contrast, Fashion generates ₹ 2.32 Crore but produces almost identical total dollar profit because of its **39.8% margin**. Accessories led all categories with a **50.0% net margin**.
> 2. **Reverse Logistics Root Causes**: Our return rate was **7.00%**, costing **₹ 9.42 Million in refunds**. Over **41.6% of returns** were caused by just two factors: **Apparel Sizing Mismatches (20.9%)** and **Damaged Goods in Transit (20.7%)**.
> 3. **UPI Dominance**: UPI processed **42.1% of all transaction volume** with a 98.8% success rate, while Cash on Delivery showed higher refusal rates."

---

### [4:00 - 4:30] 8. Strategic Recommendations
> "Based on these empirical numbers, I provided management with three actionable priorities:
> 1. **Re-Engage At-Risk Accounts**: Deploy automated WhatsApp and email win-back campaigns with 15% personalized vouchers for the 584 At-Risk customers, protecting ₹ 5.0+ Million in recurring sales.
> 2. **Rationalize Electronics Discounts & Rebalance Ad Spend**: Cap festival discounting on high-velocity electronics to recover 150–250 basis points of margin, and shift 20% of digital marketing ad spend toward 45%+ margin categories like Beauty and Accessories.
> 3. **Remediate Apparel Sizing**: Deploy standardized interactive size guides and customer fit tags on Fashion product pages to cut apparel returns by 30%."

---

### [4:30 - 5:00] 9. Business Impact & Conclusion
> "In summary, this project demonstrates how combining disciplined data engineering, rigorous statistical segmentation, and clean BI visualization turns raw transactions into executive decision intelligence. 
> 
> Implementing these recommendations provides a realistic roadmap to recover ₹ 5 Crore in at-risk revenue, lower return rates by 175 basis points, and lift blended EBITDA margins from 28.6% to over 31%. 
> 
> Thank you, and I would be glad to dive deeper into any query, DAX measure, or analytical methodology!"
