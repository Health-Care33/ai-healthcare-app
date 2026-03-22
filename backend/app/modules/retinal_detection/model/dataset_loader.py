import os
import cv2
import numpy as np
import pandas as pd
import re

from app.modules.retinal_detection.model.preprocessing import preprocess_image

DATASET_PATH = "app/modules/retinal_detection/dataset"
DATASET_FOLDER = os.listdir(DATASET_PATH)[0]

FUNDUS_PATH = os.path.join(DATASET_PATH, DATASET_FOLDER, "FundusImages")
CLINICAL_PATH = os.path.join(DATASET_PATH, DATASET_FOLDER, "ClinicalData")

EXCEL_FILE = os.path.join(CLINICAL_PATH, "patient_data_od.xlsx")


def extract_id_from_filename(filename):
    filename = filename.upper()
    match = re.search(r'RET\d+', filename)
    if match:
        return match.group()
    return None


def load_images():

    images = []
    labels = []

    print("Loading Images...")

    df = pd.read_excel(EXCEL_FILE, header=1)

    print("\n🔥 CLEANED EXCEL PREVIEW:")
    print(df.head())

    print("\nColumns:", df.columns)

    id_col = df.columns[0]

    print("\n✅ Using ID column:", id_col)

    df[id_col] = df[id_col].astype(str).str.upper()

    id_to_label = dict(zip(df[id_col], df["Diagnosis"]))

    image_files = os.listdir(FUNDUS_PATH)

    for img_file in image_files:

        img_id = extract_id_from_filename(img_file)

        if img_id is None:
            continue

        excel_id = img_id.replace("RET", "#")

        if excel_id not in id_to_label:
            continue

        label = id_to_label[excel_id]

        if pd.isna(label):
            continue

        img_path = os.path.join(FUNDUS_PATH, img_file)

        img = cv2.imread(img_path)
        if img is None:
            continue

        img = preprocess_image(img)

        images.append(img)
        labels.append(int(label))

    images = np.array(images)
    labels = np.array(labels)

    print("\n✅ Total Images Loaded:", len(images))
    print("✅ Unique Labels:", set(labels))

    return images, labels