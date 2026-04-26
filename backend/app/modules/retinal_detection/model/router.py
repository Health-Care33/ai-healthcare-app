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

    # ---------------- VALIDATION ----------------
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        # ---------------- SAVE FILE ----------------
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------- RETINA CHECK (SAFE) ----------------
        try:
            if not is_retina(file_path):
                return {
                    "success": False,
                    "error": "Invalid retina image"
                }
        except Exception as e:
            print("⚠️ Retina validation skipped:", e)

        # ---------------- PREDICTION ----------------
        result = predict_retinal_disease(file_path)

        if not result or result.get("error"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Prediction failed")
            )

        # ---------------- AI REPORT ----------------
        try:
            ai_report = get_ai_medical_report(
                result["disease"],
                result["confidence"]
            )
        except Exception as e:
            print("⚠️ AI report error:", e)
            ai_report = {"note": "AI report unavailable"}

        # ---------------- DB SAVE (SAFE) ----------------
        try:
            await prediction_collection.insert_one({
                "type": "retina",
                "file": unique_name,
                "prediction": result,
                "ai_report": ai_report
            })
        except Exception as db_error:
            print("⚠️ MongoDB Error (non-fatal):", db_error)

        # ---------------- RESPONSE ----------------
        return {
            "success": True,
            "prediction": result,
            "ai_report": ai_report
        }

    # ---------------- ERROR HANDLING ----------------
    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ RETINA ROUTE ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # ---------------- CLEANUP ----------------
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)