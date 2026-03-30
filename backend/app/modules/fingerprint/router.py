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

    try:
        file_path = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_blood_group(file_path)

        if "error" in result:
            return {"success": False, "error": result["error"]}

        await prediction_collection.insert_one({
            "type": "fingerprint",
            "file": file.filename,
            "blood_group": result["blood_group"],
            "confidence": result["confidence"]
        })

        return {
            "success": True,
            "blood_group": result["blood_group"],
            "confidence": result["confidence"]
        }

    except Exception as e:
        return {"success": False, "error": str(e)}