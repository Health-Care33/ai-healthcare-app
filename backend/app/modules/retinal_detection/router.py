import os
import shutil
from fastapi import APIRouter, UploadFile, File

from app.modules.retinal_detection.model.predictor import predict_retinal_disease
from app.modules.retinal_detection.ai_helper import get_ai_medical_report
from app.database.mongodb import prediction_collection

router = APIRouter(tags=["Retina Detection"])

UPLOAD_DIR = "uploads/retina"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/retinal-detection")
async def scan_retina(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 AI Prediction
    result = predict_retinal_disease(file_path)

    # ❌ INVALID IMAGE HANDLE
    if "error" in result:
        return {
            "error": result["error"]
        }

    # 🔥 AI MEDICAL REPORT
    ai_report = get_ai_medical_report(
        result["disease"],
        result["confidence"]
    )

    # 🔥 MongoDB SAVE
    try:
        await prediction_collection.insert_one({
            "type": "retina",
            "file": file.filename,
            "prediction": result,
            "ai_report": ai_report
        })
    except Exception as e:
        print("MongoDB Error:", e)

    # 🔥 FINAL RESPONSE
    return {
        "prediction": result,
        "ai_report": ai_report
    } 