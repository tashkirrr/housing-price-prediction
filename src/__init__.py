"""
California Housing Price Prediction Package

A comprehensive machine learning solution for predicting house prices
in California using advanced regression techniques.

Author: Your Name
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "tashkirrr"

from .data_processing import DataProcessor, FeatureEngineer
from .models import ModelTrainer, ModelEvaluator
from .utils import setup_logging, save_model, load_model

__all__ = [
    "DataProcessor",
    "FeatureEngineer", 
    "ModelTrainer",
    "ModelEvaluator",
    "setup_logging",
    "save_model",
    "load_model",
]
