.PHONY: install test lint format clean train predict docker-build docker-run

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	pytest tests/ -v

# Run linting
lint:
	pylint *.py tests/

# Format code
format:
	black .

# Clean artifacts
clean:
	rm -rf models/
	rm -rf mlruns/
	rm -rf mlartifacts/
	rm -rf __pycache__/
	rm -rf .pytest_cache/

# Train model
train:
	python train.py

# Run prediction service
predict:
	python predict.py

# Build Docker image
docker-build:
	docker build -t crop-recommendation-service:v1 .

# Run Docker container
docker-run:
	docker run -p 9696:9696 crop-recommendation-service:v1

# Run all quality checks
quality: format lint test

# Full pipeline
all: install quality train