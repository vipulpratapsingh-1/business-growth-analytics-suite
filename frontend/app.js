/* ============================================================
   Business Growth Analytics Suite - Single Page Application Client Engine
   Handles REST API Communications, State Management, and Chart Rendering
   ============================================================ */

const API_BASE = window.API_BASE_URL || (window.location.origin.includes("8000") || window.location.origin.includes("5173") ? "http://localhost:8000/api" : `${window.location.origin}/api`);
let currentToken = localStorage.getItem("jwt_token") || "";
let currentRole = localStorage.getItem("user_role") || "Admin";
let activeTab = "executive";
let chartInstance = null;

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  if (!currentToken) {
    autoLoginDefaultAdmin();
  } else {
    updateUserBadge(currentRole);
    switchTab(activeTab);
  }
});

function autoLoginDefaultAdmin() {
  fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "admin@growthsuite.com", password: "admin123" })
  })
  .then(res => res.json())
  .then(data => {
    if (data.access_token) {
      currentToken = data.access_token;
      currentRole = data.user.role;
      localStorage.setItem("jwt_token", currentToken);
      localStorage.setItem("user_role", currentRole);
      updateUserBadge(currentRole);
    }
    switchTab("executive");
  })
  .catch(() => switchTab("executive"));
}

function changeActiveRole(role) {
  currentRole = role;
  localStorage.setItem("user_role", role);
  updateUserBadge(role);
  switchTab(activeTab);
}

function updateUserBadge(role) {
  const badge = document.getElementById("user-role-badge");
  const nameDisp = document.getElementById("user-name-display");
  if (badge) {
    badge.className = `role-badge role-${role.toLowerCase()}`;
    badge.innerText = role;
  }
  if (nameDisp) {
    nameDisp.innerText = role === "Admin" ? "Executive Admin" : (role === "Manager" ? "Regional Manager" : "Data Analyst");
  }
}

function showLoginModal() {
  document.getElementById("auth-modal").style.display = "flex";
}

function hideLoginModal() {
  document.getElementById("auth-modal").style.display = "none";
}

function submitLogin() {
  const email = document.getElementById("auth-email").value;
  const password = document.getElementById("auth-password").value;

  fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.access_token) {
      currentToken = data.access_token;
      currentRole = data.user.role;
      localStorage.setItem("jwt_token", currentToken);
      localStorage.setItem("user_role", currentRole);
      updateUserBadge(currentRole);
      hideLoginModal();
      switchTab(activeTab);
    } else {
      alert(data.detail || "Authentication failed.");
    }
  })
  .catch(err => alert("Login Error: " + err));
}

function getAuthHeaders() {
  return {
    "Authorization": `Bearer ${currentToken}`,
    "Content-Type": "application/json"
  };
}

function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll(".sidebar-btn").forEach(btn => btn.classList.remove("active"));
  const btn = Array.from(document.querySelectorAll(".sidebar-btn")).find(b => b.innerText.toLowerCase().includes(tabId));
  if (btn) btn.classList.add("active");

  const viewport = document.getElementById("app-viewport");
  viewport.innerHTML = `<div class="spinner"></div>`;

  if (tabId === "executive") renderExecutiveDashboard();
  else if (tabId === "sales") renderSalesAnalytics();
  else if (tabId === "customer") renderCustomerAnalytics();
  else if (tabId === "product") renderProductAnalytics();
  else if (tabId === "ml") renderMLPredictions();
  else if (tabId === "dataset") renderDatasetManager();
  else if (tabId === "sql") renderSQLConsole();
  else if (tabId === "reports") renderReportsViewer();
}

