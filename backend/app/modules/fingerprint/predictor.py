import numpy as np
import cv2
import tensorflow as tf
import json
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

# ❌ REMOVE global model load
model = None

# load class indices
with open(CLASS_PATH, "r") as f:
    class_indices = json.load(f)

CLASS_NAMES = {v: k for k, v in class_indices.items()}


def load_model():
    global model
    if model is None:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return model


def predict_blood_group(image_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {
            "blood_group": "Unknown",
            "confidence": 0,
            "top_predictions": [],
            "error": "Image not readable"
        }

    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = img.reshape(1, 128, 128, 1)

    # ✅ load model only when needed
    model = load_model()

    prediction = model.predict(img)

    class_index = int(np.argmax(prediction))
    blood_group = CLASS_NAMES[class_index]
    confidence = float(np.max(prediction))

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
