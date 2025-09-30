FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better Docker layer caching)
COPY requirements-backend.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE $PORT

# Start command
CMD uvicorn main:app --host 0.0.0.0 --port $PORT