# Enterprise System Architecture & High-Level Design

**System Name**: Business Growth Analytics Suite  
**Architectural Style**: Modular Full-Stack Analytics Platform (Microservices / Layered Architecture)

---

## 1. High-Level System Architecture Diagram

```text
[ Data Layer ]            [ Data Engineering & ETL ]        [ Core Warehousing ]
+-------------------+      +--------------------------+     +-----------------------+
| 100K CSV Dataset  |=====>| scripts/data_cleaning.py |====>| BusinessGrowthDB      |
| (sales_data.csv)  |      | (Pandas / Data Validation)|     | (SQLite 3NF Schema)   |
+-------------------+      +--------------------------+     +-----------------------+
                                                                        |
                                                                        v
[ Machine Learning Engine ] <-------------------------------------------+
+---------------------------+
| ml/sales_forecasting.py   | (Linear Regression / Random Forest)
| ml/churn_prediction.py    | (Random Forest Classifier)
| ml/customer_segmentation.py| (K-Means Clustering)
| ml/product_recommendation.py| (Cosine Similarity Engine)
+---------------------------+
             |
             v (Serialized .joblib artifacts)
[ FastAPI REST Service Layer ]
+-------------------------------------------------------------------------------+
| backend/main.py (FastAPI / Uvicorn / CORS / Security Middleware / Swagger UI)  |
| - Authentication & RBAC (Admin, Manager, Analyst)                             |
| - REST Endpoints: /api/analytics/*, /api/ml/*, /api/dataset/*, /api/auth/*     |
+-------------------------------------------------------------------------------+
             ^
             | HTTP / REST (JWT Bearer Token)
             v
[ User Presentation Layer ]
+-------------------------------------------------------------------------------+
| frontend/ (Enterprise Glassmorphism SPA / React / Chart.js)                    |
| Power BI Desktop Dashboards (5 Executive Pages / DAX Measures Library)        |
+-------------------------------------------------------------------------------+
```

---

## 2. Component Design & Responsibility Matrix

| Layer / Component | File / Path | Responsibility |
| :--- | :--- | :--- |
| **Configuration** | `config.py` | Centralized paths, environment variables, random seeds, and global directory verifiers. |
| **Data Generation** | `scripts/generate_dataset.py` | Synthetic generation of 100,000 enterprise transactions with high logical and mathematical realism. |
| **Data Cleaning** | `scripts/data_cleaning.py` | Automated text standardization, missing value handling, date parsing, and math formula verification (`Sales = Qty * Price * (1 - Disc)`). |
| **Relational Storage** | `sql/create_tables.sql`, `indexes.sql`, `views.sql` | 3NF normalized schema with 5 tables, 7 performance B-Tree indexes, and 5 executive reporting views. |
| **Analytics Engine** | `sql/analytics_queries.sql` | 50 real business SQL queries covering basic aggregations, CTEs, Window functions (`RANK`, `DENSE_RANK`, `ROW_NUMBER`, Running Totals, Moving Averages), and executive KPIs. |
| **Machine Learning** | `ml/` & `ml/models/*.joblib` | 5 ML modules for sales forecasting (3, 6, 12 months), customer churn probability, K-Means customer segmentation, and product recommendation cross-selling. |
| **Power BI Assets** | `dashboard/` | 25+ DAX measures library (`dax_measures.dax`), Star Schema layout, and custom corporate theme JSON. |
| **REST Server** | `backend/main.py`, `auth.py`, `routers/` | FastAPI REST API backend with JWT Access/Refresh tokens, RBAC roles (`Admin`, `Manager`, `Analyst`), security headers, `/health`, `/metrics`, and OpenAPI docs. |
| **User Interface** | `frontend/` | Fortune-500 Enterprise Glassmorphism SPA with live Chart.js charts, interactive ML tools, drag-and-drop CSV uploader, and live SQL execution console. |

---

## 3. Data Flow Pipeline

1. **Ingestion & Validation**: Raw CSV datasets (`data/sales_data.csv`) are validated and cleaned via `data_cleaning.py`.
2. **Relational ETL**: Cleaned data is ingested into `BusinessGrowthDB.sqlite` across 5 normalized tables (`Customers`, `Products`, `Orders`, `Sales`, `Payments`).
3. **ML Training & Persistence**: Predictive models read cleaned tables, fit Scikit-Learn algorithms, and serialize model state to `ml/models/*.joblib`.
4. **API Serving & RBAC**: FastAPI REST endpoints load serialized models into memory to serve low-latency JSON predictions to authenticated users.
5. **Interactive UI**: The single-page web app dynamically updates visual components based on user role and query inputs.
