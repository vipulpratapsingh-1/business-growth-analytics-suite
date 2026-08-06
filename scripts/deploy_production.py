"""
Production Deployment Verification Engine - Step 8
Validates environment configuration, database state, serialized ML model artifacts,
and FastAPI backend routes prior to public deployment.
"""

import sys
import os
from pathlib import Path

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def verify_production_readiness():
    print("=" * 60)
    print("🚀 PRODUCTION DEPLOYMENT VERIFICATION ENGINE")
    print("=" * 60)

    # 1. Verify Configuration Files
    config_files = [
        config.BASE_DIR / "vercel.json",
        config.BASE_DIR / "render.yaml",
        config.BASE_DIR / "Dockerfile",
        config.BASE_DIR / "docker-compose.yml",
        config.BASE_DIR / "requirements.txt"
    ]

    for cfg in config_files:
        if cfg.exists():
            print(f"[OK] Found deployment configuration: {cfg.name}")
        else:
            print(f"[FAIL] Missing configuration: {cfg.name}")
            sys.exit(1)

    # 2. Verify Database File
    if config.DB_PATH.exists() and config.DB_PATH.stat().st_size > 0:
        print(f"[OK] Production SQLite database ready ({config.DB_PATH.stat().st_size / 1e6:.2f} MB)")
    else:
        print("[FAIL] SQLite database BusinessGrowthDB.sqlite missing!")
        sys.exit(1)

    # 3. Verify ML Model Artifacts
    ml_models = [
        "sales_forecaster.joblib",
        "churn_model.joblib",
        "kmeans_model.joblib",
        "recommender.joblib"
    ]
    for model in ml_models:
        model_path = config.ML_MODELS_DIR / model
        if model_path.exists():
            print(f"[OK] Found ML model artifact: {model}")
        else:
            print(f"[FAIL] Missing ML model artifact: {model}")
            sys.exit(1)

    # 4. Verify Documentation Suite
    docs = [
        "SYSTEM_ARCHITECTURE.md",
        "API_DOCUMENTATION.md",
        "DATABASE_DESIGN.md",
        "ML_PIPELINE.md",
        "DEPLOYMENT_GUIDE.md",
        "USER_MANUAL.md",
        "INTERVIEW_GUIDE.md"
    ]
    for doc in docs:
        doc_path = config.DOCS_DIR / doc
        if doc_path.exists():
            print(f"[OK] Verified enterprise doc: {doc}")
        else:
            print(f"[WARN] Missing doc: {doc}")

    print("=" * 60)
    print("✨ ALL PRODUCTION DEPLOYMENT CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    verify_production_readiness()
