"""
Pytest Configuration and Fixtures

This module provides shared fixtures for all tests.
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression


@pytest.fixture(scope="session")
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    
    n_samples = 1000
    
    data = {
        'longitude': np.random.uniform(-125, -114, n_samples),
        'latitude': np.random.uniform(32, 43, n_samples),
        'housing_median_age': np.random.uniform(1, 52, n_samples),
        'total_rooms': np.random.uniform(2, 5000, n_samples),
        'total_bedrooms': np.random.uniform(1, 1000, n_samples),
        'population': np.random.uniform(3, 15000, n_samples),
        'households': np.random.uniform(1, 5000, n_samples),
        'median_income': np.random.uniform(0.5, 15, n_samples),
        'ocean_proximity': np.random.choice(
            ['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'], 
            n_samples
        ),
        'median_house_value': np.random.uniform(15000, 500000, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure bedrooms <= rooms
    df['total_bedrooms'] = df[['total_bedrooms', 'total_rooms']].min(axis=1)
    
    # Ensure households <= population
    df['households'] = df[['households', 'population']].min(axis=1)
    
    return df


@pytest.fixture
def sample_features():
    """Create sample features dictionary for testing."""
    return {
        'longitude': -122.23,
        'latitude': 37.88,
        'housing_median_age': 41.0,
        'total_rooms': 880.0,
        'total_bedrooms': 129.0,
        'population': 322.0,
        'households': 126.0,
        'median_income': 8.3252,
        'ocean_proximity': 'NEAR BAY'
    }


@pytest.fixture
def mock_model():
    """Create a simple mock model for testing."""
    from sklearn.linear_model import LinearRegression
    
    # Create dummy data
    X = np.random.randn(100, 10)
    y = np.random.randn(100) * 50000 + 200000
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model
