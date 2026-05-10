"""
Modern California Housing Price Predictor - Training Pipeline
Incorporates 2024 Market Adjustments and Advanced Feature Engineering.
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

# Constants
RANDOM_STATE = 42
# 1990 to 2024 inflation factor (Median price: $194k -> $870k)
MARKET_SCALING_FACTOR = 4.48 

def load_and_preprocess():
    print("Loading modern data pipeline...")
    if not os.path.exists("housing.csv"):
        raise FileNotFoundError("housing.csv not found in root directory.")
    
    df = pd.read_csv("housing.csv")
    
    # Target scaling (Bringing 1990 data to 2024 levels)
    df['median_house_value_2024'] = df['median_house_value'] * MARKET_SCALING_FACTOR
    
    # Drop old target
    X = df.drop(columns=['median_house_value', 'median_house_value_2024'])
    y = df['median_house_value_2024']
    
    return train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

def engineer_features(data):
    data = data.copy()
    # Basic ratios
    data['rooms_per_household'] = data['total_rooms'] / data['households'].clip(lower=1)
    data['bedrooms_per_room'] = data['total_bedrooms'] / data['total_rooms'].clip(lower=1)
    data['population_per_household'] = data['population'] / data['households'].clip(lower=1)
    
    # Distance to Economic Hubs (SF and LA)
    data['dist_to_sf'] = np.sqrt((data['latitude'] - 37.7749)**2 + (data['longitude'] - (-122.4194))**2)
    data['dist_to_la'] = np.sqrt((data['latitude'] - 34.0522)**2 + (data['longitude'] - (-118.2437))**2)
    
    # Income metrics
    data['income_per_capita'] = (data['median_income'] * 10000) / data['population_per_household'].clip(lower=1)
    
    return data

def build_pipeline():
    # Feature groups
    num_features = [
        'longitude', 'latitude', 'housing_median_age', 'total_rooms', 
        'total_bedrooms', 'population', 'households', 'median_income',
        'rooms_per_household', 'bedrooms_per_room', 'population_per_household',
        'dist_to_sf', 'dist_to_la', 'income_per_capita'
    ]
    cat_features = ['ocean_proximity']
    
    num_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler()) # Better for outliers in housing data
    ])
    
    cat_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', num_transformer, num_features),
        ('cat', cat_transformer, cat_features)
    ])
    
    model = Pipeline([
        ('engineer', None), # Placeholder for logic if needed in pipeline
        ('preprocess', preprocessor),
        ('regressor', HistGradientBoostingRegressor(
            max_iter=500,
            learning_rate=0.05,
            max_depth=10,
            l2_regularization=0.5,
            random_state=RANDOM_STATE
        ))
    ])
    
    return model

def main():
    X_train, X_test, y_train, y_test = load_and_preprocess()
    
    # Manual feature engineering (since I'm not using a custom transformer class for simplicity)
    X_train_eng = engineer_features(X_train)
    X_test_eng = engineer_features(X_test)
    
    pipeline = build_pipeline()
    
    print("Training Modern Model...")
    pipeline.fit(X_train_eng, y_train)
    
    # Evaluation
    y_pred = pipeline.predict(X_test_eng)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Training Complete!")
    print(f"R2 Score: {r2:.4f}")
    print(f"RMSE: ${rmse:,.2f}")
    
    # Save artifacts
    os.makedirs('models/modern', exist_ok=True)
    joblib.dump(pipeline, 'models/modern/house_price_model_v2.pkl')
    
    # Export stats for UI
    stats = {
        "scaling_factor": MARKET_SCALING_FACTOR,
        "r2": float(r2),
        "rmse": float(rmse),
        "median_price_2024": float(y_test.median())
    }
    joblib.dump(stats, 'models/modern/model_stats.pkl')
    print("Artifacts saved to models/modern/")

if __name__ == "__main__":
    main()
