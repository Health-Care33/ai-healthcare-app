import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import threading

model = None
model_lock = threading.Lock()

# ================= CLASSES =================
class_names = [
    "AMD",
    "CNV",
    "CSR",
    "DME",
    "DR",
    "DRUSEN",
    "MH",
    "NORMAL"
]

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "retinal_model.h5")


# ================= LOAD MODEL (SAFE) =================
def load_retinal_model():
    global model

    if model is None:
        with model_lock:
            if model is None:
                try:
                    print("🔄 Loading retinal model...")
                    print("MODEL PATH:", MODEL_PATH)

                    # ✅ SAFE FIX (NO CRASH)
                    if not os.path.exists(MODEL_PATH):
                        print("⚠️ Retinal model not found yet")
                        return None

                    model = load_model(MODEL_PATH, compile=False)

                    print("✅ Retinal model loaded successfully")

                except Exception as e:
                    print("❌ Model loading failed:", e)
                    model = None

    return model


# ================= PREPROCESS =================
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)

    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# ================= MAIN FUNCTION =================
def predict_retinal_disease(img_path):
    try:
        model_instance = load_retinal_model()

        if model_instance is None:
            return {"error": "Model not loaded"}

        img_array = preprocess_image(img_path)

        predictions = model_instance.predict(img_array, verbose=0)[0]
        predictions = np.nan_to_num(predictions)

        max_conf = float(np.max(predictions))
        top_index = int(np.argmax(predictions))
        top_2_indices = predictions.argsort()[-2:][::-1]

        return {
            "success": True,
            "disease": class_names[top_index],
            "confidence": round(max_conf * 100, 2),
            "warning": "Low confidence" if max_conf < 0.4 else "High confidence",
            "top_2": [
                {
                    "disease": class_names[int(i)],
                    "confidence": round(float(predictions[i]) * 100, 2)
                }
                for i in top_2_indices
            ]
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }