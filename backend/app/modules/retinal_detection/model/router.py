import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.retinal_detection.model.predictor import predict_retinal_disease
from app.modules.retinal_detection.model.retina_validation import is_retina
from app.modules.retinal_detection.ai_helper import get_ai_medical_report
from app.database.mongodb import prediction_collection

router = APIRouter(tags=["Retina Detection"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "retina")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/retinal-detection")
async def scan_retina(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not is_retina(file_path):
            raise HTTPException(
                status_code=400,
                detail="Invalid image. Please upload a valid retina (fundus) image."
            )

        result = predict_retinal_disease(file_path)

        if not result or result.get("error"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Prediction failed")
            )

        ai_report = get_ai_medical_report(
            result["disease"],
            result["confidence"]
        )

        try:
            await prediction_collection.insert_one({
                "type": "retina",
                "file": unique_name,
                "prediction": result,
                "ai_report": ai_report
            })
        except Exception as db_error:
            print("⚠️ MongoDB Error:", db_error)

        return {
            "success": True,
            "prediction": result,
            "ai_report": ai_report
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)