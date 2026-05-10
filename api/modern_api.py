from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
from typing import List, Optional
from datetime import datetime
import os

app = FastAPI(
    title="Realteak Modern Prediction API",
    description="Advanced housing price prediction for the 2024 California market.",
    version="2.0.0"
)

# Load Model
MODEL_PATH = "models/modern/house_price_model_v2.pkl"
STATS_PATH = "models/modern/model_stats.pkl"

class ModelEngine:
    def __init__(self):
        self.pipeline = None
        self.stats = None
        self.load()

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.pipeline = joblib.load(MODEL_PATH)
            self.stats = joblib.load(STATS_PATH)
            print(f"Loaded Modern Model V2 (R2: {self.stats['r2']:.4f})")
        else:
            print("Model not found. Run training script first.")

    def engineer_features(self, data: dict):
        df = pd.DataFrame([data])
        df['rooms_per_household'] = df['total_rooms'] / df['households'].clip(lower=1)
        df['bedrooms_per_room'] = df['total_bedrooms'] / df['total_rooms'].clip(lower=1)
        df['population_per_household'] = df['population'] / df['households'].clip(lower=1)
        df['dist_to_sf'] = np.sqrt((df['latitude'] - 37.7749)**2 + (df['longitude'] - (-122.4194))**2)
        df['dist_to_la'] = np.sqrt((df['latitude'] - 34.0522)**2 + (df['longitude'] - (-118.2437))**2)
        df['income_per_capita'] = (df['median_income'] * 10000) / df['population_per_household'].clip(lower=1)
        return df

engine = ModelEngine()

class PredictionRequest(BaseModel):
    longitude: float = Field(..., example=-122.23)
    latitude: float = Field(..., example=37.88)
    housing_median_age: float = Field(..., example=41)
    total_rooms: float = Field(..., example=880)
    total_bedrooms: float = Field(..., example=129)
    population: float = Field(..., example=322)
    households: float = Field(..., example=126)
    median_income: float = Field(..., example=8.3252)
    ocean_proximity: str = Field(..., example="NEAR BAY")

class PredictionResponse(BaseModel):
    estimated_price: float
    confidence_score: float
    market_year: int = 2024
    currency: str = "USD"
    timestamp: datetime = Field(default_factory=datetime.now)

@app.get("/health")
async def health():
    return {"status": "operational", "model_loaded": engine.pipeline is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if engine.pipeline is None:
        raise HTTPException(status_code=503, detail="Model engine not initialized.")
    
    try:
        features_df = engine.engineer_features(request.dict())
        prediction = engine.pipeline.predict(features_df)[0]
        
        # Simple confidence score based on R2 and input proximity (mock logic for demo)
        confidence = engine.stats['r2'] * 100 
        
        return PredictionResponse(
            estimated_price=round(prediction, 2),
            confidence_score=round(confidence, 1)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
