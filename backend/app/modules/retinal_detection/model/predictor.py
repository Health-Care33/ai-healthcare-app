import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import threading

model = None
model_lock = threading.Lock()

class_names = [
    "Diabetic",
    "AMD",
    "Macular_Hole",
    "Drusen",
    "Optic_Disc_Cupping",
    "Tessellation"
]


def load_retinal_model():
    global model

    if model is None:
        with model_lock:  # 🔥 thread safe
            if model is None:
                try:
                    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                    model_path = os.path.join(BASE_DIR, "retinal_model.keras")

                    print("🔄 Loading retinal model...")
                    print("MODEL PATH:", model_path)

                    if not os.path.exists(model_path):
                        raise FileNotFoundError("Model file not found")

                    model = load_model(model_path, compile=False)

                    print("✅ Retinal model loaded successfully")

                except Exception as e:
                    print("❌ Model loading failed:", e)
                    model = None

    return model


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_retinal_disease(img_path):
    model_instance = load_retinal_model()

    if model_instance is None:
        return {"error": "Retinal model not loaded"}

    try:
        img_array = preprocess_image(img_path)

        predictions = model_instance.predict(img_array, verbose=0)[0]

        max_conf = float(np.max(predictions))
        top_index = int(np.argmax(predictions))

        if max_conf < 0.4:
            return {
                "error": "Invalid Retina Image",
                "confidence": round(max_conf * 100, 2)
            }

        top_2_indices = predictions.argsort()[-2:][::-1]

        return {
            "disease": class_names[top_index],
            "confidence": round(max_conf * 100, 2),
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