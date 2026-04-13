import cv2
import numpy as np

def preprocess_image(img_path):
    try:
        img = cv2.imread(img_path)

        if img is None:
            raise ValueError("Image not found or invalid")

        # ✅ BGR → RGB (VERY IMPORTANT)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # ✅ Resize
        img = cv2.resize(img, (224, 224))

        # ✅ Normalize
        img = img.astype("float32") / 255.0

        # ✅ Add batch dimension
        img = np.expand_dims(img, axis=0)

        return img

    except Exception as e:
        raise Exception(f"Preprocessing failed: {str(e)}")