"""
Main Execution Module for Business Growth Analytics Suite - Step 1
Handles project verification, data generation triggering, and initial dataset health checks.
"""

import sys
import os
from pathlib import Path
import pandas as pd
from tabulate import tabulate

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import config
from scripts.generate_dataset import generate_sales_dataset

def verify_dataset_health(df: pd.DataFrame) -> bool:
    """
    Validates dataset integrity against project specification requirements.
    """
    print("\n" + "=" * 60)
    print("[CHECK] RUNNING STEP 1 DATASET INTEGRITY VERIFICATION")
    print("=" * 60)

    expected_rows = config.TOTAL_ROWS
    actual_rows = len(df)
    
    # 1. Check Row Count
    if actual_rows == expected_rows:
        print(f"[OK] Row Count Check PASSED: Exactly {actual_rows:,} rows found.")
    else:
        print(f"[FAIL] Row Count Check FAILED: Expected {expected_rows:,}, but got {actual_rows:,}.")

    # 2. Check Column Schema (14 Required Columns)
    expected_columns = [
        "Order ID", "Order Date", "Customer ID", "Customer Name", "City", "State",
        "Product", "Category", "Quantity", "Unit Price", "Discount",
        "Sales", "Profit", "Payment Method"
    ]
    missing_cols = set(expected_columns) - set(df.columns)
    if not missing_cols:
        print(f"[OK] Column Schema Check PASSED: All 14 required columns present.")
    else:
        print(f"[FAIL] Column Schema Check FAILED: Missing columns -> {missing_cols}")

    # 3. Null Values Check
    null_count = df.isnull().sum().sum()
    if null_count == 0:
        print(f"[OK] Data Completeness PASSED: 0 missing values detected.")
    else:
        print(f"[WARN] Found {null_count} null values in dataset.")

    # 4. Summary Statistics Snapshot
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    unique_customers = df["Customer ID"].nunique()

    print("\n" + "-" * 60)
    print("[SUMMARY] DATASET BUSINESS SUMMARY SNAPSHOT")
    print("-" * 60)
    metrics_data = [
        ["Total Orders", f"{total_orders:,}"],
        ["Unique Customers", f"{unique_customers:,}"],
        ["Total Sales Revenue", f"INR {total_sales:,.2f}"],
        ["Total Net Profit", f"INR {total_profit:,.2f}"],
        ["Overall Profit Margin", f"{(total_profit / total_sales) * 100:.2f}%"],
        ["Date Range", f"{df['Order Date'].min()[:10]} to {df['Order Date'].max()[:10]}"]
    ]
    print(tabulate(metrics_data, headers=["Metric", "Value"], tablefmt="github"))

    print("\n" + "-" * 60)
    print("[PREVIEW] FIRST 5 ROWS PREVIEW")
    print("-" * 60)
    preview_cols = ["Order ID", "Order Date", "Customer Name", "City", "Category", "Sales", "Profit"]
    print(tabulate(df[preview_cols].head(5), headers="keys", tablefmt="github", showindex=False))

    return actual_rows == expected_rows and len(missing_cols) == 0

def main():
    """Main execution flow for Step 1."""
    print("=== BUSINESS GROWTH ANALYTICS SUITE - STEP 1 INITIALIZATION ===\n")
    
    # 1. Ensure directory tree exists
    config.ensure_directories_exist()

    # 2. Generate or Load Dataset
    if not config.DATASET_PATH.exists():
        print("[INFO] Sales dataset not found in data/. Triggering dataset generator...")
        df = generate_sales_dataset()
    else:
        print(f"[INFO] Found existing dataset at: {config.DATASET_PATH}")
        print("Reading CSV dataset...")
        df = pd.read_csv(config.DATASET_PATH)

    # 3. Perform Integrity & Health Verification
    success = verify_dataset_health(df)

    if success:
        print("\n[SUCCESS] STEP 1 COMPLETED SUCCESSFULLY! Project foundation is ready for analysis.")
    else:
        print("\n[WARNING] STEP 1 completed with warnings. Check logs above.")

if __name__ == "__main__":
    main()
