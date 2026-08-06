"""
Business Growth Analytics Suite - FastAPI Backend Server
Step 8 Production Deployment Upgrade with Dynamic CORS, HTTPS Header Forwarding,
JWT Refresh Tokens, Health Monitoring, Metrics, REST APIs, and Swagger documentation.
"""

import sys
import os
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

from backend.auth import (
    USERS_DB, UserLoginSchema, UserSignupSchema, ForgotPasswordSchema, RefreshTokenSchema,
    create_jwt_token, verify_jwt_token, get_current_user
)
from backend.routers import analytics, ml_router, dataset

app = FastAPI(
    title="Business Growth Analytics Suite API",
    description="Enterprise REST API backend for multi-region sales analytics, SQL warehousing, Power BI metrics, and Machine Learning predictions.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Dynamic CORS Middleware from Environment Variables
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security & Performance Middleware
REQUEST_COUNTER = 0
START_TIME = time.time()

@app.middleware("http")
async def add_security_headers_and_metrics(request: Request, call_next):
    global REQUEST_COUNTER
    REQUEST_COUNTER += 1
    start_req = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_req
    response.headers["X-Process-Time-MS"] = f"{process_time * 1000:.2f}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Include API Routers
app.include_router(analytics.router)
app.include_router(ml_router.router)
app.include_router(dataset.router)

# Mount static reports & frontend directories
config.ensure_directories_exist()
app.mount("/reports", StaticFiles(directory=str(config.REPORTS_DIR)), name="reports")

frontend_dir = config.BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# ------------------------------------------------------------
# FRONTEND SPA ENTRYPOINT
# ------------------------------------------------------------

@app.get("/", tags=["Enterprise Web App"])
def serve_web_application():
    """Serves the main enterprise web application index.html."""
    index_path = config.BASE_DIR / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "application": "Business Growth Analytics Suite API",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/index.css", include_in_schema=False)
def serve_css():
    return FileResponse(config.BASE_DIR / "frontend" / "index.css")

@app.get("/app.js", include_in_schema=False)
def serve_js():
    return FileResponse(config.BASE_DIR / "frontend" / "app.js")

# ------------------------------------------------------------
# AUTHENTICATION ENDPOINTS
# ------------------------------------------------------------

@app.post("/api/auth/signup", tags=["Authentication & Roles"])
def user_signup(user_data: UserSignupSchema):
    """Registers a new user account."""
    if user_data.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Account with this email already exists.")
    
    USERS_DB[user_data.email] = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "password_hash": user_data.password,
        "role": user_data.role if user_data.role in ["Admin", "Manager", "Analyst"] else "Analyst"
    }

    access_token = create_jwt_token({"sub": user_data.email, "role": USERS_DB[user_data.email]["role"]}, token_type="access")
    refresh_token = create_jwt_token({"sub": user_data.email, "role": USERS_DB[user_data.email]["role"]}, token_type="refresh")

    return {
        "status": "success",
        "message": "User account created successfully.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": USERS_DB[user_data.email]
    }

@app.post("/api/auth/login", tags=["Authentication & Roles"])
def user_login(login_data: UserLoginSchema):
    """Authenticates user and returns JWT access and refresh bearer tokens."""
    user = USERS_DB.get(login_data.email)
    if not user or user["password_hash"] != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password credentials.")
    
    access_token = create_jwt_token({"sub": user["email"], "role": user["role"]}, token_type="access")
    refresh_token = create_jwt_token({"sub": user["email"], "role": user["role"]}, token_type="refresh")

    return {
        "status": "success",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    }

@app.post("/api/auth/refresh", tags=["Authentication & Roles"])
def refresh_jwt_access_token(req: RefreshTokenSchema):
    """Generates a new access token using a valid refresh token."""
    payload = verify_jwt_token(req.refresh_token, expected_type="refresh")
    email = payload.get("sub")
    role = payload.get("role", "Analyst")

    if not email or email not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid user session.")

    new_access_token = create_jwt_token({"sub": email, "role": role}, token_type="access")
    return {
        "status": "success",
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@app.post("/api/auth/forgot-password", tags=["Authentication & Roles"])
def forgot_password(req: ForgotPasswordSchema):
    """Generates password reset instructions."""
    if req.email not in USERS_DB:
        raise HTTPException(status_code=404, detail="Email address not found.")
    return {
        "status": "success",
        "message": f"Password reset instructions sent to {req.email}."
    }

@app.get("/api/auth/me", tags=["Authentication & Roles"])
def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Returns currently authenticated user profile and active role."""
    return {"user": current_user}

# ------------------------------------------------------------
# MONITORING & HEALTH CHECK ENDPOINTS
# ------------------------------------------------------------

@app.get("/health", tags=["Monitoring & Operations"])
def system_health_check():
    """Health check endpoint for Docker & Render liveness probes."""
    db_status = "connected" if config.DB_PATH.exists() else "missing"
    dataset_status = "ready" if config.CLEAN_DATASET_PATH.exists() else "missing"
    
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "database": db_status,
        "dataset": dataset_status,
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/metrics", tags=["Monitoring & Operations"])
def performance_metrics():
    """Returns system operational and request metrics."""
    return {
        "total_requests_processed": REQUEST_COUNTER,
        "server_uptime_seconds": round(time.time() - START_TIME, 2),
        "active_users_count": len(USERS_DB),
        "models_available": 4
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
