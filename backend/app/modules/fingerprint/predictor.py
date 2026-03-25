import numpy as np
import cv2
import json
import os

# ---------- SAFE PATH SETUP ----------

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

# ---------- GLOBAL CACHE ----------

model = None
CLASS_NAMES = None


# ---------- LOAD MODEL (LAZY LOAD) ----------

def load_model():
    global model

    if model is None:
        print("🔄 Loading TensorFlow model...")

        import tensorflow as tf  # ✅ lazy import (IMPORTANT)

        model = tf.keras.models.load_model(MODEL_PATH)

    return model


# ---------- LOAD CLASS INDICES ----------

def load_classes():
    global CLASS_NAMES

    if CLASS_NAMES is None:
        with open(CLASS_PATH, "r") as f:
            class_indices = json.load(f)

        # index → class name
        CLASS_NAMES = {v: k for k, v in class_indices.items()}

    return CLASS_NAMES


# ---------- PREDICTION FUNCTION ----------

def predict_blood_group(image_path):

    print("📸 READING IMAGE:", image_path)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {
            "blood_group": "Unknown",
            "confidence": 0,
            "top_predictions": [],
            "error": "Image not readable"
        }

    # resize image
    img = cv2.resize(img, (128, 128))

    # normalize
    img = img / 255.0

    # reshape for CNN input
    img = img.reshape(1, 128, 128, 1)

    # ---------- LOAD MODEL & CLASSES ----------
    model = load_model()
    CLASS_NAMES = load_classes()

    # prediction
    prediction = model.predict(img)

    print("📊 RAW PREDICTION:", prediction)

    # best prediction
    class_index = int(np.argmax(prediction))
    blood_group = CLASS_NAMES[class_index]
    confidence = float(np.max(prediction))

    # ---------- TOP 3 PREDICTIONS ----------
    top3 = prediction[0].argsort()[-3:][::-1]

    top_predictions = []

    for i in top3:
        top_predictions.append({
            "blood_group": CLASS_NAMES[int(i)],
            "confidence": float(prediction[0][i])
        })

    return {
        "blood_group": blood_group,
        "confidence": confidence,
        "top_predictions": top_predictions
    }