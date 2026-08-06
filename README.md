# Business Growth Analytics Suite

An enterprise-grade data analytics, machine learning, and full-stack web platform designed to analyze multi-region sales performance, customer purchasing behavior, product category profitability, revenue growth metrics, and predictive business intelligence.

This repository is structured following industry-standard data analytics & software engineering practices, tailored for hands-on learning, interview preparation, and professional portfolio building.

---

## 🚀 DevOps & Production Deployment Readiness

- 💻 **Backend REST API Framework**: FastAPI + Uvicorn
- 🗄️ **Database Engine**: SQLite (3NF) with PostgreSQL connection string abstraction
- 🤖 **Machine Learning**: 4 Serialized Scikit-Learn `.joblib` models
- 🎨 **Frontend**: Enterprise Glassmorphism React SPA
- 🧪 **Testing Suite**: 17 Pytest automated test cases (**100% Pass Rate**)
- 📦 **DevOps Infrastructure**: Dockerfile, docker-compose.yml, vercel.json, render.yaml, GitHub Actions CI/CD

---

## 📁 Folder Structure

```text
business-growth-analytics-suite/
│
├── .github/               # GitHub Actions CI/CD Workflows
│   └── workflows/
│       └── ci.yml         # Automated testing, linting, and Docker build pipeline
│
├── backend/               # FastAPI REST Backend Server
│   ├── main.py            # FastAPI server entry point, static router, & security headers
│   ├── auth.py            # JWT Access/Refresh tokens & Role-Based Access Control (RBAC)
│   └── routers/           # Modular REST API endpoints
│       ├── analytics.py   # Analytics, KPIs, and custom SQL execution (SQLite/PostgreSQL)
│       ├── ml_router.py   # ML inference endpoints (Forecast, Churn, K-Means, Recommend)
│       └── dataset.py     # CSV uploader, cleaning pipeline, and CSV download endpoints
│
├── frontend/              # Enterprise Single Page React/JS Application
│   ├── index.html         # SPA HTML template
│   ├── index.css          # Glassmorphism enterprise design system styling
│   └── app.js             # Client SPA router, state management, and Chart.js integration
│
├── tests/                 # Pytest Automated Test Suite (17 Test Cases)
│   ├── test_unit.py       # Data cleaning, formula math, and configuration unit tests
│   ├── test_integration.py# SQLite ETL loading, table schema, and view integration tests
│   ├── test_api.py        # FastAPI REST API authentication, RBAC, and SQL endpoint tests
│   └── test_ml.py         # ML model artifact loading and inference tests
│
├── data/                  # Primary data storage (Raw, Cleaned & SQLite DB)
│   ├── sales_data.csv     # 100,000-row raw enterprise sales dataset
│   ├── clean_sales_data.csv # 100,000-row cleaned enterprise sales dataset
│   └── BusinessGrowthDB.sqlite # Production-ready normalized relational SQL database (3NF)
│
├── sql/                   # Analytical SQL scripts, queries, and schema definitions
│   ├── create_tables.sql  # DDL schema (5 normalized tables with PK/FK constraints)
│   ├── import_data.sql    # Data import & ETL insertion documentation
│   ├── indexes.sql        # B-Tree performance optimization indexes
│   ├── views.sql          # 5 executive reporting views for dashboards
│   └── analytics_queries.sql # 50 real business SQL queries (Basic -> Window Functions -> CTEs)
│
├── ml/                    # Machine Learning & Predictive Analytics Modules
│   ├── models/            # Serialized trained model artifacts (.joblib)
│   │   ├── sales_forecaster.joblib # Time-series sales forecasting model
│   │   ├── churn_model.joblib      # Customer churn classification model
│   │   ├── kmeans_model.joblib     # K-Means RFM customer segmentation model
│   │   └── recommender.joblib      # Cosine similarity product recommendation model
│   ├── sales_forecasting.py # Time-series regression forecaster (3, 6, 12 months)
│   ├── churn_prediction.py  # Random Forest customer churn classifier
│   ├── customer_segmentation.py # K-Means RFM customer clustering
│   ├── product_recommendation.py # Item-to-item co-occurrence recommender
│   └── business_recommender.py # Executive Business Recommendation Engine
│
├── scripts/               # Python utility, ETL, and master orchestrator scripts
│   ├── generate_dataset.py# Synthetic dataset generation engine
│   ├── data_cleaning.py   # Automated data cleaning & validation pipeline
│   ├── eda_analysis.py    # EDA engine & chart generator
│   ├── sql_integration.py # Database ETL builder & query benchmark runner
│   ├── run_ml_pipeline.py # Master Machine Learning orchestrator
│   └── deploy_production.py # Production deployment verification script
│
├── dashboard/             # Power BI Dashboard assets & DAX Measure Library
│   ├── dax_measures.dax   # Production DAX measures library (25+ business KPIs)
│   ├── powerbi_theme.json # Fortune-500 modern corporate color theme JSON
│   ├── powerbi_model_config.json # Star Schema data model & relationship layout
│   └── generate_powerbi_assets.py # Automation script to validate DAX & render 5 dashboard pages
│
├── reports/               # Executive summaries, exported charts, and reports
│   ├── charts/            # 11 static visualization charts & Power BI page previews (PNG)
│   ├── ml/                # 4 Machine Learning graph visual outputs (PNG)
│   ├── EDA_Report.md      # Comprehensive Executive EDA Markdown Report
│   └── ML_Report.md       # Comprehensive Executive ML & Business Intelligence Report
│
├── docs/                  # Enterprise Documentation Suite
│   ├── SYSTEM_ARCHITECTURE.md # System architecture & design diagrams
│   ├── API_DOCUMENTATION.md   # Complete REST API reference documentation
│   ├── DATABASE_DESIGN.md     # 3NF database schema, ER diagrams, and indexes
│   ├── ML_PIPELINE.md         # Machine Learning lifecycle documentation
│   ├── DEPLOYMENT_GUIDE.md    # Production Vercel & Render deployment guide
│   ├── USER_MANUAL.md         # End-user platform operational manual
│   ├── INTERVIEW_GUIDE.md     # B.Tech technical & HR interview Q&A guide
│   ├── PRESENTATION_DECK.md   # 10-slide PowerPoint presentation script
│   └── RESUME_DESCRIPTION.md  # ATS-friendly resume bullet points and descriptions
│
├── vercel.json            # Vercel deployment configuration file
├── render.yaml            # Render deployment manifest
├── Dockerfile             # Multi-stage production Docker container file
├── docker-compose.yml     # Multi-container orchestration file
├── .env.example           # Environment configuration template
├── config.py              # Centralized configuration (Paths, settings, constants)
├── main.py                # Primary execution entry point and verification script
├── requirements.txt       # Python dependency specifications
└── README.md              # Project documentation and setup guide
```

---

## 🚀 Local Quickstart & Verification

```bash
pip install -r requirements.txt
python scripts/deploy_production.py
pytest -v tests/
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Access local server at `http://localhost:8000/`.

---

## 📝 License
Distributed under the MIT License. Prepared for Data Analytics learning, interview preparation, and portfolio building.
