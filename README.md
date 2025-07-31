# Crop Recommendation MLOps Project

A machine learning project that recommends optimal crops based on soil and environmental conditions using MLOps best practices.

## 🌾 Project Overview

This project implements an end-to-end MLOps pipeline for crop recommendation using:
- **Random Forest Classifier** for crop prediction
- **MLflow** for experiment tracking and model registry
- **Prefect** for workflow orchestration
- **Docker** for containerization
- **Grafana & PostgreSQL** for monitoring

## 📁 Project Structure

```
mlops-zoomcamp-project/
├── data/
│   └── Crop_recommendation.csv
├── models/
│   ├── dv.pkl
│   └── random_forest_model.pkl
├── tests/
│   └── integration_test.py
├── config/
│   ├── grafana_datasources.yaml
│   └── grafana_dashboards.yaml
├── dashboards/
│   └── crop_monitoring.json
├── train.py
├── predict.py
├── prefect_flow.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── Makefile
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
git clone <repository-url>
cd mlops-zoomcamp-project
```

2. **Install dependencies:**
```bash
make install
# or
pip install -r requirements.txt
```

3. **Start MLflow server:**
```bash
mlflow server --host 0.0.0.0 --port 5000
```

## 🔧 Usage

### Training the Model

**Option 1: Direct training**
```bash
make train
# or
python train.py
```

**Option 2: Using Prefect flow**
```bash
python prefect_flow.py
```

### Running Predictions

1. **Start the prediction service:**
```bash
make predict
# or
python predict.py
```

2. **Make predictions:**
```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '[{"N": 90, "P": 42, "K": 43, "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9}]'
```

### Docker Deployment

1. **Build Docker image:**
```bash
make docker-build
```

2. **Run container:**
```bash
make docker-run
```

### Monitoring with Grafana

1. **Start monitoring stack:**
```bash
docker compose up -d
```

2. **Access services:**
- Grafana: http://localhost:3000
- Adminer: http://localhost:8080
- PostgreSQL: localhost:5432

## 🧪 Testing & Quality

### Run Tests
```bash
make test
```

### Code Formatting
```bash
make format
```

### Linting
```bash
make lint
```

### All Quality Checks
```bash
make quality
```

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
- Grafana dashboards for visualization

## 🛠️ Development

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
make install
```

### Adding New Features
1. Create feature branch
2. Implement changes
3. Run quality checks: `make quality`
4. Submit pull request

## 📈 Experiment Tracking

All experiments are tracked in MLflow:
- **Metrics**: Accuracy, Precision, Recall
- **Parameters**: Model hyperparameters
- **Artifacts**: Trained models, preprocessors

Access MLflow UI at: http://localhost:5000

## 🐳 Docker Commands

```bash
# Build image
docker build -t crop-recommendation-service:v1 .

# Run container
docker run -p 9696:9696 crop-recommendation-service:v1

# Run with monitoring stack
docker compose up --build
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

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 🆘 Troubleshooting

### Common Issues

**MLflow server not running:**
```bash
mlflow server --host 0.0.0.0 --port 5000
```

**Port already in use:**
```bash
# Kill process using port 9696
netstat -ano | findstr :9696
taskkill /PID <PID> /F
```

**Docker build fails:**
```bash
# Clean Docker cache
docker system prune -a
```

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section