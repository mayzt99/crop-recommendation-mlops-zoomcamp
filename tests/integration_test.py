import pytest

# test endpoint for the Flask app
from crop_prediction.predict import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_predict_endpoint(client):
    response = client.post('/predict', json={
        'N': 30,
        'P': 137,
        'K': 200,
        'temperature': 22.91430043,
        'humidity': 90.70475565,
        'ph': 5.603413172000001,
        'rainfall': 118.6044645
    })
    assert response.status_code == 200
    assert 'Crop Recommendation' in response.json
    assert response.json['Crop Recommendation'] == 'apple'