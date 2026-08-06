# Business Growth Analytics Suite - End-User Manual

Welcome to the **Business Growth Analytics Suite**. This user manual guides business executives, regional managers, and data analysts through navigating the web platform.

---

## 1. System Access & Signing In

1. Open your browser and navigate to `http://localhost:8000/`.
2. Click **Sign In / Token** in the top right header.
3. Select your role credentials:
   - **Admin**: `admin@growthsuite.com` / `admin123` (Full system access)
   - **Manager**: `manager@growthsuite.com` / `manager123` (Upload CSV datasets & run ML)
   - **Analyst**: `analyst@growthsuite.com` / `analyst123` (Analytics & custom SQL console)

---

## 2. Navigating Platform Views

### 📊 1. Executive Overview Tab
- **KPI Cards**: View Total Sales Revenue, Net Profit, Profit Margin %, Total Orders, and Average Order Value.
- **Interactive Revenue Chart**: Displays 24-month revenue and net profit trends. Hover over data points to inspect monthly figures.

### 📈 2. Sales Analytics Tab
- **State Leaderboard**: Sort state sales from highest revenue to lowest.
- **Top 10 City Chart**: Inspect top revenue-generating urban centers.

### 👥 3. Customer Analytics Tab
- **Customer Retention Rate**: View repeat vs. single buyer ratios.
- **Top CLV Table**: Review the top 10 highest spending customer accounts.

### 🤖 4. ML Forecast & Predictions Tab
- **Time-Series Sales Forecaster**: Select **Next 3 Months**, **Next 6 Months**, or **Next 12 Months** to view AI-projected revenue numbers.
- **Customer Churn Risk Calculator**: Type a Customer ID (e.g. `CUST-10001`) to calculate churn risk probability % and risk tier.

### 📁 5. Dataset Manager Tab
- **Upload Raw CSV**: Drag and drop a new enterprise sales CSV file.
- **Run Data Cleaning**: Click **Run Cleaning Pipeline** to standardize text, convert dates, and clean data automatically.

### ⚡ 6. SQL Query Console Tab
- Type custom SQL SELECT queries into the editor and click **Execute SQL Query** to view results in a responsive data table.

### 📑 7. Power BI & Reports Tab
- Download cleaned CSV datasets or open full Markdown executive reports in a new browser tab.
