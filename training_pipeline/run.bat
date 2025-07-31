@echo off

if "%1"=="install" (
    pip install -r requirements.txt
) else if "%1"=="test" (
    pytest tests/ -v
) else if "%1"=="lint" (
    pylint *.py tests/
) else if "%1"=="format" (
    black .
) else if "%1"=="train" (
    python train.py
) else if "%1"=="predict" (
    python predict.py
) else if "%1"=="docker-build" (
    docker build -t crop-recommendation-service:v1 .
) else if "%1"=="docker-run" (
    docker run -p 9696:9696 crop-recommendation-service:v1
) else if "%1"=="quality" (
    black .
    pylint *.py tests/
    pytest tests/ -v
) else (
    echo Usage: run.bat [install^|test^|lint^|format^|train^|predict^|docker-build^|docker-run^|quality]
)