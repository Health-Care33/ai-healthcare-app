import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "health_risk_model.pkl")

# ❌ remove global load
model = None

def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model


def predict_health_risk(data):

    model = load_model()

    input_data = np.array([data])
    prediction = model.predict(input_data)

    return prediction[0]
