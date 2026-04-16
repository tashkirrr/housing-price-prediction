"""
Data Processing Module

Handles all data loading, cleaning, feature engineering, and preprocessing
for the California Housing Price Prediction project.
"""

import logging
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Handles data loading, cleaning, and basic preprocessing.
    
    This class takes care of the messy reality of real-world data:
    missing values, inconsistent formats, and the need for careful
    train-test separation to avoid data leakage.
    """
    
    def __init__(self, data_path: str, target_col: str = "median_house_value",
                 test_size: float = 0.2, random_state: int = 42):
        """
        Initialize the DataProcessor.
        
        Args:
            data_path: Path to the CSV file
            target_col: Name of the target column
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
        """
        self.data_path = Path(data_path)
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state
        self.df: Optional[pd.DataFrame] = None
        self.X_train: Optional[pd.DataFrame] = None
        self.X_test: Optional[pd.DataFrame] = None
        self.y_train: Optional[pd.Series] = None
        self.y_test: Optional[pd.Series] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file with proper error handling.
        
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            pd.errors.EmptyDataError: If file is empty
        """
        logger.info(f"Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded {len(self.df):,} rows and {len(self.df.columns)} columns")
            return self.df
        except pd.errors.EmptyDataError:
            logger.error("Data file is empty")
            raise
    
    def get_column_types(self) -> Tuple[List[str], List[str]]:
        """
        Identify numerical and categorical columns.
        
        Returns:
            Tuple of (numerical_columns, categorical_columns)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=["object"]).columns.tolist()
        
        # Remove target from numerical columns if present
        if self.target_col in num_cols:
            num_cols.remove(self.target_col)
        
        logger.info(f"Found {len(num_cols)} numerical and {len(cat_cols)} categorical features")
        return num_cols, cat_cols
    
    def analyze_missing_values(self) -> pd.Series:
        """
        Analyze missing values in the dataset.
        
        Returns:
            Series with count of missing values per column
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        missing = self.df.isna().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'missing_count': missing,
            'missing_percentage': missing_pct
        })
        
        cols_with_missing = missing_df[missing_df['missing_count'] > 0]
        if len(cols_with_missing) > 0:
            logger.warning(f"Missing values detected:\n{cols_with_missing}")
        else:
            logger.info("No missing values found in the dataset")
        
        return missing
    
    def split_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into training and testing sets.
        
        We use stratified sampling based on income categories to ensure
        our test set is representative of the overall population.
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Create income categories for stratified sampling
        self.df["income_category"] = pd.cut(
            self.df["median_income"],
            bins=[0, 1.5, 3.0, 4.5, 6.0, np.inf],
            labels=[1, 2, 3, 4, 5]
        )
        
        X = self.df.drop(columns=[self.target_col, "income_category"])
        y = self.df[self.target_col]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=self.df["income_category"]
        )
        
        # Drop the temporary category column
        self.df = self.df.drop(columns=["income_category"])
        
        logger.info(f"Data split complete: {len(self.X_train):,} train, {len(self.X_test):,} test")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the dataset.
        
        Returns:
            Dictionary containing dataset statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "memory_usage_mb": self.df.memory_usage(deep=True).sum() / 1024**2,
            "numeric_columns": len(self.df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": len(self.df.select_dtypes(include=["object"]).columns),
            "missing_values_total": self.df.isna().sum().sum(),
            "duplicate_rows": self.df.duplicated().sum(),
            "target_stats": {
                "mean": self.df[self.target_col].mean(),
                "median": self.df[self.target_col].median(),
                "std": self.df[self.target_col].std(),
                "min": self.df[self.target_col].min(),
                "max": self.df[self.target_col].max()
            }
        }
        
        return summary


class FeatureEngineer:
    """
    Creates meaningful features from raw data.
    
    Feature engineering is where domain knowledge meets creativity.
    We transform raw measurements into insights that help our models
    understand the underlying patterns in housing prices.
    """
    
    def __init__(self):
        self.preprocessor: Optional[ColumnTransformer] = None
        self.feature_names: Optional[List[str]] = None
        
    def create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create meaningful ratio features that capture relationships
        between raw measurements.
        
        These ratios often reveal more about a property than raw counts:
        - rooms_per_household: Spaciousness indicator
        - bedrooms_per_room: Bedroom density
        - population_per_household: Crowding indicator
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with new ratio features
        """
        df = df.copy()
        
        # Avoid division by zero
        df["rooms_per_household"] = df["total_rooms"] / df["households"].replace(0, np.nan)
        df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"].replace(0, np.nan)
        df["population_per_household"] = df["population"] / df["households"].replace(0, np.nan)
        
        logger.info("Created ratio features: rooms_per_household, bedrooms_per_room, population_per_household")
        return df
    
    def create_location_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create location-based features.
        
        California's geography heavily influences housing prices.
        These features capture spatial relationships.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with new location features
        """
        df = df.copy()
        
        # Distance from major cities (approximate coordinates)
        # San Francisco: 37.7749, -122.4194
        df["distance_to_sf"] = np.sqrt(
            (df["latitude"] - 37.7749)**2 + (df["longitude"] - (-122.4194))**2
        )
        
        # Los Angeles: 34.0522, -118.2437
        df["distance_to_la"] = np.sqrt(
            (df["latitude"] - 34.0522)**2 + (df["longitude"] - (-118.2437))**2
        )
        
        logger.info("Created location features: distance_to_sf, distance_to_la")
        return df
    
    def build_preprocessing_pipeline(self, X_train: pd.DataFrame) -> ColumnTransformer:
        """
        Build a comprehensive preprocessing pipeline.
        
        This pipeline handles:
        - Missing value imputation
        - Feature scaling for numerical data
        - One-hot encoding for categorical data
        
        Args:
            X_train: Training data to fit the pipeline
            
        Returns:
            Fitted ColumnTransformer
        """
        num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()
        
        # Numerical pipeline: impute with median, then scale
        numerical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        
        # Categorical pipeline: impute with most frequent, then one-hot encode
        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer([
            ("num", numerical_pipeline, num_cols),
            ("cat", categorical_pipeline, cat_cols)
        ], remainder="drop")
        
        # Fit the preprocessor
        self.preprocessor.fit(X_train)
        
        # Store feature names
        num_features = num_cols
        cat_features = []
        if cat_cols:
            cat_encoder = self.preprocessor.named_transformers_["cat"].named_steps["onehot"]
            cat_features = [f"{col}_{cat}" for col in cat_cols for cat in cat_encoder.categories_[cat_cols.index(col)]]
        
        self.feature_names = num_features + cat_features
        
        logger.info(f"Preprocessing pipeline built with {len(self.feature_names)} output features")
        return self.preprocessor
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform data using the fitted preprocessor.
        
        Args:
            X: Data to transform
            
        Returns:
            Transformed numpy array
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call build_preprocessing_pipeline() first.")
        
        return self.preprocessor.transform(X)
    
    def get_feature_importance_df(self, importances: np.ndarray) -> pd.DataFrame:
        """
        Create a DataFrame mapping features to their importance scores.
        
        Args:
            importances: Array of feature importances
            
        Returns:
            DataFrame with feature names and importance scores
        """
        if self.feature_names is None:
            raise ValueError("Feature names not available. Build preprocessing pipeline first.")
        
        importance_df = pd.DataFrame({
            "feature": self.feature_names,
            "importance": importances
        }).sort_values("importance", ascending=False)
        
        return importance_df
