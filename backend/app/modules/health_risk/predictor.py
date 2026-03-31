import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "health_risk_model.pkl"

# Load trained model
model = joblib.load(MODEL_PATH)


def predict_health_risk(data):

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

    risk_level = "High Risk" if prediction == 1 else "Low Risk"

    return {
        "risk_level": risk_level,
        "probability": float(probability)
    } 