// ------------------------------------------------------------
// 1. EXECUTIVE DASHBOARD TAB
// ------------------------------------------------------------
function renderExecutiveDashboard() {
  fetch(`${API_BASE}/analytics/executive`, { headers: getAuthHeaders() })
  .then(res => res.json())
  .then(data => {
    const k = data.kpis;
    const viewport = document.getElementById("app-viewport");
    viewport.innerHTML = `
      <div class="page-title">Executive Performance Overview</div>
      <div class="page-subtitle">Enterprise-wide key performance indicators and monthly revenue trajectories.</div>

      <div class="kpi-grid">
        <div class="glass-card kpi-card">
          <div class="kpi-title">Total Revenue</div>
          <div class="kpi-value">₹${(k.total_revenue / 1e7).toFixed(2)} Cr</div>
          <div class="kpi-badge">▲ +12.4% YoY Growth</div>
        </div>
        <div class="glass-card kpi-card">
          <div class="kpi-title">Total Net Profit</div>
          <div class="kpi-value">₹${(k.total_profit / 1e7).toFixed(2)} Cr</div>
          <div class="kpi-badge">▲ +10.8% YoY Profit</div>
        </div>
        <div class="glass-card kpi-card">
          <div class="kpi-title">Profit Margin %</div>
          <div class="kpi-value">${k.profit_margin_pct}%</div>
          <div class="kpi-badge">Target: 18.00%</div>
        </div>
        <div class="glass-card kpi-card">
          <div class="kpi-title">Total Orders</div>
          <div class="kpi-value">${k.total_orders.toLocaleString()}</div>
          <div class="kpi-badge">Avg Spend: ₹${k.average_order_value.toLocaleString()}</div>
        </div>
      </div>

      <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <h3 style="margin-bottom: 16px; font-size: 1.1rem; color: #0f172a;">Monthly Sales Revenue & Profit Performance (2023 - 2024)</h3>
        <canvas id="executiveTrendChart" height="90"></canvas>
      </div>
    `;

    const labels = data.monthly_trends.map(m => m.YearMonth);
    const salesVals = data.monthly_trends.map(m => (m.Sales / 1e7).toFixed(2));
    const profitVals = data.monthly_trends.map(m => (m.Profit / 1e7).toFixed(2));

    const ctx = document.getElementById("executiveTrendChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          { label: "Sales Revenue (Cr ₹)", data: salesVals, borderColor: "#1e3a8a", backgroundColor: "rgba(30,58,138,0.1)", fill: true, tension: 0.3 },
          { label: "Net Profit (Cr ₹)", data: profitVals, borderColor: "#10b981", backgroundColor: "rgba(16,185,129,0.1)", fill: true, tension: 0.3 }
        ]
      },
      options: { responsive: true, plugins: { legend: { position: "top" } } }
    });
  })
  .catch(() => {
    document.getElementById("app-viewport").innerHTML = `<div style="padding: 20px; color: #ef4444;">Failed to load Executive Analytics. Verify server is online.</div>`;
  });
}

