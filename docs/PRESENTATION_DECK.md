# Executive Presentation Deck - Business Growth Analytics Suite

**Slide Deck Structure for Project Presentation**

---

## 📌 Slide 1: Title & Executive Summary
- **Title**: Business Growth Analytics Suite
- **Subtitle**: Full-Stack Enterprise Analytics & Machine Learning Platform
- **Presenter**: B.Tech Data Analytics Engineering Candidate
- **Key Message**: Transforming 100,000 transaction records into executive decision intelligence.

---

## 📌 Slide 2: Problem Statement & Industry Relevance
- **Business Challenge**: Multi-region sales data is often siloed, unstructured, and noisy.
- **Goal**: Build a scalable analytics platform providing real-time executive visibility, automated data pipelines, predictive forecasting, and customer retention insights.

---

## 📌 Slide 3: System Architecture & Technology Stack
- **Languages & Frameworks**: Python 3.10, SQL, FastAPI, React, DAX
- **Database & Storage**: SQLite 3NF Relational Database (5 Tables, 7 Indexes, 5 Views)
- **Machine Learning**: Scikit-Learn (Linear Regression, Random Forest, K-Means, Cosine Similarity)
- **DevOps**: Docker, Pytest, GitHub Actions CI/CD

---

## 📌 Slide 4: Data Engineering & Cleaning Pipeline
- Automated cleaning script enforcing zero missing values.
- Mathematical integrity check: `Sales = Quantity * Unit_Price * (1 - Discount)`.
- 100,000 clean records exported to `data/clean_sales_data.csv`.

---

## 📌 Slide 5: SQL Analytics & Relational Warehousing
- 3NF Schema: `Customers`, `Products`, `Orders`, `Sales`, `Payments`.
- 50 Production Queries: Window Functions (`RANK`, `DENSE_RANK`, `ROW_NUMBER`), CTEs, Running Totals, and 3-Month Moving Averages.

---

## 📌 Slide 6: Power BI Executive Dashboards
- 5 Executive Pages: Overview, Sales Analytics, Customer RFM, Financial Margins, Interactive Slicers.
- 25+ DAX Measures: Total Revenue, YoY Growth %, CLV, AOV, Repeat Rate %.

---

## 📌 Slide 7: Machine Learning & Predictive BI
- **Sales Forecasting**: 3, 6, 12-month time-series revenue projections.
- **Churn Classifier**: Random Forest model predicting customer churn with 99.36% accuracy.
- **Customer Segmentation**: K-Means clustering discovering 4 buyer personas (Champions, At-Risk).
- **Recommendation Engine**: Cosine similarity product cross-selling.

---

## 📌 Slide 8: Enterprise Web Application & Security
- FastAPI REST backend with OAuth2 JWT Access & Refresh Tokens.
- Role-Based Access Control (`Admin`, `Manager`, `Analyst`).
- Modern Glassmorphism React UI with live Chart.js visualizations.

---

## 📌 Slide 9: Automated Testing & CI/CD Pipeline
- 17 Pytest automated test cases covering unit, integration, API, and ML logic.
- GitHub Actions CI/CD pipeline & multi-stage Docker containerization.

---

## 📌 Slide 10: Strategic Recommendations & Conclusion
- Cap maximum promotional discounts at 10% to protect margins.
- Focus commercial expansion in high-growth cities (`Indore`, `Mysuru`, `Jaipur`).
- Deploy win-back promotions for 1,713 at-risk customer accounts.
