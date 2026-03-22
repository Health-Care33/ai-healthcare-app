import os
import shutil
from fastapi import APIRouter, UploadFile, File

from app.modules.fingerprint.predictor import predict_blood_group
from app.database.mongodb import prediction_collection

router = APIRouter(tags=["Fingerprint"])

UPLOAD_DIR = "uploads/fingerprints"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predict-blood-group")
async def predict_fingerprint(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # AI prediction
    result = predict_blood_group(file_path)

    blood_group = result["blood_group"]
    confidence = result["confidence"]

    # 🔥 SAVE TO DATABASE
    await prediction_collection.insert_one({
        "type": "fingerprint",
        "file": file.filename,
        "blood_group": blood_group,
        "confidence": confidence
    })

    return {
        "success": True,
        "blood_group": blood_group,
        "confidence": confidence
    }