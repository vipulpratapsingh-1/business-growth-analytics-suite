"""
Customer Segmentation Module - Step 5
Uses K-Means Unsupervised Clustering on Recency, Frequency, and Monetary (RFM)
data to segment customers into actionable business buyer personas.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def build_customer_segmentation_model(clean_data_path=config.CLEAN_DATASET_PATH, n_clusters=4):
    """
    Performs RFM feature engineering, standardizes scales, fits K-Means clustering,
    and maps numeric clusters to strategic business customer segments.
    """
    print("\n" + "=" * 60)
    print("[ML] MODULE C: K-MEANS CUSTOMER SEGMENTATION ENGINE")
    print("=" * 60)

    # 1. Load Clean Dataset
    df = pd.read_csv(clean_data_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    max_date = df["Order Date"].max()

    # 2. Engineer RFM Features per Customer
    rfm = df.groupby("Customer ID").agg(
        Recency=("Order Date", lambda dates: (max_date - dates.max()).days),
        Frequency=("Order ID", "nunique"),
        Monetary=("Sales", "sum")
    ).reset_index()

    # Log transform Monetary to reduce right-skewness
    rfm["Monetary_Log"] = np.log1p(rfm["Monetary"])

    # 3. Feature Scaling using StandardScaler
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary_Log"]])

    # 4. Fit K-Means Model
    kmeans = KMeans(n_clusters=n_clusters, random_state=config.RANDOM_SEED, n_init=10)
    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    # 5. Interpret Clusters & Assign Business Personas based on Cluster Centroids
    cluster_means = rfm.groupby("Cluster").agg(
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary=("Monetary", "mean"),
        Customer_Count=("Customer ID", "count")
    ).reset_index()

    # Dynamic Segment Labeling Assignment
    # Persona Mapping Logic:
    # High Frequency & High Monetary = "Champions (VIPs)"
    # High Frequency & Moderate Monetary = "Loyal Customers"
    # Low Recency (Recent) & Low Frequency = "New / Promising Buyers"
    # High Recency (Inactive) & Moderate Spend = "At-Risk / Hibernating"
    
    segment_names = {}
    for _, row in cluster_means.iterrows():
        c_id = int(row["Cluster"])
        rec = row["Avg_Recency"]
        freq = row["Avg_Frequency"]
        mon = row["Avg_Monetary"]

        if freq >= cluster_means["Avg_Frequency"].median() and mon >= cluster_means["Avg_Monetary"].median():
            segment_names[c_id] = "Champions (VIP Spenders)"
        elif freq >= cluster_means["Avg_Frequency"].median():
            segment_names[c_id] = "Loyal Regular Buyers"
        elif rec <= cluster_means["Avg_Recency"].median():
            segment_names[c_id] = "Promising / Recent Buyers"
        else:
            segment_names[c_id] = "At-Risk / Hibernating Buyers"

    rfm["Segment_Name"] = rfm["Cluster"].map(segment_names)

    print("\n[SUMMARY] Discovered Customer Segments:")
    print(rfm.groupby("Segment_Name").agg(
        Count=("Customer ID", "count"),
        Mean_Recency_Days=("Recency", "mean"),
        Mean_Frequency=("Frequency", "mean"),
        Mean_Spend_INR=("Monetary", "mean")
    ).to_string())

    # 6. Save Trained Artifact
    config.ensure_directories_exist()
    model_path = config.ML_MODELS_DIR / "kmeans_model.joblib"
    joblib.dump({
        "kmeans": kmeans,
        "scaler": scaler,
        "rfm_data": rfm,
        "cluster_means": cluster_means,
        "segment_names": segment_names
    }, model_path)
    print(f"\n[OK] Saved trained K-Means segmentation artifact to: {model_path}")

    return {
        "rfm_data": rfm,
        "cluster_means": cluster_means,
        "segment_names": segment_names
    }

if __name__ == "__main__":
    build_customer_segmentation_model()
