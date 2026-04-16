"""
Train the California House Price Prediction model and export for web use.
This script trains the model and exports it in a format suitable for browser use.
"""

import numpy as np
import pandas as pd
import json
from sklearn.model_selection import train_test_split, KFold, cross_validate, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import joblib
import os

RANDOM_STATE = 42
CSV_PATH = "housing.csv"
TARGET_COL = "median_house_value"

def main():
    print("🚀 Loading data...")
    df = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded {df.shape[0]} rows and {df.shape[1]} columns")
    
    # Separate features and target
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"📊 Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Feature engineering
    def add_features(data):
        data = data.copy()
        data['rooms_per_household'] = data['total_rooms'] / data['households'].clip(lower=1)
        data['bedrooms_per_room'] = data['total_bedrooms'] / data['total_rooms'].clip(lower=1)
        data['population_per_household'] = data['population'] / data['households'].clip(lower=1)
        data['distance_to_sf'] = np.sqrt(
            (data['latitude'] - 37.7749)**2 + 
            (data['longitude'] - (-122.4194))**2
        )
        data['distance_to_la'] = np.sqrt(
            (data['latitude'] - 34.0522)**2 + 
            (data['longitude'] - (-118.2437))**2
        )
        data['income_per_room'] = data['median_income'] / data['rooms_per_household'].clip(lower=0.1)
        return data
    
    X_train = add_features(X_train)
    X_test = add_features(X_test)
    
    # Define features
    numerical_features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
                         'total_bedrooms', 'population', 'households', 'median_income',
                         'rooms_per_household', 'bedrooms_per_room', 'population_per_household',
                         'distance_to_sf', 'distance_to_la', 'income_per_room']
    categorical_features = ['ocean_proximity']
    
    # Preprocessing
    numerical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Create pipeline with best parameters
    print("🔧 Training model with optimized parameters...")
    model = Pipeline([
        ('preprocess', preprocessor),
        ('regressor', HistGradientBoostingRegressor(
            l2_regularization=0.1,
            learning_rate=0.1,
            max_depth=None,
            max_leaf_nodes=63,
            min_samples_leaf=20,
            random_state=RANDOM_STATE
        ))
    ])
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    print("\n📈 Model Performance:")
    print(f"Train R²: {r2_score(y_train, train_pred):.3f}")
    print(f"Test R²:  {r2_score(y_test, test_pred):.3f}")
    print(f"Train RMSE: ${root_mean_squared_error(y_train, train_pred):,.0f}")
    print(f"Test RMSE:  ${root_mean_squared_error(y_test, test_pred):,.0f}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/house_price_model.pkl')
    print("\n💾 Model saved to models/house_price_model.pkl")
    
    # Export model parameters for JavaScript (simplified linear approximation)
    # Get feature importances from the tree model
    feature_names = numerical_features + list(
        model.named_steps['preprocess']
        .named_transformers_['cat']
        .named_steps['onehot']
        .get_feature_names_out(categorical_features)
    )
    
    # Add engineered features to original df for correlation calculation
    df_engineered = add_features(df)
    
    # Calculate correlations for simplified prediction
    correlations = df_engineered[numerical_features + [TARGET_COL]].corr()[TARGET_COL].drop(TARGET_COL)
    
    # Calculate means and stds for normalization
    num_stats = {}
    for col in numerical_features:
        num_stats[col] = {
            'mean': float(df_engineered[col].mean()),
            'std': float(df_engineered[col].std()),
            'min': float(df_engineered[col].min()),
            'max': float(df_engineered[col].max())
        }
    
    # Calculate average price by ocean proximity
    ocean_price_map = df.groupby('ocean_proximity')[TARGET_COL].mean().to_dict()
    
    # Export simplified model data
    model_data = {
        'numerical_features': numerical_features,
        'categorical_features': categorical_features,
        'num_stats': num_stats,
        'ocean_price_map': ocean_price_map,
        'correlations': correlations.to_dict(),
        'target_mean': float(df[TARGET_COL].mean()),
        'target_std': float(df[TARGET_COL].std()),
        'feature_means': {col: float(X_train[col].mean()) for col in numerical_features},
        'feature_stds': {col: float(X_train[col].std()) for col in numerical_features},
        'ocean_categories': list(df['ocean_proximity'].unique())
    }
    
    # Save as JSON for web use
    with open('docs/model_data.json', 'w') as f:
        json.dump(model_data, f, indent=2)
    print("📄 Model data exported to docs/model_data.json")
    
    # Create a simple linear approximation for browser prediction
    # This is a simplified model that works in JavaScript
    X_train_processed = preprocessor.transform(X_train)
    
    # Get the mean target value for baseline
    baseline_price = float(y_train.mean())
    
    # Calculate feature weights based on correlation and importance
    weights = {}
    for col in numerical_features:
        weights[col] = float(correlations.get(col, 0) * 50000)  # Scale to price impact
    
    # Ocean proximity multipliers
    ocean_multipliers = {}
    for ocean, price in ocean_price_map.items():
        ocean_multipliers[ocean] = float(price / baseline_price)
    
    # Export simplified prediction formula
    web_model = {
        'baseline_price': baseline_price,
        'weights': weights,
        'ocean_multipliers': ocean_multipliers,
        'feature_means': model_data['feature_means'],
        'num_stats': num_stats,
        'version': '1.0.0'
    }
    
    with open('docs/web_model.json', 'w') as f:
        json.dump(web_model, f, indent=2)
    print("🌐 Web model exported to docs/web_model.json")
    
    print("\n✅ Training complete!")
    return model

if __name__ == "__main__":
    main()
