import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fingerprint_validation_model.h5")

model = None
model_lock = threading.Lock()


def load_validation_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading fingerprint validation model...")

                    if not os.path.exists(MODEL_PATH):
                        raise FileNotFoundError("Validation model not found")

                    model = tf.keras.models.load_model(MODEL_PATH)

                    print("✅ Validation model loaded")

                except Exception as e:
                    print("❌ Validation model load error:", e)
                    model = None

    return model


def is_fingerprint(img_path):
    model_instance = load_validation_model()

    if model_instance is None:
        return False

    try:
        # ================= PREPROCESS =================
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model_instance.predict(img_array, verbose=0)

        print("🧠 RAW Prediction:", prediction)

        # ================= SIGMOID MODEL =================
        if prediction.shape[-1] == 1 or len(prediction.shape) == 2 and prediction.shape[1] == 1:

            confidence = float(prediction[0][0])
            print("🔥 Sigmoid Confidence:", confidence)

            # 🔥 SAFE THRESHOLD (important fix)
            return confidence >= 0.90

        # ================= SOFTMAX MODEL =================
        else:

            class_index = int(np.argmax(prediction))
            confidence = float(np.max(prediction))

            print("🔥 Softmax Class:", class_index, "Confidence:", confidence)

            # class 1 = fingerprint
            return class_index == 1 and confidence >= 0.85

    except Exception as e:
        print("❌ Validation Error:", e)
        return False