import numpy as np
import cv2
import os
import threading
from tensorflow.keras.models import load_model

# ✅ paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_model.h5")

model = None
model_lock = threading.Lock()

# ✅ class names (same as training)
CLASS_NAMES = ["A", "B", "AB", "O"]


def load_fingerprint_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading fingerprint model...")

                    if not os.path.exists(MODEL_PATH):
                        raise FileNotFoundError("Model file not found")

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Fingerprint model loaded successfully")

                except Exception as e:
                    print("❌ MODEL LOAD ERROR:", e)
                    model = None

    return model


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not readable")

    # ✅ BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ✅ resize (same as training)
    img = cv2.resize(img, (224, 224))

    # ✅ normalize
    img = img.astype("float32") / 255.0

    # ✅ batch dimension
    img = np.expand_dims(img, axis=0)

    return img


def predict_blood_group(image_path):

    model_instance = load_fingerprint_model()

    if model_instance is None:
        return {"error": "Fingerprint model not loaded"}

    try:
        img = preprocess_image(image_path)

        prediction = model_instance.predict(img, verbose=0)[0]

        class_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        return {
            "blood_group": CLASS_NAMES[class_index],
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }