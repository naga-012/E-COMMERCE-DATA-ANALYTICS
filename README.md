# E-Commerce Sales, Customer & Profitability Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-Financial_Model-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/excel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, portfolio-ready Data Analytics and Business Intelligence project analyzing multi-year transactional sales, customer lifetime value, product margin economics, and reverse logistics for a multi-million rupee Indian e-commerce marketplace.

---

## Executive Overview & Core KPIs

Across the 3-year operating horizon (**2022–2024**), the platform processed **52,500 transactions** across **5,156 active customers** and **550 catalog SKUs**, generating **INR 134.77 Million (~₹ 13.5 Crore)** in gross revenue with an overall profit margin of **28.63%**.

```
+---------------------+---------------------+---------------------+---------------------+
|    GROSS REVENUE    |     NET PROFIT      |    TOTAL ORDERS     |   ACTIVE CUSTOMERS  |
|  INR 134,770,139    |   INR 38,585,429    |       52,500        |        5,156        |
|    (~₹ 13.48 Cr)    |    (~₹ 3.86 Cr)     |  (45,614 Delivered) |  (99.0% Repeat Rate)|
+---------------------+---------------------+---------------------+---------------------+
|  AVG ORDER VALUE    |    PROFIT MARGIN    |     RETURN RATE     |  CANCELLATION RATE  |
|    INR 2,567.05     |       28.63%        |        7.00%        |        6.11%        |
| (Stable basket size)|  (Accessories 50%)  |   (3,676 Orders)    |   (3,210 Orders)    |
+---------------------+---------------------+---------------------+---------------------+
```

---

## Key Business Insights

1. **The "Electronics Paradox"**: Electronics is our commercial flagship, generating **40.18% of total revenue (INR 54.15 Million)** across 10,642 orders. However, aggressive promotional discounting suppresses its net margin to **17.52%**. In contrast, Fashion accounts for less than half the sales volume (INR 23.25 Million) but produces nearly identical total dollar profit (**INR 9.25M vs INR 9.48M**) due to its **39.80% margin**.
2. **Customer Revenue Concentration (RFM)**: An elite tier of **945 Champions (18.3% of users)** generates **35.81% of all marketplace revenue (INR 48.26 Million)**, averaging 18.5 orders per customer.
3. **The At-Risk Churn Vulnerability**: **584 high-value customers** classified as *At Risk* have generated **INR 20.28 Million (15.05% of company sales)**, but have been inactive for an average of **143.6 days**.
4. **Reverse Logistics Root Causes**: Total returns amounted to **INR 9.42 Million in refunds**. Over **41.59% of all returns** were driven by just two operational factors: **Apparel Sizing Mismatches (20.89%)** and **Goods Damaged in Transit (20.70%)**.
5. **Payment Ecosystem Dominance**: **UPI is the primary payment tender**, processing **INR 56.68 Million (42.06% of volume)** across 22,088 orders with a 98.8% success rate. Cash on Delivery (COD) exhibited the highest delivery friction with an 8.8% cancellation/refusal rate.

---

## Project Architecture

