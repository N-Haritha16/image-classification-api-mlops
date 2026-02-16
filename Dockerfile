# Dockerfile
# Stage 1: Build environment for installing dependencies
FROM python:3.9-slim-buster as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Minimal runtime environment
FROM python:3.9-slim-buster

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy application source code and model artifacts
COPY src/ ./src/
COPY models/ ./models/
COPY .env.example ./ .env.example  # example only; real .env will be mounted or provided

EXPOSE 8000

ENV MODEL_PATH=/app/models/my_classifier_model.h5
ENV LOG_LEVEL=INFO

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
