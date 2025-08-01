# Crop Recommendation MLOps Project

A machine learning project that recommends optimal crops based on soil and environmental conditions using MLOps best practices.

## Project Overview

This project implements an end-to-end MLOps pipeline for crop recommendation using:
- **Random Forest Classifier** for crop prediction
- **MLflow** for experiment tracking and model registry
- **Prefect** for workflow orchestration
- **Docker** for containerization
- **Evidently AI** for monitoring
- **Github Actions** for CI/CD

## 📁 Project Structure

```
mlops-zoomcamp-project/
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── crop_monitoring
│   ├──monitoring_report.html
│   └──monitoring.py
├── data/
│   └── Crop_recommendation.csv
├── models/
│   ├── dv.pkl
│   └── random_forest_model.pkl
├── tests/
│   ├── integration_test.py
│   └── unit_test.py
├── crop_prediction/
│   ├── predict.py
│   ├── Dockerfile
│   ├── test.py
│   └── requirements.txt
├── training_pipeline/
│   ├── prefect_training_pipeline.py
│   └── train.ipynb
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mayzt99/crop-recommendation-mlops-zoomcamp.git
cd mlops-zoomcamp-project
```
2. **Create Virtual Environment**
```bash
python -m venv venv
```

3. **Install dependencies:**
```bash
pip install -r crop_prediction/requirements.txt
```

4. **Start MLflow server:**
```bash
mlflow server --host 127.0.0.1 --port 5000
```

5. **Start Prefect server:**
```bash
prefect orion start
```

## 🔧 Usage

### Training the Model

**Train the Model with MLflow and Prefect**
```bash
python training_pipeline/prefect_training_pipeline.py
```

### Running Predictions

1. **Start the prediction service:**
```bash
uvicorn predict:app --host 0.0.0.0 --port 9696
```

2. **Make predictions:**
```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '[{"N": 90, "P": 42, "K": 43, "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9}]'
OR
python crop_prediction/predict.py
```

### Docker Deployment

1. **Build Docker image:**
```bash
docker build -t crop-recommendation-service:v1 crop_prediction/
```

2. **Run container:**
```bash
docker run -p 9696:9696 crop-recommendation-service:v1
```

## 🧪 Testing & Quality

### Run Tests
```bash
cd tests
pytest unit_test.py -v
pytest integration_test.py -v
```

### Code Formatting
```bash
black .
```

### Linting
```bash
pylint *.py tests/
```

## 📈 Model Performance
The Random Forest model achieves an accuracy of approximately 95% on the crop recommendation dataset.


## 📊 Model Features

The model uses the following features to predict optimal crops:

| Feature | Description | Unit |
|---------|-------------|------|
| N | Nitrogen content | ratio |
| P | Phosphorous content | ratio |
| K | Potassium content | ratio |
| temperature | Temperature | °C |
| humidity | Relative humidity | % |
| ph | pH value | - |
| rainfall | Rainfall | mm |

## 🎯 Supported Crops

The model can recommend the following crops:
- Rice
- Maize
- Chickpea
- Kidneybeans
- Pigeonpeas
- Mothbeans
- Mungbean
- Blackgram
- Lentil
- Pomegranate
- Banana
- Mango
- Grapes
- Watermelon
- Muskmelon
- Apple
- Orange
- Papaya
- Coconut
- Cotton
- Jute
- Coffee

## 🔄 MLOps Pipeline

### 1. Data Pipeline
- Load crop recommendation dataset
- Feature engineering and preprocessing
- Train/test split

### 2. Training Pipeline
- Hyperparameter optimization with Hyperopt
- Model training with Random Forest
- Experiment tracking with MLflow
- Model registration

### 3. Deployment Pipeline
- Model serving with Flask
- Containerization with Docker
- Health checks and monitoring

### 4. Monitoring Pipeline
- Model performance tracking
- Data drift detection with Evidently

### 5. CI/CD Pipeline
- Automated testing with GitHub Actions
- Continuous integration and deployment

```

## 📝 API Documentation

### Prediction Endpoint

**POST** `/predict`

**Request Body:**
```json
[{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}]
```

**Response:**
```json
{
  "Crop Recommendation": ["rice"]
}
```

