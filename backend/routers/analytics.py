"""
Analytics REST API Router - Step 8 Production Enhancement
Serves executive summaries, sales performance, customer RFM distributions,
financial margins, and direct SQL query execution endpoints with SQLite/PostgreSQL support.
"""

import os
import sqlite3
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import pandas as pd

import config
from backend.auth import get_current_user, require_role

router = APIRouter(prefix="/api/analytics", tags=["Analytics & BI Engine"])

# Global in-memory DataFrame cache for ultra-fast startup and response times
_CACHED_DF: Optional[pd.DataFrame] = None

def get_clean_dataframe() -> pd.DataFrame:
    """Returns cached clean sales DataFrame, loading from CSV on first access."""
    global _CACHED_DF
    if _CACHED_DF is None:
        if not config.CLEAN_DATASET_PATH.exists():
            raise HTTPException(status_code=404, detail="Clean dataset missing. Run data cleaning pipeline.")
        _CACHED_DF = pd.read_csv(config.CLEAN_DATASET_PATH)
    return _CACHED_DF

class SQLQueryRequest(BaseModel):
    sql_query: str

def get_db_connection():
    """Returns a database connection (SQLite or PostgreSQL based on DATABASE_URL)."""
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
        try:
            import psycopg2
            return psycopg2.connect(db_url)
        except ImportError:
            pass  # Fallback to SQLite if psycopg2 is not installed
    
    if not config.DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database file BusinessGrowthDB.sqlite not found.")
    return sqlite3.connect(config.DB_PATH)

@router.get("/executive")
def get_executive_summary(current_user: dict = Depends(get_current_user)):
    """Returns top-level executive KPIs and monthly trends."""
    df = get_clean_dataframe()
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(len(df))
    total_customers = int(df["Customer ID"].nunique())
    profit_margin = float((total_profit / total_sales) * 100)

    df_monthly = df.copy()
    df_monthly["YearMonth"] = pd.to_datetime(df_monthly["Order Date"]).dt.to_period("M").astype(str)
    monthly = df_monthly.groupby("YearMonth")[["Sales", "Profit"]].sum().reset_index()

    return {
        "status": "success",
        "kpis": {
            "total_revenue": total_sales,
            "total_profit": total_profit,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "profit_margin_pct": round(profit_margin, 2),
            "average_order_value": round(total_sales / total_orders, 2)
        },
        "monthly_trends": monthly.to_dict(orient="records")
    }

@router.get("/sales")
def get_sales_analytics(current_user: dict = Depends(get_current_user)):
    """Returns detailed sales breakdowns by Category, State, City, and Products."""
    df = get_clean_dataframe()

    cat_sales = df.groupby("Category").agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
        units_sold=("Quantity", "sum")
    ).reset_index()

    state_sales = df.groupby("State")["Sales"].sum().sort_values(ascending=False).reset_index()
    top_cities = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
    top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
    bottom_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=True).head(10).reset_index()

    return {
        "category_performance": cat_sales.to_dict(orient="records"),
        "state_leaderboard": state_sales.to_dict(orient="records"),
        "top_10_cities": top_cities.to_dict(orient="records"),
        "top_10_products": top_products.to_dict(orient="records"),
        "bottom_10_products": bottom_products.to_dict(orient="records")
    }

@router.get("/customers")
def get_customer_analytics(current_user: dict = Depends(get_current_user)):
    """Returns customer retention, CLV tiers, and RFM distributions."""
    df = get_clean_dataframe()

    cust_summary = df.groupby("Customer ID").agg(
        total_spent=("Sales", "sum"),
        order_count=("Order ID", "count")
    ).reset_index()

    repeat_count = int((cust_summary["order_count"] > 1).sum())
    single_count = int((cust_summary["order_count"] == 1).sum())

    top_clv = cust_summary.sort_values("total_spent", ascending=False).head(10)

    return {
        "total_unique_customers": len(cust_summary),
        "retention": {
            "repeat_buyers": repeat_count,
            "single_buyers": single_count,
            "repeat_ratio_pct": round((repeat_count / len(cust_summary)) * 100, 2)
        },
        "top_10_clv_customers": top_clv.to_dict(orient="records")
    }

@router.get("/financials")
def get_financial_analytics(current_user: dict = Depends(get_current_user)):
    """Returns discount profitability impact and payment method market share."""
    df = get_clean_dataframe().copy()

    df["Disc_Bin"] = pd.cut(df["Discount"], bins=[-0.01, 0.0, 0.10, 0.20, 1.0], labels=["0% (No Discount)", "1-10% (Low)", "11-20% (Medium)", ">20% (High)"])
    disc_summary = df.groupby("Disc_Bin", observed=False).agg(
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        order_count=("Sales", "count")
    ).reset_index()
    disc_summary["margin_pct"] = round((disc_summary["profit"] / disc_summary["sales"]) * 100, 2)

    payment_summary = df.groupby("Payment Method").agg(
        total_volume=("Sales", "sum"),
        order_count=("Sales", "count"),
        avg_transaction=("Sales", "mean")
    ).reset_index()

    return {
        "discount_impact": disc_summary.to_dict(orient="records"),
        "payment_market_share": payment_summary.to_dict(orient="records")
    }

@router.post("/sql")
def execute_custom_sql(
    query_req: SQLQueryRequest,
    current_user: dict = Depends(require_role(["Admin", "Analyst"]))
):
    """Allows Analysts and Admins to execute SQL queries directly against BusinessGrowthDB."""
    clean_query = query_req.sql_query.strip()
    if not clean_query.upper().startswith("SELECT") and not clean_query.upper().startswith("WITH"):
        raise HTTPException(status_code=400, detail="Only SELECT and WITH read-only queries are permitted.")

    try:
        conn = get_db_connection()
        df_result = pd.read_sql(clean_query, conn)
        conn.close()
        return {
            "status": "success",
            "query": clean_query,
            "row_count": len(df_result),
            "columns": list(df_result.columns),
            "data": df_result.head(100).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL Execution Error: {str(e)}")
