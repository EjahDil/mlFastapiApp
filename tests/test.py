# tests/test_main.py
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..mainls import appls
from ..pydanticbm import PredictionRequest
from dotenv import load_dotenv


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


# @pytest.fixture
# def mock_model():
#     """Fixture to simulate a fake model with a predict method."""
#     class FakeModel:
#         def predict(self, data):
#             return ["mocked_prediction"]

#     return FakeModel()


# def test_prediction_valid_model_name(mock_model):
#     """Test prediction with a valid model name (mocked)."""

#     # Patch the models dictionary so that "logistic_regression" points to our mock
#     with patch("mainls.models", {"logistic_regression": mock_model}):
#         response = client.post(
#             "/predict_async_bg/logistic_regression",
#             json={"features": [5.1, 3.5, 1.4, 0.2]}
#         )

#     assert response.status_code == 200
#     body = response.json()
#     assert "prediction" in body
#     assert body["prediction"] == ["mocked_prediction"]


def test_prediction_invalid_model_name():
    """Test invalid model name with new Iris-style input."""
    response = client.post(
        "/predict_async/invalid_model",
        json={
            "sepal_length": 2.3,
            "sepal_width": 4.4,
            "petal_length": 3.3,
            "petal_width": 4.4,
        },
        # headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 404
    assert "error" in response.json() or "detail" in response.json()


# def test_prediction_valid_model_name(mock_model):
#     """Test valid model name with mocked model and new input format."""

#     with patch("mainls.models", {"logistic_regression": mock_model}):
#         response = client.post(
#             "/predict_async/logistic_regression",
#             json={
#                 "sepal_length": 2.3,
#                 "sepal_width": 4.4,
#                 "petal_length": 3.3,
#                 "petal_width": 4.4,
#             },
#             # headers={"x-api-key": API_KEY}
#         )

#     assert response.status_code == 200
#     body = response.json()
#     assert "prediction" in body
#     assert body["prediction"] == ["mocked_prediction"]
