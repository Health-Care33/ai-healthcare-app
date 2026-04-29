import os
import joblib
import numpy as np
import threading

# ✅ AI FUNCTION
from app.modules.health_risk.service import get_ai_disease_prediction

# ✅ paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "health_risk_model.pkl")

model = None
model_lock = threading.Lock()

# ⚠️ DO NOT CHANGE ORDER (model trained on this)
FEATURE_ORDER = [
    "age",
    "bmi",
    "blood_pressure",
    "cholesterol",
    "glucose",
    "smoking",
    "alcohol",
    "physical_activity"
]


def load_health_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading health risk model...")

                    if not os.path.exists(MODEL_PATH):
                        raise FileNotFoundError("Model file not found")

                    model = joblib.load(MODEL_PATH)

                    print("✅ Health risk model loaded successfully")

                except Exception as e:
                    print("❌ MODEL LOAD ERROR:", e)
                    model = None

    return model


def preprocess_input(data: dict):
    try:
        input_list = [data.get(feature, 0) for feature in FEATURE_ORDER]
        return np.array([input_list])
    except Exception as e:
        raise Exception(f"Input preprocessing failed: {str(e)}")


def predict_health_risk(data: dict):

    model_instance = load_health_model()

    if model_instance is None:
        return {"error": "Health risk model not loaded"}

    try:
        input_data = preprocess_input(data)

        prediction = model_instance.predict(input_data)[0]

        confidence = None
        if hasattr(model_instance, "predict_proba"):
            confidence = float(np.max(model_instance.predict_proba(input_data)))

        # ✅ CLEAN RISK LABEL
        risk = "High" if str(prediction) == "1" else "Low"

        # ✅ AI CALL (GROQ)
        diseases = get_ai_disease_prediction(data, risk)

        return {
            "risk_level": risk,
            "confidence": round(confidence * 100, 2) if confidence else None,
            "possible_diseases": diseases
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }