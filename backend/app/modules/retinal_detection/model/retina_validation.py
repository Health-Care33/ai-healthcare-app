import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "retina_validation_model.h5")

model = None


# ================= SAFE MODEL LOADER =================
def load_model_safe():
    global model

    if model is None:
        try:
            if not os.path.exists(MODEL_PATH):
                print("⚠️ Retina model not found yet")
                return None

            print("🔄 Loading retina model...")
            model = tf.keras.models.load_model(MODEL_PATH)
            print("✅ Retina model loaded")

        except Exception as e:
            print("❌ Model load error:", e)
            model = None

    return model


# ================= VALIDATION =================
def is_retina(img_path):
    try:
        model_instance = load_model_safe()

        if model_instance is None:
            return False

        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = model_instance.predict(img_array, verbose=0)

        confidence = float(prediction[0][0])

        print("Validation Confidence:", confidence)

        return confidence > 0.5

    except Exception as e:
        print("Validation Error:", e)
        return False