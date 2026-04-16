"""
Models Module

Contains model definitions, training procedures, and evaluation metrics
for the California Housing Price Prediction project.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
import numpy as np
import pandas as pd
import joblib
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import cross_validate, KFold, GridSearchCV
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Handles model training, cross-validation, and hyperparameter tuning.
    
    This class implements a systematic approach to finding the best model:
    1. Baseline model for reference
    2. Multiple model comparison with cross-validation
    3. Hyperparameter tuning for the best performers
    4. Final model training with optimal parameters
    """
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models: Dict[str, BaseEstimator] = {
            "LinearRegression": LinearRegression(),
            "Ridge": Ridge(random_state=random_state),
            "Lasso": Lasso(random_state=random_state, max_iter=10000),
            "RandomForest": RandomForestRegressor(random_state=random_state, n_estimators=100),
            "HistGradientBoosting": HistGradientBoostingRegressor(random_state=random_state)
        }
        self.best_model: Optional[BaseEstimator] = None
        self.best_model_name: Optional[str] = None
        self.cv_results: Optional[pd.DataFrame] = None
        
    def compare_models(self, X_train: np.ndarray, y_train: np.ndarray,
                       cv_folds: int = 5) -> pd.DataFrame:
        """
        Compare multiple models using cross-validation.
        
        This gives us an unbiased estimate of how each model will perform
        on unseen data, helping us make an informed choice.
        
        Args:
            X_train: Training features (preprocessed)
            y_train: Training target
            cv_folds: Number of cross-validation folds
            
        Returns:
            DataFrame with CV results for each model
        """
        logger.info(f"Comparing {len(self.models)} models with {cv_folds}-fold CV...")
        
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)
        
        scoring = {
            "rmse": "neg_root_mean_squared_error",
            "mae": "neg_mean_absolute_error",
            "r2": "r2"
        }
        
        results = []
        
        for name, model in self.models.items():
            logger.info(f"  Evaluating {name}...")
            
            scores = cross_validate(
                model, X_train, y_train,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                return_train_score=False
            )
            
            results.append({
                "model": name,
                "cv_rmse_mean": -scores["test_rmse"].mean(),
                "cv_rmse_std": scores["test_rmse"].std(),
                "cv_mae_mean": -scores["test_mae"].mean(),
                "cv_mae_std": scores["test_mae"].std(),
                "cv_r2_mean": scores["test_r2"].mean(),
                "cv_r2_std": scores["test_r2"].std()
            })
        
        self.cv_results = pd.DataFrame(results).sort_values("cv_rmse_mean")
        
        logger.info("\n" + "="*60)
        logger.info("Cross-Validation Results (sorted by RMSE):")
        logger.info("="*60)
        for _, row in self.cv_results.iterrows():
            logger.info(f"{row['model']:<20} RMSE: {row['cv_rmse_mean']:.3f} (+/- {row['cv_rmse_std']*2:.3f})")
        
        return self.cv_results
    
    def tune_hyperparameters(self, X_train: np.ndarray, y_train: np.ndarray,
                            model_name: str, param_grid: Dict[str, List],
                            cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform grid search for hyperparameter tuning.
        
        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model to tune
            param_grid: Dictionary of parameters to search
            cv_folds: Number of CV folds
            
        Returns:
            Dictionary with best parameters and score
        """
        logger.info(f"\nTuning hyperparameters for {model_name}...")
        
        model = self.models[model_name]
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)
        
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best CV RMSE: {-grid_search.best_score_:.3f}")
        logger.info(f"Best parameters: {grid_search.best_params_}")
        
        return {
            "best_params": grid_search.best_params_,
            "best_score": -grid_search.best_score_,
            "cv_results": pd.DataFrame(grid_search.cv_results_)
        }
    
    def train_final_model(self, X_train: np.ndarray, y_train: np.ndarray,
                         model_name: str, **model_params) -> BaseEstimator:
        """
        Train the final model with specified parameters.
        
        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model to train
            **model_params: Model parameters
            
        Returns:
            Trained model
        """
        logger.info(f"\nTraining final {model_name} model...")
        
        model_class = type(self.models[model_name])
        self.best_model = model_class(random_state=self.random_state, **model_params)
        self.best_model.fit(X_train, y_train)
        self.best_model_name = model_name
        
        logger.info("Final model trained successfully!")
        
        return self.best_model
    
    def get_default_param_grids(self) -> Dict[str, Dict[str, List]]:
        """
        Get default hyperparameter grids for each model.
        
        Returns:
            Dictionary mapping model names to parameter grids
        """
        return {
            "Ridge": {
                "alpha": [0.1, 1.0, 10.0, 100.0]
            },
            "Lasso": {
                "alpha": [0.001, 0.01, 0.1, 1.0, 10.0]
            },
            "RandomForest": {
                "n_estimators": [100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10]
            },
            "HistGradientBoosting": {
                "learning_rate": [0.03, 0.05, 0.1],
                "max_depth": [None, 3, 6],
                "max_leaf_nodes": [15, 31, 63],
                "min_samples_leaf": [20, 50],
                "l2_regularization": [0.0, 0.1, 1.0]
            }
        }


class ModelEvaluator:
    """
    Comprehensive model evaluation and analysis.
    
    Beyond just metrics, we analyze:
    - Prediction errors by value ranges
    - Feature importance
    - Residual patterns
    - Model behavior on edge cases
    """
    
    def __init__(self):
        self.metrics: Dict[str, float] = {}
        self.predictions: Optional[np.ndarray] = None
        self.residuals: Optional[np.ndarray] = None
        
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray,
                 dataset_name: str = "Test") -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True target values
            y_pred: Predicted values
            dataset_name: Name of the dataset (for logging)
            
        Returns:
            Dictionary of metrics
        """
        self.predictions = y_pred
        self.residuals = y_true - y_pred
        
        self.metrics = {
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "mape": mean_absolute_percentage_error(y_true, y_pred) * 100,
            "r2": r2_score(y_true, y_pred),
            "mean_residual": np.mean(self.residuals),
            "std_residual": np.std(self.residuals)
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Evaluation Results - {dataset_name} Set")
        logger.info(f"{'='*60}")
        logger.info(f"RMSE:  ${self.metrics['rmse']:,.2f}")
        logger.info(f"MAE:   ${self.metrics['mae']:,.2f}")
        logger.info(f"MAPE:  {self.metrics['mape']:.2f}%")
        logger.info(f"R²:    {self.metrics['r2']:.4f}")
        logger.info(f"Mean Residual: ${self.metrics['mean_residual']:,.2f}")
        
        return self.metrics
    
    def analyze_errors_by_range(self, y_true: np.ndarray, y_pred: np.ndarray,
                                 price_ranges: List[float] = None) -> pd.DataFrame:
        """
        Analyze prediction errors across different price ranges.
        
        This helps us understand if our model performs better on
        certain types of properties.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            price_ranges: Price range boundaries
            
        Returns:
            DataFrame with error analysis by range
        """
        if price_ranges is None:
            price_ranges = [0, 100000, 200000, 300000, 400000, 500000, np.inf]
        
        df = pd.DataFrame({
            "y_true": y_true,
            "y_pred": y_pred,
            "abs_error": np.abs(y_true - y_pred),
            "pct_error": np.abs(y_true - y_pred) / y_true * 100
        })
        
        df["price_range"] = pd.cut(df["y_true"], bins=price_ranges)
        
        analysis = df.groupby("price_range").agg({
            "abs_error": ["mean", "std", "count"],
            "pct_error": "mean"
        }).round(2)
        
        return analysis
    
    def get_feature_importance(self, model: BaseEstimator,
                               feature_names: List[str]) -> Optional[pd.DataFrame]:
        """
        Extract feature importance from tree-based models.
        
        Args:
            model: Trained model
            feature_names: List of feature names
            
        Returns:
            DataFrame with feature importances or None if not available
        """
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "coef_"):
            importances = np.abs(model.coef_)
        else:
            logger.warning("Model doesn't have feature_importances_ or coef_ attribute")
            return None
        
        importance_df = pd.DataFrame({
            "feature": feature_names[:len(importances)],
            "importance": importances
        }).sort_values("importance", ascending=False)
        
        return importance_df
    
    def identify_worst_predictions(self, y_true: np.ndarray, y_pred: np.ndarray,
                                    X_test: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Identify the predictions with largest errors.
        
        Analyzing worst predictions often reveals:
        - Data quality issues
        - Missing important features
        - Edge cases the model struggles with
        
        Args:
            y_true: True values
            y_pred: Predicted values
            X_test: Test features
            n: Number of worst predictions to return
            
        Returns:
            DataFrame with worst predictions
        """
        errors = np.abs(y_true - y_pred)
        worst_indices = np.argsort(errors)[-n:][::-1]
        
        worst_df = X_test.iloc[worst_indices].copy()
        worst_df["true_value"] = y_true[worst_indices]
        worst_df["predicted_value"] = y_pred[worst_indices]
        worst_df["absolute_error"] = errors[worst_indices]
        worst_df["percentage_error"] = (errors[worst_indices] / y_true[worst_indices]) * 100
        
        return worst_df


def save_model(model: BaseEstimator, filepath: str) -> None:
    """Save a trained model to disk."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)
    logger.info(f"Model saved to {filepath}")


def load_model(filepath: str) -> BaseEstimator:
    """Load a trained model from disk."""
    model = joblib.load(filepath)
    logger.info(f"Model loaded from {filepath}")
    return model
