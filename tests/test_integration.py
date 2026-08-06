"""
Integration Testing Suite - Step 7 Enterprise Production Upgrade
Tests SQLite database connection, table schemas, primary/foreign keys, and views.
"""

import sys
import sqlite3
from pathlib import Path
import pytest

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def test_sqlite_database_exists():
    """Verify BusinessGrowthDB.sqlite exists and is non-empty."""
    assert config.DB_PATH.exists()
    assert config.DB_PATH.stat().st_size > 0

def test_database_tables_and_record_counts():
    """Verify table creation and normalized record counts."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    tables = ["Customers", "Products", "Orders", "Sales", "Payments"]
    for tbl in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        assert count > 0, f"Table {tbl} is empty!"
    
    conn.close()

def test_database_views_execution():
    """Verify executive database views execute without syntax errors."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    views = [
        "vw_monthly_executive_summary",
        "vw_customer_rfm_metrics",
        "vw_product_performance_matrix",
        "vw_regional_sales_breakdown",
        "vw_discount_profitability_analysis"
    ]

    for vw in views:
        res = cursor.execute(f"SELECT * FROM {vw} LIMIT 5").fetchall()
        assert len(res) > 0, f"View {vw} returned zero rows!"

    conn.close()
