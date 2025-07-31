import requests

soil_data = {
    "N": 16,
    "P": 39,
    "K": 20,
    "temperature": 22.5,
    "humidity": 60,
    "ph": 6.5,
    "rainfall": 100.0,
}

url = "http://localhost:9696/predict"
response = requests.post(url, json=soil_data)

print(response.json())
