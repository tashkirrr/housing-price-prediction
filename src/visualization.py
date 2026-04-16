"""
Visualization Module

Creates insightful visualizations for EDA and model evaluation.
"""

import logging
from pathlib import Path
from typing import Optional, List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

# Set default style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 10


class EDAVisualizer:
    """Visualizations for Exploratory Data Analysis."""
    
    def __init__(self, output_dir: str = "reports/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_target_distribution(self, df: pd.DataFrame, target_col: str,
                                  save: bool = True) -> None:
        """Plot the distribution of the target variable."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        sns.histplot(df[target_col], bins=50, kde=True, ax=axes[0])
        axes[0].set_title(f"Distribution of {target_col}")
        axes[0].set_xlabel("Value ($)")
        axes[0].axvline(df[target_col].mean(), color='r', linestyle='--', 
                        label=f'Mean: ${df[target_col].mean():,.0f}')
        axes[0].axvline(df[target_col].median(), color='g', linestyle='--',
                        label=f'Median: ${df[target_col].median():,.0f}')
        axes[0].legend()
        
        # Box plot
        sns.boxplot(x=df[target_col], ax=axes[1])
        axes[1].set_title(f"Box Plot of {target_col}")
        axes[1].set_xlabel("Value ($)")
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "target_distribution.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved target distribution plot")
        plt.show()
    
    def plot_correlation_matrix(self, df: pd.DataFrame, save: bool = True) -> None:
        """Plot correlation matrix of numerical features."""
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", 
                    cmap="RdBu_r", center=0, square=True, linewidths=0.5)
        plt.title("Feature Correlation Matrix")
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "correlation_matrix.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved correlation matrix plot")
        plt.show()
    
    def plot_feature_distributions(self, df: pd.DataFrame, save: bool = True) -> None:
        """Plot distributions of all numerical features."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        n_cols = len(numeric_cols)
        n_rows = (n_cols + 2) // 3
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(15, n_rows * 4))
        axes = axes.flatten()
        
        for i, col in enumerate(numeric_cols):
            sns.histplot(df[col], kde=True, ax=axes[i])
            axes[i].set_title(f"Distribution of {col}")
            axes[i].tick_params(axis='x', rotation=45)
        
        # Hide unused subplots
        for i in range(n_cols, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "feature_distributions.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved feature distributions plot")
        plt.show()
    
    def plot_geographic_distribution(self, df: pd.DataFrame, target_col: str,
                                      save: bool = True) -> None:
        """Plot geographic distribution of housing prices."""
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(df["longitude"], df["latitude"],
                             c=df[target_col], cmap="viridis",
                             alpha=0.5, s=df["population"]/100)
        plt.colorbar(scatter, label=f"{target_col} ($)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("California Housing Prices by Location\n(Size = Population)")
        
        if save:
            plt.savefig(self.output_dir / "geographic_distribution.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved geographic distribution plot")
        plt.show()
    
    def plot_categorical_features(self, df: pd.DataFrame, save: bool = True) -> None:
        """Plot categorical feature distributions."""
        cat_cols = df.select_dtypes(include=["object"]).columns
        
        if len(cat_cols) == 0:
            return
        
        fig, axes = plt.subplots(1, len(cat_cols), figsize=(6*len(cat_cols), 5))
        if len(cat_cols) == 1:
            axes = [axes]
        
        for i, col in enumerate(cat_cols):
            value_counts = df[col].value_counts()
            sns.barplot(x=value_counts.index, y=value_counts.values, ax=axes[i])
            axes[i].set_title(f"Distribution of {col}")
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "categorical_features.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved categorical features plot")
        plt.show()


class ModelVisualizer:
    """Visualizations for model evaluation."""
    
    def __init__(self, output_dir: str = "reports/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_predictions_vs_actual(self, y_true: np.ndarray, y_pred: np.ndarray,
                                    save: bool = True) -> None:
        """Plot predicted vs actual values."""
        plt.figure(figsize=(10, 8))
        
        # Scatter plot
        plt.scatter(y_true, y_pred, alpha=0.5, s=20)
        
        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        plt.xlabel("Actual Price ($)")
        plt.ylabel("Predicted Price ($)")
        plt.title("Predicted vs Actual House Prices")
        plt.legend()
        
        # Format axes as currency
        ax = plt.gca()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "predictions_vs_actual.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved predictions vs actual plot")
        plt.show()
    
    def plot_residuals(self, y_true: np.ndarray, y_pred: np.ndarray,
                       save: bool = True) -> None:
        """Plot residual analysis."""
        residuals = y_true - y_pred
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Residuals vs Predicted
        axes[0, 0].scatter(y_pred, residuals, alpha=0.5, s=20)
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_xlabel("Predicted Price ($)")
        axes[0, 0].set_ylabel("Residuals ($)")
        axes[0, 0].set_title("Residuals vs Predicted")
        
        # Residual distribution
        sns.histplot(residuals, kde=True, ax=axes[0, 1])
        axes[0, 1].axvline(x=0, color='r', linestyle='--')
        axes[0, 1].set_xlabel("Residual ($)")
        axes[0, 1].set_title("Residual Distribution")
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title("Q-Q Plot (Normality Check)")
        
        # Residuals vs Actual
        axes[1, 1].scatter(y_true, residuals, alpha=0.5, s=20)
        axes[1, 1].axhline(y=0, color='r', linestyle='--')
        axes[1, 1].set_xlabel("Actual Price ($)")
        axes[1, 1].set_ylabel("Residuals ($)")
        axes[1, 1].set_title("Residuals vs Actual")
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "residual_analysis.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved residual analysis plot")
        plt.show()
    
    def plot_feature_importance(self, importance_df: pd.DataFrame, top_n: int = 15,
                                 save: bool = True) -> None:
        """Plot feature importance."""
        plt.figure(figsize=(10, 8))
        
        top_features = importance_df.head(top_n)
        sns.barplot(x="importance", y="feature", data=top_features)
        plt.title(f"Top {top_n} Most Important Features")
        plt.xlabel("Importance")
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "feature_importance.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved feature importance plot")
        plt.show()
    
    def plot_cv_results(self, cv_results: pd.DataFrame, save: bool = True) -> None:
        """Plot cross-validation results comparison."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # RMSE comparison
        sns.barplot(x="model", y="cv_rmse_mean", data=cv_results, ax=axes[0])
        axes[0].set_title("CV RMSE (lower is better)")
        axes[0].set_ylabel("RMSE ($)")
        axes[0].tick_params(axis='x', rotation=45)
        
        # MAE comparison
        sns.barplot(x="model", y="cv_mae_mean", data=cv_results, ax=axes[1])
        axes[1].set_title("CV MAE (lower is better)")
        axes[1].set_ylabel("MAE ($)")
        axes[1].tick_params(axis='x', rotation=45)
        
        # R² comparison
        sns.barplot(x="model", y="cv_r2_mean", data=cv_results, ax=axes[2])
        axes[2].set_title("CV R² (higher is better)")
        axes[2].set_ylabel("R² Score")
        axes[2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / "cv_results_comparison.png", dpi=300, bbox_inches="tight")
            logger.info(f"Saved CV results comparison plot")
        plt.show()
