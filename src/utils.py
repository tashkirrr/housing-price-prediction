"""
Utilities Module

Helper functions and utilities for the California Housing Price Prediction project.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import json
import joblib


def setup_logging(log_level: int = logging.INFO, 
                  log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Optional file path for logging
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def save_model(model, filepath: str, metadata: Optional[dict] = None) -> None:
    """
    Save a model with optional metadata.
    
    Args:
        model: Trained model to save
        filepath: Path to save the model
        metadata: Optional dictionary with model metadata
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    save_dict = {
        "model": model,
        "metadata": metadata or {},
        "saved_at": datetime.now().isoformat()
    }
    
    joblib.dump(save_dict, filepath)
    logging.info(f"Model saved to {filepath}")


def load_model(filepath: str):
    """
    Load a model and its metadata.
    
    Args:
        filepath: Path to the saved model
        
    Returns:
        Tuple of (model, metadata)
    """
    save_dict = joblib.load(filepath)
    model = save_dict["model"]
    metadata = save_dict.get("metadata", {})
    
    logging.info(f"Model loaded from {filepath}")
    if "saved_at" in save_dict:
        logging.info(f"Model originally saved at: {save_dict['saved_at']}")
    
    return model, metadata


def format_currency(value: float) -> str:
    """Format a number as currency."""
    return f"${value:,.2f}"


def create_experiment_dir(base_dir: str = "experiments") -> Path:
    """
    Create a timestamped experiment directory.
    
    Args:
        base_dir: Base directory for experiments
        
    Returns:
        Path to the created directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_dir = Path(base_dir) / timestamp
    exp_dir.mkdir(parents=True, exist_ok=True)
    return exp_dir


def save_metrics(metrics: dict, filepath: str) -> None:
    """Save metrics to a JSON file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=2)
    
    logging.info(f"Metrics saved to {filepath}")


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, "r") as f:
        return json.load(f)
