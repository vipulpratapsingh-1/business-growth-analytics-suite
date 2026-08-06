"""
Sales Forecasting Module - Step 5
Builds and compares Linear Regression vs. Random Forest Regressor time-series models
to forecast enterprise sales revenue for the next 3, 6, and 12 months.
Evaluates MAE, RMSE, and R2 performance metrics.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def build_sales_forecast_model(clean_data_path=config.CLEAN_DATASET_PATH):
    """
    Trains, compares, and evaluates time-series sales forecasting models.
    Returns evaluation metrics, predictions, and saves the best trained model.
    """
    print("\n" + "=" * 60)
    print("[ML] MODULE A: TIME-SERIES SALES FORECASTING ENGINE")
    print("=" * 60)

    # 1. Load Clean Dataset
    df = pd.read_csv(clean_data_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    
    # 2. Aggregate Sales to Monthly Time-Series
    monthly_df = df.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"].sum().reset_index()
    monthly_df["Month_Index"] = np.arange(len(monthly_df))
    
    # 3. Create Feature Matrix (Month Index + Seasonal Lags)
    monthly_df["Lag_1"] = monthly_df["Sales"].shift(1).fillna(monthly_df["Sales"].mean())
    monthly_df["Lag_2"] = monthly_df["Sales"].shift(2).fillna(monthly_df["Sales"].mean())

    X = monthly_df[["Month_Index", "Lag_1", "Lag_2"]]
    y = monthly_df["Sales"]

    # 4. Train/Test Split (80% Train, 20% Test for temporal sequence)
    split_idx = int(len(monthly_df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    # 5. Train Linear Regression Model
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)

    # 6. Train Random Forest Regressor Model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=config.RANDOM_SEED)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)

    # 7. Evaluate Metrics: MAE, RMSE, R2
    def eval_metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        return mae, rmse, r2

    lr_mae, lr_rmse, lr_r2 = eval_metrics(y_test, lr_preds)
    rf_mae, rf_rmse, rf_r2 = eval_metrics(y_test, rf_preds)

    print("[METRICS] Model Performance Comparison:")
    print(f"  • Linear Regression : MAE = ₹{lr_mae:,.2f} | RMSE = ₹{lr_rmse:,.2f} | R² = {lr_r2:.4f}")
    print(f"  • Random Forest     : MAE = ₹{rf_mae:,.2f} | RMSE = ₹{rf_rmse:,.2f} | R² = {rf_r2:.4f}")

    # Select best model (based on lowest RMSE)
    best_model = rf_model if rf_rmse < lr_rmse else lr_model
    best_model_name = "Random Forest Regressor" if best_model == rf_model else "Linear Regression"
    print(f"[OK] Selected Best Model: {best_model_name}")

    # 8. Forecast Future 3, 6, and 12 Months
    future_months = [3, 6, 12]
    forecast_results = {}
    last_month_idx = monthly_df["Month_Index"].max()
    last_sales = monthly_df["Sales"].iloc[-1]

    for f_period in future_months:
        future_x = []
        curr_lag1 = last_sales
        curr_lag2 = monthly_df["Sales"].iloc[-2]
        
        preds_list = []
        for i in range(1, f_period + 1):
            feat = [[last_month_idx + i, curr_lag1, curr_lag2]]
            pred_val = best_model.predict(feat)[0]
            preds_list.append(pred_val)
            curr_lag2 = curr_lag1
            curr_lag1 = pred_val

        total_projected_revenue = sum(preds_list)
        forecast_results[f_period] = {
            "period_months": f_period,
            "monthly_forecasts": preds_list,
            "total_projected_revenue": total_projected_revenue
        }
        print(f"[FORECAST] Next {f_period:02d} Months Projected Revenue: ₹{total_projected_revenue/1e7:,.2f} Cr")

    # 9. Save Trained Model Artifact
    config.ensure_directories_exist()
    model_save_path = config.ML_MODELS_DIR / "sales_forecaster.joblib"
    joblib.dump({
        "model": best_model,
        "model_name": best_model_name,
        "lr_metrics": {"MAE": lr_mae, "RMSE": lr_rmse, "R2": lr_r2},
        "rf_metrics": {"MAE": rf_mae, "RMSE": rf_rmse, "R2": rf_r2},
        "monthly_history": monthly_df,
        "forecast_results": forecast_results
    }, model_save_path)
    print(f"[OK] Saved trained forecasting model artifact to: {model_save_path}")

    return {
        "monthly_df": monthly_df,
        "lr_metrics": (lr_mae, lr_rmse, lr_r2),
        "rf_metrics": (rf_mae, rf_rmse, rf_r2),
        "best_model_name": best_model_name,
        "forecast_results": forecast_results
    }

if __name__ == "__main__":
    build_sales_forecast_model()
