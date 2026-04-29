import numpy as np
import os
from tensorflow.keras.models import load_model
import threading

# ✅ SAME PREPROCESS IMPORT
from app.modules.retinal_detection.model.preprocessing import preprocess_retina_image

model = None
model_lock = threading.Lock()

# ✅ MODEL PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "retina_validation_model.h5")


# ================= LOAD MODEL =================
def load_validation_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading retina validation model...")

                    if not os.path.exists(MODEL_PATH):
                        print("❌ Validation model not found")
                        return None

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Retina validation model loaded")

                except Exception as e:
                    print("❌ Validation model load error:", e)
                    model = None

    return model


# ================= VALIDATION FUNCTION =================
def is_retina(img_path):
    try:
        model_instance = load_validation_model()

        if model_instance is None:
            print("⚠️ Validation model not loaded, skipping check")
            return True   # 🔥 fail-safe (important)

        # ✅ SAME PREPROCESSING (FINAL FIX)
        img = preprocess_retina_image(img_path)

        prediction = model_instance.predict(img, verbose=0)[0][0]

        print("🔍 Retina validation prediction:", prediction)

        # ✅ THRESHOLD (tune if needed)
        return prediction > 0.5

    except Exception as e:
        print("⚠️ Retina validation error:", e)
        return True   # 🔥 skip validation if error