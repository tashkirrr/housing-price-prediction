"""
Tests for Models Module

Tests cover:
- Model training
- Cross-validation
- Hyperparameter tuning
- Model evaluation
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.models import ModelTrainer, ModelEvaluator, save_model, load_model


class TestModelTrainer:
    """Test cases for ModelTrainer class."""
    
    @pytest.fixture
    def regression_data(self):
        """Create sample regression data."""
        X, y = make_regression(
            n_samples=200,
            n_features=10,
            noise=10,
            random_state=42
        )
        return X, y
    
    def test_initialization(self):
        """Test ModelTrainer initialization."""
        trainer = ModelTrainer(random_state=42)
        
        assert trainer.random_state == 42
        assert len(trainer.models) == 5  # 5 models defined
        assert "LinearRegression" in trainer.models
        assert "HistGradientBoosting" in trainer.models
        assert trainer.best_model is None
    
    def test_compare_models(self, regression_data):
        """Test model comparison with cross-validation."""
        X, y = regression_data
        trainer = ModelTrainer(random_state=42)
        
        results = trainer.compare_models(X, y, cv_folds=3)
        
        assert isinstance(results, pd.DataFrame)
        assert len(results) == 5  # All models compared
        assert "model" in results.columns
        assert "cv_rmse_mean" in results.columns
        assert "cv_r2_mean" in results.columns
        assert results["cv_rmse_mean"].is_monotonic_increasing  # Sorted by RMSE
    
    def test_get_default_param_grids(self):
        """Test default parameter grids."""
        trainer = ModelTrainer()
        grids = trainer.get_default_param_grids()
        
        assert "Ridge" in grids
        assert "Lasso" in grids
        assert "RandomForest" in grids
        assert "HistGradientBoosting" in grids
        
        # Check HistGradientBoosting has expected params
        hgb_grid = grids["HistGradientBoosting"]
        assert "learning_rate" in hgb_grid
        assert "max_depth" in hgb_grid


class TestModelEvaluator:
    """Test cases for ModelEvaluator class."""
    
    @pytest.fixture
    def predictions(self):
        """Create sample predictions."""
        np.random.seed(42)
        y_true = np.random.randn(100) * 50000 + 200000
        y_pred = y_true + np.random.randn(100) * 30000  # Add some error
        return y_true, y_pred
    
    def test_initialization(self):
        """Test ModelEvaluator initialization."""
        evaluator = ModelEvaluator()
        
        assert evaluator.metrics == {}
        assert evaluator.predictions is None
        assert evaluator.residuals is None
    
    def test_evaluate(self, predictions):
        """Test model evaluation."""
        y_true, y_pred = predictions
        evaluator = ModelEvaluator()
        
        metrics = evaluator.evaluate(y_true, y_pred, dataset_name="Test")
        
        assert "rmse" in metrics
        assert "mae" in metrics
        assert "mape" in metrics
        assert "r2" in metrics
        assert "mean_residual" in metrics
        
        # Check residuals calculated
        assert evaluator.predictions is not None
        assert evaluator.residuals is not None
        assert len(evaluator.residuals) == len(y_true)
    
    def test_analyze_errors_by_range(self, predictions):
        """Test error analysis by price range."""
        y_true, y_pred = predictions
        evaluator = ModelEvaluator()
        evaluator.evaluate(y_true, y_pred)
        
        # Create dummy X_test
        X_test = pd.DataFrame({
            'feature1': np.random.randn(len(y_true)),
            'feature2': np.random.randn(len(y_true))
        })
        
        analysis = evaluator.analyze_errors_by_range(y_true, y_pred)
        
        assert isinstance(analysis, pd.DataFrame)
        assert len(analysis) > 0
    
    def test_get_feature_importance_with_tree_model(self):
        """Test feature importance extraction from tree-based model."""
        from sklearn.ensemble import RandomForestRegressor
        
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = np.random.randn(100) * 50000 + 200000
        
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        evaluator = ModelEvaluator()
        feature_names = ['f1', 'f2', 'f3', 'f4', 'f5']
        
        importance_df = evaluator.get_feature_importance(model, feature_names)
        
        assert importance_df is not None
        assert len(importance_df) == 5
        assert list(importance_df.columns) == ['feature', 'importance']
        assert importance_df['importance'].is_monotonic_decreasing
    
    def test_get_feature_importance_with_linear_model(self):
        """Test feature importance extraction from linear model."""
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = np.random.randn(100) * 50000 + 200000
        
        model = LinearRegression()
        model.fit(X, y)
        
        evaluator = ModelEvaluator()
        feature_names = ['f1', 'f2', 'f3', 'f4', 'f5']
        
        importance_df = evaluator.get_feature_importance(model, feature_names)
        
        assert importance_df is not None
        assert len(importance_df) == 5
    
    def test_get_feature_importance_unsupported_model(self):
        """Test feature importance with unsupported model."""
        class DummyModel:
            pass
        
        evaluator = ModelEvaluator()
        importance_df = evaluator.get_feature_importance(DummyModel(), ['f1', 'f2'])
        
        assert importance_df is None
    
    def test_identify_worst_predictions(self, predictions):
        """Test identification of worst predictions."""
        y_true, y_pred = predictions
        evaluator = ModelEvaluator()
        
        X_test = pd.DataFrame({
            'feature1': np.random.randn(len(y_true)),
            'feature2': np.random.randn(len(y_true))
        })
        
        worst_df = evaluator.identify_worst_predictions(y_true, y_pred, X_test, n=10)
        
        assert len(worst_df) == 10
        assert 'true_value' in worst_df.columns
        assert 'predicted_value' in worst_df.columns
        assert 'absolute_error' in worst_df.columns
        assert 'percentage_error' in worst_df.columns


class TestModelPersistence:
    """Test cases for model saving and loading."""
    
    def test_save_and_load_model(self, tmp_path):
        """Test saving and loading a model."""
        from sklearn.linear_model import Ridge
        
        # Create and train a simple model
        np.random.seed(42)
        X = np.random.randn(50, 5)
        y = np.random.randn(50)
        
        model = Ridge()
        model.fit(X, y)
        
        # Save model
        model_path = tmp_path / "test_model.pkl"
        save_model(model, str(model_path))
        
        assert model_path.exists()
        
        # Load model
        loaded_model = load_model(str(model_path))
        
        # Verify loaded model works
        X_test = np.random.randn(10, 5)
        original_pred = model.predict(X_test)
        loaded_pred = loaded_model.predict(X_test)
        
        np.testing.assert_array_almost_equal(original_pred, loaded_pred)
