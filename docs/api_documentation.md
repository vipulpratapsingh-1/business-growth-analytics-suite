# REST API & Enterprise Web Architecture Documentation

**Base API URL**: `http://localhost:8000/api`  
**Swagger UI Documentation**: `http://localhost:8000/docs`  
**ReDoc Documentation**: `http://localhost:8000/redoc`  
**Security**: OAuth2 HTTP Bearer JWT Authentication with Role-Based Access Control (RBAC)

---

## 1. Authentication & Role-Based Access Control (RBAC)

The system supports three user privilege tiers:

| Role Name | Access Privileges | Default Test Account |
| :--- | :--- | :--- |
| **Admin** | Full system permissions (Upload CSV, Trigger ML, Run SQL, Execute Cleaning) | `admin@growthsuite.com` / `admin123` |
| **Manager** | Operational permissions (Upload CSV, Run Cleaning, Analytics & ML Inference) | `manager@growthsuite.com` / `manager123` |
| **Analyst** | Read-only analytics permissions + Custom SQL Execution | `analyst@growthsuite.com` / `analyst123` |

### Authentication Endpoints

#### `POST /api/auth/login`
- **Description**: Authenticates user credentials and returns JWT bearer token.
- **Request Body**:
  ```json
  {
    "email": "admin@growthsuite.com",
    "password": "admin123"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "bearer",
    "user": {
      "email": "admin@growthsuite.com",
      "full_name": "Executive Admin",
      "role": "Admin"
    }
  }
  ```

#### `POST /api/auth/signup`
- **Description**: Registers a new user account with assigned role (`Admin`, `Manager`, `Analyst`).

#### `GET /api/auth/me`
- **Description**: Validates active JWT token and returns current user session profile.

---

## 2. Analytics & Business Intelligence Endpoints

#### `GET /api/analytics/executive`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Returns top-level KPIs (Total Sales, Total Profit, Profit Margin %, AOV) and 24-month revenue trends.

#### `GET /api/analytics/sales`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Returns product category breakdown, state sales leaderboard, top 10 cities, top 10 products, and bottom 10 products.

#### `GET /api/analytics/customers`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Returns total customer profiles, repeat vs single purchase retention ratios, and top 10 CLV account leaderboards.

#### `GET /api/analytics/financials`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Returns discount tier margin impact and payment method transaction share.

#### `POST /api/analytics/sql`
- **Header**: `Authorization: Bearer <token>` (Requires `Admin` or `Analyst` role)
- **Description**: Executes custom SELECT/WITH SQL queries directly against `BusinessGrowthDB.sqlite`.
- **Request Body**:
  ```json
  {
    "sql_query": "SELECT city, SUM(sales_amount) FROM Orders o JOIN Sales s ON o.order_id = s.order_id GROUP BY city LIMIT 5;"
  }
  ```

---

## 3. Machine Learning Inference Endpoints

#### `POST /api/ml/forecast`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Generates time-series sales predictions for specified month horizons (3, 6, 12 months).
- **Request Body**: `{ "horizon_months": 6 }`

#### `POST /api/ml/churn`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Evaluates customer churn probability score and risk level for a specific customer ID.
- **Request Body**: `{ "customer_id": "CUST-10001" }`

#### `GET /api/ml/segments`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Retrieves K-Means RFM customer clusters (Champions, Loyal Buyers, At-Risk Customers).

#### `POST /api/ml/recommend`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Returns top-N cross-sell product recommendations based on item co-occurrence similarity.
- **Request Body**: `{ "product_name": "MacBook Pro 16-inch", "top_n": 3 }`

---

## 4. Dataset Management Endpoints

#### `POST /api/dataset/upload`
- **Header**: `Authorization: Bearer <token>` (Requires `Admin` or `Manager` role)
- **Description**: Uploads a new raw sales dataset CSV file (`multipart/form-data`).

#### `POST /api/dataset/clean`
- **Header**: `Authorization: Bearer <token>` (Requires `Admin` or `Manager` role)
- **Description**: Triggers the automated data cleaning and validation pipeline.

#### `GET /api/dataset/download`
- **Header**: `Authorization: Bearer <token>`
- **Description**: Downloads the clean sales dataset CSV file (`clean_sales_data.csv`).

---
*Documentation generated for Step 6 of Business Growth Analytics Suite.*
