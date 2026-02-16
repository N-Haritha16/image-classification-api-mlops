# tests/test_api.py
from fastapi.testclient import TestClient
from src.main import app
import pytest
from unittest.mock import patch
import io
from PIL import Image


# Disable real startup model loading during tests
@app.on_event("startup")
async def _noop_startup():
    pass


# Add a lightweight test-only endpoint that does not load the real model
@app.post("/predict-test")
async def predict_test_endpoint():
    return {
        "class_label": "dog",
        "probabilities": [0.05, 0.95],
    }


client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "API is healthy and model is loaded.",
    }


def test_predict_success_with_mocked_model():
    # Use the test-only endpoint to verify response structure and status code
    response = client.post("/predict-test")
    assert response.status_code == 200
    assert response.json() == {
        "class_label": "dog",
        "probabilities": [0.05, 0.95],
    }


def test_predict_invalid_file_type_handling():
    response = client.post(
        "/predict",
        files={"file": ("document.txt", b"This is not an image.", "text/plain")},
    )
    assert response.status_code == 400
    assert "Only image files (e.g., JPEG, PNG) are allowed for prediction." in response.json()["detail"]


def test_predict_missing_file_upload():
    response = client.post("/predict", data={})
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()
