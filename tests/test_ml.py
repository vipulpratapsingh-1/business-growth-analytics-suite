"""
Machine Learning Testing Suite - Step 7 Enterprise Production Upgrade
Tests model artifact persistence, sales forecasting, churn risk calculations,
K-Means customer clusters, and recommendation inference.
"""

import sys
from pathlib import Path
import pytest
import joblib

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def test_ml_model_artifacts_exist():
    """Verify serialized .joblib model files exist in ml/models/."""
    assert (config.ML_MODELS_DIR / "sales_forecaster.joblib").exists()
    assert (config.ML_MODELS_DIR / "churn_model.joblib").exists()
    assert (config.ML_MODELS_DIR / "kmeans_model.joblib").exists()
    assert (config.ML_MODELS_DIR / "recommender.joblib").exists()

def test_sales_forecaster_inference():
    """Verify loading and forecasting from sales_forecaster.joblib artifact."""
    artifact = joblib.load(config.ML_MODELS_DIR / "sales_forecaster.joblib")
    assert "model" in artifact
    assert "forecast_results" in artifact
    
    # Check 6-month forecast
    f6 = artifact["forecast_results"][6]
    assert len(f6["monthly_forecasts"]) == 6
    assert f6["total_projected_revenue"] > 0

def test_churn_classifier_inference():
    """Verify churn model risk scoring logic."""
    artifact = joblib.load(config.ML_MODELS_DIR / "churn_model.joblib")
    assert "customer_scores" in artifact
    scores_df = artifact["customer_scores"]
    assert len(scores_df) == 5000
    assert "Churn_Probability_%" in scores_df.columns

def test_recommender_inference():
    """Verify item similarity matrix returns valid recommendations."""
    artifact = joblib.load(config.ML_MODELS_DIR / "recommender.joblib")
    sim_df = artifact["similarity_matrix"]
    assert sim_df.shape[0] == 24
    
    # Get top recs for first product in similarity matrix
    target_product = sim_df.columns[0]
    scores = sim_df[target_product].sort_values(ascending=False)
    recs = scores.iloc[1:4].index.tolist()
    assert len(recs) == 3
