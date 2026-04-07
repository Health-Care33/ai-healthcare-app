import numpy as np
import cv2
import json
import os
import threading
from tensorflow.keras.models import load_model as keras_load_model

# ✅ paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

model = None
model_lock = threading.Lock()

# ✅ load class labels safely
try:
    with open(CLASS_PATH, "r") as f:
        class_indices = json.load(f)
    CLASS_NAMES = {v: k for k, v in class_indices.items()}
except Exception as e:
    print("❌ Class file error:", e)
    CLASS_NAMES = {}


def load_fingerprint_model():
    global model

    if model is None:
        with model_lock:  # 🔥 thread-safe
            if model is None:
                try:
                    print("🔄 Loading fingerprint model...")

                    if not os.path.exists(MODEL_PATH):
                        raise FileNotFoundError("Model file not found")

                    model = keras_load_model(MODEL_PATH, compile=False)

                    print("✅ Fingerprint model loaded successfully")

                except Exception as e:
                    print("❌ MODEL LOAD ERROR:", e)
                    model = None

    return model


def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not readable")

    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = img.reshape(1, 128, 128, 1)

    return img


def predict_blood_group(image_path):

    model_instance = load_fingerprint_model()

    if model_instance is None:
        return {"error": "Fingerprint model not loaded"}

    try:
        img = preprocess_image(image_path)

        prediction = model_instance.predict(img, verbose=0)

        class_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        blood_group = CLASS_NAMES.get(class_index, "Unknown")

        return {
            "blood_group": blood_group,
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }