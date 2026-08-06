"""
Customer Churn Prediction Module - Step 5
Builds a machine learning classifier to identify customers at risk of churn
(inactivity > 180 days). Calculates churn probability scores and feature importances.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def build_churn_prediction_model(clean_data_path=config.CLEAN_DATASET_PATH):
    """
    Engineers customer RFM features, defines churn targets (inactivity > 180 days),
    trains a Random Forest Classifier, and calculates churn probabilities.
    """
    print("\n" + "=" * 60)
    print("[ML] MODULE B: CUSTOMER CHURN PREDICTION ENGINE")
    print("=" * 60)

    # 1. Load Clean Dataset
    df = pd.read_csv(clean_data_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    max_dataset_date = df["Order Date"].max()

    # 2. Engineer Customer Features (Recency, Frequency, Monetary Value, Avg Discount, Margin Ratio)
    customer_features = df.groupby("Customer ID").agg(
        Last_Order_Date=("Order Date", "max"),
        First_Order_Date=("Order Date", "min"),
        Frequency=("Order ID", "nunique"),
        Monetary_Value=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Order_Value=("Sales", "mean"),
        Avg_Discount=("Discount", "mean"),
        Total_Quantity=("Quantity", "sum")
    ).reset_index()

    # Calculate Recency in Days relative to dataset end date
    customer_features["Recency_Days"] = (max_dataset_date - customer_features["Last_Order_Date"]).dt.days
    customer_features["Tenure_Days"] = (max_dataset_date - customer_features["First_Order_Date"]).dt.days

    # 3. Define Churn Label (Target: Recency > 180 days = Churned [1], else Retained [0])
    customer_features["Churned"] = (customer_features["Recency_Days"] > 180).astype(int)

    feature_cols = [
        "Frequency", "Monetary_Value", "Total_Profit", 
        "Avg_Order_Value", "Avg_Discount", "Total_Quantity", "Tenure_Days"
    ]
    X = customer_features[feature_cols]
    y = customer_features["Churned"]

    print(f"[INFO] Total Customer Profiles Analyzed : {len(customer_features):,}")
    print(f"[INFO] Retained Customers (Active)     : {(y == 0).sum():,} ({(y == 0).mean()*100:.1f}%)")
    print(f"[INFO] Churned Customers (>180d inactive): {(y == 1).sum():,} ({(y == 1).mean()*100:.1f}%)")

    # 4. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=config.RANDOM_SEED, stratify=y
    )

    # 5. Train Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=config.RANDOM_SEED)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    # 6. Evaluation Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)

    print("[METRICS] Churn Classification Performance:")
    print(f"  • Accuracy  : {acc*100:.2f}%")
    print(f"  • Precision : {prec*100:.2f}%")
    print(f"  • Recall    : {rec*100:.2f}%")
    print(f"  • F1 Score  : {f1:.4f}")
    print(f"  • ROC-AUC   : {auc:.4f}")

    # 7. Extract Feature Importances
    importances = clf.feature_importances_
    feat_imp = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": importances
    }).sort_values("Importance", ascending=False)

    print("\n[FEATURE IMPORTANCE] Key Drivers of Customer Churn:")
    for idx, row in feat_imp.iterrows():
        print(f"  • {row['Feature']:<20} : {row['Importance']*100:.2f}%")

    # 8. Predict Churn Risk Probabilities across entire Customer Base
    customer_features["Churn_Probability_%"] = np.round(clf.predict_proba(X)[:, 1] * 100, 2)
    customer_features["Risk_Tier"] = pd.cut(
        customer_features["Churn_Probability_%"],
        bins=[-0.1, 30, 70, 100.1],
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )

    # 9. Save Trained Artifact
    config.ensure_directories_exist()
    model_path = config.ML_MODELS_DIR / "churn_model.joblib"
    joblib.dump({
        "model": clf,
        "feature_cols": feature_cols,
        "feature_importance": feat_imp,
        "customer_scores": customer_features,
        "metrics": {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1, "AUC": auc}
    }, model_path)
    print(f"[OK] Saved trained churn model artifact to: {model_path}")

    return {
        "customer_features": customer_features,
        "feature_importance": feat_imp,
        "metrics": (acc, prec, rec, f1, auc)
    }

if __name__ == "__main__":
    build_churn_prediction_model()
