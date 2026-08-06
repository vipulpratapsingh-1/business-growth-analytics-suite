# Multi-Stage Production Dockerfile for Business Growth Analytics Suite

FROM python:3.10-slim as builder

WORKDIR /app

# Prevent python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project source code
COPY . .

# Run initial pipeline tasks to ensure database and ML models are pre-compiled
RUN python main.py && \
    python scripts/data_cleaning.py && \
    python scripts/sql_integration.py && \
    python scripts/run_ml_pipeline.py

EXPOSE 8000

# Healthcheck for container liveness probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
