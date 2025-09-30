FROM python:3.11-slim

WORKDIR /app

# Copy and install backend requirements
COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copy application code
COPY . .

# Start FastAPI app
CMD uvicorn main:app --host 0.0.0.0 --port $PORT