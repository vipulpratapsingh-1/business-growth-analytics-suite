"""
Machine Learning REST API Router - Step 6
Provides REST endpoints for Sales Forecasting, Churn Risk Calculation,
K-Means Customer Personas, and Product Cross-Sell Recommendations.
"""

import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

import config
from backend.auth import get_current_user

router = APIRouter(prefix="/api/ml", tags=["Machine Learning Inference Engine"])

class ForecastRequest(BaseModel):
    horizon_months: int = 6

class ChurnRequest(BaseModel):
    customer_id: str

class RecommendRequest(BaseModel):
    product_name: str
    top_n: int = 3

@router.post("/forecast")
def predict_sales_forecast(req: ForecastRequest, current_user: dict = Depends(get_current_user)):
    """Serves time-series sales forecasting predictions for 3, 6, or 12 months."""
    model_path = config.ML_MODELS_DIR / "sales_forecaster.joblib"
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Forecasting model artifact missing. Run ML pipeline.")

    data = joblib.load(model_path)
    forecasts = data["forecast_results"].get(req.horizon_months)
    
    if not forecasts:
        # Fallback to closest period
        forecasts = data["forecast_results"].get(6)

    return {
        "status": "success",
        "model_used": data["model_name"],
        "evaluation_metrics": data["rf_metrics"],
        "horizon_months": req.horizon_months,
        "total_projected_revenue": forecasts["total_projected_revenue"],
        "monthly_forecast_breakdown": forecasts["monthly_forecasts"]
    }

@router.post("/churn")
def predict_customer_churn(req: ChurnRequest, current_user: dict = Depends(get_current_user)):
    """Returns customer churn probability score and risk level."""
    model_path = config.ML_MODELS_DIR / "churn_model.joblib"
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Churn model artifact missing. Run ML pipeline.")

    data = joblib.load(model_path)
    cust_df = data["customer_scores"]
    
    match = cust_df[cust_df["Customer ID"] == req.customer_id.strip().upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Customer ID '{req.customer_id}' not found.")

    row = match.iloc[0]
    return {
        "customer_id": row["Customer ID"],
        "recency_days": int(row["Recency_Days"]),
        "frequency": int(row["Frequency"]),
        "monetary_value": float(row["Monetary_Value"]),
        "churn_probability_pct": float(row["Churn_Probability_%"]),
        "risk_tier": str(row["Risk_Tier"])
    }

@router.get("/segments")
def get_customer_segments(current_user: dict = Depends(get_current_user)):
    """Returns K-Means customer RFM clusters and persona counts."""
    model_path = config.ML_MODELS_DIR / "kmeans_model.joblib"
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="K-Means model artifact missing. Run ML pipeline.")

    data = joblib.load(model_path)
    rfm_df = data["rfm_data"]

    segment_summary = rfm_df.groupby("Segment_Name").agg(
        customer_count=("Customer ID", "count"),
        avg_recency_days=("Recency", "mean"),
        avg_frequency=("Frequency", "mean"),
        avg_spend_inr=("Monetary", "mean")
    ).reset_index()

    return {
        "status": "success",
        "discovered_segments": segment_summary.to_dict(orient="records")
    }

@router.post("/recommend")
def recommend_products(req: RecommendRequest, current_user: dict = Depends(get_current_user)):
    """Returns cross-sell product recommendations based on item similarity."""
    model_path = config.ML_MODELS_DIR / "recommender.joblib"
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Recommender model artifact missing. Run ML pipeline.")

    data = joblib.load(model_path)
    sim_df = data["similarity_matrix"]

    prod_name = req.product_name.strip()
    if prod_name not in sim_df.index:
        # Match case-insensitive
        matches = [p for p in sim_df.index if prod_name.lower() in p.lower()]
        if matches:
            prod_name = matches[0]
        else:
            raise HTTPException(status_code=404, detail=f"Product '{req.product_name}' not found in catalog.")

    scores = sim_df[prod_name].sort_values(ascending=False)
    top_recs = scores.iloc[1:req.top_n+1].index.tolist()

    return {
        "target_product": prod_name,
        "recommended_products": top_recs
    }