```
ecommerce-data-analytics/
│
├── data/
│   ├── raw/                       # Raw synthetic CSVs with realistic defects
│   │   ├── customers.csv          # 5,225 records (contains duplicates, null cities)
│   │   ├── products.csv           # 560 records (contains duplicates, whitespace)
│   │   ├── orders.csv             # 52,520 records (mixed date formats, trailing spaces)
│   │   ├── payments.csv           # 52,530 records (contains duplicate payment attempts)
│   │   └── returns.csv            # 3,676 records
│   │
│   └── cleaned/                   # Analytically validated production CSVs
│       ├── customers_cleaned.csv  # 5,200 unique records (deduplicated, imputed)
│       ├── products_cleaned.csv   # 550 unique SKUs (standardized taxonomy & margins)
│       ├── orders_cleaned.csv     # 52,500 validated orders (reconciled financial math)
│       ├── payments_cleaned.csv   # 52,500 payment records (1:1 referential integrity)
│       ├── returns_cleaned.csv    # 3,676 verified returns
│       ├── customer_rfm_profiles.csv       # RFM quintile scores & 7 customer segments
│       ├── product_performance_metrics.csv # SKU Pareto 80/20 & BCG quadrant tags
│       └── monthly_sales_summary.csv       # 36-month time-series & MoM/YoY growth
│
├── python/
│   ├── 01_data_generation.py     # Reproducible synthetic generator (seed=42)
│   ├── 02_data_cleaning.py       # Diagnostic audit, deduplication, imputation pipeline
│   ├── 03_eda.py                 # Core KPI calculations & 14 publication-grade charts
│   ├── 04_customer_analysis.py   # RFM quintile calculation & segment allocation
│   ├── 05_product_analysis.py    # SKU profitability, Pareto 80/20, & margin classification
│   ├── 06_sales_analysis.py      # Time-series, seasonality index, MoM & YoY metrics
│   ├── 07_business_insights.py   # Programmatic fact generator outputting business_facts.json
│   └── build_excel_workbook.py   # Automated openpyxl financial workbook generator
│
├── notebooks/
│   ├── data_cleaning.ipynb       # Interactive step-by-step cleaning audit notebook
│   └── exploratory_data_analysis.ipynb # Interactive EDA & visual discovery notebook
│
├── sql/
│   ├── 01_create_database.sql    # Database initialization & collation
│   ├── 02_create_tables.sql      # Normalized DDL (PKs, FKs, CHECK constraints, Indexes)
│   ├── 03_insert_or_load_data.sql# Bulk CSV ingestion via LOAD DATA INFILE
│   ├── 04_basic_analysis.sql     # Questions 1 to 15 (KPIs, aggregations, filters)
│   ├── 05_intermediate_analysis.sql # Questions 16 to 33 (CTEs, subqueries, LAG, DENSE_RANK)
│   ├── 06_advanced_analysis.sql  # Questions 34 to 50 (Window partitions, Pareto, churn risk)
│   └── 07_business_questions.sql # Master query dictionary answering all 50 business questions
│
├── excel/
│   ├── ecommerce_analysis.xlsx   # Formula-driven financial model with KPI cards & dashboard
│   └── excel_analysis_guide.md   # Formula reference (XLOOKUP, SUMIFS, Pivot Table guide)
│
├── powerbi/
│   ├── data_model.md             # Star Schema dimensional blueprint (Kimball method)
│   ├── dax_measures.md           # 22 production DAX measures with business logic
│   ├── dashboard_design.md       # 4-page UI/UX layout blueprint & wireframes
│   └── powerbi_setup.md          # Step-by-step tutorial for Power BI Desktop
│
├── reports/
│   ├── executive_summary.md      # C-Suite management report with verified figures
│   ├── business_insights.md      # Detailed findings across categories, cohorts, & geography
│   ├── recommendations.md        # Strategic, tactical, and operational action plans
│   ├── interview_questions.md    # 35 project-specific interview Q&As
│   ├── resume_project_description.md # ATS-ready bullet points & project summaries
│   ├── project_presentation.md   # 5-minute verbal walkthrough script
│   └── business_facts.json       # Centralized machine-readable fact sheet
│
├── visuals/                      # 14 high-resolution (300 DPI) publication-grade PNGs
│   ├── monthly_sales.png         # Monthly revenue trend with peak annotations
│   ├── monthly_profit.png        # Monthly profit volume & margin % trend
│   ├── category_sales.png        # Gross revenue by category
│   ├── category_profit.png       # Net profit by category
│   ├── top_products.png          # Top 10 revenue-generating SKUs
│   ├── top_profit_products.png   # Top 10 net profit SKUs
│   ├── regional_sales.png        # Regional revenue vs profit comparison
│   ├── state_sales.png           # Top 10 Indian states by sales
│   ├── customer_segments.png     # Customer segment revenue share donut chart
│   ├── new_vs_returning.png      # Monthly order volume: new vs returning customers
│   ├── payment_distribution.png  # Transaction volume by payment rail
│   ├── return_analysis.png       # Return incidents by root cause
│   ├── monthly_orders.png        # Order volume & AOV trajectory
│   └── profit_margin_category.png# Net profit margin % across categories
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Visual Analytics Highlights

The analysis generates 14 high-resolution visual exhibits in `visuals/`:

| Visualization | Description | Business Impact |
|---|---|---|
| **[Monthly Revenue Trend](visuals/monthly_sales.png)** | 36-month timeline tracking commercial volume | Highlights recurring Q4 Diwali peaks and June clearance surge |
| **[Profit Margin by Category](visuals/profit_margin_category.png)** | Horizontal bar chart of net margin percentages | Illustrates Accessories (50.0%) and Beauty (44.6%) margin power |
| **[Customer Segment Revenue](visuals/customer_segments.png)** | Donut chart of revenue contribution by RFM tier | Validates Champions driving 35.8% and At-Risk accounts holding 15.0% |
| **[Return Reasons Root Cause](visuals/return_analysis.png)** | Root-cause breakdown of 3,676 return events | Flags Sizing (20.9%) and Damaged packaging (20.7%) as primary friction |
| **[Regional Sales Comparison](visuals/regional_sales.png)** | Revenue vs Profit across South, West, North, East, Central | Demonstrates Southern territory generating 32.4% of all sales |

---

## Data Model Architecture (Power BI Star Schema)

The semantic model follows Kimball dimensional modeling principles with **1-to-many single-direction relationships** filtering from Dimensions to Facts:

```
        [DimCustomer] (1) ───────< (*) [FactOrders] (*) >─────── (1) [DimProduct]
                                            │
                                            ├───────< (*) [FactPayments]
                                            │
                                            ├───────< (*) [FactReturns]
                                            │
         [DimDate] (1) ──────────< (*) ─────┤
                                            │
     [DimGeography] (1) ─────────< (*) ─────┘
