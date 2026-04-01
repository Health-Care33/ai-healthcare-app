import numpy as np
import os
from keras.models import load_model
from keras.preprocessing import image

model = None

# ✅ CLASS NAMES
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
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(BASE_DIR, "retinal_model.keras")

            print("🔄 Loading retinal model...")
            print("MODEL PATH:", model_path)

            # 🔥 DEBUG (VERY IMPORTANT)
            print("FILES IN MODEL DIR:", os.listdir(BASE_DIR))

            if not os.path.exists(model_path):
                print("❌ MODEL FILE NOT FOUND")
                return None

            model = load_model(model_path, compile=False)

            print("✅ Retinal model loaded successfully")

        except Exception as e:
            print("❌ Model loading failed:", e)
            return None

    return model


def predict_retinal_disease(img_path):

    model = load_retinal_model()

    if model is None:
        return {"error": "Retinal model not loaded"}

    try:
        # ✅ IMAGE PREPROCESSING
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # ✅ PREDICTION
        predictions = model.predict(img_array)[0]

        max_conf = np.max(predictions)
        top_index = np.argmax(predictions)

        # 🔥 INVALID IMAGE CHECK
        if max_conf < 0.4:
            return {
                "error": "Invalid Retina Image",
                "confidence": round(float(max_conf * 100), 2)
            }

        # 🔥 TOP 2 PREDICTIONS
        top_2_indices = predictions.argsort()[-2:][::-1]

        return {
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

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }
