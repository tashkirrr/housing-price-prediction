"""
California House Price Prediction API

A production-ready FastAPI application for predicting house prices.

Run with: uvicorn api.main:app --reload
"""

import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from contextlib import asynccontextmanager

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


# ============================================================================
# Pydantic Models for Request/Response
# ============================================================================

class HouseFeatures(BaseModel):
    """Input features for house price prediction."""
    
    longitude: float = Field(
        ..., ge=-125.0, le=-114.0,
        description="Longitude coordinate (-125 to -114)"
    )
    latitude: float = Field(
        ..., ge=32.0, le=43.0,
        description="Latitude coordinate (32 to 43)"
    )
    housing_median_age: float = Field(
        ..., ge=1, le=52,
        description="Median age of houses in the block (1-52 years)"
    )
    total_rooms: float = Field(
        ..., ge=1, le=50000,
        description="Total rooms in the block"
    )
    total_bedrooms: float = Field(
        ..., ge=1, le=10000,
        description="Total bedrooms in the block"
    )
    population: float = Field(
        ..., ge=1, le=50000,
        description="Population of the block"
    )
    households: float = Field(
        ..., ge=1, le=10000,
        description="Number of households"
    )
    median_income: float = Field(
        ..., ge=0.5, le=15.0,
        description="Median income in $10,000s"
    )
    ocean_proximity: str = Field(
        ..., 
        description="Ocean proximity category",
        enum=["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
    )
    
    @validator('total_bedrooms')
    def bedrooms_less_than_rooms(cls, v, values):
        if 'total_rooms' in values and v > values['total_rooms']:
            raise ValueError('total_bedrooms cannot exceed total_rooms')
        return v
    
    @validator('households')
    def households_less_than_population(cls, v, values):
        if 'population' in values and v > values['population']:
            raise ValueError('households cannot exceed population')
        return v


class PredictionResponse(BaseModel):
    """Response model for price prediction."""
    
    predicted_price: float = Field(..., description="Predicted median house value in USD")
    currency: str = Field(default="USD", description="Currency of the prediction")
    timestamp: str = Field(..., description="Timestamp of the prediction")
    model_version: str = Field(..., description="Version of the model used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 225000.50,
                "currency": "USD",
                "timestamp": "2024-01-15T10:30:00",
                "model_version": "1.0.0"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    model_loaded: bool
    timestamp: str
    version: str


class ModelInfoResponse(BaseModel):
    """Model information response."""
    
    model_type: str
    version: str
    features: list
    description: str


# ============================================================================
# Model Loading and Global State
# ============================================================================

class ModelState:
    """Global state for the model and preprocessor."""
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        self.is_loaded = False
    
    def load(self):
        """Load model and preprocessor from disk."""
        try:
            model_path = Path(__file__).parent.parent / "models" / "house_price_model.pkl"
            preprocessor_path = Path(__file__).parent.parent / "models" / "preprocessor.pkl"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not preprocessor_path.exists():
                raise FileNotFoundError(f"Preprocessor file not found: {preprocessor_path}")
            
            self.model = joblib.load(model_path)
            self.preprocessor = joblib.load(preprocessor_path)
            self.is_loaded = True
            print(f"✅ Model loaded successfully from {model_path}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
    
    def predict(self, features: dict) -> float:
        """Make a prediction using the loaded model."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        # Calculate engineered features
        features['rooms_per_household'] = features['total_rooms'] / max(features['households'], 1)
        features['bedrooms_per_room'] = features['total_bedrooms'] / max(features['total_rooms'], 1)
        features['population_per_household'] = features['population'] / max(features['households'], 1)
        features['distance_to_sf'] = np.sqrt(
            (features['latitude'] - 37.7749)**2 + 
            (features['longitude'] - (-122.4194))**2
        )
        features['distance_to_la'] = np.sqrt(
            (features['latitude'] - 34.0522)**2 + 
            (features['longitude'] - (-118.2437))**2
        )
        features['income_per_room'] = features['median_income'] / max(features['rooms_per_household'], 0.1)
        
        # Create DataFrame and predict
        input_df = pd.DataFrame([features])
        input_processed = self.preprocessor.transform(input_df)
        prediction = self.model.predict(input_processed)[0]
        
        return float(prediction)


# Global model state
model_state = ModelState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting up API...")
    model_state.load()
    yield
    # Shutdown
    print("🛑 Shutting down API...")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="California House Price Prediction API",
    description="""
    A production-ready API for predicting California house prices using machine learning.
    
    ## Features
    
    * **Predict Prices**: Get price predictions for California properties
    * **Health Checks**: Monitor API and model status
    * **Model Info**: Get information about the deployed model
    
    ## Data Source
    
    The model was trained on the California Housing Dataset from the 1990 census.
    Predictions are in 1990 dollars and should be adjusted for inflation for current values.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "California House Price Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API and whether the model is loaded.
    """
    return HealthResponse(
        status="healthy" if model_state.is_loaded else "unhealthy",
        model_loaded=model_state.is_loaded,
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def model_info():
    """
    Get information about the deployed model.
    
    Returns details about the model type, version, and features used.
    """
    if not model_state.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return ModelInfoResponse(
        model_type="HistGradientBoostingRegressor",
        version="1.0.0",
        features=[
            "longitude", "latitude", "housing_median_age", "total_rooms",
            "total_bedrooms", "population", "households", "median_income",
            "ocean_proximity", "rooms_per_household", "bedrooms_per_room",
            "population_per_household", "distance_to_sf", "distance_to_la",
            "income_per_room"
        ],
        description="Gradient boosting model trained on California Housing Dataset (1990 census)"
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid input data"},
        503: {"description": "Model not available"}
    }
)
async def predict(features: HouseFeatures):
    """
    Predict house price for a given set of features.
    
    ## Parameters
    
    All parameters are required and validated:
    
    - **longitude**: -125 to -114 (how far west)
    - **latitude**: 32 to 43 (how far north)
    - **housing_median_age**: 1 to 52 years
    - **total_rooms**: Total rooms in the block
    - **total_bedrooms**: Total bedrooms (must be ≤ total_rooms)
    - **population**: Population of the block
    - **households**: Number of households (must be ≤ population)
    - **median_income**: In $10,000s (0.5 to 15.0)
    - **ocean_proximity**: One of <1H OCEAN, INLAND, ISLAND, NEAR BAY, NEAR OCEAN
    
    ## Response
    
    Returns the predicted price in USD along with metadata.
    """
    if not model_state.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Convert Pydantic model to dict
        features_dict = features.model_dump()
        
        # Make prediction
        predicted_price = model_state.predict(features_dict)
        
        return PredictionResponse(
            predicted_price=round(predicted_price, 2),
            currency="USD",
            timestamp=datetime.now().isoformat(),
            model_version="1.0.0"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(features_list: list[HouseFeatures]):
    """
    Predict house prices for multiple properties in a single request.
    
    Accepts a list of HouseFeatures objects and returns predictions for all.
    """
    if not model_state.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    predictions = []
    for features in features_list:
        try:
            features_dict = features.model_dump()
            predicted_price = model_state.predict(features_dict)
            predictions.append({
                "predicted_price": round(predicted_price, 2),
                "currency": "USD",
                "status": "success"
            })
        except Exception as e:
            predictions.append({
                "status": "error",
                "error": str(e)
            })
    
    return {
        "predictions": predictions,
        "timestamp": datetime.now().isoformat(),
        "model_version": "1.0.0"
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return {
        "error": "Internal server error",
        "detail": str(exc),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
