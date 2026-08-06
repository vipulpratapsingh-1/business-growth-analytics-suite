"""
Data Cleaning Script for Business Growth Analytics Suite - Step 2
Performs missing value handling, duplicate removal, text standardization,
datetime conversion, numerical validation, and mathematical sanity checks.
Saves output to data/clean_sales_data.csv.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def clean_dataset(raw_dataset_path=config.DATASET_PATH, output_dataset_path=config.CLEAN_DATASET_PATH) -> pd.DataFrame:
    """
    Executes an enterprise-grade data cleaning pipeline on the sales dataset.
    """
    print("\n" + "=" * 60)
    print("[CLEANING] STARTING DATA CLEANING & VALIDATION PIPELINE")
    print("=" * 60)

    # 1. Load Raw Dataset
    if not raw_dataset_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {raw_dataset_path}. Please run main.py first.")

    print(f"[INFO] Loading raw dataset from: {raw_dataset_path}")
    df = pd.read_csv(raw_dataset_path)
    initial_rows = len(df)
    print(f"[INFO] Initial Row Count: {initial_rows:,} rows")

    # 2. Duplicate Detection & Removal
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        print(f"[ACTION] Removing {duplicate_count:,} duplicate rows...")
        df = df.drop_duplicates().reset_index(drop=True)
    else:
        print("[OK] Duplicate Check: 0 duplicate rows found.")

    # 3. Missing Value Handling
    missing_report = df.isnull().sum()
    total_missing = missing_report.sum()
    if total_missing > 0:
        print(f"[ACTION] Handling {total_missing} missing values...")
        # Fill categorical missing values with 'Unknown' or mode, numeric with median
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == "object":
                    df[col] = df[col].fillna("Unknown")
                else:
                    df[col] = df[col].fillna(df[col].median())
    else:
        print("[OK] Missing Value Check: 0 missing values found.")

    # 4. Text Standardization
    text_columns = ["Customer Name", "City", "State", "Product", "Category", "Payment Method"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Standardize Order ID and Customer ID to uppercase
    df["Order ID"] = df["Order ID"].astype(str).str.strip().str.upper()
    df["Customer ID"] = df["Customer ID"].astype(str).str.strip().str.upper()

    # 5. Datetime Conversion & Validation
    print("[ACTION] Standardizing date formats...")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    
    # Drop rows with unparseable dates if any
    invalid_dates = df["Order Date"].isnull().sum()
    if invalid_dates > 0:
        print(f"[ACTION] Removing {invalid_dates} rows with invalid date formats...")
        df = df.dropna(subset=["Order Date"]).reset_index(drop=True)

    # Convert back to standardized string representation (YYYY-MM-DD HH:MM:SS)
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 6. Numerical Validation & Outlier/Impossible Value Filters
    print("[ACTION] Validating numeric boundaries...")
    
    # Filter rules:
    # - Quantity must be > 0
    # - Unit Price must be > 0
    # - Discount must be between 0.0 and 1.0 (0% to 100%)
    # - Sales must be >= 0
    valid_mask = (
        (df["Quantity"] > 0) &
        (df["Unit Price"] > 0) &
        (df["Discount"] >= 0.0) & (df["Discount"] <= 1.0) &
        (df["Sales"] >= 0)
    )
    
    invalid_records_count = len(df) - valid_mask.sum()
    if invalid_records_count > 0:
        print(f"[ACTION] Removing {invalid_records_count} invalid numerical records...")
        df = df[valid_mask].reset_index(drop=True)
    else:
        print("[OK] Numeric Validation Check: All records satisfy valid physical boundaries.")

    # 7. Mathematical Sanity Check: Recalculate Sales
    print("[ACTION] Verifying mathematical formula: Sales = Quantity * Unit Price * (1 - Discount)...")
    expected_sales = np.round(df["Quantity"] * df["Unit Price"] * (1.0 - df["Discount"]), 2)
    math_discrepancies = (np.abs(df["Sales"] - expected_sales) > 0.05).sum()
    
    if math_discrepancies > 0:
        print(f"[ACTION] Correcting {math_discrepancies} calculated sales values for mathematical consistency...")
        df["Sales"] = expected_sales

    # 8. Sort chronologically by Order Date
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values("Order Date").reset_index(drop=True)
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 9. Save Cleaned Dataset
    config.ensure_directories_exist()
    df.to_csv(output_dataset_path, index=False)
    
    final_rows = len(df)
    rows_removed = initial_rows - final_rows

    print("\n" + "-" * 60)
    print("[SUMMARY] DATA CLEANING AUDIT REPORT")
    print("-" * 60)
    print(f"Initial Row Count  : {initial_rows:,}")
    print(f"Duplicates Removed : {duplicate_count:,}")
    print(f"Invalid Rows Dropped: {invalid_records_count:,}")
    print(f"Final Clean Rows   : {final_rows:,}")
    print(f"Total Rows Removed : {rows_removed:,} ({(rows_removed / initial_rows) * 100:.2f}%)")
    print(f"[OK] Cleaned dataset successfully saved to: {output_dataset_path}")
    
    return df

if __name__ == "__main__":
    clean_dataset()
