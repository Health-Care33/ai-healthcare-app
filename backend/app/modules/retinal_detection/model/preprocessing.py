import cv2
import numpy as np

def preprocess_image(img_path):
    try:
        img = cv2.imread(img_path)

        if img is None:
            raise ValueError(f"Image not readable: {img_path}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype("float32") / 255.0

        return np.expand_dims(img, axis=0)

    except Exception as e:
        raise Exception(f"Preprocessing failed: {str(e)}")