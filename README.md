## ML Image Prediction API

A production‑style ML prediction API built with FastAPI and a Keras image classification model, containerized with Docker and orchestrated with Docker Compose. The project also includes a basic CI/CD pipeline using GitHub Actions to run tests and build a Docker image on every push to main.
​
## Features

1. RESTful health and predict endpoints built with FastAPI.
​
2. Loads a pre‑trained Keras .h5 image classification model from the models directory.
​
3. Image preprocessing (resize, normalize) consistent with model input expectations.
​
4. Dockerized application with a multi‑stage Dockerfile for a smaller runtime image.
​
​5. docker-compose.yml for simple local startup using docker compose up --build.
​
​6. GitHub Actions workflow for basic CI: install dependencies, run tests, and build the Docker image.
​
7. predictions/ directory with example JSON outputs from successful /predict calls.
​
## Project Structure

your-ml-api/
├─ .github/
│  └─ workflows/
│     └─ main.yml              # GitHub Actions CI/CD pipeline
├─ models/
│  └─ my_classifier_model.h5   # Trained Keras model
├─ predictions/
│  └─ example_prediction.json  # Example prediction output
├─ src/
│  ├─ __init__.py
│  ├─ main.py                  # FastAPI app and endpoints
│  └─ model.py                 # Model loading & preprocessing logic
├─ tests/
│  └─ test_api.py              # Basic API tests with pytest
├─ .env.example                # Example environment variables
├─ conftest.py                 # Makes src importable in tests
├─ Dockerfile                  # Multi-stage Docker image build
├─ docker-compose.yml          # Local compose configuration
├─ requirements.txt            # Python dependencies
├─ train_model.py              # Helper script to create the model file
└─ README.md

## Setup (Local Python + venv): 

1. Clone the repo

git clone https://github.com/N-Haritha16/image-classification-api-mlops
cd your-ml-api

2. Create and activate virtual environment (Windows)

python -m venv .venv
.venv\Scripts\activate
Install dependencies

pip install -r requirements.txt
Run tests

pytest tests/
Start the API locally (without Docker)

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
The API will be available at:

Health: http://localhost:8000/health

Docs (Swagger UI): http://localhost:8000/docs
​
## Docker Usage

Make sure Docker Desktop is installed and running.

1. Build the Docker image
From the project root:

docker build -t my-ml-api:latest .
Verify:

docker images

2. Run the container directly (optional)

docker run --rm -p 8000:8000 ^
  -e MODELPATH=/app/models/my_classifier_model.h5 ^
  -e LOGLEVEL=INFO ^
  my-ml-api:latest

3. Test in another terminal:

curl http://localhost:8000/health
curl -X POST "http://localhost:8000/predict" -F "file=@sample.png"
Stop with Ctrl + C.

3. Run with Docker Compose (recommended)

From the project root:

docker compose up --build
This will:

Build the my-ml-api image using the Dockerfile.

Start the ml_api service defined in docker-compose.yml on port 8000.
​
Test:

curl http://localhost:8000/health
curl -X POST "http://localhost:8000/predict" -F "file=@sample.png"
To stop:

## docker compose down

API Endpoints
Health Check
Method: GET

URL: /health

Example:

bash
curl http://localhost:8000/health
Example response:

json
{
  "status": "ok",
  "message": "API is healthy and model is loaded."
}
Prediction
Method: POST

URL: /predict

Body: multipart/form-data with an image file field named file (e.g. JPEG/PNG).
​

Example:

bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample.png"
Example response (values will vary):

json
{
  "class_label": "class_7",
  "probabilities": [0.10, 0.09, 0.11, 0.11, 0.09, 0.08, 0.06, 0.12, 0.09, 0.11]
}

## Environment Variables

These are configured via .env.example and/or Docker environment variables.​

MODELPATH – path to the Keras model inside the container

default: /app/models/my_classifier_model.h5

LOGLEVEL – logging level (INFO, DEBUG, etc.)

## In docker-compose.yml:

text
environment:
  MODELPATH: /app/models/my_classifier_model.h5
  LOGLEVEL: DEBUG
CI/CD with GitHub Actions
The workflow .github/workflows/main.yml runs on:

push to main

pull_request targeting main
​

## It performs:

Checks out the repository.

Sets up Python (3.9).

Installs dependencies with pip install -r requirements.txt.

Runs tests with pytest.

Builds the Docker image with docker build -t my-ml-api:${{ github.sha }} ..

Contains optional (simulated) login/push steps to a container registry.

Creates example prediction files in predictions/ and uploads them as a workflow artifact.
​
You can see workflow runs and artifacts under the Actions tab of the GitHub repository.

Predictions Directory

The predictions/ folder in the repository root contains example JSON outputs from successful POST /predict calls, e.g.:

## predictions/example_prediction.json:

json
{
  "class_label": "class_7",
  "probabilities": [0.10, 0.09, 0.11, 0.11, 0.09, 0.08, 0.06, 0.12, 0.09, 0.11]
}
These files demonstrate sample model outputs and are also used as artifacts in the CI pipeline.
​

## Future Improvements

More robust integration tests (end‑to‑end prediction with real images).
​
Containerized tests executed inside Docker as part of CI.
​
Advanced logging, monitoring, and model versioning.
​
Deployment to a cloud environment (e.g., AWS ECS, Azure Container Apps, or Kubernetes) using the same Docker image.
​

