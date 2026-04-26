import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# ✅ Absolute path (Render safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "retina_validation_model.h5")  # ✅ correct


# ✅ Load model once (IMPORTANT)
model = tf.keras.models.load_model(MODEL_PATH)

def is_retina(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = model.predict(img_array)

        # 🔥 Tune threshold if needed
        confidence = float(prediction[0][0])

        print("Validation Confidence:", confidence)

        return confidence > 0.5

    except Exception as e:
        print("Validation Error:", e)
        return False
