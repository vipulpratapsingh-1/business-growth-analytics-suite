"""
API Testing Suite - Step 7 Enterprise Production Upgrade
Tests FastAPI REST endpoints, JWT authentication, RBAC permissions, and health monitoring.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config
from backend.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Test /health liveness probe."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_metrics_endpoint():
    """Test /metrics monitoring endpoint."""
    res = client.get("/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "total_requests_processed" in data

def test_auth_login_success():
    """Test POST /api/auth/login credentials authentication."""
    res = client.post("/api/auth/login", json={"email": "admin@growthsuite.com", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["role"] == "Admin"

def test_auth_login_invalid_credentials():
    """Test POST /api/auth/login with wrong password."""
    res = client.post("/api/auth/login", json={"email": "admin@growthsuite.com", "password": "wrongpassword"})
    assert res.status_code == 401

def test_protected_analytics_endpoint_unauthorized():
    """Test protected GET /api/analytics/executive fails without JWT token."""
    res = client.get("/api/analytics/executive")
    assert res.status_code == 403 or res.status_code == 401

def test_protected_analytics_endpoint_authorized():
    """Test protected GET /api/analytics/executive with valid JWT token."""
    login_res = client.post("/api/auth/login", json={"email": "admin@growthsuite.com", "password": "admin123"})
    token = login_res.json()["access_token"]

    res = client.get("/api/analytics/executive", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert data["kpis"]["total_orders"] == 100000

def test_sql_execution_endpoint_rbac():
    """Test custom SQL execution via POST /api/analytics/sql."""
    login_res = client.post("/api/auth/login", json={"email": "admin@growthsuite.com", "password": "admin123"})
    token = login_res.json()["access_token"]

    query = "SELECT city, COUNT(order_id) FROM Orders GROUP BY city LIMIT 5;"
    res = client.post(
        "/api/analytics/sql",
        headers={"Authorization": f"Bearer {token}"},
        json={"sql_query": query}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 5
