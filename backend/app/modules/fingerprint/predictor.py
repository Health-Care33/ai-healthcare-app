import numpy as np
import cv2
import os
import threading
from tensorflow.keras.models import load_model

from app.modules.fingerprint.model.fingerprint_validation import is_fingerprint

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
                    print("📂 MODEL PATH:", MODEL_PATH)

                    if not os.path.exists(MODEL_PATH):
                        raise Exception("Fingerprint prediction model not found")

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Prediction model loaded successfully")

                except Exception as e:
                    print("❌ MODEL LOAD ERROR:", e)
                    raise e

    return model


# ================= PREPROCESS =================
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Image not readable: {image_path}")

    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0

    return np.expand_dims(img, axis=0)


# ================= FILENAME VALIDATION =================
def is_valid_fingerprint_filename(filename: str):
    name = filename.lower()

    allowed_keywords = [
        "finger",
        "fingerprint",
        "thumb",
        "blood",
        "patient"
    ]

    return any(keyword in name for keyword in allowed_keywords)


# ================= MAIN FUNCTION =================
def predict_blood_group(image_path, filename=None):
    try:

        # filename validation
        if filename and not is_valid_fingerprint_filename(filename):
            return {
                "error": "Invalid filename",
                "details": "Filename must contain fingerprint/blood/patient keyword"
            }

        # fingerprint validation
        try:
            if not is_fingerprint(image_path):
                return {
                    "error": "Invalid image",
                    "details": "Not a valid fingerprint"
                }
        except Exception as e:
            return {
                "error": "Validation failed",
                "details": str(e)
            }

        model_instance = load_fingerprint_model()

        if model_instance is None:
            return {"error": "Prediction model not loaded"}

        img = preprocess_image(image_path)

        # ✅ FINAL FIX (NO DOUBLE SOFTMAX)
        predictions = model_instance.predict(img, verbose=0)[0]
        predictions = np.nan_to_num(predictions)

        print("🔍 FINAL PROBABILITIES:", predictions)
        print("🔢 SUM:", np.sum(predictions))

        max_conf = float(np.max(predictions))
        top_index = int(np.argmax(predictions))

        # Top 2 predictions
        top_2_indices = predictions.argsort()[-2:][::-1]

        return {
            "success": True,
            "blood_group": CLASS_NAMES[top_index],
            "confidence": round(max_conf * 100, 2),
            "warning": (
                "Very Low Confidence ❌" if max_conf < 0.4 else
                "Medium Confidence ⚠️" if max_conf < 0.7 else
                "High Confidence ✅"
            ),
            "top_2": [
                {
                    "blood_group": CLASS_NAMES[int(i)],
                    "confidence": round(float(predictions[i]) * 100, 2)
                }
                for i in top_2_indices
            ]
        }

    except Exception as e:
        print("❌ Prediction error:", e)
        return {
            "error": "Prediction failed",
            "details": str(e)
        }