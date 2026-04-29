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
                    print("📂 MODEL PATH:", MODEL_PATH)

                    if not os.path.exists(MODEL_PATH):
                        raise Exception("Validation model file not found")

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Retina validation model loaded successfully")

                except Exception as e:
                    print("❌ Validation model load error:", e)
                    raise e   # 🔥 DO NOT SILENT FAIL

    return model


# ================= VALIDATION FUNCTION =================
def is_retina(img_path):
    try:
        model_instance = load_validation_model()

        # ❌ agar model load nahi hua → reject karo (skip nahi)
        if model_instance is None:
            print("❌ Validation model is None")
            return False

        # ✅ SAME PREPROCESSING
        img = preprocess_retina_image(img_path)

        print("📊 Input shape:", img.shape)
        print("📊 Min/Max:", img.min(), img.max())

        prediction = model_instance.predict(img, verbose=0)[0][0]

        print("🔍 Retina validation prediction:", prediction)

        # ✅ threshold (tuneable)
        if prediction > 0.5:
            return True
        else:
            return False

    except Exception as e:
        print("❌ Retina validation runtime error:", e)
        return False   # 🔥 FAIL SAFE = REJECT (not accept)