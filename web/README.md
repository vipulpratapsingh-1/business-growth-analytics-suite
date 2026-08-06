# Enterprise Web Application - Setup & Deployment Guide

This directory documents the full-stack Web Application for **Business Growth Analytics Suite**.

## 🚀 Quickstart Guide

### 1. Start FastAPI Server
Run the following command from the project root directory:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. Access Web Application
Open your browser and navigate to:
- **Web App Interface**: `http://localhost:8000/`
- **Interactive Swagger API Docs**: `http://localhost:8000/docs`
- **ReDoc API Docs**: `http://localhost:8000/redoc`

---

## 🔐 Default Test Accounts

| Email Address | Password | Role | Privileges |
| :--- | :--- | :--- | :--- |
| `admin@growthsuite.com` | `admin123` | **Admin** | Full system access (Upload CSV, Clean Data, SQL Console, ML Models) |
| `manager@growthsuite.com` | `manager123` | **Manager** | Operations access (Upload CSV, Clean Data, View Analytics & ML) |
| `analyst@growthsuite.com` | `analyst123` | **Analyst** | Read-only analytics access + Custom SQL Execution |

---

## 🎨 Enterprise UI Architecture
- **Theme**: Fortune 500 Modern Corporate Glassmorphism
- **Color Palette**: Corporate Navy (`#1E3A8A`), Cyan Accent (`#0EA5E9`), Slate Gray (`#64748B`), White (`#FFFFFF`)
- **Features**: Single Page Application, JWT Bearer Token Security, Live Chart.js visualizations, Drag-and-Drop CSV Uploader, ML Inference Calculator, SQL Execution Console.
