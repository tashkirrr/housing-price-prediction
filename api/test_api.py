"""
API Test Script

Simple script to test the API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()


def test_model_info():
    """Test model info endpoint."""
    response = requests.get(f"{BASE_URL}/model/info")
    print("Model Info:")
    print(json.dumps(response.json(), indent=2))
    print()


def test_predict():
    """Test prediction endpoint."""
    payload = {
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
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print("Prediction:")
    print(json.dumps(response.json(), indent=2))
    print()


def test_batch_predict():
    """Test batch prediction endpoint."""
    payload = [
        {
            "longitude": -122.23,
            "latitude": 37.88,
            "housing_median_age": 41,
            "total_rooms": 880,
            "total_bedrooms": 129,
            "population": 322,
            "households": 126,
            "median_income": 8.3252,
            "ocean_proximity": "NEAR BAY"
        },
        {
            "longitude": -118.24,
            "latitude": 34.05,
            "housing_median_age": 25,
            "total_rooms": 1500,
            "total_bedrooms": 300,
            "population": 1000,
            "households": 400,
            "median_income": 4.5,
            "ocean_proximity": "<1H OCEAN"
        }
    ]
    
    response = requests.post(f"{BASE_URL}/predict/batch", json=payload)
    print("Batch Prediction:")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("=" * 60)
    print("Testing California House Price Prediction API")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_model_info()
        test_predict()
        test_batch_predict()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API.")
        print("   Make sure the server is running: uvicorn api.main:app --reload")
