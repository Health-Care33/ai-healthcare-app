import os
import tensorflow as tf
import numpy as np
import threading
import cv2

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
                    print("📂 MODEL PATH:", MODEL_PATH)

                    if not os.path.exists(MODEL_PATH):
                        raise Exception("Validation model not found")

                    model = tf.keras.models.load_model(MODEL_PATH, compile=False)

                    print("✅ Validation model loaded successfully")

                except Exception as e:
                    print("❌ Validation model load error:", e)
                    raise e

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

        if model_instance is None:
            print("❌ Model not loaded")
            return False

        img = preprocess(img_path)

        prediction = model_instance.predict(img, verbose=0)

        print("🧠 RAW Prediction:", prediction)

        # ================= SIGMOID (Binary Model) =================
        if prediction.shape[-1] == 1:
            confidence = float(prediction[0][0])
            print("🔥 Sigmoid Confidence:", confidence)

            # 🔥 FIXED LOGIC (better handling)
            if confidence >= 0.5:
                print("✅ Fingerprint Detected")
                return True
            else:
                print("❌ Not a Fingerprint")
                return False

        # ================= SOFTMAX (Multi-class Model) =================
        else:
            class_index = int(np.argmax(prediction))
            confidence = float(np.max(prediction))

            print("🔥 Softmax Class:", class_index, "Confidence:", confidence)

            # 🔥 safer logic (no hardcoded class)
            if confidence >= 0.5:
                print(f"✅ Likely class: {class_index}")
                return True
            else:
                print("❌ Low confidence prediction")
                return False

    except Exception as e:
        print("❌ Validation Error:", e)
        return False