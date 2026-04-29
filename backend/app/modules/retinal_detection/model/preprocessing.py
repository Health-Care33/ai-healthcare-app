import numpy as np
from tensorflow.keras.preprocessing import image

def preprocess_retina_image(img_path):
    try:
        # ✅ Load image in RGB (important)
        img = image.load_img(img_path, target_size=(224, 224), color_mode="rgb")

        # ✅ Convert to array
        img_array = image.img_to_array(img)

        # ✅ Normalize (0–1)
        img_array = img_array.astype("float32") / 255.0

        # ✅ Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    except Exception as e:
        raise Exception(f"Preprocessing failed: {str(e)}")