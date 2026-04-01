import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ✅ LOAD MODEL (SAFE + CORRECT PATH)
model = None

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "retinal_model.h5")

    model = load_model(model_path)
    print("✅ Retinal model loaded successfully")

except Exception as e:
    print("❌ Model loading failed:", e)


# ✅ CLASS NAMES
class_names = [
    "Diabetic",
    "AMD",
    "Macular_Hole",
    "Drusen",
    "Optic_Disc_Cupping",
    "Tessellation"
]


def predict_retinal_disease(img_path):

    if model is None:
        return {"error": "Model not loaded"}

    try:
        # ✅ IMAGE PREPROCESSING
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # ✅ PREDICTION
        predictions = model.predict(img_array)[0]

        max_conf = np.max(predictions)
        top_index = np.argmax(predictions)

        # 🔥 INVALID IMAGE CHECK (Improved)
        if max_conf < 0.4:
            return {
                "error": "Invalid Retina Image",
                "confidence": round(float(max_conf * 100), 2)
            }

        # 🔥 TOP 2 PREDICTIONS (SMART FEATURE)
        top_2_indices = predictions.argsort()[-2:][::-1]

        result = {
            "disease": class_names[top_index],
            "confidence": round(float(max_conf * 100), 2),
            "all_predictions": {
                class_names[i]: round(float(predictions[i] * 100), 2)
                for i in range(len(class_names))
            },
            "top_2": [
                {
                    "disease": class_names[i],
                    "confidence": round(float(predictions[i] * 100), 2)
                }
                for i in top_2_indices
            ]
        }

        return result

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        } 