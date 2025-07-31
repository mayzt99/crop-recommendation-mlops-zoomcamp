FROM python:3.11.3-slim

RUN python -m venv venv

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY predict.py .
COPY models/ ./models/

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]