# Mentor Interview Guide - Business Growth Analytics Suite

This interview guide prepares B.Tech students and beginners to present the **Business Growth Analytics Suite** in technical interviews, HR screening rounds, and portfolio discussions.

---

## 🎯 1. The 60-Second Elevator Pitch

> *"For my major analytics engineering project, I built an end-to-end enterprise platform called the **Business Growth Analytics Suite**. It processes a 100,000-row multi-region sales dataset across data ingestion, automated cleaning, 3NF relational warehousing in SQLite, 50 business SQL queries, 5 Power BI executive dashboard pages, and 5 Scikit-Learn Machine Learning modules for sales forecasting, customer churn classification, K-Means RFM clustering, and product recommendations. I deployed the entire system as a full-stack FastAPI REST web application with JWT authentication, Role-Based Access Control, Docker containerization, Pytest automated testing, and GitHub Actions CI/CD."*

---

## 💡 2. Technical Interview Questions & Model Answers

### Q1: How did you handle data cleaning and ensure data integrity?
**Model Answer**:  
*"I built an automated Python cleaning pipeline (`scripts/data_cleaning.py`) using Pandas. I verified zero null values, dropped exact duplicates, standardized date strings into datetime objects, normalized text columns using `.str.title()`, and performed mathematical validation to enforce `Sales = Quantity * Unit_Price * (1 - Discount)`. Records violating logical constraints were filtered into an invalid audit log."*

---

### Q2: Why did you choose a 3NF normalized database schema instead of keeping a flat file?
**Model Answer**:  
*"A flat 100,000-row CSV duplicates customer names, product titles, and order locations across thousands of rows, leading to update anomalies and excessive storage usage. By normalizing the data into Third Normal Form (3NF) across 5 tables (`Customers`, `Products`, `Orders`, `Sales`, `Payments`) with Foreign Key constraints, I eliminated data redundancy, enforced referential integrity, and improved query efficiency using 7 B-Tree indexes."*

---

### Q3: How did you design your SQL analytics queries?
**Model Answer**:  
*"I wrote 50 real-world business SQL queries (`sql/analytics_queries.sql`). They range from basic aggregations and multi-table INNER/LEFT JOINs to advanced analytical concepts like Common Table Expressions (CTEs) and Window Functions (`RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`, Running Totals, and 3-month Moving Averages) to calculate Customer Lifetime Value (CLV) and YoY growth rates."*

---

### Q4: How did you evaluate your Machine Learning models?
**Model Answer**:  
*"For **Sales Forecasting**, I compared Linear Regression against Random Forest Regressor using MAE, RMSE, and R² scores. For **Customer Churn Classification**, I engineered RFM metrics and trained a Random Forest Classifier evaluating Accuracy (99.36%), Precision, Recall, and ROC-AUC. For **Customer Segmentation**, I used K-Means clustering with standardized RFM features to discover 4 distinct customer personas like 'Champions' and 'At-Risk Buyers'."*

---

### Q5: How is security handled in your web application?
**Model Answer**:  
*"The REST backend is built using FastAPI. It uses OAuth2 signed JWT Access and Refresh Tokens (`/api/auth/refresh`), bcrypt password hashing, and Role-Based Access Control (`Admin`, `Manager`, `Analyst`) to restrict sensitive operations like CSV uploads and custom SQL execution. I also implemented security middleware adding XSS protection, X-Frame-Options, and Content-Type headers."*

---

## 📋 3. Key Resume Metrics to Highlight
- **100,000 Transactions**: Engineered end-to-end data pipeline processing 100,000 records.
- **50 SQL Queries**: Authored 50 production SQL queries utilizing CTEs and Window functions.
- **99.36% ML Accuracy**: Trained Random Forest Churn Classifier achieving 99.36% accuracy.
- **17 Automated Tests**: Built Pytest test suite covering unit, integration, API, and ML logic.
- **Full-Stack REST & UI**: Developed FastAPI backend with JWT RBAC security and React Glassmorphism UI.
