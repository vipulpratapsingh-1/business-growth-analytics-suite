# Machine Learning Pipeline & Predictive Analytics Lifecycle

This document describes the 5 Machine Learning modules in **Business Growth Analytics Suite**, detailing model selection, feature engineering, evaluation metrics, and model persistence.

---

## 1. Machine Learning Architecture Overview

```text
[ Cleaned Dataset ] ---> [ Feature Engineering & Scaling ] ---> [ Model Training ] ---> [ Serialized Models ]
 data/clean_sales_data.csv   - Temporal Lags (Lag1, Lag2)        - Linear Regression       ml/models/sales_forecaster.joblib
                             - Customer RFM Metrics              - Random Forest           ml/models/churn_model.joblib
                             - Standardized Scaling              - K-Means Clustering      ml/models/kmeans_model.joblib
                             - Item Cosine Similarity            - Cosine Similarity       ml/models/recommender.joblib
```

---

## 2. Machine Learning Modules Detailed

### 📈 Module A: Time-Series Sales Forecasting
- **Script**: `ml/sales_forecasting.py`
- **Algorithms**: Linear Regression vs. Random Forest Regressor
- **Features**: Month Index, Lag 1 Sales, Lag 2 Sales
- **Horizon**: Forecasts 3, 6, and 12 months into the future
- **Evaluation**: 
  - MAE (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)
  - R² (R-Squared Score)
- **Artifact**: `ml/models/sales_forecaster.joblib`

### ⚠️ Module B: Customer Churn Classification
- **Script**: `ml/churn_prediction.py`
- **Algorithm**: Random Forest Classifier (150 estimators, max depth 8)
- **Target Label**: Inactivity > 180 days (`1` = Churned, `0` = Retained)
- **Features**: Recency Days, Frequency, Monetary Value, Total Profit, Avg Order Value, Avg Discount, Tenure Days
- **Evaluation**: Accuracy (99.36%), Precision, Recall, F1-Score, ROC-AUC Score (0.7363)
- **Artifact**: `ml/models/churn_model.joblib`

### 👥 Module C: K-Means Customer Segmentation
- **Script**: `ml/customer_segmentation.py`
- **Algorithm**: K-Means Clustering ($K=4$) with `StandardScaler`
- **Features**: Recency, Frequency, Log-Transformed Monetary Value
- **Business Personas**:
  - `Champions (VIP Spenders)`: High spend, high purchase frequency.
  - `Loyal Regular Buyers`: Frequent orders, moderate ticket sizes.
  - `Promising / Recent Buyers`: Low recency days, high potential.
  - `At-Risk / Hibernating Buyers`: High recency days (inactive), requires win-back promotions.
- **Artifact**: `ml/models/kmeans_model.joblib`

### 🛍️ Module D: Product Recommendation Engine
- **Script**: `ml/product_recommendation.py`
- **Algorithm**: Cosine Similarity on Customer-Product Binary Purchase Matrix
- **Functionality**: Returns top-$N$ complementary cross-sell recommendations for any selected product.
- **Artifact**: `ml/models/recommender.joblib`

### 💡 Module E: Executive Business Recommender
- **Script**: `ml/business_recommender.py`
- **Functionality**: Synthesizes model outputs to generate executive recommendations (Products to Promote, Growth Cities, Inventory Buffers, Discount Rules).
