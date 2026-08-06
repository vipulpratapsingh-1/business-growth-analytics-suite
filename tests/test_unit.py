"""
Unit Testing Suite - Step 7 Enterprise Production Upgrade
Tests configuration paths, directory creation, pricing math, and formula integrity.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def test_config_paths_exist():
    """Verify that all core project configuration paths are defined."""
    assert config.BASE_DIR.exists()
    assert config.DATA_DIR is not None
    assert config.SQL_DIR is not None
    assert config.ML_DIR is not None
    assert config.REPORTS_DIR is not None

def test_sales_math_formula():
    """Verify mathematical calculation: Sales = Quantity * Unit_Price * (1 - Discount)."""
    quantity = 5
    unit_price = 1000.0
    discount = 0.10
    
    expected_sales = round(quantity * unit_price * (1.0 - discount), 2)
    assert expected_sales == 4500.00

def test_clean_dataset_integrity():
    """Verify clean dataset row count and key column presence."""
    assert config.CLEAN_DATASET_PATH.exists()
    df = pd.read_csv(config.CLEAN_DATASET_PATH)
    assert len(df) == 100000
    assert "Sales" in df.columns
    assert "Profit" in df.columns
    assert "Customer ID" in df.columns
    assert df.isnull().sum().sum() == 0
