# ---------- Stage 1: Build / install dependencies ----------
FROM python:3.9-slim-buster AS builder

# Set working directory
WORKDIR /app

# Install system deps if needed (optional – uncomment if TensorFlow complains)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: Runtime image ----------
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy application source code and model
COPY src/ ./src/
COPY models/ ./models/
COPY .env.example ./.env.example

# Environment variables
ENV MODELPATH=/app/models/my_classifier_model.h5
ENV LOGLEVEL=INFO

# Expose API port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