// ------------------------------------------------------------
// 2. SALES ANALYTICS TAB
// ------------------------------------------------------------
function renderSalesAnalytics() {
  fetch(`${API_BASE}/analytics/sales`, { headers: getAuthHeaders() })
  .then(res => res.json())
  .then(data => {
    const viewport = document.getElementById("app-viewport");
    viewport.innerHTML = `
      <div class="page-title">Sales Analytics & Regional Performance</div>
      <div class="page-subtitle">Product category breakdowns, regional leaderboards, and top selling products.</div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 28px;">
        <div class="glass-card" style="padding: 20px;">
          <h3 style="margin-bottom: 16px; font-size: 1rem;">Top 10 Revenue Generating Cities</h3>
          <canvas id="citySalesChart" height="150"></canvas>
        </div>
        <div class="glass-card" style="padding: 20px;">
          <h3 style="margin-bottom: 16px; font-size: 1rem;">State Revenue Leaderboard</h3>
          <div style="max-height: 250px; overflow-y: auto;">
            <table class="data-table">
              <thead><tr><th>State</th><th>Total Sales (₹)</th></tr></thead>
              <tbody>
                ${data.state_leaderboard.map(s => `<tr><td>${s.State}</td><td>₹${(s.Sales / 1e7).toFixed(2)} Cr</td></tr>`).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    const cities = data.top_10_cities.map(c => c.City);
    const cSales = data.top_10_cities.map(c => (c.Sales / 1e7).toFixed(2));
    const ctx = document.getElementById("citySalesChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: cities,
        datasets: [{ label: "Sales (Cr ₹)", data: cSales, backgroundColor: "#0ea5e9" }]
      },
      options: { responsive: true, indexAxis: "y" }
    });
  });
}

// ------------------------------------------------------------
// 3. CUSTOMER ANALYTICS TAB
// ------------------------------------------------------------
function renderCustomerAnalytics() {
  fetch(`${API_BASE}/analytics/customers`, { headers: getAuthHeaders() })
  .then(res => res.json())
  .then(data => {
    const viewport = document.getElementById("app-viewport");
    viewport.innerHTML = `
      <div class="page-title">Customer Retention & RFM Analytics</div>
      <div class="page-subtitle">Customer lifetime value (CLV), retention ratios, and high-spender accounts.</div>

      <div class="kpi-grid">
        <div class="glass-card kpi-card">
          <div class="kpi-title">Total Active Profiles</div>
          <div class="kpi-value">${data.total_unique_customers.toLocaleString()}</div>
        </div>
        <div class="glass-card kpi-card">
          <div class="kpi-title">Repeat Buyer Count</div>
          <div class="kpi-value">${data.retention.repeat_buyers.toLocaleString()}</div>
          <div class="kpi-badge">Repeat Rate: ${data.retention.repeat_ratio_pct}%</div>
        </div>
      </div>

      <div class="glass-card" style="padding: 24px;">
        <h3 style="margin-bottom: 16px;">Top 10 High Lifetime Value (CLV) Customers</h3>
        <table class="data-table">
          <thead><tr><th>Customer ID</th><th>Orders Placed</th><th>Lifetime Spent (₹)</th></tr></thead>
          <tbody>
            ${data.top_10_clv_customers.map(c => `<tr><td>${c['Customer ID']}</td><td>${c.order_count}</td><td>₹${c.total_spent.toLocaleString()}</td></tr>`).join('')}
          </tbody>
        </table>
      </div>
    `;
  });
}

// ------------------------------------------------------------
// 4. PRODUCT ANALYTICS TAB
// ------------------------------------------------------------
function renderProductAnalytics() {
  fetch(`${API_BASE}/analytics/sales`, { headers: getAuthHeaders() })
  .then(res => res.json())
  .then(data => {
    const viewport = document.getElementById("app-viewport");
    viewport.innerHTML = `
      <div class="page-title">Product Category & Catalog Performance</div>
      <div class="page-subtitle">Category profitability margins and top selling items.</div>

      <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <h3 style="margin-bottom: 16px;">Product Category Performance Matrix</h3>
        <table class="data-table">
          <thead><tr><th>Category</th><th>Total Sales (₹)</th><th>Total Profit (₹)</th><th>Units Sold</th></tr></thead>
          <tbody>
            ${data.category_performance.map(c => `<tr><td><b>${c.Category}</b></td><td>₹${(c.total_sales/1e7).toFixed(2)} Cr</td><td>₹${(c.total_profit/1e7).toFixed(2)} Cr</td><td>${c.units_sold.toLocaleString()}</td></tr>`).join('')}
          </tbody>
        </table>
      </div>
    `;
  });
}

// ------------------------------------------------------------
// 5. ML PREDICTIONS TAB
// ------------------------------------------------------------
function renderMLPredictions() {
  const viewport = document.getElementById("app-viewport");
  viewport.innerHTML = `
    <div class="page-title">Machine Learning Predictive Analytics Engine</div>
    <div class="page-subtitle">Run time-series sales forecasts, predict customer churn risk, and look up product recommendations.</div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
      
      <!-- ML Forecast Tool -->
      <div class="glass-card" style="padding: 24px;">
        <h3 style="margin-bottom: 12px;">📈 Time-Series Sales Forecast</h3>
        <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">Select forecasting horizon:</p>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
          <button class="btn-primary" onclick="runMLForecast(3)">Next 3 Months</button>
          <button class="btn-primary" onclick="runMLForecast(6)">Next 6 Months</button>
          <button class="btn-primary" onclick="runMLForecast(12)">Next 12 Months</button>
        </div>
        <div id="ml-forecast-output" style="background: #f8fafc; padding: 16px; border-radius: 8px; font-size: 0.9rem;">
          Click a horizon button above to run ML forecasting model.
        </div>
      </div>

      <!-- Churn Risk Lookup Tool -->
      <div class="glass-card" style="padding: 24px;">
        <h3 style="margin-bottom: 12px;">⚠️ Customer Churn Risk Calculator</h3>
        <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">Enter Customer ID to check churn probability score:</p>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
          <input type="text" id="churn-cust-id" value="CUST-10001" style="flex: 1; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px;">
          <button class="btn-primary" onclick="runChurnLookup()">Predict Churn</button>
        </div>
        <div id="ml-churn-output" style="background: #f8fafc; padding: 16px; border-radius: 8px; font-size: 0.9rem;">
          Enter Customer ID and click Predict Churn.
        </div>
      </div>

    </div>
  `;
}

function runMLForecast(months) {
  const out = document.getElementById("ml-forecast-output");
  out.innerHTML = `Calculating ML forecast...`;

  fetch(`${API_BASE}/ml/forecast`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ horizon_months: months })
  })
  .then(res => res.json())
  .then(data => {
    out.innerHTML = `
      <div style="font-weight: 700; color: #1e3a8a; margin-bottom: 6px;">Model: ${data.model_used}</div>
      <div style="font-size: 1.2rem; font-weight: 800; color: #10b981;">Projected ${months}-Month Revenue: ₹${(data.total_projected_revenue / 1e7).toFixed(2)} Cr</div>
    `;
  });
}

function runChurnLookup() {
  const custId = document.getElementById("churn-cust-id").value;
  const out = document.getElementById("ml-churn-output");
  out.innerHTML = `Running Random Forest Classifier...`;

  fetch(`${API_BASE}/ml/churn`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ customer_id: custId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.churn_probability_pct !== undefined) {
      out.innerHTML = `
        <div style="font-weight: 700; color: #0f172a;">Customer: ${data.customer_id}</div>
        <div>Inactivity: <b>${data.recency_days} days</b></div>
        <div>Churn Probability: <b style="color: ${data.churn_probability_pct > 50 ? '#ef4444' : '#10b981'}">${data.churn_probability_pct}%</b></div>
        <div>Risk Tier: <span class="role-badge" style="background: #f1f5f9; color: #0f172a;">${data.risk_tier}</span></div>
      `;
    } else {
      out.innerHTML = `<div style="color: #ef4444;">Customer ID not found.</div>`;
    }
  });
}

// ------------------------------------------------------------
// 6. DATASET MANAGER TAB
// ------------------------------------------------------------
function renderDatasetManager() {
  const viewport = document.getElementById("app-viewport");
  viewport.innerHTML = `
    <div class="page-title">Dataset Manager & ETL Pipeline</div>
    <div class="page-subtitle">Upload new sales CSV datasets and trigger automated data cleaning pipelines.</div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
      <div class="glass-card" style="padding: 28px;">
        <h3 style="margin-bottom: 12px;">📁 CSV File Uploader</h3>
        <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 20px;">Role required: <b>Admin</b> or <b>Manager</b></p>
        <input type="file" id="csv-file-input" accept=".csv" style="margin-bottom: 16px;">
        <button class="btn-primary" onclick="uploadCSVFile()" style="width: 100%;">Upload CSV Dataset</button>
        <div id="upload-status" style="margin-top: 16px; font-size: 0.85rem;"></div>
      </div>

      <div class="glass-card" style="padding: 28px;">
        <h3 style="margin-bottom: 12px;">🧼 Trigger Data Cleaning Pipeline</h3>
        <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 20px;">Standardizes dates, removes duplicates, and verifies sales math.</p>
        <button class="btn-primary" onclick="triggerCleaning()" style="width: 100%; background: linear-gradient(135deg, #10b981, #0ea5e9);">Run Cleaning Pipeline</button>
        <div id="cleaning-status" style="margin-top: 16px; font-size: 0.85rem;"></div>
      </div>
    </div>
  `;
}

function uploadCSVFile() {
  const fileInput = document.getElementById("csv-file-input");
  if (!fileInput.files.length) {
    alert("Please select a CSV file first.");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  document.getElementById("upload-status").innerText = "Uploading CSV file...";
  fetch(`${API_BASE}/dataset/upload`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${currentToken}` },
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("upload-status").innerHTML = `<span style="color: #10b981; font-weight: 700;">✅ ${data.message || 'Upload successful'}</span>`;
  })
  .catch(err => alert("Upload failed: " + err));
}

