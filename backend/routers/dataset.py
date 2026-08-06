"""
Dataset Management REST API Router - Step 6
Handles CSV file uploads, automated data cleaning execution, and dataset exports.
"""

import shutil
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

import config
from backend.auth import require_role
from scripts.data_cleaning import clean_dataset

router = APIRouter(prefix="/api/dataset", tags=["Dataset Management Engine"])

@router.post("/upload")
def upload_sales_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_role(["Admin", "Manager"]))
):
    """Uploads a new raw sales dataset CSV file."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV format files are allowed.")

    config.ensure_directories_exist()
    destination = config.DATASET_PATH

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "message": f"Successfully uploaded '{file.filename}' to raw data directory.",
        "saved_path": str(destination)
    }

@router.post("/clean")
def trigger_data_cleaning(
    current_user: dict = Depends(require_role(["Admin", "Manager"]))
):
    """Triggers the automated data cleaning and validation pipeline."""
    try:
        df_clean = clean_dataset()
        return {
            "status": "success",
            "message": "Data cleaning pipeline executed successfully.",
            "clean_row_count": len(df_clean),
            "output_file": str(config.CLEAN_DATASET_PATH)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data cleaning failed: {str(e)}")

@router.get("/download")
def download_clean_dataset(current_user: dict = Depends(require_role(["Admin", "Manager", "Analyst"]))):
    """Downloads the cleaned sales dataset CSV file."""
    if not config.CLEAN_DATASET_PATH.exists():
        raise HTTPException(status_code=404, detail="Clean dataset file not found.")
    
    return FileResponse(
        path=config.CLEAN_DATASET_PATH,
        filename="clean_sales_data.csv",
        media_type="text/csv"
    )
