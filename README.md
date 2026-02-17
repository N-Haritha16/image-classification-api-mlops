## ML Image Prediction API

A production-style ML Prediction API built with FastAPI and a Keras image classification model, containerized with Docker and orchestrated with Docker Compose. The project includes a basic CI/CD pipeline using GitHub Actions to run tests and build a Docker image on every push to main.
​
​## Features

RESTful health and predict endpoints using FastAPI.

Loads a pre-trained Keras .h5 image classification model from the models directory.

Image preprocessing (resize, normalize) consistent with model training.

Dockerized application with a multi-stage Dockerfile for smaller images.

docker-compose.yml for simple local startup using docker-compose up --build.
​
​
GitHub Actions workflow for basic CI: install deps, run tests, build Docker image.

predictions directory with example JSON outputs from successful predict calls.
​

## Project Structure

text
your-ml-api/
├─ .github/
│  └─ workflows/
│     └─ main.yml           # GitHub Actions CI/CD pipeline
├─ models/
│  └─ my_classifier_model.h5
├─ predictions/
│  └─ example_prediction.json
├─ src/
│  ├─ __init__.py
│  ├─ main.py               # FastAPI app, endpoints
│  └─ model.py              # Model loading & preprocessing
├─ tests/
│  └─ test_api.py           # Basic API tests with pytest
├─ .env.example             # Example environment variables
├─ Dockerfile               # Multi-stage Docker image build
├─ docker-compose.yml       # Local compose configuration
├─ requirements.txt         # Python dependencies
└─ README.md
Setup (Local Python + venv)

Clone the repo:
bash
git clone https://github.com/N-Haritha16/image-classification-api-mlops
cd your-ml-api

Create and activate virtual environment (Windows):

bash
python -m venv .venv
.venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Run tests:

bash
python -m pytest
Start the API locally (without Docker):

bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
The API will be available at:

Health: http://localhost:8000/health

Docs (Swagger UI): http://localhost:8000/docs
​

Docker Usage
Make sure Docker Desktop is installed and running.
​

1. Build the Docker image
From the project root:

bash
docker build -t my-ml-api:latest .
You can verify:

bash
docker images
2. Run the container directly (optional)
bash
docker run --rm -p 8000:8000 ^
  -e MODELPATH=/app/models/my_classifier_model.h5 ^
  -e LOGLEVEL=INFO ^
  my-ml-api:latest
Now test in another terminal:

bash
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/predict" -F "file=@sample.png"
Stop with Ctrl + C.

3. Run with Docker Compose (recommended)
From the project root:

bash
docker-compose up --build
This will:

Build the my-ml-api image using the Dockerfile.

Start the ml_api service defined in docker-compose.yml on port 8000.
​

## Test:

bash
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/predict" -F "file=@sample.png"
To stop:

bash
docker-compose down
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

Body: multipart form-data with an image file field named file (JPEG/PNG).
​
​

Example:

bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample.png"
Example response:

json
{
  "class_label": "cat",
  "probabilities": [0.8, 0.2]
}
Environment Variables
These are configured via .env.example and/or Docker environment variables.
​

MODELPATH – path to the Keras model inside the container

default: /app/models/my_classifier_model.h5

LOGLEVEL – logging level (INFO, DEBUG, etc.)

In docker-compose.yml:

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

Checkout the repository.

Set up Python (3.9).

pip install -r requirements.txt.

pytest to run unit tests.

docker build -t my-ml-api:${{ github.sha }} . to build the image.

Optional (simulated) login and push steps to a container registry.

Create example prediction files in predictions/ and upload them as a workflow artifact.
​
​

You can see workflow runs and download artifacts under the Actions tab of the GitHub repository.
​

## Predictions Directory

The predictions folder in the repository root contains example JSON outputs from successful POST /predict calls, e.g.:

predictions/example_prediction.json:

json
{
  "class_label": "cat",
  "probabilities": [0.8, 0.2]
}
These files demonstrate sample model outputs and are also used as artifacts in the CI pipeline.
​

## Future Improvements

More robust integration tests (end-to-end prediction with real images).

Containerized tests executed inside Docker as part of CI.

Advanced logging, monitoring, and model versioning.

Deployment to a cloud environment (e.g., AWS/ECS or similar) using the same Docker image.
​
​

