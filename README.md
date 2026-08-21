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

1. Install existing Streamlit dependencies:

pip install -r requirement.txt

2. Run the application:

streamlit run hackathon.py

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
