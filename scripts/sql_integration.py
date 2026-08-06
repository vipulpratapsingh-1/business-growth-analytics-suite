"""
SQL Integration & ETL Pipeline Script - Step 3
Transforms clean CSV dataset into normalized SQLite database (data/BusinessGrowthDB.sqlite),
executes DDL table creation, populates data, creates indexes & views, and verifies all 50 SQL queries.
"""

import sys
import os
import sqlite3
import time
from pathlib import Path
import pandas as pd
from tabulate import tabulate

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def build_database():
    """
    Builds the relational BusinessGrowthDB SQLite database from data/clean_sales_data.csv.
    """
    print("\n" + "=" * 60)
    print("[SQL] STARTING DATABASE INTEGRATION & ETL PIPELINE")
    print("=" * 60)

    clean_csv_path = config.CLEAN_DATASET_PATH
    db_path = config.DB_PATH

    if not clean_csv_path.exists():
        raise FileNotFoundError(f"Clean dataset not found at {clean_csv_path}. Please run data_cleaning script first.")

    print(f"[INFO] Reading clean sales CSV from: {clean_csv_path}")
    df = pd.read_csv(clean_csv_path)

    # Recreate DB file to ensure clean schema build
    if db_path.exists():
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Execute DDL Table Creation (sql/create_tables.sql)
    create_tables_sql = (config.SQL_DIR / "create_tables.sql").read_text(encoding="utf-8")
    cursor.executescript(create_tables_sql)
    print("[OK] Executed sql/create_tables.sql: 5 tables created.")

    # 2. Normalize and Load Data into SQLite Tables
    print("[ETL] Normalizing flat CSV into relational tables...")

    # A. Customers Table
    customers_df = df[["Customer ID", "Customer Name"]].drop_duplicates().rename(
        columns={"Customer ID": "customer_id", "Customer Name": "customer_name"}
    )
    customers_df.to_sql("Customers", conn, if_exists="append", index=False)

    # B. Products Table
    products_df = df[["Product", "Category"]].drop_duplicates().rename(
        columns={"Product": "product_name", "Category": "category"}
    )
    products_df.to_sql("Products", conn, if_exists="append", index=False)

    # Map product_id back to main dataframe
    product_map = pd.read_sql("SELECT product_id, product_name FROM Products", conn)
    df = df.merge(product_map, left_on="Product", right_on="product_name", how="left")

    # C. Orders Table
    orders_df = df[["Order ID", "Order Date", "Customer ID", "City", "State"]].drop_duplicates(subset=["Order ID"]).rename(
        columns={
            "Order ID": "order_id",
            "Order Date": "order_date",
            "Customer ID": "customer_id",
            "City": "city",
            "State": "state"
        }
    )
    orders_df.to_sql("Orders", conn, if_exists="append", index=False)

    # D. Sales Table
    sales_df = df[["Order ID", "product_id", "Quantity", "Unit Price", "Discount", "Sales", "Profit"]].rename(
        columns={
            "Order ID": "order_id",
            "Quantity": "quantity",
            "Unit Price": "unit_price",
            "Discount": "discount",
            "Sales": "sales_amount",
            "Profit": "profit_amount"
        }
    )
    sales_df.to_sql("Sales", conn, if_exists="append", index=False)

    # E. Payments Table
    payments_df = df[["Order ID", "Payment Method", "Sales"]].rename(
        columns={
            "Order ID": "order_id",
            "Payment Method": "payment_method",
            "Sales": "transaction_amount"
        }
    )
    payments_df.to_sql("Payments", conn, if_exists="append", index=False)

    print("[OK] ETL Complete: Data loaded into Customers, Products, Orders, Sales, and Payments.")

    # 3. Create Performance Indexes (sql/indexes.sql)
    indexes_sql = (config.SQL_DIR / "indexes.sql").read_text(encoding="utf-8")
    cursor.executescript(indexes_sql)
    print("[OK] Executed sql/indexes.sql: 7 performance indexes applied.")

    # 4. Create Reporting Views (sql/views.sql)
    views_sql = (config.SQL_DIR / "views.sql").read_text(encoding="utf-8")
    cursor.executescript(views_sql)
    print("[OK] Executed sql/views.sql: 5 reporting database views built.")

    conn.commit()

    # 5. Verify Table Row Counts
    tables = ["Customers", "Products", "Orders", "Sales", "Payments"]
    print("\n" + "-" * 60)
    print("[SUMMARY] DATABASE TABLES ROW COUNT AUDIT")
    print("-" * 60)
    audit_data = []
    for tbl in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        audit_data.append([tbl, f"{count:,}"])
    print(tabulate(audit_data, headers=["Table Name", "Total Records"], tablefmt="github"))

    # 6. Execute & Benchmark 50 SQL Queries (sql/analytics_queries.sql)
    print("\n" + "-" * 60)
    print("[BENCHMARK] EXECUTING ALL 50 BUSINESS SQL QUERIES")
    print("-" * 60)

    queries_file = config.SQL_DIR / "analytics_queries.sql"
    raw_sql = queries_file.read_text(encoding="utf-8")

    # Split SQL file by semicolon delimiter, stripping inline/header comments
    raw_statements = raw_sql.split(";")
    statements = []
    for stmt in raw_statements:
        # Remove line comments
        clean_lines = [line for line in stmt.splitlines() if not line.strip().startswith("--")]
        clean_stmt = " ".join(clean_lines).strip()
        if clean_stmt:
            statements.append(clean_stmt)

    success_count = 0
    start_time = time.time()

    for idx, stmt in enumerate(statements, start=1):
        try:
            cur_start = time.time()
            res = cursor.execute(stmt).fetchall()
            cur_duration = (time.time() - cur_start) * 1000
            success_count += 1
            # Print milestone checks
            if idx in [1, 12, 25, 38, 50] or idx % 10 == 0:
                print(f"[QUERY Q{idx:02d}] Executed successfully in {cur_duration:.2f} ms ({len(res)} rows returned).")
        except Exception as e:
            print(f"[FAIL] Query Q{idx} failed: {e}\nStatement: {stmt[:100]}...")

    total_duration = time.time() - start_time
    print(f"\n[OK] Executed {success_count} / {len(statements)} queries successfully in {total_duration:.2f} seconds.")

    # 7. Sample Output from Executive View
    print("\n" + "-" * 60)
    print("[VIEW SAMPLE] PREVIEW FROM vw_monthly_executive_summary")
    print("-" * 60)
    sample_view_df = pd.read_sql("SELECT * FROM vw_monthly_executive_summary LIMIT 5", conn)
    print(tabulate(sample_view_df, headers="keys", tablefmt="github", showindex=False))

    conn.close()
    print("\n" + "=" * 60)
    print("✨ STEP 3 SQL INTEGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    build_database()
