import numpy as np
import cv2
import json
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

model = None
CLASS_NAMES = None


def load_model():
    global model
    if model is None:
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            print("Model Load Error:", e)
    return model


def load_classes():
    global CLASS_NAMES
    if CLASS_NAMES is None:
        with open(CLASS_PATH, "r") as f:
            class_indices = json.load(f)
        CLASS_NAMES = {v: k for k, v in class_indices.items()}
    return CLASS_NAMES


def predict_blood_group(image_path):

    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {"error": "Image not readable"}

        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        img = img.reshape(1, 128, 128, 1)

        model = load_model()
        CLASS_NAMES = load_classes()

        if model is None:
            return {"error": "Model not loaded"}

        prediction = model.predict(img)

        class_index = int(np.argmax(prediction))
        blood_group = CLASS_NAMES[class_index]
        confidence = float(np.max(prediction))

        return {
            "blood_group": blood_group,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}