# System Architecture

## Overview

This document describes the architecture of the California House Price Prediction system.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Jupyter    │  │  Streamlit   │  │   API Clients        │  │
│  │   Notebook   │  │     App      │  │   (curl, Python)     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────┼─────────────────────┼──────────────┘
          │                 │                     │
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INTERFACE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              FastAPI REST API (api/main.py)              │    │
│  │  • /predict (single prediction)                         │    │
│  │  • /predict/batch (batch predictions)                   │    │
│  │  • /health (health check)                               │    │
│  │  • /model/info (model metadata)                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Data       │  │   Feature    │  │   Model              │  │
│  │ Processing   │  │ Engineering  │  │   Training           │  │
│  │              │  │              │  │   & Evaluation       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Trained ML Model                           │    │
│  │         (HistGradientBoostingRegressor)                 │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Data       │  │   Models     │  │   MLflow             │  │
│  │   (CSV)      │  │   (joblib)   │  │   Experiments        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Client Layer

**Jupyter Notebook**
- Interactive exploration and model development
- Educational walkthrough of the ML pipeline
- Visualization and analysis

**Streamlit App**
- User-friendly web interface
- Interactive sliders for feature input
- Real-time predictions with map visualization

**API Clients**
- Programmatic access to predictions
- Integration with external systems
- Batch processing capabilities

### 2. Interface Layer

**FastAPI Application**
- RESTful API endpoints
- Automatic API documentation (Swagger/OpenAPI)
- Input validation with Pydantic models
- Error handling and logging

### 3. Service Layer

**Data Processing (`src/data_processing.py`)**
- Data loading and validation
- Missing value handling
- Train-test splitting with stratification
- Data quality checks

**Feature Engineering (`src/data_processing.py`)**
- Ratio feature creation
- Distance calculations
- Preprocessing pipeline construction

**Model Training (`src/models.py`)**
- Multiple model comparison
- Cross-validation
- Hyperparameter tuning
- Model evaluation

### 4. Model Layer

**HistGradientBoostingRegressor**
- Final selected model
- Trained on engineered features
- Persisted with joblib

### 5. Storage Layer

**Data Storage**
- Raw CSV files
- Version controlled (if small)

**Model Storage**
- Serialized models (joblib)
- Preprocessors and metadata

**Experiment Tracking**
- MLflow for experiment management
- Parameter and metric logging
- Model versioning

## Data Flow

```
1. Input → Validation → Preprocessing → Feature Engineering
2. Features → Model → Prediction
3. Prediction → Formatting → Response
```

## Deployment Options

### Local Development
```
Jupyter Notebook → Local Python Environment
```

### Docker Deployment
```
Docker Compose → API + Streamlit + MLflow
```

### Production Deployment
```
Kubernetes → Scalable API pods
Cloud Services → AWS/GCP/Azure
```

## Security Considerations

- Input validation on all endpoints
- No sensitive data in logs
- Docker non-root user
- CORS configuration for API

## Monitoring

- Health check endpoints
- MLflow experiment tracking
- Logging at all layers
- Performance metrics
