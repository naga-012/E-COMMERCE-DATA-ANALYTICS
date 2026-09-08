"""
generate_html_dashboard.py
==========================
Generates an interactive, standalone executive HTML web dashboard with year filtering:
- Button selector: All Years, 2022, 2023 (default), 2024
- Dynamic KPI card updates
- Dynamic Chart.js charts
- Dynamic Category tables
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON_PATH = os.path.join(BASE_DIR, "dashboard_data.json")

with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
    dashboard_data = json.load(f)

json_str = json.dumps(dashboard_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E-Commerce Executive Sales & Profitability Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --success: #10b981;
      --accent: #f59e0b;
      --danger: #ef4444;
      --radius: 12px;
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
    }}
    .container {{
      max-width: 1440px;
      margin: 0 auto;
    }}
    header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }}
    .title-area h1 {{
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.5px;
      color: #fff;
    }}
    .title-area p {{
      font-size: 14px;
      color: var(--text-muted);
      margin-top: 4px;
    }}
    .year-filter-wrapper {{
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(30, 41, 59, 0.7);
      padding: 6px 12px;
      border-radius: 40px;
      border: 1px solid var(--card-border);
    }}
    .year-filter-wrapper span {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      margin-right: 4px;
    }}
    .btn-year {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text);
      padding: 8px 18px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .btn-year:hover {{
      background: rgba(59, 130, 246, 0.2);
      color: #fff;
    }}
    .btn-year.active {{
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 20px;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
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
    .kpi-label {{
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
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
    .charts-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}
    @media (max-width: 1024px) {{
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
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 600;
      color: #fff;
    }}
    .chart-container {{
      position: relative;
      height: 320px;
      width: 100%;
    }}
    .table-container {{
      overflow-x: auto;
      margin-top: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}
    th {{
      background: rgba(15, 23, 42, 0.6);
      padding: 12px;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--card-border);
    }}
    td {{
      padding: 12px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      color: #e2e8f0;
    }}
    tr:hover td {{
      background: rgba(59, 130, 246, 0.05);
    }}
    .badge {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }}
    .badge-green {{ background: rgba(16, 185, 129, 0.15); color: #34d399; }}
    .badge-blue {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; }}
    .footer-note {{
      text-align: center;
      color: var(--text-muted);
      font-size: 12px;
      margin-top: 24px;
      padding-top: 16px;
      border-top: 1px solid var(--card-border);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="title-area">
        <h1>E-Commerce Executive Sales & Profitability Dashboard</h1>
        <p>Interactive Reporting Model | Multi-Year Transaction Analysis (INR &#8377;)</p>
      </div>
      <div class="year-filter-wrapper">
        <span>Select Year:</span>
        <button class="btn-year" onclick="filterYear('all', this)">All Years</button>
        <button class="btn-year" onclick="filterYear('2022', this)">2022</button>
        <button class="btn-year active" onclick="filterYear('2023', this)">2023</button>
        <button class="btn-year" onclick="filterYear('2024', this)">2024</button>
      </div>
    </header>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Total Gross Sales</div>
        <div class="kpi-value" id="kpi-rev">&#8377; 4.78 Cr</div>
        <div class="kpi-sub" id="kpi-rev-sub">&#8377; 47,821,993</div>
      </div>
      <div class="kpi-card kpi-profit">
        <div class="kpi-label">Total Net Profit</div>
        <div class="kpi-value" id="kpi-prof">&#8377; 1.37 Cr</div>
        <div class="kpi-sub" id="kpi-prof-sub">&#8377; 13,678,420</div>
      </div>
      <div class="kpi-card kpi-margin">
        <div class="kpi-label">Profit Margin %</div>
        <div class="kpi-value" id="kpi-margin">28.60%</div>
        <div class="kpi-sub">Healthy enterprise margin</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total Orders</div>
        <div class="kpi-value" id="kpi-orders">19,096</div>
        <div class="kpi-sub" id="kpi-cust">4,772 Active Customers</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Average Order Value</div>
        <div class="kpi-value" id="kpi-aov">&#8377; 2,504.29</div>
        <div class="kpi-sub">Average spend per order</div>
      </div>
      <div class="kpi-card kpi-ret">
        <div class="kpi-label">Order Return Rate</div>
        <div class="kpi-value" id="kpi-ret">7.00%</div>
        <div class="kpi-sub">Reverse logistics rate</div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-grid">
      <div class="card">
        <div class="card-header">
          <div class="card-title" id="chart-title">Monthly Sales & Net Profit (2023)</div>
        </div>
        <div class="chart-container">
          <canvas id="monthlyChart"></canvas>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title">Regional Revenue Distribution</div>
        </div>
        <div class="chart-container">
          <canvas id="regionalChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Tables Row -->
    <div class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title" id="table-title">Category Financial Contribution (2023)</div>
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
            </tr>
          </thead>
          <tbody id="category-table-body"></tbody>
        </table>
      </div>
    </div>

    <div class="footer-note">
      E-Commerce Sales, Customer & Profitability Analytics Project | Automated Interactive Dashboard
    </div>
  </div>

  <script>
    const dataset = {json_str};

    function formatINR(val) {{
      if (Math.abs(val) >= 10000000) {{
        return '&#8377; ' + (val / 10000000).toFixed(2) + ' Cr';
      }} else if (Math.abs(val) >= 100000) {{
        return '&#8377; ' + (val / 100000).toFixed(2) + ' L';
      }} else {{
        return '&#8377; ' + Number(val).toLocaleString('en-IN');
      }}
    }}

    let monthlyChartInstance = null;
    let regionalChartInstance = null;

    function renderCharts(yearKey) {{
      const data = dataset[yearKey];

      // Monthly Chart
      const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
      if (monthlyChartInstance) monthlyChartInstance.destroy();

      monthlyChartInstance = new Chart(ctxMonthly, {{
        type: 'bar',
        data: {{
          labels: data.monthly.labels,
          datasets: [
            {{
              label: 'Gross Sales (INR)',
              data: data.monthly.rev,
              backgroundColor: 'rgba(59, 130, 246, 0.8)',
              borderRadius: 6,
              yAxisID: 'y'
            }},
            {{
              label: 'Net Profit (INR)',
              data: data.monthly.prof,
              backgroundColor: 'rgba(16, 185, 129, 0.8)',
              borderRadius: 6,
              yAxisID: 'y'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#cbd5e1', font: {{ size: 12 }} }} }},
            tooltip: {{
              callbacks: {{
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

      // Regional Chart
      const ctxRegional = document.getElementById('regionalChart').getContext('2d');
      if (regionalChartInstance) regionalChartInstance.destroy();

      regionalChartInstance = new Chart(ctxRegional, {{
        type: 'doughnut',
        data: {{
          labels: data.regions.map(r => r.name),
          datasets: [{{
            data: data.regions.map(r => r.rev),
            backgroundColor: [
              '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'
            ],
            borderWidth: 2,
            borderColor: '#1e293b'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }},
            tooltip: {{
              callbacks: {{
                label: function(c) {{
                  const val = c.raw;
                  return c.label + ': ₹ ' + Number(val).toLocaleString('en-IN');
                }}
              }}
            }}
          }}
        }}
      }});
    }}

    function renderTable(categories) {{
      const tbody = document.getElementById('category-table-body');
      tbody.innerHTML = '';
      categories.forEach(cat => {{
        const tag = cat.margin >= 40 ? 'High Margin' : (cat.margin >= 25 ? 'Core Driver' : 'Volume Driver');
        const badgeClass = cat.margin >= 40 ? 'badge-green' : 'badge-blue';
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-weight: 600;">${{cat.name}}</td>
          <td>${{cat.orders.toLocaleString('en-IN')}}</td>
          <td style="color: #60a5fa; font-weight: 600;">&#8377; ${{cat.rev.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="color: #34d399; font-weight: 600;">&#8377; ${{cat.prof.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
          <td style="font-weight: 600;">${{cat.margin.toFixed(1)}}%</td>
          <td><span class="badge ${{badgeClass}}">${{tag}}</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filterYear(year, btn) {{
      document.querySelectorAll('.btn-year').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const data = dataset[year];
      const yearLabel = year === 'all' ? 'All Operating Years (2022-2024)' : year;

      // Update KPIs
      document.getElementById('kpi-rev').innerHTML = formatINR(data.rev);
      document.getElementById('kpi-rev-sub').innerHTML = '&#8377; ' + data.rev.toLocaleString('en-IN');
      document.getElementById('kpi-prof').innerHTML = formatINR(data.prof);
      document.getElementById('kpi-prof-sub').innerHTML = '&#8377; ' + data.prof.toLocaleString('en-IN');
      document.getElementById('kpi-margin').innerHTML = data.margin.toFixed(2) + '%';
      document.getElementById('kpi-orders').innerHTML = data.orders.toLocaleString('en-IN');
      document.getElementById('kpi-cust').innerHTML = data.cust.toLocaleString('en-IN') + ' Active Customers';
      document.getElementById('kpi-aov').innerHTML = '&#8377; ' + data.aov.toLocaleString('en-IN', {{minimumFractionDigits: 2}});
      document.getElementById('kpi-ret').innerHTML = data.ret_rate.toFixed(2) + '%';

      // Update titles
      document.getElementById('chart-title').innerHTML = `Monthly Sales & Net Profit (${{yearLabel}})`;
      document.getElementById('table-title').innerHTML = `Category Financial Contribution (${{yearLabel}})`;

      renderCharts(year);
      renderTable(data.categories);
    }}

    // Initialize with 2023 by default as requested
    window.onload = function() {{
      filterYear('2023', document.querySelector('.btn-year.active'));
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

print("Successfully generated index.html and dashboard/index.html!")