```

Detailed model relationships, data types, and cardinality configurations are documented in [powerbi/data_model.md](powerbi/data_model.md). Complete formulas for all 22 DAX measures are documented in [powerbi/dax_measures.md](powerbi/dax_measures.md).

---

## Production SQL Analysis (50 Business Questions)

The SQL architecture (`sql/`) provides complete coverage across Basic, Intermediate, and Advanced analytical operations:

- **Aggregations & Filtering (`04_basic_analysis.sql`)**: Q1–Q15 (Gross revenue, net profit, delivered orders, AOV, category shares).
- **Relational Joins & Window Rankings (`05_intermediate_analysis.sql`)**: Q16–Q33 (Cohort acquisition, customer retention, `DENSE_RANK()`, `LAG()` for MoM growth, partitioned category rankings).
- **Advanced Window Aggregations & RFM (`06_advanced_analysis.sql`)**: Q34–Q50 (Cumulative Pareto 80/20 running sums, `NTILE(4)` quartile alerts for high-revenue/low-margin SKUs, inter-purchase cycle cadence, churn risk identification).
- **Master Query Dictionary (`07_business_questions.sql`)**: Unified reference mapping all 50 business questions with code and business explanations.

---

## Excel Financial Model (`ecommerce_analysis.xlsx`)

The workbook in `excel/ecommerce_analysis.xlsx` contains 8 structured sheets:
- **`Dashboard`**: Executive overview with formatted KPI cards (`₹ #,##0`), dynamic summary tables, and profit margin formulas.
- **`KPI Summary`**: Enterprise metrics dictionary with benchmark targets.
- **`Sales Analysis`**: 36-month chronological financial statement with MoM growth calculations.
- **`Product Analysis`**: SKU performance matrix with BCG portfolio segment tags.
- **`Customer Analysis`**: Customer RFM segment breakdown.
- **`Regional Analysis`**: State-level and regional volume and margin rollups.
- **`Returns Analysis`**: Return root-cause distribution and payment method processing volumes.
- **`Pivot Tables`**: Source data table with 10,000 transactions for interactive exploration.

---

## How to Run & Reproduce

### 1. Environment Setup
Clone the repository and install required dependencies:
```bash
git clone https://github.com/your-username/ecommerce-data-analytics.git
cd ecommerce-data-analytics
pip install -r requirements.txt
```

### 2. Generate Synthetic Raw Data
Generate 52,000+ orders, 5,000+ customers, products, payments, and returns with reproducible seed `42`:
```bash
python python/01_data_generation.py
```

### 3. Run Data Cleaning & Audit Pipeline
Deduplicate, resolve missing values, parse mixed dates, and export clean datasets:
```bash
python python/02_data_cleaning.py
```

### 4. Execute Analytics & Generate Visualizations
Calculate KPIs and render all 14 visual charts into `visuals/`:
```bash
python python/03_eda.py
python python/04_customer_analysis.py
python python/05_product_analysis.py
python python/06_sales_analysis.py
python python/07_business_insights.py
```

### 5. Build the Excel Financial Workbook
Programmatically generate the styled `excel/ecommerce_analysis.xlsx` workbook:
```bash
python python/build_excel_workbook.py
```

### 6. Ingest into MySQL Database
Execute the SQL scripts in order using MySQL Workbench or CLI:
```bash
mysql -u root -p < sql/01_create_database.sql
mysql -u root -p < sql/02_create_tables.sql
mysql -u root -p --local-infile=1 < sql/03_insert_or_load_data.sql
```

### 7. Power BI Dashboard Setup
To open or build the Power BI dashboard:
1. Open **Power BI Desktop**.
2. Follow the step-by-step import instructions in [powerbi/powerbi_setup.md](powerbi/powerbi_setup.md).
3. Connect the cleaned CSV files from `data/cleaned/`.
4. Create the `DimDate` table and establish relationships as specified in [powerbi/data_model.md](powerbi/data_model.md).
5. Copy and paste the DAX measures from [powerbi/dax_measures.md](powerbi/dax_measures.md).

---

## Career & Interview Collateral

- **[Executive Summary](reports/executive_summary.md)**: Management report evaluating multi-year commercial performance.
- **[Business Insights](reports/business_insights.md)**: Detailed analysis of the Electronics Paradox, customer cohorts, and return root causes.
- **[Strategic Recommendations](reports/recommendations.md)**: Actionable 30/90/180-day operational roadmap.
- **[Interview Preparation](reports/interview_questions.md)**: 35 technical, analytical, and behavioral interview questions with strong model answers.
- **[Resume Bullet Points](reports/resume_project_description.md)**: Quantified, ATS-compliant bullet points and 60-second elevator pitch.
- **[5-Minute Project Presentation](reports/project_presentation.md)**: Spoken presentation script tailored for technical hiring interviews.

---

## License
This project is open-source and available under the [MIT License](LICENSE).
