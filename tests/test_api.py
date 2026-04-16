"""
Tests for FastAPI Application

Tests cover:
- Health check endpoint
- Prediction endpoint
- Input validation
- Error handling
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from api.main import app, model_state


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "timestamp" in data
        assert "version" in data


class TestPredictionEndpoints:
    """Test prediction endpoints."""
    
    @pytest.fixture
    def valid_payload(self):
        """Create valid prediction payload."""
        return {
            "longitude": -122.23,
            "latitude": 37.88,
            "housing_median_age": 41,
            "total_rooms": 880,
            "total_bedrooms": 129,
            "population": 322,
            "households": 126,
            "median_income": 8.3252,
            "ocean_proximity": "NEAR BAY"
        }
    
    def test_predict_endpoint_structure(self, client, valid_payload, monkeypatch):
        """Test prediction endpoint structure (mocked)."""
        # Mock the model prediction
        def mock_predict(features):
            return 200000.0
        
        monkeypatch.setattr(model_state, "is_loaded", True)
        monkeypatch.setattr(model_state, "predict", mock_predict)
        
        response = client.post("/predict", json=valid_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "predicted_price" in data
        assert "currency" in data
        assert "timestamp" in data
        assert "model_version" in data
        assert data["currency"] == "USD"
    
    def test_predict_without_model(self, client, valid_payload):
        """Test prediction fails when model not loaded."""
        # Ensure model is marked as not loaded
        original_state = model_state.is_loaded
        model_state.is_loaded = False
        
        try:
            response = client.post("/predict", json=valid_payload)
            
            assert response.status_code == 503
            data = response.json()
            assert "detail" in data
        finally:
            model_state.is_loaded = original_state
    
    def test_predict_invalid_longitude(self, client, valid_payload):
        """Test prediction with invalid longitude."""
        invalid_payload = valid_payload.copy()
        invalid_payload["longitude"] = -200  # Out of range
        
        response = client.post("/predict", json=invalid_payload)
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_invalid_latitude(self, client, valid_payload):
        """Test prediction with invalid latitude."""
        invalid_payload = valid_payload.copy()
        invalid_payload["latitude"] = 100  # Out of range
        
        response = client.post("/predict", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_predict_invalid_income(self, client, valid_payload):
        """Test prediction with invalid income."""
        invalid_payload = valid_payload.copy()
        invalid_payload["median_income"] = -5  # Negative income
        
        response = client.post("/predict", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_predict_invalid_ocean_proximity(self, client, valid_payload):
        """Test prediction with invalid ocean proximity."""
        invalid_payload = valid_payload.copy()
        invalid_payload["ocean_proximity"] = "INVALID_VALUE"
        
        response = client.post("/predict", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_predict_missing_field(self, client, valid_payload):
        """Test prediction with missing required field."""
        incomplete_payload = valid_payload.copy()
        del incomplete_payload["median_income"]
        
        response = client.post("/predict", json=incomplete_payload)
        
        assert response.status_code == 422
    
    def test_batch_predict_endpoint(self, client, valid_payload, monkeypatch):
        """Test batch prediction endpoint."""
        # Mock the model prediction
        def mock_predict(features):
            return 200000.0
        
        monkeypatch.setattr(model_state, "is_loaded", True)
        monkeypatch.setattr(model_state, "predict", mock_predict)
        
        batch_payload = [valid_payload, valid_payload]
        
        response = client.post("/predict/batch", json=batch_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2
        assert "timestamp" in data


class TestModelInfoEndpoint:
    """Test model info endpoint."""
    
    def test_model_info_with_model(self, client, monkeypatch):
        """Test model info when model is loaded."""
        monkeypatch.setattr(model_state, "is_loaded", True)
        
        response = client.get("/model/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "model_type" in data
        assert "version" in data
        assert "features" in data
        assert "description" in data
        assert isinstance(data["features"], list)
    
    def test_model_info_without_model(self, client):
        """Test model info when model is not loaded."""
        original_state = model_state.is_loaded
        model_state.is_loaded = False
        
        try:
            response = client.get("/model/info")
            
            assert response.status_code == 503
            data = response.json()
            assert "detail" in data
        finally:
            model_state.is_loaded = original_state
