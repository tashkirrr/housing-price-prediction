# California House Price Prediction

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688)](https://fastapi.tiangolo.com/)

A comprehensive, production-ready machine learning solution for predicting California house prices using advanced regression techniques.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project implements an end-to-end machine learning pipeline for predicting median house values in California based on the 1990 census data. It demonstrates industry best practices including:

- Comprehensive EDA with insightful visualizations
- Feature engineering to extract maximum value from data
- Multiple model comparison with cross-validation
- Hyperparameter tuning for optimal performance
- Production deployment via FastAPI and Streamlit
- Experiment tracking with MLflow

### Why This Project?

Whether you're a data science beginner looking to learn ML workflows or a practitioner seeking a reference implementation, this project provides:

- Clean, modular, and well-documented code
- Production-ready API and web interface
- Comprehensive testing and CI/CD setup
- Docker support for easy deployment
- Detailed explanations at every step

---

## Features

### Machine Learning
- **5 Regression Models**: Linear Regression, Ridge, Lasso, Random Forest, HistGradientBoosting
- **Feature Engineering**: Ratio features, distance calculations, and more
- **Cross-Validation**: 5-fold CV for robust model evaluation
- **Hyperparameter Tuning**: GridSearchCV for optimal parameters
- **Model Persistence**: Save/load trained models with joblib

### Web Applications
- **Streamlit App**: Interactive web interface for predictions
- **FastAPI**: Production-ready REST API with auto-generated docs
- **Batch Predictions**: Process multiple properties at once

### Visualization & Analysis
- Geographic distribution maps
- Correlation heatmaps
- Feature importance plots
- Residual analysis
- Model comparison charts

### Developer Tools
- **MLflow Integration**: Track experiments and compare runs
- **Comprehensive Logging**: Detailed logs for debugging
- **Unit Tests**: pytest suite for code quality
- **Docker Support**: Containerized deployment

---

## Project Structure

```
housing-price-prediction/
├── api/                          # FastAPI application
│   ├── main.py                   # API endpoints
│   ├── requirements.txt          # API dependencies
│   └── test_api.py               # API tests
│
├── app/                          # Streamlit web app
│   ├── app.py                    # Streamlit application
│   └── requirements.txt          # App dependencies
│
├── data/                         # Dataset storage
│   ├── housing.csv               # California housing data
│   └── README.md                 # Data documentation
│
├── docs/                         # Additional documentation
│   └── architecture.md           # System architecture
│
├── models/                       # Saved models
│   ├── house_price_model.pkl     # Trained model
│   └── preprocessor.pkl          # Data preprocessor
│
├── notebooks/                    # Jupyter notebooks
│   └── 01_end_to_end_house_price_prediction.ipynb
│
├── reports/                      # Generated reports
│   └── figures/                  # Visualization outputs
│
├── src/                          # Source code package
│   ├── __init__.py
│   ├── data_processing.py        # Data loading & preprocessing
│   ├── models.py                 # Model training & evaluation
│   ├── visualization.py          # Plotting functions
│   ├── experiment_tracking.py    # MLflow integration
│   └── utils.py                  # Utility functions
│
├── tests/                        # Unit tests
│   ├── test_data_processing.py
│   ├── test_models.py
│   └── conftest.py
│
├── .dockerignore                 # Docker ignore rules
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker Compose config
├── Dockerfile                    # Docker image definition
├── LICENSE                       # MIT License
├── README.md                     # This file
├── requirements.txt              # Main dependencies
└── setup.py                      # Package setup
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/tashkirrr/housing-price-prediction.git
   cd housing-price-prediction
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model** (or use pre-trained)
   ```bash
   # Run the Jupyter notebook
   jupyter notebook notebooks/01_end_to_end_house_price_prediction.ipynb
   ```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t housing-price-prediction .
docker run -p 8000:8000 -p 8501:8501 housing-price-prediction
```

---

## Usage

### 1. Jupyter Notebook (Recommended for Learning)

Explore the complete ML workflow with detailed explanations:

```bash
jupyter notebook notebooks/01_end_to_end_house_price_prediction.ipynb
```

**What you'll learn:**
- Data exploration and visualization
- Feature engineering techniques
- Model comparison methodology
- Hyperparameter tuning strategies
- Model evaluation best practices

### 2. Streamlit Web App (Interactive Predictions)

Launch the interactive web interface:

```bash
streamlit run app/app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Interactive sliders for all features
- Real-time map visualization
- Property profile metrics
- Model insights and tips

### 3. FastAPI (Production API)

Start the REST API server:

```bash
# From project root
uvicorn api.main:app --reload
```

API will be available at `http://localhost:8000`

**Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /model/info` - Model metadata
- `POST /predict` - Single prediction
- `POST /predict/batch` - Batch predictions
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

**Example API call:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 41,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "ocean_proximity": "NEAR BAY"
  }'
```

### 4. Python Package

Use the package programmatically:

```python
from src.data_processing import DataProcessor, FeatureEngineer
from src.models import ModelTrainer, ModelEvaluator

# Load and process data
processor = DataProcessor("data/housing.csv")
df = processor.load_data()
X_train, X_test, y_train, y_test = processor.split_data()

# Engineer features
engineer = FeatureEngineer()
X_train = engineer.create_ratio_features(X_train)
preprocessor = engineer.build_preprocessing_pipeline(X_train)

# Train and evaluate
trainer = ModelTrainer()
results = trainer.compare_models(X_train_processed, y_train)
```

---

## Model Performance

Our final model (HistGradientBoostingRegressor) achieves excellent performance:

| Metric | Training | Test |
|--------|----------|------|
| **R² Score** | 0.89 | 0.81 |
| **RMSE** | $35,000 | $45,000 |
| **MAE** | $25,000 | $32,000 |
| **MAPE** | 12.5% | 16.2% |

### Key Insights

- **Median Income** is the strongest predictor (correlation: 0.69)
- **Ocean Proximity** significantly impacts prices
- **Location Features** (distance to SF/LA) add value
- **Ratio Features** improve model understanding

### Feature Importance (Top 10)

1. Median Income (35%)
2. Ocean Proximity (18%)
3. Distance to SF (12%)
4. Rooms per Household (8%)
5. Latitude (7%)
6. Longitude (6%)
7. Housing Median Age (5%)
8. Distance to LA (4%)
9. Population per Household (3%)
10. Bedrooms per Room (2%)

---

## API Documentation

### Request Format

```json
{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252,
  "ocean_proximity": "NEAR BAY"
}
```

### Response Format

```json
{
  "predicted_price": 225000.50,
  "currency": "USD",
  "timestamp": "2024-01-15T10:30:00",
  "model_version": "1.0.0"
}
```

### Validation Rules

- `total_bedrooms` must be less than or equal to `total_rooms`
- `households` must be less than or equal to `population`
- `ocean_proximity` must be one of: `<1H OCEAN`, `INLAND`, `ISLAND`, `NEAR BAY`, `NEAR OCEAN`

---

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Dataset**: California Housing Prices dataset from the 1990 census
- **Inspiration**: Based on the classic California Housing example from scikit-learn
- **Tutorial Reference**: [YouTube Tutorial](https://youtu.be/I0-xdYWLLKQ)

---

## Contact

tashkirrr - [https://github.com/tashkirrr](https://github.com/tashkirrr)

Project Link: [https://github.com/tashkirrr/housing-price-prediction](https://github.com/tashkirrr/housing-price-prediction)

---

<p align="center">
  Made with Python and Machine Learning
</p>
