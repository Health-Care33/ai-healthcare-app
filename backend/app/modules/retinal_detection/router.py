import os
import shutil
from fastapi import APIRouter, UploadFile, File

from app.modules.retinal_detection.model.predictor import predict_retinal_disease
from app.modules.retinal_detection.ai_helper import get_ai_medical_report
from app.database.mongodb import prediction_collection

# ❌ REMOVE circular import

router = APIRouter(tags=["Retinal Detection"])

UPLOAD_DIR = "uploads/retina"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/scan")
async def scan_retina(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 Prediction
    result = predict_retinal_disease(file_path)

    if "error" in result:
        return {
            "success": False,
            "error": result["error"]
        }

    # 🔥 AI Report
    ai_report = get_ai_medical_report(
        result["disease"],
        result["confidence"]
    )

    # 🔥 Save to DB
    try:
        await prediction_collection.insert_one({
            "type": "retina",
            "file": file.filename,
            "prediction": result,
            "ai_report": ai_report
        })
    except Exception as e:
        print("MongoDB Error:", e)

    return {
        "success": True,
        "prediction": result,
        "ai_report": ai_report
    }