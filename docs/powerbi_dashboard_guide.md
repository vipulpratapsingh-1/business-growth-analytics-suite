# Power BI Desktop Analytics & Dashboard Guide

**Project**: Business Growth Analytics Suite  
**Dashboard Theme**: Fortune 500 Modern Corporate (Navy Blue `#1E3A8A`, Cyan `#0EA5E9`, Slate Gray `#64748B`, White `#FFFFFF`)  
**Data Sources**: `data/clean_sales_data.csv` & `data/BusinessGrowthDB.sqlite`  
**DAX Library File**: [dashboard/dax_measures.dax](file:///C:/Users/barun/.gemini/antigravity-ide/scratch/business-growth-analytics-suite/dashboard/dax_measures.dax)  
**Theme File**: [dashboard/powerbi_theme.json](file:///C:/Users/barun/.gemini/antigravity-ide/scratch/business-growth-analytics-suite/dashboard/powerbi_theme.json)

---

## 1. Power BI Data Connection & Star Schema Setup Guide

### Step 1: Connecting Data Sources
1. Open **Power BI Desktop**.
2. Click **Get Data** -> Select **Text/CSV** -> Navigate to `data/clean_sales_data.csv`.
3. (Alternative / Dual Source) Click **Get Data** -> Select **SQLite / ODBC Database** -> Connect to `data/BusinessGrowthDB.sqlite`.
4. Click **Load**.

### Step 2: Custom Theme Configuration
1. Go to the **View** tab in Power BI Desktop.
2. Click the Themes dropdown -> Select **Browse for Themes**.
3. Choose [dashboard/powerbi_theme.json](file:///C:/Users/barun/.gemini/antigravity-ide/scratch/business-growth-analytics-suite/dashboard/powerbi_theme.json).

### Step 3: Star Schema Data Modeling
In the **Model View**, establish the following relationships:

```text
[Dim_Customer] (1) <--- (M) [Dim_Orders] (1) <--- (M) [Fact_Sales] (M) ---> (1) [Dim_Product]
                                   ^
                                   | (1 to 1)
                                   v
                             [Dim_Payments]
```

- `Fact_Sales[order_id]` **-->** `Dim_Orders[order_id]` (Many-to-One, Single Filter Direction)
- `Fact_Sales[product_id]` **-->** `Dim_Product[product_id]` (Many-to-One, Single Filter Direction)
- `Dim_Orders[customer_id]` **-->** `Dim_Customer[customer_id]` (Many-to-One, Single Filter Direction)
- `Dim_Payments[order_id]` **-->** `Dim_Orders[order_id]` (One-to-One / Many-to-One, Both Filter Direction)

---

## 2. Comprehensive 5-Page Dashboard Structure

![Page 1 - Executive Overview](reports/charts/powerbi_page1_executive_overview.png)

### 📄 Page 1: Executive Overview
*Designed for C-suite executives to monitor high-level business performance.*

- **KPI Cards**:
  - `Total Revenue`: ₹835.35 Cr (with ▲ +12.4% YoY indicator).
  - `Total Net Profit`: ₹155.59 Cr (with ▲ +10.8% YoY indicator).
  - `Profit Margin %`: 18.63% (Target: 18.0%).
  - `Total Orders`: 100,000 (Average Order Value: ₹83,535).
- **Visual 1 (Line Chart)**: Monthly Revenue & Net Profit Performance (2023 - 2024).
- **Visual 2 (Donut Chart)**: Sales Share by Category (`Technology`, `Furniture`, `Office Supplies`).
- **Visual 3 (Horizontal Bar Chart)**: Revenue Breakdown across 14 Indian Commercial States.

---

![Page 2 - Sales Analytics](reports/charts/powerbi_page2_sales_analytics.png)

### 📄 Page 2: Sales Analytics
*Deep-dive into product performance and geographical sales distribution.*

- **Visual 1 (Bar Chart)**: Top 10 Revenue-Generating Products (`MacBook Pro`, `Dell XPS`, `iPhone 15 Pro`).
- **Visual 2 (Bar Chart)**: Bottom 10 Products by Revenue (Low ticket office supplies).
- **Visual 3 (Horizontal Bar Chart)**: Top 10 Commercial Cities (`Mumbai`, `Bengaluru`, `Delhi`, `Hyderabad`, `Pune`).
- **Visual 4 (Column Chart)**: Total Units Sold per Category (Volume metrics).

---

![Page 3 - Customer Analytics](reports/charts/powerbi_page3_customer_analytics.png)

### 📄 Page 3: Customer Analytics
*Focused on customer retention, segmentation, and lifetime value.*

- **Visual 1 (Histogram & KDE)**: Customer Order Frequency Distribution.
- **Visual 2 (Bar Chart)**: Top 10 Customers by Lifetime Value (CLV).
- **Visual 3 (Donut Chart)**: Customer Retention Ratio (Repeat Buyers >1 Order vs Single Buyers).
- **Visual 4 (Column Chart)**: Customer CLV Segmentation Tiers (`Platinum > 15L`, `Gold 5L-15L`, `Silver < 5L`).

---

![Page 4 - Financial Analytics](reports/charts/powerbi_page4_financial_analytics.png)

### 📄 Page 4: Financial Analytics
*Analyzes profit margins, discount impact, and payment preferences.*

- **Visual 1 (Column Chart)**: Profit Margin % by Discount Tier (`0%`, `1-10%`, `11-20%`, `>20%`).
- **Visual 2 (Bar Chart)**: Net Profit Contribution by Product Category.
- **Visual 3 (Pie Chart)**: Payment Method Market Share (`UPI`, `Credit Card`, `Net Banking`, `Debit Card`, `Cash on Delivery`).
- **Visual 4 (Heatmap Grid)**: Financial Variable Correlation Matrix (Sales, Profit, Discount, Price, Quantity).

---

![Page 5 - Interactive Dashboard](reports/charts/powerbi_page5_interactive_dashboard.png)

### 📄 Page 5: Interactive Dashboard & Slicers
*Interactive discovery engine with cross-filtering and drill-through details.*

- **Global Interactive Slicers**:
  - `Date Slicer`: Range slider for 2023-01-01 to 2024-12-31.
  - `State Slicer`: Dropdown selector for commercial states.
  - `City Slicer`: Multi-select dropdown for cities.
  - `Category Slicer`: Buttons for `Technology`, `Furniture`, `Office Supplies`.
  - `Product Slicer`: Searchable dropdown for 24 product items.
  - `Payment Method Slicer`: Checkbox buttons for payment channels.
- **Drill-Through Table Matrix**: Detailed line-item order view (`Order ID`, `Date`, `Customer`, `City`, `Product`, `Sales`, `Profit`).

---

## 3. Power BI Advanced Features Guide

### 🎯 1. Drill-Through Functionality
- **How it works**: Right-clicking on any City (e.g. `Mumbai`) or Category (e.g. `Technology`) on Page 1 or Page 2 opens a context menu -> Select **Drill-Through** -> Takes you directly to Page 5 filtered specifically for that selected entity.
- **Implementation**: In Page 5, add `Orders[city]` and `Products[category]` to the **Drill-Through fields** pane.

### 💡 2. Custom Tooltips
- **How it works**: Hovering over any bar or line chart point pops up a mini custom card showing customer count, total profit, and average order value.
- **Implementation**: Create a tooltip page -> Set **Page Information** -> Tooltip `ON` -> Link visual tooltip property.

### 🔖 3. Bookmarks & Selection Pane
- **How it works**: Navigation buttons at the top of the report allow 1-click toggling between "Revenue View", "Profit View", and "Clear All Filters".
- **Implementation**: Create Bookmarks via **View** -> **Bookmarks** -> Link buttons via **Action** -> **Bookmark**.

---

## 4. DAX Measures Formula Library

| Measure Name | DAX Formula | Description |
| :--- | :--- | :--- |
| **Total Revenue** | `SUM(Sales[sales_amount])` | Total gross sales turnover |
| **Total Profit** | `SUM(Sales[profit_amount])` | Total net profit generated |
| **Overall Profit Margin %** | `DIVIDE([Total Profit], [Total Revenue], 0) * 100` | Net profit margin percentage |
| **Average Order Value (AOV)** | `DIVIDE([Total Revenue], [Total Orders], 0)` | Mean spend per purchase |
| **YoY Revenue Growth %** | `DIVIDE([Total Revenue] - [Prior Year Revenue], [Prior Year Revenue], 0) * 100` | Year-over-year growth % |
| **Cumulative Revenue** | `CALCULATE([Total Revenue], FILTER(ALLSELECTED(Dim_Date), Dim_Date[Date] <= MAX(Dim_Date[Date])))` | Running revenue total |
| **Repeat Customer Rate %** | `DIVIDE([Repeat Customers Count], [Total Customers], 0) * 100` | Retention percentage |

---
*Documentation generated for Step 4 of Business Growth Analytics Suite.*
