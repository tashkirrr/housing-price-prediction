"""
Tests for Data Processing Module

Tests cover:
- Data loading and validation
- Feature engineering
- Preprocessing pipeline
- Data transformations
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.data_processing import DataProcessor, FeatureEngineer


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def test_initialization(self):
        """Test DataProcessor initialization."""
        processor = DataProcessor(
            data_path="data/housing.csv",
            target_col="median_house_value",
            test_size=0.2,
            random_state=42
        )
        
        assert processor.data_path == Path("data/housing.csv")
        assert processor.target_col == "median_house_value"
        assert processor.test_size == 0.2
        assert processor.random_state == 42
        assert processor.df is None
    
    def test_load_data_file_not_found(self):
        """Test loading non-existent file raises error."""
        processor = DataProcessor(data_path="nonexistent.csv")
        
        with pytest.raises(FileNotFoundError):
            processor.load_data()
    
    def test_get_column_types_before_load(self, sample_data):
        """Test get_column_types raises error before loading data."""
        processor = DataProcessor(data_path="dummy.csv")
        
        with pytest.raises(ValueError, match="Data not loaded"):
            processor.get_column_types()
    
    def test_get_column_types(self, sample_data, tmp_path):
        """Test column type identification."""
        # Save sample data to temp file
        data_path = tmp_path / "test_data.csv"
        sample_data.to_csv(data_path, index=False)
        
        processor = DataProcessor(data_path=str(data_path))
        processor.load_data()
        
        num_cols, cat_cols = processor.get_column_types()
        
        assert "median_income" in num_cols
        assert "ocean_proximity" in cat_cols
        assert "median_house_value" not in num_cols  # Excluded as target
    
    def test_analyze_missing_values(self, sample_data, tmp_path):
        """Test missing value analysis."""
        # Add some missing values
        sample_data.loc[0:5, 'total_bedrooms'] = np.nan
        
        data_path = tmp_path / "test_data.csv"
        sample_data.to_csv(data_path, index=False)
        
        processor = DataProcessor(data_path=str(data_path))
        processor.load_data()
        
        missing = processor.analyze_missing_values()
        
        assert missing['total_bedrooms'] == 6
        assert missing['median_income'] == 0
    
    def test_split_data(self, sample_data, tmp_path):
        """Test train-test split."""
        data_path = tmp_path / "test_data.csv"
        sample_data.to_csv(data_path, index=False)
        
        processor = DataProcessor(data_path=str(data_path), test_size=0.2)
        processor.load_data()
        
        X_train, X_test, y_train, y_test = processor.split_data()
        
        # Check shapes
        assert len(X_train) == int(len(sample_data) * 0.8)
        assert len(X_test) == len(sample_data) - len(X_train)
        assert len(y_train) == len(X_train)
        assert len(y_test) == len(X_test)
        
        # Check target not in features
        assert "median_house_value" not in X_train.columns
        assert "median_house_value" not in X_test.columns
    
    def test_get_data_summary(self, sample_data, tmp_path):
        """Test data summary generation."""
        data_path = tmp_path / "test_data.csv"
        sample_data.to_csv(data_path, index=False)
        
        processor = DataProcessor(data_path=str(data_path))
        processor.load_data()
        
        summary = processor.get_data_summary()
        
        assert summary["total_rows"] == len(sample_data)
        assert summary["total_columns"] == len(sample_data.columns)
        assert "target_stats" in summary
        assert "mean" in summary["target_stats"]


class TestFeatureEngineer:
    """Test cases for FeatureEngineer class."""
    
    def test_create_ratio_features(self, sample_data):
        """Test ratio feature creation."""
        engineer = FeatureEngineer()
        df_result = engineer.create_ratio_features(sample_data)
        
        # Check new features exist
        assert "rooms_per_household" in df_result.columns
        assert "bedrooms_per_room" in df_result.columns
        assert "population_per_household" in df_result.columns
        
        # Check calculations
        expected_ratio = sample_data["total_rooms"] / sample_data["households"]
        pd.testing.assert_series_equal(
            df_result["rooms_per_household"],
            expected_ratio,
            check_names=False
        )
    
    def test_create_location_features(self, sample_data):
        """Test location feature creation."""
        engineer = FeatureEngineer()
        df_result = engineer.create_location_features(sample_data)
        
        # Check new features exist
        assert "distance_to_sf" in df_result.columns
        assert "distance_to_la" in df_result.columns
        
        # Check distances are positive
        assert (df_result["distance_to_sf"] >= 0).all()
        assert (df_result["distance_to_la"] >= 0).all()
    
    def test_build_preprocessing_pipeline(self, sample_data):
        """Test preprocessing pipeline building."""
        engineer = FeatureEngineer()
        
        X = sample_data.drop(columns=["median_house_value"])
        preprocessor = engineer.build_preprocessing_pipeline(X)
        
        assert preprocessor is not None
        assert engineer.feature_names is not None
        assert len(engineer.feature_names) > 0
    
    def test_transform_before_pipeline_built(self, sample_data):
        """Test transform raises error before pipeline is built."""
        engineer = FeatureEngineer()
        X = sample_data.drop(columns=["median_house_value"])
        
        with pytest.raises(ValueError, match="Preprocessor not fitted"):
            engineer.transform(X)
    
    def test_transform_after_pipeline_built(self, sample_data):
        """Test transform works after pipeline is built."""
        engineer = FeatureEngineer()
        
        X = sample_data.drop(columns=["median_house_value"])
        preprocessor = engineer.build_preprocessing_pipeline(X)
        
        X_transformed = engineer.transform(X)
        
        assert isinstance(X_transformed, np.ndarray)
        assert X_transformed.shape[0] == len(X)
    
    def test_get_feature_importance_df(self, sample_data):
        """Test feature importance DataFrame creation."""
        engineer = FeatureEngineer()
        
        X = sample_data.drop(columns=["median_house_value"])
        engineer.build_preprocessing_pipeline(X)
        
        # Create dummy importances
        importances = np.random.rand(len(engineer.feature_names))
        
        importance_df = engineer.get_feature_importance_df(importances)
        
        assert len(importance_df) == len(engineer.feature_names)
        assert "feature" in importance_df.columns
        assert "importance" in importance_df.columns
        assert importance_df["importance"].is_monotonic_decreasing
