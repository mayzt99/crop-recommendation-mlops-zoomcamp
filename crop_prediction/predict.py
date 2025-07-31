import os

# Determine directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change working directory to script’s directory
os.chdir(script_dir)

import pickle
from flask import Flask, request, jsonify

with open("./models/random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("./models/dv.pkl", "rb") as dv_file:
    dv = pickle.load(dv_file)


def predict(data):
    X = dv.transform(data)
    preds = model.predict(X)
    return preds


app = Flask("Crop Recommendation")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    soil_data = request.get_json()
    predictions = predict(soil_data)
    predictions = str(predictions[0])
    result = {"Crop Recommendation": predictions}
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9696, debug=True)
