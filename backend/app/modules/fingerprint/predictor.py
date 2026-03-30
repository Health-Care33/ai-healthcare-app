import numpy as np
import cv2
import json
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "model", "fingerprint_bloodgroup_model.h5")
CLASS_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

model = None
CLASS_NAMES = None


# ---------- LOAD MODEL ----------
def load_model():
    global model

    if model is None:
        try:
            print("🔄 Loading Fingerprint Model...")

            import tensorflow as tf  # ✅ lazy import

            if not os.path.exists(MODEL_PATH):
                print("❌ Model file not found:", MODEL_PATH)
                return None

            model = tf.keras.models.load_model(MODEL_PATH)

            print("✅ Fingerprint model loaded")

        except Exception as e:
            print("❌ Model Load Error:", e)
            model = None

    return model


# ---------- LOAD CLASS LABELS ----------
def load_classes():
    global CLASS_NAMES

    if CLASS_NAMES is None:
        try:
            if not os.path.exists(CLASS_PATH):
                print("❌ Class file not found:", CLASS_PATH)
                return None

            with open(CLASS_PATH, "r") as f:
                class_indices = json.load(f)

            CLASS_NAMES = {v: k for k, v in class_indices.items()}
            print("✅ Classes loaded")

        except Exception as e:
            print("❌ Class Load Error:", e)
            CLASS_NAMES = None

    return CLASS_NAMES


# ---------- PREDICTION ----------
def predict_blood_group(image_path):

    try:
        # ---------- IMAGE CHECK ----------
        if not os.path.exists(image_path):
            return {"error": "Image file not found"}

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {"error": "Image not readable"}

        # ---------- PREPROCESS ----------
        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        img = img.reshape(1, 128, 128, 1)

        print("📊 Image processed")

        model = load_model()
        CLASS_NAMES = load_classes()

        if model is None:
            return {"error": "Model not loaded"}

        if CLASS_NAMES is None:
            return {"error": "Class labels not loaded"}

        # ---------- PREDICT ----------
        prediction = model.predict(img)

        class_index = int(np.argmax(prediction))
        blood_group = CLASS_NAMES.get(class_index, "Unknown")
        confidence = float(np.max(prediction)) * 100  # ✅ convert to %

        return {
            "blood_group": blood_group,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        print("❌ Prediction Error:", e)
        return {"error": str(e)}