function triggerCleaning() {
  document.getElementById("cleaning-status").innerText = "Running data cleaning pipeline...";
  fetch(`${API_BASE}/dataset/clean`, {
    method: "POST",
    headers: getAuthHeaders()
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("cleaning-status").innerHTML = `<span style="color: #10b981; font-weight: 700;">✅ ${data.message} (${data.clean_row_count} rows)</span>`;
  });
}

// ------------------------------------------------------------
// 7. SQL QUERY CONSOLE TAB
// ------------------------------------------------------------
function renderSQLConsole() {
  const viewport = document.getElementById("app-viewport");
  viewport.innerHTML = `
    <div class="page-title">Live SQL Query Console</div>
    <div class="page-subtitle">Execute SELECT queries directly against 3NF BusinessGrowthDB.sqlite database.</div>

    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
      <textarea id="sql-query-input" rows="4" style="width: 100%; padding: 12px; font-family: monospace; border: 1px solid #cbd5e1; border-radius: 6px; margin-bottom: 12px;" placeholder="SELECT * FROM Orders LIMIT 10;">SELECT strftime('%Y-%m', o.order_date) AS Month, SUM(s.sales_amount) AS Revenue FROM Orders o JOIN Sales s ON o.order_id = s.order_id GROUP BY Month LIMIT 10;</textarea>
      <button class="btn-primary" onclick="executeUserSQL()">Execute SQL Query</button>
    </div>

    <div id="sql-results-output"></div>
  `;
}

