# BuildAtlas AI

## Overview

BuildAtlas AI is an end-to-end AI-powered construction planning platform designed to simplify house construction, cost estimation, material procurement, and project management.

## Key Features

* AI Floor Plan Generator
* Construction Cost Estimation
* Material Marketplace
* Supplier Comparison
* Procurement & Quote System
* OCR Bill Scanner
* AI Construction Assistant
* Vastu Intelligence
* Construction Progress Tracking

## Technology Stack

* Python
* Streamlit
* Pandas
* Plotly
* Scikit-Learn
* Google Gemini AI
* Supabase PostgreSQL

## Project Structure

* hackathon.py (Main Application)
* cost_model.pkl
* model_columns.pkl
* generate_dataset.py
* train_model.py
* requirement.txt (existing Streamlit dependencies)
* backend/ (FastAPI migration foundation)
* frontend/ (React + Vite migration shell)
* ml/ (reserved for future model extraction)

## How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Run the application:

streamlit run hackathon1.py

### Supabase setup

Run [`supabase_schema.sql`](supabase_schema.sql) in the Supabase SQL editor. Add these values to `.streamlit/secrets.toml` locally and to Streamlit Community Cloud secrets:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your-server-side-key"
```

The app uses Supabase as the authoritative store for accounts, role profiles, products, inventory, enquiries, quotations, orders, deliveries, reviews, and project quote requests. Passwords and OTPs are never stored in plaintext. `buildatlas_users.json` and `buildatlas_quote_requests.json` are retained only for an explicitly enabled local migration fallback:

```powershell
$env:BUILDATLAS_ALLOW_LOCAL_FILE_FALLBACK = "true"
```

Do not enable that fallback in production. Do not commit `.streamlit/secrets.toml` or `.env`.


## Migration Foundation

The existing Streamlit app remains the reference and fallback application. The new React shell preserves the approved BuildAtlas navigation and visual language, while the FastAPI service currently exposes only `/api/health`.

### Run the backend

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Copy `backend/.env.example` to `backend/.env` and provide integration credentials only when the corresponding module is migrated.

### Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env` to configure `VITE_API_BASE_URL`.

The conceptual layout generator and floor-plan engine are deliberately excluded from the migration shell. No database migration has been started.

## Team

BuildAtlas AI Development Team

## Future Scope

* Live Builder Marketplace
* Real-time Material Pricing
* Advanced Construction Monitoring
* Smart Procurement Optimization
