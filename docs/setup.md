# Local Setup Guide

## Backend Setup

```bash
cd server

# Create virtual environment
python -m venv env
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database tables (one time)
python -m db.models

# Run server
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

---

## Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`