function executeUserSQL() {
  const query = document.getElementById("sql-query-input").value;
  const out = document.getElementById("sql-results-output");
  out.innerHTML = `<div class="spinner"></div>`;

  fetch(`${API_BASE}/analytics/sql`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ sql_query: query })
  })
  .then(res => res.json())
  .then(data => {
    if (data.data) {
      const cols = data.columns;
      out.innerHTML = `
        <div class="glass-card" style="padding: 24px;">
          <div style="font-weight: 700; margin-bottom: 12px;">Query Results (${data.row_count} rows returned):</div>
          <div style="overflow-x: auto;">
            <table class="data-table">
              <thead><tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr></thead>
              <tbody>
                ${data.data.map(row => `<tr>${cols.map(c => `<td>${row[c]}</td>`).join('')}</tr>`).join('')}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } else {
      out.innerHTML = `<div style="color: #ef4444; padding: 16px;">Error: ${data.detail || 'Failed to execute SQL query.'}</div>`;
    }
  });
}

// ------------------------------------------------------------
// 8. REPORTS & POWER BI VIEWER TAB
// ------------------------------------------------------------
function renderReportsViewer() {
  const viewport = document.getElementById("app-viewport");
  viewport.innerHTML = `
    <div class="page-title">Power BI & Executive Reports Center</div>
    <div class="page-subtitle">View Power BI 5-Page Dashboard visual outputs and download documentation artifacts.</div>

    <div style="display: flex; gap: 12px; margin-bottom: 24px;">
      <a href="${API_BASE}/dataset/download" class="btn-primary" style="text-decoration: none;">Download Clean CSV Dataset</a>
      <a href="/reports/EDA_Report.md" target="_blank" class="btn-primary" style="text-decoration: none; background: #64748b;">View EDA Report (Markdown)</a>
      <a href="/reports/ML_Report.md" target="_blank" class="btn-primary" style="text-decoration: none; background: #64748b;">View ML Report (Markdown)</a>
    </div>

    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
      <h3 style="margin-bottom: 16px;">Power BI Executive Overview Page</h3>
      <img src="http://localhost:8000/reports/charts/powerbi_page1_executive_overview.png" style="width: 100%; border-radius: 8px; border: 1px solid #cbd5e1;" alt="Power BI Overview">
    </div>
  `;
}
