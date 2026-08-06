"""
Business Growth Analytics Suite - Configuration Module
Centralized configuration settings for paths, data generation parameters, and constants.
"""

import os
from pathlib import Path

# Base Directory (Project Root)
BASE_DIR = Path(__file__).resolve().parent

# Directory Paths
DATA_DIR = BASE_DIR / "data"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SQL_DIR = BASE_DIR / "sql"
SCRIPTS_DIR = BASE_DIR / "scripts"
DASHBOARD_DIR = BASE_DIR / "dashboard"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
DOCS_DIR = BASE_DIR / "docs"

# ML & Web Paths
ML_DIR = BASE_DIR / "ml"
ML_MODELS_DIR = ML_DIR / "models"
ML_REPORTS_DIR = REPORTS_DIR / "ml"
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

# File Paths
DATASET_PATH = DATA_DIR / "sales_data.csv"
CLEAN_DATASET_PATH = DATA_DIR / "clean_sales_data.csv"
DB_PATH = DATA_DIR / "BusinessGrowthDB.sqlite"
EDA_REPORT_PATH = REPORTS_DIR / "EDA_Report.md"
SQL_DOCS_PATH = DOCS_DIR / "sql_documentation.md"
DAX_FILE_PATH = DASHBOARD_DIR / "dax_measures.dax"
POWERBI_DOCS_PATH = DOCS_DIR / "powerbi_dashboard_guide.md"
ML_REPORT_PATH = REPORTS_DIR / "ML_Report.md"
API_DOCS_PATH = DOCS_DIR / "api_documentation.md"

# Dataset Generation Settings
TOTAL_ROWS = 100_000
RANDOM_SEED = 42
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

# JWT Auth Secret
JWT_SECRET_KEY = "enterprise_growth_analytics_secret_key_2026"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24

# Create directories if they do not exist
DIRECTORIES = [
    DATA_DIR,
    NOTEBOOKS_DIR,
    SQL_DIR,
    SCRIPTS_DIR,
    DASHBOARD_DIR,
    REPORTS_DIR,
    CHARTS_DIR,
    DOCS_DIR,
    ML_DIR,
    ML_MODELS_DIR,
    ML_REPORTS_DIR,
    BACKEND_DIR,
]

def ensure_directories_exist():
    """Ensure all core project folders exist."""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    ensure_directories_exist()
    print("Project directory structure verified.")
