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
                if not os.path.exists(MODEL_PATH):
                    raise Exception("Model not found")

                model = load_model(MODEL_PATH, compile=False)

    return model


# ================= FILE NAME CHECK =================
def is_valid_fingerprint_filename(filename: str):
    if not filename:
        return False

    name = filename.lower()

    allowed_keywords = [
        "finger",
        "fingerprint",
        "thumb",
        "blood",
        "patient"
    ]

    return any(keyword in name for keyword in allowed_keywords)


# ================= PREPROCESS =================
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not readable")

    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0

    return np.expand_dims(img, axis=0)


# ================= MAIN =================
def predict_blood_group(image_path, filename=None):

    try:

        # ✅ 1️⃣ FILE NAME CHECK
        if not is_valid_fingerprint_filename(filename):
            return {
                "success": False,
                "error": "Invalid filename (use finger/blood/patient keyword)"
            }

        # ✅ 2️⃣ MODEL LOAD
        model_instance = load_fingerprint_model()

        # ✅ 3️⃣ PREPROCESS
        img = preprocess_image(image_path)

        # ✅ 4️⃣ PREDICT
        predictions = model_instance.predict(img, verbose=0)[0]
        predictions = np.nan_to_num(predictions)

        top_index = int(np.argmax(predictions))
        top_conf = float(predictions[top_index])

        # ✅ 5️⃣ RESPONSE
        return {
            "success": True,
            "blood_group": CLASS_NAMES[top_index],
            "confidence": round(top_conf * 100, 2),
            "top_2": [
                {
                    "blood_group": CLASS_NAMES[i],
                    "confidence": round(float(predictions[i]) * 100, 2)
                }
                for i in predictions.argsort()[-2:][::-1]
            ]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
