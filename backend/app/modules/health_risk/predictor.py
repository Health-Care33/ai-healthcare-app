import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "health_risk_model.pkl"

model = None


def load_model():
    global model
    if model is None:
        try:
            print("📦 Loading health risk model...")
            model = joblib.load(MODEL_PATH)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            raise e
    return model


def predict_health_risk(data):
    try:
        model = load_model()

        # ✅ SAFE input conversion
        features = np.array([[
            float(data.age),
            float(data.gender),
            float(data.bmi),
            float(data.blood_pressure),
            float(data.cholesterol),
            float(data.glucose),
            float(data.heart_rate),
            float(data.smoking),
            float(data.activity)
        ]], dtype=np.float32)

        print("📊 Features:", features)

        prediction = model.predict(features)[0]

        # ✅ SAFE probability handling
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(features)[0][1]
        else:
            probability = 0.0

        return {
            "risk_level": "High Risk" if int(prediction) == 1 else "Low Risk",
            "probability": float(probability)
        }

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return {
            "error": str(e),
            "message": "Model prediction failed"
        }