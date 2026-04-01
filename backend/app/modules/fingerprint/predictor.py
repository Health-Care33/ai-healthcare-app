import numpy as np
import cv2
import json
import os
from keras.models import load_model   # ✅ IMPORTANT CHANGE

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

model = None

# load class indices
with open(CLASS_PATH, "r") as f:
    class_indices = json.load(f)

CLASS_NAMES = {v: k for k, v in class_indices.items()}


def load_model():
    global model
    if model is None:
        try:
            print("🔄 Loading fingerprint model...")
            print("MODEL PATH:", MODEL_PATH)

            if not os.path.exists(MODEL_PATH):
                print("❌ MODEL FILE NOT FOUND")
                return None

            # ✅ FIX: use keras instead of tensorflow
            model = load_model(MODEL_PATH, compile=False)

            print("✅ MODEL LOADED SUCCESS")

        except Exception as e:
            print("❌ MODEL LOAD ERROR:", e)
            return None

    return model


def predict_blood_group(image_path):

    model = load_model()

    if model is None:
        return {
            "error": "Fingerprint model not loaded"
        }

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {
            "error": "Image not readable"
        }

    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = img.reshape(1, 128, 128, 1)

    prediction = model.predict(img)

    class_index = int(np.argmax(prediction))
    blood_group = CLASS_NAMES[class_index]
    confidence = float(np.max(prediction))

    return {
        "blood_group": blood_group,
        "confidence": confidence
    }
