import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "health_risk_model.pkl"

model = None

def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model


def predict_health_risk(data):
    try:
        model = load_model()

        features = np.array([[  
            data.age,
            data.gender,
            data.bmi,
            data.blood_pressure,
            data.cholesterol,
            data.glucose,
            data.heart_rate,
            data.smoking,
            data.activity
        ]])

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        return {
            "risk_level": "High Risk" if prediction == 1 else "Low Risk",
            "probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}