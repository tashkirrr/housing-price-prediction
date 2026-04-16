"""
MLflow Experiment Tracking Module

Tracks machine learning experiments including parameters, metrics, and artifacts.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import json

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)


class ExperimentTracker:
    """
    Tracks ML experiments using MLflow.
    
    This class provides a convenient interface for:
    - Starting and managing experiments
    - Logging parameters, metrics, and artifacts
    - Tracking model versions
    - Comparing runs
    """
    
    def __init__(self, experiment_name: str = "california_housing",
                 tracking_uri: Optional[str] = None):
        """
        Initialize the experiment tracker.
        
        Args:
            experiment_name: Name of the MLflow experiment
            tracking_uri: URI for MLflow tracking server (None for local)
        """
        self.experiment_name = experiment_name
        
        # Set tracking URI if provided
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        
        # Create or get experiment
        self.experiment = mlflow.set_experiment(experiment_name)
        self.experiment_id = self.experiment.experiment_id
        
        self.current_run_id: Optional[str] = None
        
        logger.info(f"Experiment '{experiment_name}' initialized (ID: {self.experiment_id})")
    
    def start_run(self, run_name: Optional[str] = None,
                  nested: bool = False) -> str:
        """
        Start a new MLflow run.
        
        Args:
            run_name: Optional name for the run
            nested: Whether this is a nested run
            
        Returns:
            Run ID
        """
        run = mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=run_name,
            nested=nested
        )
        self.current_run_id = run.info.run_id
        
        logger.info(f"Started run: {run_name or self.current_run_id}")
        return self.current_run_id
    
    def end_run(self) -> None:
        """End the current run."""
        mlflow.end_run()
        logger.info(f"Ended run: {self.current_run_id}")
        self.current_run_id = None
    
    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log parameters to the current run.
        
        Args:
            params: Dictionary of parameter names and values
        """
        for key, value in params.items():
            mlflow.log_param(key, value)
        logger.info(f"Logged {len(params)} parameters")
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        """
        Log metrics to the current run.
        
        Args:
            metrics: Dictionary of metric names and values
            step: Optional step number for the metrics
        """
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
        logger.info(f"Logged {len(metrics)} metrics")
    
    def log_model(self, model, artifact_path: str = "model",
                  registered_model_name: Optional[str] = None) -> None:
        """
        Log a trained model.
        
        Args:
            model: Trained sklearn model
            artifact_path: Path within the run's artifact directory
            registered_model_name: Optional name to register the model
        """
        mlflow.sklearn.log_model(
            model,
            artifact_path=artifact_path,
            registered_model_name=registered_model_name
        )
        logger.info(f"Logged model to {artifact_path}")
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None) -> None:
        """
        Log a local file as an artifact.
        
        Args:
            local_path: Path to the local file
            artifact_path: Optional directory within the artifact store
        """
        mlflow.log_artifact(local_path, artifact_path)
        logger.info(f"Logged artifact: {local_path}")
    
    def log_artifacts(self, local_dir: str, artifact_path: Optional[str] = None) -> None:
        """
        Log all files in a directory as artifacts.
        
        Args:
            local_dir: Path to the local directory
            artifact_path: Optional directory within the artifact store
        """
        mlflow.log_artifacts(local_dir, artifact_path)
        logger.info(f"Logged artifacts from directory: {local_dir}")
    
    def log_dict(self, dictionary: Dict, artifact_file: str) -> None:
        """
        Log a dictionary as a JSON artifact.
        
        Args:
            dictionary: Dictionary to log
            artifact_file: Name of the artifact file
        """
        mlflow.log_dict(dictionary, artifact_file)
        logger.info(f"Logged dictionary to {artifact_file}")
    
    def set_tags(self, tags: Dict[str, Any]) -> None:
        """
        Set tags for the current run.
        
        Args:
            tags: Dictionary of tag names and values
        """
        for key, value in tags.items():
            mlflow.set_tag(key, value)
        logger.info(f"Set {len(tags)} tags")
    
    def get_best_run(self, metric: str = "rmse", mode: str = "min") -> Optional[Dict]:
        """
        Get the best run based on a metric.
        
        Args:
            metric: Metric name to compare
            mode: 'min' or 'max'
            
        Returns:
            Dictionary with run information or None
        """
        client = MlflowClient()
        runs = client.search_runs(
            experiment_ids=[self.experiment_id],
            order_by=[f"metrics.{metric} {'ASC' if mode == 'min' else 'DESC'}"]
        )
        
        if not runs:
            return None
        
        best_run = runs[0]
        return {
            "run_id": best_run.info.run_id,
            "params": dict(best_run.data.params),
            "metrics": dict(best_run.data.metrics),
            "tags": dict(best_run.data.tags)
        }
    
    def compare_runs(self, metric: str = "rmse") -> list:
        """
        Compare all runs based on a metric.
        
        Args:
            metric: Metric name to compare
            
        Returns:
            List of run information dictionaries
        """
        client = MlflowClient()
        runs = client.search_runs(experiment_ids=[self.experiment_id])
        
        results = []
        for run in runs:
            results.append({
                "run_id": run.info.run_id,
                "run_name": run.data.tags.get("mlflow.runName", "unnamed"),
                "params": dict(run.data.params),
                "metrics": dict(run.data.metrics),
                "start_time": run.info.start_time
            })
        
        # Sort by metric if available
        results.sort(key=lambda x: x["metrics"].get(metric, float('inf')))
        
        return results
    
    def save_model_version(self, model_name: str, run_id: str,
                          description: Optional[str] = None) -> str:
        """
        Save a model version to the model registry.
        
        Args:
            model_name: Name of the registered model
            run_id: Run ID containing the model
            description: Optional description
            
        Returns:
            Version number
        """
        client = MlflowClient()
        
        # Create registered model if it doesn't exist
        try:
            client.create_registered_model(model_name)
        except Exception:
            pass  # Model already exists
        
        # Create model version
        model_version = client.create_model_version(
            name=model_name,
            source=f"runs:/{run_id}/model",
            run_id=run_id,
            description=description
        )
        
        logger.info(f"Created model version: {model_name} v{model_version.version}")
        return model_version.version


def track_experiment(model, X_train, X_test, y_train, y_test,
                    preprocessor, model_name: str = "HistGradientBoosting",
                    params: Optional[Dict] = None,
                    metrics: Optional[Dict] = None) -> str:
    """
    Convenience function to track a complete experiment.
    
    Args:
        model: Trained model
        X_train: Training features
        X_test: Test features
        y_train: Training target
        y_test: Test target
        preprocessor: Fitted preprocessor
        model_name: Name of the model
        params: Model parameters
        metrics: Evaluation metrics
        
    Returns:
        Run ID
    """
    tracker = ExperimentTracker()
    
    with mlflow.start_run(experiment_id=tracker.experiment_id) as run:
        run_id = run.info.run_id
        
        # Log parameters
        if params:
            tracker.log_params(params)
        
        # Log metrics
        if metrics:
            tracker.log_metrics(metrics)
        
        # Log model
        tracker.log_model(model, artifact_path="model")
        
        # Log preprocessor
        import joblib
        preprocessor_path = "preprocessor.pkl"
        joblib.dump(preprocessor, preprocessor_path)
        tracker.log_artifact(preprocessor_path)
        Path(preprocessor_path).unlink()  # Clean up
        
        # Set tags
        tracker.set_tags({
            "model_type": model_name,
            "dataset": "california_housing",
            "version": "1.0.0"
        })
        
        logger.info(f"Experiment tracked with run ID: {run_id}")
        return run_id
