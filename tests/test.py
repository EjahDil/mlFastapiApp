# tests/test_main.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..mainls import appls

client = TestClient(appls)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_models():
    response = client.get("/models")
    assert response.status_code == 200
    json_data = response.json()
    assert "available_models" in json_data
    assert isinstance(json_data["available_models"], list)


# def test_prediction_invalid_model():
#     payload = {"model_name": "invalid_model", "inputs": [1, 2, 3]}
#     response = client.post("/predict", json=payload)
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Model not found"


# def test_prediction_valid_model(mocker):
#     payload = {"model_name": "modelA", "inputs": [1, 2, 3]}

#     # Patch AVAILABLE_MODELS["modelA"].predict to return a fake value
#     with patch("main.AVAILABLE_MODELS", {"modelA": "mock"}):
#         response = client.post("/predict", json=payload)

#     assert response.status_code == 200
#     assert "prediction" in response.json()
