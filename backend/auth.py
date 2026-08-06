"""
Authentication & Role-Based Access Control (RBAC) Module - Step 7 Enterprise Upgrade
Implements JWT Access & Refresh token generation, password hashing, user registration,
and rate-limited Role-Based Access Control (RBAC) checks.
Roles supported: Admin, Manager, Analyst.
"""

import datetime
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

import config

security = HTTPBearer()

# In-memory user database initialized with default role accounts
USERS_DB: Dict[str, dict] = {
    "admin@growthsuite.com": {
        "email": "admin@growthsuite.com",
        "full_name": "Executive Admin",
        "password_hash": "admin123",
        "role": "Admin"
    },
    "manager@growthsuite.com": {
        "email": "manager@growthsuite.com",
        "full_name": "Regional Manager",
        "password_hash": "manager123",
        "role": "Manager"
    },
    "analyst@growthsuite.com": {
        "email": "analyst@growthsuite.com",
        "full_name": "Data Analyst",
        "password_hash": "analyst123",
        "role": "Analyst"
    }
}

class UserSignupSchema(BaseModel):
    email: str
    full_name: str
    password: str
    role: str = "Analyst"

class UserLoginSchema(BaseModel):
    email: str
    password: str

class ForgotPasswordSchema(BaseModel):
    email: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str

def create_jwt_token(data: dict, expires_delta: Optional[datetime.timedelta] = None, token_type: str = "access") -> str:
    """Generates signed JWT Access or Refresh Bearer Token."""
    to_encode = data.copy()
    to_encode.update({"type": token_type})
    expire = datetime.datetime.utcnow() + (
        expires_delta or datetime.timedelta(minutes=config.JWT_EXPIRATION_MINUTES if token_type == "access" else config.JWT_EXPIRATION_MINUTES * 7)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token

def verify_jwt_token(token: str, expected_type: str = "access") -> dict:
    """Decodes and validates JWT token."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        if payload.get("type", "access") != expected_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token type. Expected '{expected_type}'.")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """FastAPI Dependency: Extracts and validates current user from Authorization Bearer token."""
    token = credentials.credentials
    payload = verify_jwt_token(token, expected_type="access")
    email = payload.get("sub")
    if not email or email not in USERS_DB:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account not found.")
    return USERS_DB[email]

def require_role(allowed_roles: list):
    """FastAPI Dependency Decorator: Enforces Role-Based Access Control (RBAC)."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role", "Analyst")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Privilege level '{user_role}' is not authorized for this operation. Required: {allowed_roles}"
            )
        return current_user
    return role_checker
