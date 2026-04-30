import os
import joblib
import numpy as np
import threading

from app.modules.health_risk.service import get_ai_disease_prediction

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "health_risk_model.pkl")

model = None
model_lock = threading.Lock()

# ================= FEATURE ORDER =================
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


# ================= LOAD MODEL =================
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


# ================= PREPROCESS =================
def preprocess_input(data: dict):
    try:
        return np.array([[float(data.get(f, 0)) for f in FEATURE_ORDER]])
    except Exception as e:
        raise Exception(f"Input preprocessing failed: {str(e)}")


# ================= PREDICT =================
def predict_health_risk(data: dict):

    try:
        model_instance = load_health_model()

        if model_instance is None:
            return {"error": "Health risk model not loaded"}

        input_data = preprocess_input(data)

        # ================= ML PREDICTION =================
        prediction = model_instance.predict(input_data)[0]

        # safe conversion
        try:
            prediction = int(prediction)
        except:
            prediction = 0

        risk = "High" if prediction == 1 else "Low"

        # ================= CONFIDENCE (SAFE) =================
        confidence = None
        if hasattr(model_instance, "predict_proba"):
            proba = model_instance.predict_proba(input_data)
            confidence = float(np.max(proba)) * 100

        # ================= AI CALL (SAFE WRAP) =================
        try:
            diseases = get_ai_disease_prediction(data, risk)
        except Exception as ai_error:
            print("⚠️ AI Error:", ai_error)
            diseases = "AI prediction unavailable"

        # ================= RESPONSE =================
        return {
            "risk_level": risk,
            "confidence": round(confidence, 2) if confidence is not None else 0,
            "possible_diseases": diseases
        }

    except Exception as e:
        print("❌ Prediction Error:", e)
        return {
            "error": "Prediction failed",
            "details": str(e)
        }