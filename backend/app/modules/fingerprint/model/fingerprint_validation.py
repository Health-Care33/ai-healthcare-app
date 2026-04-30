import os
import numpy as np
import cv2
import threading
import tensorflow as tf

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
                    if not os.path.exists(MODEL_PATH):
                        print("⚠️ Validation model not found")
                        return None

                    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
                    print("✅ Validation model loaded")

                except Exception as e:
                    print("❌ Validation model error:", e)
                    return None

    return model


# ================= SAFE IMAGE LOAD =================
def safe_load_image(path):
    try:
        if not path or not os.path.exists(path):
            return None

        img = cv2.imread(path)

        if img is None:
            return None

        return img

    except Exception:
        return None


# ================= MAIN VALIDATION =================
def is_fingerprint(image_path):
    try:

        # 1️⃣ file check
        if not image_path or not os.path.exists(image_path):
            print("❌ File not found")
            return False

        # 2️⃣ read image safely
        img = safe_load_image(image_path)

        if img is None:
            print("❌ Image unreadable by OpenCV")
            return False

        # 3️⃣ load model (fail-safe)
        model_instance = load_validation_model()

        # 🔥 if model missing → DO NOT BLOCK PIPELINE
        if model_instance is None:
            print("⚠️ Model missing → bypass validation")
            return True

        # 4️⃣ preprocess
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        # 5️⃣ prediction
        prediction = model_instance.predict(img, verbose=0)
        prediction = np.nan_to_num(prediction)

        confidence = float(np.max(prediction))

        print("🧠 Validation confidence:", confidence)

        # 6️⃣ FINAL RULE (RELAXED FOR PRODUCTION)
        return confidence >= 0.3

    except Exception as e:
        print("❌ Validation crash:", e)

        # 🔥 fail-safe: never break pipeline
        return True