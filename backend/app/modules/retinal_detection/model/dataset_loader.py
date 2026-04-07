# ❗ ONLY FOR TRAINING - NOT FOR DEPLOYMENT

import os
import cv2
import numpy as np
import pandas as pd
import re
from app.modules.retinal_detection.model.preprocessing import preprocess_image


def extract_id_from_filename(filename):
    filename = filename.upper()
    match = re.search(r'RET\d+', filename)
    return match.group() if match else None


def load_images(dataset_path):
    dataset_folder = os.listdir(dataset_path)[0]

    fundus_path = os.path.join(dataset_path, dataset_folder, "FundusImages")
    clinical_path = os.path.join(dataset_path, dataset_folder, "ClinicalData")

    excel_file = os.path.join(clinical_path, "patient_data_od.xlsx")

    images = []
    labels = []

    df = pd.read_excel(excel_file, header=1)

    id_col = df.columns[0]
    df[id_col] = df[id_col].astype(str).str.upper()

    id_to_label = dict(zip(df[id_col], df["Diagnosis"]))

    for img_file in os.listdir(fundus_path):

        img_id = extract_id_from_filename(img_file)
        if img_id is None:
            continue

        excel_id = img_id.replace("RET", "#")

        if excel_id not in id_to_label:
            continue

        label = id_to_label[excel_id]
        if pd.isna(label):
            continue

        img_path = os.path.join(fundus_path, img_file)
        img = cv2.imread(img_path)

        if img is None:
            continue

        img = preprocess_image(img)

        images.append(img)
        labels.append(int(label))

    return np.array(images), np.array(labels)