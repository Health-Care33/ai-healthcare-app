import os
import joblib
import numpy as np
import threading

# ✅ paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "health_risk_model.pkl")

model = None
model_lock = threading.Lock()

# 🔥 IMPORTANT: feature order (MUST MATCH TRAINING)
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
        with model_lock:  # 🔥 thread-safe
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
        # 🔥 ensure correct order
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

        # 🔥 optional probability (if supported)
        confidence = None
        if hasattr(model_instance, "predict_proba"):
            confidence = float(np.max(model_instance.predict_proba(input_data)))

        return {
            "risk_level": str(prediction),
            "confidence": round(confidence * 100, 2) if confidence else None
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }