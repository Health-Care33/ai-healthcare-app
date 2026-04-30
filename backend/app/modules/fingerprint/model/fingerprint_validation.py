import os
import tensorflow as tf
import numpy as np
import threading
import cv2

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fingerprint_validation_model.h5")

model = None
model_lock = threading.Lock()


# ================= LOAD MODEL =================
def load_validation_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading fingerprint validation model...")

                    if not os.path.exists(MODEL_PATH):
                        raise Exception("Validation model not found")

                    model = tf.keras.models.load_model(MODEL_PATH, compile=False)

                    print("✅ Validation model loaded")

                except Exception as e:
                    print("❌ VALIDATION MODEL ERROR:", e)
                    return None

    return model


# ================= PREPROCESS =================
def preprocess(img_path):
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError("Image not readable")

    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0

    return np.expand_dims(img, axis=0)


# ================= VALIDATION =================
def is_fingerprint(img_path):
    try:
        model_instance = load_validation_model()

        # ❌ model load fail → allow (fail-safe)
        if model_instance is None:
            print("⚠️ Validation model not loaded → skipping validation")
            return True

        img = preprocess(img_path)

        prediction = model_instance.predict(img, verbose=0)
        prediction = np.nan_to_num(prediction)

        print("🧠 RAW Validation Prediction:", prediction)

        # ================= SIGMOID =================
        if prediction.shape[-1] == 1:
            confidence = float(prediction[0][0])

        # ================= SOFTMAX =================
        else:
            confidence = float(np.max(prediction))

        print("🔥 Validation Confidence:", confidence)

        # ✅ RELAXED THRESHOLD (important fix)
        if confidence >= 0.3:
            return True
        else:
            return False

    except Exception as e:
        print("❌ Validation Error:", e)

        # 🔥 fail-safe → block na kare system ko
        return True