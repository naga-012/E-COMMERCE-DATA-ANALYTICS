"""
generate_html_dashboard.py
==========================
Generates an interactive, standalone executive HTML web dashboard with complete multi-dimensional filtering:
- Year filter: All Years, 2022, 2023 (default), 2024
- Month filter: Month buttons (All Months, Jan - Dec) + Clickable Chart.js Monthly Chart bars!
- Category filter: Category buttons + Clickable Category table rows + Category breakdown chips!
- REGION FILTER (Front & Center):
  * Dedicated "Select Region" button toolbar: All Regions, South, West, North, East, Central
  * Clickable Regional Doughnut Chart slices AND Legend labels
  * Interactive Regional Financial Breakdown Table with clickable rows
  * Dedicated Region badge in every transaction record row
  * Selecting any region immediately displays 100% of all matching records (e.g. 6,393 for South)!
- City filter: Dropdown + Top city pills + Clickable city badges in records table
- Dynamic KPI card updates reflecting the active filter scope (Year, Month, Category, Region, City)
- Dynamic Category Breakdown Bar directly in the records explorer
- Real-time search, status pills, column sorting, and pagination across all 52,500 real records.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON_PATH = os.path.join(BASE_DIR, "dashboard_data.json")

with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
    dashboard_data = json.load(f)

json_str = json.dumps(dashboard_data, separators=(',', ':'))

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E-Commerce Executive Sales & Profitability Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: #151e2e;
      --card-inner: #1c2638;
      --card-border: #263449;
      --card-hover: #324460;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --primary-glow: rgba(59, 130, 246, 0.35);
      --success: #10b981;
      --success-glow: rgba(16, 185, 129, 0.35);
      --accent: #f59e0b;
      --danger: #ef4444;
      --purple: #8b5cf6;
      --purple-glow: rgba(139, 92, 246, 0.35);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.35);
      --radius: 12px;
      --radius-sm: 8px;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      padding: 24px;
      min-height: 100vh;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1520px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }}
    .title-area h1 {{
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.5px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .title-badge {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(59, 130, 246, 0.2);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}
    .title-area p {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    /* Filter Toolbars */
    .filter-section {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}
    .filter-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }}
    .filter-label {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      min-width: 115px;
    }}
    .btn-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }}
    .btn-filter {{
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }}
    .btn-filter:hover {{
      background: rgba(59, 130, 246, 0.15);
      color: #fff;
      border-color: rgba(59, 130, 246, 0.4);
    }}
    .btn-filter.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
      box-shadow: 0 2px 10px var(--primary-glow);
    }}
    .btn-month.active {{
      background: #10b981;
      border-color: #10b981;
      box-shadow: 0 2px 10px var(--success-glow);
    }}
    .btn-cat.active {{
      background: #8b5cf6;
      border-color: #8b5cf6;
      box-shadow: 0 2px 10px var(--purple-glow);
    }}
    .btn-reg.active {{
      background: #06b6d4;
      border-color: #06b6d4;
      color: #0b0f19;
      font-weight: 700;
      box-shadow: 0 2px 10px var(--cyan-glow);
    }}

    .select-dropdown {{
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .select-dropdown:focus {{
      border-color: var(--cyan);
      box-shadow: 0 0 0 2px var(--cyan-glow);
    }}

    /* Active Filter Banner */
    .filter-status-banner {{
      display: none;
      align-items: center;
      justify-content: space-between;
      background: linear-gradient(90deg, rgba(6, 182, 212, 0.18), rgba(139, 92, 246, 0.18), rgba(16, 185, 129, 0.18));
      border: 1px solid rgba(6, 182, 212, 0.4);
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      animation: fadeIn 0.3s ease;
    }}
    .filter-status-banner.show {{
      display: flex;
    }}
    .banner-content {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .banner-tag {{
      background: rgba(6, 182, 212, 0.25);
      color: #67e8f9;
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      border: 1px solid rgba(6, 182, 212, 0.4);
    }}
    .btn-clear-filter {{
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      padding: 5px 14px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-clear-filter:hover {{
      background: var(--danger);
      color: #fff;
    }}

    /* KPI Cards */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 18px 20px;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
      border-color: var(--card-hover);
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: var(--primary);
    }}
    .kpi-card.kpi-profit::before {{ background: var(--success); }}
    .kpi-card.kpi-margin::before {{ background: var(--accent); }}
    .kpi-card.kpi-ret::before {{ background: var(--danger); }}
    .kpi-card.kpi-growth::before {{ background: var(--purple); }}
    .kpi-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .kpi-value {{
      font-size: 26px;
      font-weight: 700;
      color: #fff;
      letter-spacing: -0.5px;
    }}
    .kpi-sub {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 6px;
    }}
    .kpi-scope {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
      font-weight: 500;
      max-width: 160px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    /* Charts Grid */
    .charts-grid {{
      display: grid;
      grid-template-columns: 1.8fr 1.2fr;
      gap: 20px;
      margin-bottom: 24px;
    }}
    @media (max-width: 1100px) {{
      .charts-grid {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 20px;
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 600;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .card-hint {{
      font-size: 12px;
      color: #60a5fa;
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.2);
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 500;
    }}
    .card-hint-cyan {{
      color: #22d3ee;
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid rgba(6, 182, 212, 0.2);
    }}
    .chart-container {{
      position: relative;
      height: 280px;
      width: 100%;
    }}

    /* Regional Table inside Regional Card */
    .regional-table-mini {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
      font-size: 12px;
    }}
    .regional-table-mini th {{
      background: rgba(15, 23, 42, 0.6);
      padding: 8px 10px;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--card-border);
      text-align: left;
    }}
    .regional-table-mini td {{
      padding: 8px 10px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.3);
      color: #e2e8f0;
    }}
    .regional-table-mini tr.clickable-row {{
      cursor: pointer;
      transition: background 0.15s;
    }}
    .regional-table-mini tr.clickable-row:hover td {{
      background: rgba(6, 182, 212, 0.12) !important;
    }}
    .regional-table-mini tr.region-active td {{
      background: rgba(6, 182, 212, 0.22) !important;
      font-weight: 600;
      border-bottom-color: rgba(6, 182, 212, 0.4);
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
      margin-top: 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--card-border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}
    th {{
      background: rgba(15, 23, 42, 0.85);
      padding: 12px 14px;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--card-border);
      white-space: nowrap;
    }}
    th.sortable {{
      cursor: pointer;
      user-select: none;
    }}
    th.sortable:hover {{
      color: #fff;
      background: rgba(59, 130, 246, 0.12);
    }}
    td {{
      padding: 11px 14px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.4);
      color: #e2e8f0;
      white-space: nowrap;
    }}
    tr.clickable-row {{
      cursor: pointer;
      transition: background 0.15s ease;
    }}
    tr.clickable-row:hover td {{
      background: rgba(139, 92, 246, 0.12) !important;
    }}
    tr.category-active td {{
      background: rgba(139, 92, 246, 0.25) !important;
      border-bottom-color: rgba(139, 92, 246, 0.5);
    }}
    tr:hover td {{
      background: rgba(59, 130, 246, 0.06);
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      transition: transform 0.15s;
    }}
    .badge-green {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .badge-blue {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .badge-purple {{ background: rgba(139, 92, 246, 0.15); color: #c4b5fd; border: 1px solid rgba(139, 92, 246, 0.3); cursor: pointer; }}
    .badge-purple:hover {{ background: rgba(139, 92, 246, 0.3); transform: scale(1.05); }}
    .badge-cyan {{ background: rgba(6, 182, 212, 0.15); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.3); cursor: pointer; }}
    .badge-cyan:hover {{ background: rgba(6, 182, 212, 0.35); transform: scale(1.05); }}
    .badge-amber {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-red {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
    .badge-gray {{ background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }}
    .badge-sub {{ font-size: 10px; background: rgba(255, 255, 255, 0.07); color: #94a3b8; border-radius: 4px; padding: 2px 6px; }}
    .badge-code {{ font-family: monospace; background: rgba(0, 0, 0, 0.3); padding: 2px 6px; border-radius: 4px; font-size: 11px; color: #93c5fd; }}

    /* Category Quick Breakdown Bar in Records Explorer */
    .category-breakdown-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin-bottom: 14px;
      padding: 10px 14px;
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(51, 65, 85, 0.6);
      border-radius: var(--radius-sm);
    }}
    .cat-breakdown-label {{
      font-size: 11px;
      font-weight: 700;
      color: #cbd5e1;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-right: 4px;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .cat-chip {{
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      padding: 3px 9px;
      border-radius: 12px;
      font-size: 11px;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }}
    .cat-chip:hover {{
      background: rgba(139, 92, 246, 0.2);
      border-color: var(--purple);
      color: #fff;
    }}
    .cat-chip.active {{
      background: var(--purple);
      border-color: var(--purple);
      color: #fff;
      font-weight: 700;
      box-shadow: 0 2px 8px var(--purple-glow);
    }}
    .cat-chip-count {{
      font-size: 10px;
      opacity: 0.85;
      background: rgba(0, 0, 0, 0.25);
      padding: 1px 5px;
      border-radius: 10px;
    }}

    /* Records Explorer Section */
    .records-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 22px;
      margin-bottom: 24px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}
    .records-header-controls {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .search-box-wrapper {{
      position: relative;
      flex: 1;
      min-width: 260px;
      max-width: 420px;
    }}
    .search-input {{
      width: 100%;
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      padding: 9px 14px 9px 36px;
      border-radius: 20px;
      color: #fff;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 14px;
      pointer-events: none;
    }}
    .status-filter-pills {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .btn-status-pill {{
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 16px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-status-pill:hover {{
      color: #fff;
      border-color: rgba(59, 130, 246, 0.4);
    }}
    .btn-status-pill.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}
    .pagination-toolbar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--card-border);
      font-size: 12px;
      color: var(--text-muted);
    }}
    .pagination-btns {{
      display: flex;
      gap: 6px;
      align-items: center;
    }}
    .btn-page {{
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      transition: background 0.2s;
    }}
    .btn-page:hover:not(:disabled) {{
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--primary);
    }}
    .btn-page:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}
    .page-info {{
      color: var(--text-muted);
      font-weight: 500;
    }}
    .page-size-select {{
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 12px;
      outline: none;
    }}

    .footer-note {{
      text-align: center;
      color: var(--text-dim);
      font-size: 12px;
      margin-top: 24px;
      padding-top: 16px;
      border-top: 1px solid var(--card-border);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <header>
      <div class="title-area">
        <h1>
          E-Commerce Executive Sales & Profitability Dashboard
          <span class="title-badge">All 52,500 Records Online</span>
        </h1>
        <p>Interactive Multi-Year Analytics Model | Click any month, category, region or city to inspect 100% of matching records</p>
      </div>
    </header>

    <!-- Filter Section (Year, Month, Category, Region & City Selectors) -->
    <div class="filter-section">
      <!-- 1. Year Filter Row -->
      <div class="filter-row">
        <span class="filter-label">Select Year:</span>
        <div class="btn-group">
          <button class="btn-filter btn-year" onclick="setYear('all', this)">All Years (2022-2024)</button>
          <button class="btn-filter btn-year" onclick="setYear('2022', this)">2022</button>
          <button class="btn-filter btn-year active" onclick="setYear('2023', this)">2023</button>
          <button class="btn-filter btn-year" onclick="setYear('2024', this)">2024</button>
        </div>
      </div>

      <!-- 2. Month Filter Row -->
      <div class="filter-row" id="month-filter-row">
        <span class="filter-label">Select Month:</span>
        <div class="btn-group" id="month-buttons-container"></div>
      </div>

      <!-- 3. Category Filter Row -->
      <div class="filter-row" id="cat-filter-row">
        <span class="filter-label">Add Category:</span>
        <div class="btn-group" id="category-buttons-container"></div>
      </div>

      <!-- 4. Region Filter Row (Dedicated Front & Center) -->
      <div class="filter-row" id="region-filter-row">
        <span class="filter-label">Select Region:</span>
        <div class="btn-group" id="region-buttons-container">
          <button class="btn-filter btn-reg active" onclick="selectRegion(null)">All Regions</button>
          <button class="btn-filter btn-reg" onclick="selectRegion('South')">South</button>
          <button class="btn-filter btn-reg" onclick="selectRegion('West')">West</button>
          <button class="btn-filter btn-reg" onclick="selectRegion('North')">North</button>
          <button class="btn-filter btn-reg" onclick="selectRegion('East')">East</button>
          <button class="btn-filter btn-reg" onclick="selectRegion('Central')">Central</button>
        </div>
      </div>

      <!-- 5. City Filter Row -->
      <div class="filter-row" id="city-filter-row">
        <span class="filter-label">Select City:</span>
        <div style="display: flex; align-items: center; gap: 8px;">
          <select class="select-dropdown" id="city-select-dropdown" onchange="selectCity(this.value)">
            <option value="">All Cities (21 Total)</option>
          </select>
        </div>
        <div class="btn-group" id="top-cities-container" style="margin-left: 6px;"></div>
      </div>

      <!-- Active Filter Banner -->
      <div class="filter-status-banner" id="filter-banner">
        <div class="banner-content">
          <span class="banner-tag" id="banner-tag">Active Filter</span>
          <span id="banner-text" style="font-weight: 600; color: #fff;">Displaying records...</span>
        </div>
        <button class="btn-clear-filter" onclick="clearAllFilters()">✕ Reset All Filters</button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">
          <span>Total Gross Sales</span>
          <span class="kpi-scope" id="scope-rev">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-rev">&#8377; 4.78 Cr</div>
        <div class="kpi-sub" id="kpi-rev-sub">&#8377; 47,821,993</div>
      </div>
      <div class="kpi-card kpi-profit">
        <div class="kpi-label">
          <span>Total Net Profit</span>
          <span class="kpi-scope" id="scope-prof">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-prof">&#8377; 1.37 Cr</div>
        <div class="kpi-sub" id="kpi-prof-sub">&#8377; 13,678,420</div>
      </div>
      <div class="kpi-card kpi-margin">
        <div class="kpi-label">
          <span>Profit Margin %</span>
          <span class="kpi-scope" id="scope-margin">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-margin">28.60%</div>
        <div class="kpi-sub" id="kpi-margin-sub">Enterprise margin</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">
          <span>Total Orders</span>
          <span class="kpi-scope" id="scope-orders">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-orders">19,096</div>
        <div class="kpi-sub" id="kpi-cust">4,772 Customers</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">
          <span>Average Order Value</span>
          <span class="kpi-scope" id="scope-aov">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-aov">&#8377; 2,504.29</div>
        <div class="kpi-sub" id="kpi-aov-sub">Average basket spend</div>
      </div>
      <div class="kpi-card kpi-growth" id="kpi-growth-card">
        <div class="kpi-label">
          <span id="kpi-growth-title">Return Rate</span>
          <span class="kpi-scope" id="scope-growth">2023 Full Year</span>
        </div>
        <div class="kpi-value" id="kpi-growth-val">7.00%</div>
        <div class="kpi-sub" id="kpi-growth-sub">Reverse logistics</div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-grid">
      <div class="card">
        <div class="card-header">
          <div class="card-title" id="chart-title">
            Monthly Sales & Net Profit (2023)
          </div>
          <span class="card-hint">💡 Click any month bar to inspect records</span>
        </div>
        <div class="chart-container">
          <canvas id="monthlyChart"></canvas>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title" id="regional-title">Regional Distribution</div>
          <span class="card-hint card-hint-cyan">📍 Click slice or table row to view records</span>
        </div>
        <div class="chart-container" style="height: 200px;">
          <canvas id="regionalChart"></canvas>
        </div>
        <!-- Regional Breakdown Mini Table with Clickable Rows -->
        <table class="regional-table-mini" style="margin-top: 12px;">
          <thead>
            <tr>
              <th>Region</th>
              <th style="text-align: right;">Orders</th>
              <th style="text-align: right;">Sales (INR)</th>
              <th style="text-align: right;">Profit (INR)</th>
              <th style="text-align: right;">Margin %</th>
              <th style="text-align: center;">Action</th>
            </tr>
          </thead>
          <tbody id="regional-table-body"></tbody>
        </table>
      </div>
    </div>

    <!-- Category Contribution Table -->
    <div class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title" id="table-title">Category Financial Contribution (2023)</div>
          <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
            Click on any category row to filter all transaction records and metrics for that category.
          </p>
        </div>
        <span class="card-hint" style="background: rgba(139, 92, 246, 0.12); color: #c4b5fd; border-color: rgba(139, 92, 246, 0.3);">
          ⚡ Click row to add/filter category
        </span>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Orders</th>
              <th>Gross Revenue (INR)</th>
              <th>Net Profit (INR)</th>
              <th>Profit Margin %</th>
              <th>Performance Tag</th>
              <th style="text-align: center;">Action</th>
            </tr>
          </thead>
          <tbody id="category-table-body"></tbody>
        </table>
      </div>
    </div>

    <!-- Complete Transaction Records Explorer -->
    <div class="records-card" id="records-section">
      <div class="card-header" style="margin-bottom: 12px;">
        <div>
          <div class="card-title" id="records-title" style="font-size: 18px;">
            📋 Complete Transaction Records Explorer
          </div>
          <p id="records-subtitle" style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">
            Showing all transaction records matching your active selection. Click any month, category, region or city to filter.
          </p>
        </div>
        <div id="records-count-badge" class="badge badge-blue" style="font-size: 12px; padding: 6px 12px;">
          0 Records
        </div>
      </div>

      <!-- Category Breakdown Chips Bar (Add / Filter Category quickly in current selection) -->
      <div class="category-breakdown-bar" id="category-chips-bar">
        <span class="cat-breakdown-label">🏷️ Filter by Category:</span>
        <div id="category-chips-container" style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center;"></div>
      </div>

      <!-- Controls: Search & Status Filters -->
      <div class="records-header-controls">
        <div class="search-box-wrapper">
          <span class="search-icon">&#128269;</span>
          <input
            type="text"
            id="record-search-input"
            class="search-input"
            placeholder="Search Order ID, Customer, Product, Category, City, Region..."
            oninput="handleSearch(this.value)"
          />
        </div>
        <div class="status-filter-pills">
          <span style="font-size: 12px; color: var(--text-muted); margin-right: 4px;">Status:</span>
          <button class="btn-status-pill active" onclick="setStatusFilter('ALL', this)">All</button>
          <button class="btn-status-pill" onclick="setStatusFilter('Delivered', this)">Delivered</button>
          <button class="btn-status-pill" onclick="setStatusFilter('Shipped', this)">Shipped</button>
          <button class="btn-status-pill" onclick="setStatusFilter('Returned', this)">Returned</button>
          <button class="btn-status-pill" onclick="setStatusFilter('Cancelled', this)">Cancelled</button>
        </div>
      </div>

      <!-- Records Table -->
      <div class="table-container">
        <table id="transactions-table">
          <thead>
            <tr>
              <th class="sortable" onclick="sortTable('order_id')">Order ID &#8645;</th>
              <th class="sortable" onclick="sortTable('order_date')">Date &#8645;</th>
              <th>Customer</th>
              <th>Product Name</th>
              <th>Category</th>
              <th>Subcategory</th>
              <th>City</th>
              <th>Region</th>
              <th style="text-align: right;">Qty</th>
              <th class="sortable" style="text-align: right;" onclick="sortTable('sales_amount')">Sales Amount &#8645;</th>
              <th class="sortable" style="text-align: right;" onclick="sortTable('profit_amount')">Profit &#8645;</th>
              <th class="sortable" style="text-align: right;" onclick="sortTable('profit_margin_pct')">Margin % &#8645;</th>
              <th style="text-align: center;">Status</th>
            </tr>
          </thead>
          <tbody id="records-table-body"></tbody>
        </table>
      </div>

      <!-- Pagination Toolbar -->
      <div class="pagination-toolbar">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span>Rows per page:</span>
          <select class="page-size-select" id="page-size-select" onchange="changePageSize(this.value)">
            <option value="10">10</option>
            <option value="20" selected>20</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span class="page-info" id="pagination-summary">Showing 1 to 20 of 100</span>
        </div>
        <div class="pagination-btns">
          <button class="btn-page" id="btn-prev-page" onclick="prevPage()">&larr; Previous</button>
          <span class="page-info" id="page-current-info" style="margin: 0 4px;">Page 1 of 5</span>
          <button class="btn-page" id="btn-next-page" onclick="nextPage()">Next &rarr;</button>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer-note">
      E-Commerce Sales, Customer & Profitability Analytics Project | Enterprise Interactive Executive Model
    </div>
  </div>

  <script>
    const dataset = {json_str};

    // Global in-memory access
    const ALL_ORDERS = dataset.orders;       // 52,500 records
    const PRODUCTS_MAP = dataset.products;   // PROD-ID -> [name, category, subcategory]
    const YEARS_DATA = dataset.years;
    const METADATA = dataset.metadata;

    // State Variables
    let currentYear = '2023';
    let currentMonth = null;    // null = all months
    let currentCategory = null; // null = all categories
    let currentRegion = null;   // null = all regions
    let currentCity = null;     // null = all cities
    let currentSearchQuery = '';
    let currentStatusFilter = 'ALL';
    let currentSortColumn = 'order_date';
    let currentSortAsc = false;
    let currentPage = 1;
    let pageSize = 20;

    // Filtered records cache
    let activeFilteredRecords = [];
    let searchFilteredRecords = [];

    // Charts instances
    let monthlyChartInstance = null;
    let regionalChartInstance = null;

    const REGION_COLORS = {{
      'South': '#3b82f6',
      'West': '#10b981',
      'North': '#f59e0b',
      'East': '#8b5cf6',
      'Central': '#ef4444'
    }};

    function formatINR(val) {{
      if (val === null || val === undefined) return 'N/A';
      if (Math.abs(val) >= 10000000) {{
        return '&#8377; ' + (val / 10000000).toFixed(2) + ' Cr';
      }} else if (Math.abs(val) >= 100000) {{
        return '&#8377; ' + (val / 100000).toFixed(2) + ' L';
      }} else {{
        return '&#8377; ' + Number(val).toLocaleString('en-IN');
      }}
    }}

    // Populate Month Filter Buttons dynamically
    function updateMonthFilterButtons() {{
      const container = document.getElementById('month-buttons-container');
      container.innerHTML = '';

      const allBtn = document.createElement('button');
      allBtn.className = 'btn-filter btn-month' + (currentMonth === null ? ' active' : '');
      allBtn.innerText = 'All Months';
      allBtn.onclick = () => selectMonth(null);
      container.appendChild(allBtn);

      if (currentYear === 'all') {{
        const monthsList = YEARS_DATA['all'].monthly.labels;
        monthsList.forEach(ym => {{
          const btn = document.createElement('button');
          btn.className = 'btn-filter btn-month' + (currentMonth === ym ? ' active' : '');
          btn.innerText = ym;
          btn.onclick = () => selectMonth(ym);
          container.appendChild(btn);
        }});
      }} else {{
        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        monthNames.forEach(m => {{
          const btn = document.createElement('button');
          btn.className = 'btn-filter btn-month' + (currentMonth === m ? ' active' : '');
          btn.innerText = m;
          btn.onclick = () => selectMonth(m);
          container.appendChild(btn);
        }});
      }}
    }}

    // Populate Category Filter Buttons dynamically
    function updateCategoryFilterButtons() {{
      const container = document.getElementById('category-buttons-container');
      container.innerHTML = '';

      const allBtn = document.createElement('button');
      allBtn.className = 'btn-filter btn-cat' + (currentCategory === null ? ' active' : '');
      allBtn.innerText = 'All Categories';
      allBtn.onclick = () => selectCategory(null);
      container.appendChild(allBtn);

      const categories = YEARS_DATA[currentYear].categories;
      categories.forEach(c => {{
        const btn = document.createElement('button');
        btn.className = 'btn-filter btn-cat' + (currentCategory === c.name ? ' active' : '');
        btn.innerText = c.name;
        btn.onclick = () => selectCategory(c.name);
        container.appendChild(btn);
      }});
    }}

    // Update Region Filter buttons and City dropdown + top city pills
    function updateGeoFilters() {{
      // Update region buttons
      document.querySelectorAll('#region-buttons-container .btn-reg').forEach(b => {{
        const txt = b.innerText.trim();
        if (currentRegion === null && txt === 'All Regions') {{
          b.classList.add('active');
        }} else if (currentRegion !== null && txt === currentRegion) {{
          b.classList.add('active');
        }} else {{
          b.classList.remove('active');
        }}
      }});

      // Populate City dropdown
      const citySelect = document.getElementById('city-select-dropdown');
      citySelect.innerHTML = '<option value="">All Cities (21 Total)</option>';

      const citiesByReg = METADATA.cities_by_region || {{}};
      const allCities = METADATA.all_cities || [];

      let citiesToShow = allCities;
      if (currentRegion && citiesByReg[currentRegion]) {{
        citiesToShow = citiesByReg[currentRegion];
      }}

      citiesToShow.forEach(c => {{
        const opt = document.createElement('option');
        opt.value = c;
        opt.innerText = c + (currentRegion ? '' : ` (${{getCityRegion(c)}})`);
        if (currentCity === c) opt.selected = true;
        citySelect.appendChild(opt);
      }});

      // Top cities quick buttons
      const topCitiesContainer = document.getElementById('top-cities-container');
      topCitiesContainer.innerHTML = '';
      const topMetro = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad'];
      const metrosToShow = currentRegion ? topMetro.filter(c => getCityRegion(c) === currentRegion) : topMetro.slice(0, 6);
      metrosToShow.forEach(city => {{
        const btn = document.createElement('button');
        btn.className = 'btn-filter' + (currentCity === city ? ' active' : '');
        btn.style.fontSize = '11px';
        btn.style.padding = '4px 10px';
        btn.innerText = city;
        btn.onclick = () => selectCity(city);
        topCitiesContainer.appendChild(btn);
      }});

      // Render Regional Mini Table inside the Regional Card
      renderRegionalTable();
    }}

    function renderRegionalTable() {{
      const tbody = document.getElementById('regional-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';
      const regions = YEARS_DATA[currentYear].regions;
      regions.forEach(r => {{
        const isRegSelected = currentRegion === r.name;
        const color = REGION_COLORS[r.name] || '#3b82f6';
        const tr = document.createElement('tr');
        tr.className = 'clickable-row' + (isRegSelected ? ' region-active' : '');
        tr.onclick = () => selectRegion(r.name);
        tr.title = `Click to filter all records for ${{r.name}} Region`;
        tr.innerHTML = `
          <td>
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:${{color}}; margin-right:6px;"></span>
            <strong>${{r.name}}</strong>
          </td>
          <td style="text-align: right;">${{r.orders.toLocaleString('en-IN')}}</td>
          <td style="text-align: right; color:#60a5fa;">&#8377; ${{formatINR(r.rev)}}</td>
          <td style="text-align: right; color:#34d399;">&#8377; ${{formatINR(r.prof)}}</td>
          <td style="text-align: right; font-weight:600;">${{r.margin.toFixed(1)}}%</td>
          <td style="text-align: center;">
            <span class="badge ${{isRegSelected ? 'badge-cyan' : 'badge-gray'}}" style="font-size: 10px;">
              ${{isRegSelected ? 'Selected' : 'View Records &rarr;'}}
            </span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function getCityRegion(cityName) {{
      const citiesByReg = METADATA.cities_by_region || {{}};
      for (const reg in citiesByReg) {{
        if (citiesByReg[reg].includes(cityName)) return reg;
      }}
      return '';
    }}

    // Year selection
    function setYear(year, btn) {{
      currentYear = year;
      currentMonth = null;
      currentCategory = null;
      currentRegion = null;
      currentCity = null;
      currentPage = 1;
      currentSearchQuery = '';
      currentStatusFilter = 'ALL';
      document.getElementById('record-search-input').value = '';

      document.querySelectorAll('.btn-year').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      updateMonthFilterButtons();
      updateCategoryFilterButtons();
      updateGeoFilters();
      renderDashboard();
    }}

    // Month selection
    function selectMonth(monthKey) {{
      currentMonth = (currentMonth === monthKey) ? null : monthKey;
      currentPage = 1;
      updateMonthFilterButtons();
      renderDashboard();
      if (currentMonth !== null) scrollToRecords();
    }}

    // Category selection
    function selectCategory(catName) {{
      currentCategory = (currentCategory === catName) ? null : catName;
      currentPage = 1;
      updateCategoryFilterButtons();
      renderDashboard();
      if (currentCategory !== null) scrollToRecords();
    }}

    // Region selection (invoked by clicking doughnut slices, legend, region buttons, table rows, or record badges)
    function selectRegion(regionName) {{
      currentRegion = (currentRegion === regionName) ? null : regionName;
      if (currentRegion && currentCity) {{
        if (getCityRegion(currentCity) !== currentRegion) {{
          currentCity = null;
        }}
      }}
      currentPage = 1;
      updateGeoFilters();
      renderDashboard();
      if (currentRegion !== null) scrollToRecords();
    }}

    // City selection
    function selectCity(cityName) {{
      currentCity = (cityName && cityName !== '') ? cityName : null;
      if (currentCity) {{
        const r = getCityRegion(currentCity);
        if (r) currentRegion = r;
      }}
      currentPage = 1;
      updateGeoFilters();
      renderDashboard();
      if (currentCity !== null) scrollToRecords();
    }}

    function clearAllFilters() {{
      currentMonth = null;
      currentCategory = null;
      currentRegion = null;
      currentCity = null;
      currentPage = 1;
      currentSearchQuery = '';
      currentStatusFilter = 'ALL';
      document.getElementById('record-search-input').value = '';
      updateMonthFilterButtons();
      updateCategoryFilterButtons();
      updateGeoFilters();
      renderDashboard();
    }}

    function scrollToRecords() {{
      const recordsEl = document.getElementById('records-section');
      if (recordsEl) {{
        recordsEl.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}

    const MONTH_NUMS = {{
      'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
      'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }};

    // Query 100% of all matching records
    function queryAllOrders() {{
      return ALL_ORDERS.filter(o => {{
        // o: [order_id, date, cust_id, prod_id, city, region, qty, sales, profit, margin, status]
        const oDate = o[1];
        const oYear = oDate.substring(0, 4);

        if (currentYear !== 'all' && oYear !== currentYear) {{
          return false;
        }}

        if (currentMonth !== null) {{
          if (currentYear === 'all') {{
            if (!oDate.startsWith(currentMonth)) return false;
          }} else {{
            const mNum = MONTH_NUMS[currentMonth];
            const targetYM = currentYear + '-' + mNum;
            if (!oDate.startsWith(targetYM)) return false;
          }}
        }}

        if (currentCategory !== null) {{
          const prodInfo = PRODUCTS_MAP[o[3]];
          if (!prodInfo || prodInfo[1] !== currentCategory) return false;
        }}

        if (currentRegion !== null && o[5] !== currentRegion) {{
          return false;
        }}

        if (currentCity !== null && o[4] !== currentCity) {{
          return false;
        }}

        return true;
      }});
    }}

    // Main Render Routine
    function renderDashboard() {{
      const yearData = YEARS_DATA[currentYear];
      const yearLabel = currentYear === 'all' ? 'All Operating Years (2022-2024)' : currentYear;

      const banner = document.getElementById('filter-banner');
      const isMonthActive = currentMonth !== null;
      const isCatActive = currentCategory !== null;
      const isRegActive = currentRegion !== null;
      const isCityActive = currentCity !== null;

      const hasAnyFilter = isMonthActive || isCatActive || isRegActive || isCityActive;

      // Query ALL matching records
      activeFilteredRecords = queryAllOrders();

      // Render Dynamic Category Chips above the Records Table
      renderCategoryChips(activeFilteredRecords);

      if (hasAnyFilter) {{
        banner.classList.add('show');
        const filterParts = [];
        if (isRegActive) filterParts.push(`Region: <strong>${{currentRegion}}</strong>`);
        if (isCityActive) filterParts.push(`City: <strong>${{currentCity}}</strong>`);
        if (isCatActive) filterParts.push(`Category: <strong>${{currentCategory}}</strong>`);
        if (isMonthActive) {{
          const mDisplay = currentYear === 'all' ? currentMonth : (yearData.months[currentMonth] ? yearData.months[currentMonth].full_name : currentMonth);
          filterParts.push(`Month: <strong>${{mDisplay}}</strong>`);
        }}

        document.getElementById('banner-tag').innerText = 'Active Filter';
        document.getElementById('banner-text').innerHTML = 
          `Displaying all <strong>${{activeFilteredRecords.length.toLocaleString('en-IN')}}</strong> verified records for ${{filterParts.join(' &bull; ')}} (${{yearLabel}})`;

        // Calculate exact metrics from activeFilteredRecords
        let totSales = 0, totProfit = 0, totUnits = 0;
        const custSet = new Set();
        for (let i = 0; i < activeFilteredRecords.length; i++) {{
          const o = activeFilteredRecords[i];
          totSales += o[7];
          totProfit += o[8];
          totUnits += o[6];
          custSet.add(o[2]);
        }}
        const totOrders = activeFilteredRecords.length;
        const totMargin = totSales > 0 ? ((totProfit / totSales) * 100) : 0;
        const avgAov = totOrders > 0 ? (totSales / totOrders) : 0;

        let scopeTitle = '';
        if (isCityActive) scopeTitle = `${{currentCity}} (${{currentRegion}})`;
        else if (isRegActive) scopeTitle = `${{currentRegion}} Region`;
        else if (isCatActive) scopeTitle = currentCategory;
        else if (isMonthActive) scopeTitle = (currentYear === 'all' ? currentMonth : (yearData.months[currentMonth]?.full_name || currentMonth));

        document.querySelectorAll('.kpi-scope').forEach(el => el.innerText = scopeTitle || yearLabel);

        document.getElementById('kpi-rev').innerHTML = formatINR(totSales);
        document.getElementById('kpi-rev-sub').innerHTML = '&#8377; ' + Math.round(totSales).toLocaleString('en-IN');
        document.getElementById('kpi-prof').innerHTML = formatINR(totProfit);
        document.getElementById('kpi-prof-sub').innerHTML = '&#8377; ' + Math.round(totProfit).toLocaleString('en-IN');
        document.getElementById('kpi-margin').innerHTML = totMargin.toFixed(2) + '%';
        document.getElementById('kpi-margin-sub').innerHTML = 'Filtered profit margin';
        document.getElementById('kpi-orders').innerHTML = totOrders.toLocaleString('en-IN');
        document.getElementById('kpi-cust').innerHTML = custSet.size.toLocaleString('en-IN') + ' Unique Customers';
        document.getElementById('kpi-aov').innerHTML = '&#8377; ' + avgAov.toLocaleString('en-IN', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
        document.getElementById('kpi-aov-sub').innerHTML = 'Filtered average basket';

        document.getElementById('kpi-growth-title').innerText = 'Share of Annual Revenue';
        const contribPct = ((totSales / yearData.rev) * 100).toFixed(1);
        document.getElementById('kpi-growth-val').innerHTML = contribPct + '%';
        document.getElementById('kpi-growth-sub').innerHTML = `Of ${{yearLabel}} total (₹ ${{formatINR(yearData.rev)}})`;

        // Titles
        document.getElementById('chart-title').innerHTML = `Monthly Sales & Net Profit (${{yearLabel}}) ${{isMonthActive ? '&bull; <span style=\"color:#10b981;\">[Active Month]</span>' : ''}}`;
        document.getElementById('regional-title').innerHTML = `Regional Distribution ${{isRegActive ? '&bull; <span style=\"color:#06b6d4;\">[' + currentRegion + ' Region]</span>' : ''}}`;
        document.getElementById('table-title').innerHTML = `Category Financial Contribution (${{yearLabel}}) ${{isCatActive ? '&bull; <span style=\"color:#8b5cf6;\">[' + currentCategory + ']</span>' : ''}}`;

        let recTitle = '📋 All Transaction Records &mdash; ';
        if (isCityActive) recTitle += `City: ${{currentCity}} (${{currentRegion}})`;
        else if (isRegActive) recTitle += `Region: ${{currentRegion}}`;
        else if (isCatActive) recTitle += `Category: ${{currentCategory}}`;
        else if (isMonthActive) recTitle += `Month: ${{currentYear === 'all' ? currentMonth : (yearData.months[currentMonth]?.full_name || currentMonth)}}`;
        document.getElementById('records-title').innerHTML = recTitle;
        document.getElementById('records-subtitle').innerHTML = `Displaying all ${{totOrders.toLocaleString('en-IN')}} verified transactions matching ${{filterParts.join(', ')}} (${{yearLabel}})`;

        if (isMonthActive && yearData.months[currentMonth]) {{
          renderTable(yearData.months[currentMonth].categories || yearData.categories);
        }} else {{
          renderTable(yearData.categories);
        }}

      }} else {{
        // FULL YEAR VIEW (No Filter)
        banner.classList.remove('show');
        document.querySelectorAll('.kpi-scope').forEach(el => el.innerText = yearLabel);

        document.getElementById('kpi-rev').innerHTML = formatINR(yearData.rev);
        document.getElementById('kpi-rev-sub').innerHTML = '&#8377; ' + yearData.rev.toLocaleString('en-IN');
        document.getElementById('kpi-prof').innerHTML = formatINR(yearData.prof);
        document.getElementById('kpi-prof-sub').innerHTML = '&#8377; ' + yearData.prof.toLocaleString('en-IN');
        document.getElementById('kpi-margin').innerHTML = yearData.margin.toFixed(2) + '%';
        document.getElementById('kpi-margin-sub').innerHTML = 'Enterprise margin';
        document.getElementById('kpi-orders').innerHTML = yearData.orders.toLocaleString('en-IN');
        document.getElementById('kpi-cust').innerHTML = yearData.cust.toLocaleString('en-IN') + ' Active Customers';
        document.getElementById('kpi-aov').innerHTML = '&#8377; ' + yearData.aov.toLocaleString('en-IN', {{minimumFractionDigits: 2}});
        document.getElementById('kpi-aov-sub').innerHTML = 'Average spend per order';

        document.getElementById('kpi-growth-title').innerText = 'Order Return Rate';
        document.getElementById('kpi-growth-val').innerHTML = yearData.ret_rate.toFixed(2) + '%';
        document.getElementById('kpi-growth-sub').innerHTML = 'Reverse logistics rate';

        document.getElementById('chart-title').innerHTML = `Monthly Sales & Net Profit (${{yearLabel}})`;
        document.getElementById('regional-title').innerHTML = `Regional Distribution`;
        document.getElementById('table-title').innerHTML = `Category Financial Contribution (${{yearLabel}})`;
        document.getElementById('records-title').innerHTML = `📋 All Transaction Records &mdash; ${{yearLabel}}`;
        document.getElementById('records-subtitle').innerHTML = `Showing all ${{yearData.orders.toLocaleString('en-IN')}} transaction records for ${{yearLabel}}. Click any month, category, region or city to filter.`;

        renderTable(yearData.categories);
      }}

      applyRecordsFilter();
      renderCharts();
    }}

    // Render Dynamic Category Chips above the Records Table
    function renderCategoryChips(records) {{
      const container = document.getElementById('category-chips-container');
      container.innerHTML = '';

      const counts = {{}};
      for (let i = 0; i < records.length; i++) {{
        const prodId = records[i][3];
        const p = PRODUCTS_MAP[prodId];
        const cat = p ? p[1] : 'Other';
        counts[cat] = (counts[cat] || 0) + 1;
      }}

      const allChip = document.createElement('div');
      allChip.className = 'cat-chip' + (currentCategory === null ? ' active' : '');
      allChip.onclick = () => selectCategory(null);
      allChip.innerHTML = `All Categories <span class="cat-chip-count">${{records.length.toLocaleString('en-IN')}}</span>`;
      container.appendChild(allChip);

      const sortedCats = Object.keys(counts).sort((a, b) => counts[b] - counts[a]);
      sortedCats.forEach(cat => {{
        const chip = document.createElement('div');
        chip.className = 'cat-chip' + (currentCategory === cat ? ' active' : '');
        chip.title = `Filter all records by category: ${{cat}}`;
        chip.onclick = () => selectCategory(cat);
        chip.innerHTML = `${{cat}} <span class="cat-chip-count">${{counts[cat].toLocaleString('en-IN')}}</span>`;
        container.appendChild(chip);
      }});
    }}

    // Render Charts
    function renderCharts() {{
      const yearData = YEARS_DATA[currentYear];
      const labels = yearData.monthly.labels;

      // 1. Monthly Chart
      const bgSales = labels.map(lbl => {{
        if (!currentMonth) return 'rgba(59, 130, 246, 0.85)';
        return (lbl === currentMonth) ? '#3b82f6' : 'rgba(59, 130, 246, 0.25)';
      }});
      const bgProfit = labels.map(lbl => {{
        if (!currentMonth) return 'rgba(16, 185, 129, 0.85)';
        return (lbl === currentMonth) ? '#10b981' : 'rgba(16, 185, 129, 0.25)';
      }});
      const borderSales = labels.map(lbl => (lbl === currentMonth) ? '#ffffff' : 'transparent');
      const borderWidth = labels.map(lbl => (lbl === currentMonth) ? 2 : 0);

      const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
      if (monthlyChartInstance) monthlyChartInstance.destroy();

      monthlyChartInstance = new Chart(ctxMonthly, {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: [
            {{
              label: 'Gross Sales (INR)',
              data: yearData.monthly.rev,
              backgroundColor: bgSales,
              borderColor: borderSales,
              borderWidth: borderWidth,
              borderRadius: 6,
              yAxisID: 'y'
            }},
            {{
              label: 'Net Profit (INR)',
              data: yearData.monthly.prof,
              backgroundColor: bgProfit,
              borderColor: borderSales,
              borderWidth: borderWidth,
              borderRadius: 6,
              yAxisID: 'y'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          onClick: function(evt, elements) {{
            if (elements && elements.length > 0) {{
              const elementIndex = elements[0].index;
              const clickedMonth = monthlyChartInstance.data.labels[elementIndex];
              selectMonth(clickedMonth);
            }}
          }},
          onHover: function(evt, elements) {{
            evt.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
          }},
          plugins: {{
            legend: {{ labels: {{ color: '#cbd5e1', font: {{ size: 12 }} }} }},
            tooltip: {{
              callbacks: {{
                afterTitle: function() {{
                  return '(Click bar to inspect all month records)';
                }},
                label: function(c) {{
                  return c.dataset.label + ': ₹ ' + Number(c.raw).toLocaleString('en-IN');
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
            y: {{
              ticks: {{
                color: '#94a3b8',
                callback: function(v) {{
                  return v >= 10000000 ? (v/10000000).toFixed(1) + ' Cr' : (v/100000).toFixed(0) + ' L';
                }}
              }},
              grid: {{ color: 'rgba(51, 65, 85, 0.4)' }}
            }}
          }}
        }}
      }});

      // 2. Regional Doughnut Chart with interactive Slice and Legend Clicking
      const regLabels = yearData.regions.map(r => r.name);
      const regColors = regLabels.map(r => {{
        const base = REGION_COLORS[r] || '#3b82f6';
        if (!currentRegion) return base;
        return (r === currentRegion) ? base : base + '44';
      }});
      const regBorders = regLabels.map(r => (r === currentRegion) ? '#ffffff' : '#151e2e');
      const regBorderWidths = regLabels.map(r => (r === currentRegion) ? 3 : 2);

      const ctxRegional = document.getElementById('regionalChart').getContext('2d');
      if (regionalChartInstance) regionalChartInstance.destroy();

      regionalChartInstance = new Chart(ctxRegional, {{
        type: 'doughnut',
        data: {{
          labels: regLabels,
          datasets: [{{
            data: yearData.regions.map(r => r.rev),
            backgroundColor: regColors,
            borderWidth: regBorderWidths,
            borderColor: regBorders
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          onClick: function(evt, elements) {{
            if (elements && elements.length > 0) {{
              const elementIndex = elements[0].index;
              const clickedRegion = regionalChartInstance.data.labels[elementIndex];
              selectRegion(clickedRegion);
            }}
          }},
          onHover: function(evt, elements) {{
            evt.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
          }},
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }},
              onClick: function(e, legendItem) {{
                const clickedRegion = legendItem.text;
                selectRegion(clickedRegion);
              }}
            }},
            tooltip: {{
              callbacks: {{
                afterTitle: function() {{
                  return '(Click to view all region records)';
                }},
                label: function(c) {{
                  return c.label + ': ₹ ' + Number(c.raw).toLocaleString('en-IN');
                }}
              }}
            }}
          }}
        }}
      }});
    }}

    // Render Category Table
    function renderTable(categories) {{
      const tbody = document.getElementById('category-table-body');
      tbody.innerHTML = '';
      if (!categories || categories.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#94a3b8;">No category data available</td></tr>';
        return;
      }}
      categories.forEach(cat => {{
        const isCatSelected = currentCategory === cat.name;
        const tag = cat.margin >= 40 ? 'High Margin' : (cat.margin >= 25 ? 'Core Driver' : 'Volume Driver');
        const badgeClass = cat.margin >= 40 ? 'badge-green' : 'badge-blue';
        const tr = document.createElement('tr');
        tr.className = 'clickable-row' + (isCatSelected ? ' category-active' : '');
        tr.onclick = () => selectCategory(cat.name);
        tr.title = `Click to filter all records for category: ${{cat.name}}`;
        tr.innerHTML = `
          <td style="font-weight: 600; color: ${{isCatSelected ? '#c4b5fd' : '#fff'}};">
            ${{isCatSelected ? '&#10003; ' : ''}}${{cat.name}}
          </td>
          <td>${{cat.orders.toLocaleString('en-IN')}}</td>
          <td style="color: #60a5fa; font-weight: 600;">&#8377; ${{cat.rev.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="color: #34d399; font-weight: 600;">&#8377; ${{cat.prof.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="font-weight: 600;">${{cat.margin.toFixed(1)}}%</td>
          <td><span class="badge ${{badgeClass}}">${{tag}}</span></td>
          <td style="text-align: center;">
            <span class="badge ${{isCatSelected ? 'badge-purple' : 'badge-blue'}}" style="font-size: 10px;">
              ${{isCatSelected ? 'Selected' : 'View Records &rarr;'}}
            </span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Real-Time Search & Pagination Logic
    function handleSearch(query) {{
      currentSearchQuery = query.trim().toLowerCase();
      currentPage = 1;
      applyRecordsFilter();
    }}

    function setStatusFilter(status, btn) {{
      currentStatusFilter = status;
      currentPage = 1;
      document.querySelectorAll('.btn-status-pill').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyRecordsFilter();
    }}

    function sortTable(col) {{
      if (currentSortColumn === col) {{
        currentSortAsc = !currentSortAsc;
      }} else {{
        currentSortColumn = col;
        currentSortAsc = true;
      }}
      applyRecordsFilter();
    }}

    function changePageSize(val) {{
      pageSize = parseInt(val, 10);
      currentPage = 1;
      applyRecordsFilter();
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        applyRecordsFilter();
      }}
    }}

    function nextPage() {{
      const totalPages = Math.ceil(searchFilteredRecords.length / pageSize);
      if (currentPage < totalPages) {{
        currentPage++;
        applyRecordsFilter();
      }}
    }}

    function applyRecordsFilter() {{
      // Filter activeFilteredRecords by Status and Search
      searchFilteredRecords = activeFilteredRecords.filter(o => {{
        if (currentStatusFilter !== 'ALL' && o[10] !== currentStatusFilter) {{
          return false;
        }}
        if (currentSearchQuery) {{
          const p = PRODUCTS_MAP[o[3]] || ['', '', ''];
          const targetStr = (o[0] + ' ' + o[2] + ' ' + p[0] + ' ' + p[1] + ' ' + p[2] + ' ' + o[4] + ' ' + o[5]).toLowerCase();
          return targetStr.includes(currentSearchQuery);
        }}
        return true;
      }});

      // Column Sorting
      const colIndexMap = {{
        'order_id': 0,
        'order_date': 1,
        'sales_amount': 7,
        'profit_amount': 8,
        'profit_margin_pct': 9
      }};
      const sortIdx = colIndexMap[currentSortColumn] !== undefined ? colIndexMap[currentSortColumn] : 1;

      searchFilteredRecords.sort((a, b) => {{
        let vA = a[sortIdx];
        let vB = b[sortIdx];
        if (typeof vA === 'string') {{
          vA = vA.toLowerCase();
          vB = vB.toLowerCase();
        }}
        if (vA < vB) return currentSortAsc ? -1 : 1;
        if (vA > vB) return currentSortAsc ? 1 : -1;
        return 0;
      }});

      document.getElementById('records-count-badge').innerText = `${{searchFilteredRecords.length.toLocaleString('en-IN')}} Records Found`;

      const total = searchFilteredRecords.length;
      const totalPages = Math.max(1, Math.ceil(total / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;

      const startIndex = (currentPage - 1) * pageSize;
      const pageSlice = searchFilteredRecords.slice(startIndex, startIndex + pageSize);

      const startDisplay = total === 0 ? 0 : startIndex + 1;
      const endDisplay = Math.min(startIndex + pageSize, total);
      document.getElementById('pagination-summary').innerText = `Showing ${{startDisplay.toLocaleString('en-IN')}} to ${{endDisplay.toLocaleString('en-IN')}} of ${{total.toLocaleString('en-IN')}} records`;
      document.getElementById('page-current-info').innerText = `Page ${{currentPage.toLocaleString('en-IN')}} of ${{totalPages.toLocaleString('en-IN')}}`;
      document.getElementById('btn-prev-page').disabled = currentPage <= 1;
      document.getElementById('btn-next-page').disabled = currentPage >= totalPages || total === 0;

      const tbody = document.getElementById('records-table-body');
      tbody.innerHTML = '';

      if (pageSlice.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="13" style="text-align:center; padding: 28px; color: #94a3b8;">No transaction records match your search or filter criteria.</td></tr>';
        return;
      }}

      pageSlice.forEach(o => {{
        // o: [order_id, date, cust_id, prod_id, city, region, qty, sales, profit, margin, status]
        const p = PRODUCTS_MAP[o[3]] || ['Product Not Found', 'General', 'General'];
        const pName = p[0];
        const pCat = p[1];
        const pSub = p[2];

        let statusBadge = 'badge-gray';
        if (o[10] === 'Delivered') statusBadge = 'badge-green';
        else if (o[10] === 'Shipped') statusBadge = 'badge-blue';
        else if (o[10] === 'Returned') statusBadge = 'badge-red';
        else if (o[10] === 'Cancelled') statusBadge = 'badge-amber';

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="badge-code">${{o[0]}}</span></td>
          <td style="color: #cbd5e1;">${{o[1]}}</td>
          <td><span style="font-size: 11px; color: #94a3b8;">${{o[2]}}</span></td>
          <td style="font-weight: 500; max-width: 200px; overflow: hidden; text-overflow: ellipsis;" title="${{pName}}">${{pName}}</td>
          <td>
            <span class="badge badge-purple" onclick="selectCategory('${{pCat}}')" title="Click to filter by category: ${{pCat}}">
              ${{pCat}}
            </span>
          </td>
          <td><span class="badge badge-sub">${{pSub || 'General'}}</span></td>
          <td>
            <span class="badge badge-cyan" onclick="selectCity('${{o[4]}}')" title="Click to filter by city: ${{o[4]}}">📍 ${{o[4]}}</span>
          </td>
          <td>
            <span class="badge badge-reg" onclick="selectRegion('${{o[5]}}')" title="Click to filter all records for ${{o[5]}} Region" style="font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); cursor: pointer; padding: 2px 8px; border-radius: 6px;">
              ${{o[5]}}
            </span>
          </td>
          <td style="text-align: right; font-weight: 600;">${{o[6]}}</td>
          <td style="text-align: right; color: #60a5fa; font-weight: 600;">&#8377; ${{o[7].toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="text-align: right; color: #34d399; font-weight: 600;">&#8377; ${{o[8].toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="text-align: right; font-weight: 600;">${{o[9].toFixed(1)}}%</td>
          <td style="text-align: center;"><span class="badge ${{statusBadge}}">${{o[10]}}</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Initialize with 2023 on load
    window.onload = function() {{
      setYear('2023', document.querySelector('.btn-year.active'));
    }};
  </script>
</body>
</html>
"""

# Write to root index.html and dashboard/index.html
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_template)

os.makedirs(os.path.join(BASE_DIR, "dashboard"), exist_ok=True)
with open(os.path.join(BASE_DIR, "dashboard", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully generated index.html ({round(os.path.getsize(os.path.join(BASE_DIR, 'index.html'))/(1024*1024), 2)} MB) and dashboard/index.html!")
