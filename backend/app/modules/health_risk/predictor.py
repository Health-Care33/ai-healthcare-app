import os
import joblib
import numpy as np

# ✅ FIX: absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "health_risk_model.pkl")

model = None


def load_health_model():
    global model
    if model is None:
        try:
            print("🔄 Loading health risk model...")
            print("MODEL PATH:", MODEL_PATH)

            # 🔥 DEBUG
            print("FILES IN MODEL DIR:", os.listdir(os.path.join(BASE_DIR, "model")))

            if not os.path.exists(MODEL_PATH):
                print("❌ MODEL FILE NOT FOUND")
                return None

            model = joblib.load(MODEL_PATH)

            print("✅ Health risk model loaded successfully")

        except Exception as e:
            print("❌ MODEL LOAD ERROR:", e)
            return None

    return model


def predict_health_risk(data):

    model = load_health_model()

    if model is None:
        return {"error": "Health risk model not loaded"}

    try:
        input_data = np.array([data])
        prediction = model.predict(input_data)

        return {
            "prediction": prediction[0]
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }
