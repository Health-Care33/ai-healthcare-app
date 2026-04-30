import numpy as np
import cv2
import os
import threading
from tensorflow.keras.models import load_model

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_model.h5")

model = None
model_lock = threading.Lock()

# ================= LABELS =================
CLASS_NAMES = ["A+","B+","AB+","O+","A-","B-","AB-","O-"]


# ================= LOAD MODEL =================
def load_fingerprint_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading fingerprint prediction model...")

                    if not os.path.exists(MODEL_PATH):
                        raise Exception(f"Model not found at {MODEL_PATH}")

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Model loaded successfully")

                except Exception as e:
                    print("❌ MODEL LOAD ERROR:", e)
                    return None

    return model


# ================= PREPROCESS =================
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not readable")

    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0

    return np.expand_dims(img, axis=0)


# ================= MAIN FUNCTION =================
def predict_blood_group(image_path, filename=None):
    try:

        # ---------------- LOAD MODEL ----------------
        model_instance = load_fingerprint_model()

        if model_instance is None:
            return {
                "success": False,
                "blood_group": "Unknown",
                "confidence": 0.0,
                "warning": None,
                "top_2": [],
                "error": "Model not loaded"
            }

        # ---------------- PREPROCESS ----------------
        img = preprocess_image(image_path)

        # ---------------- PREDICTION ----------------
        predictions = model_instance.predict(img, verbose=0)[0]
        predictions = np.nan_to_num(predictions)

        print("🔍 PROBABILITIES:", predictions)

        # ---------------- RESULT ----------------
        top_index = int(np.argmax(predictions))
        max_conf = float(np.max(predictions))

        top_2_indices = predictions.argsort()[-2:][::-1]

        # ---------------- RESPONSE ----------------
        return {
            "success": True,
            "blood_group": CLASS_NAMES[top_index],

            # ✅ Always present (no crash frontend)
            "confidence": round(max_conf * 100, 2),

            "warning": (
                "Low confidence ⚠️" if max_conf < 0.5 else "High confidence ✅"
            ),

            "top_2": [
                {
                    "blood_group": CLASS_NAMES[int(i)],
                    "confidence": round(float(predictions[i]) * 100, 2)
                }
                for i in top_2_indices
            ],

            "error": None
        }

    except Exception as e:
        print("❌ Prediction error:", e)

        return {
            "success": False,
            "blood_group": "Unknown",
            "confidence": 0.0,
            "warning": None,
            "top_2": [],
            "error": "Prediction failed",
            "details": str(e)
        }