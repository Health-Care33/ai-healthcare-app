import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.fingerprint.predictor import predict_blood_group
from app.database.mongodb import prediction_collection

router = APIRouter(tags=["Fingerprint"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predict-blood-group")
async def predict_fingerprint(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_blood_group(file_path, file.filename)

        if not result or result.get("error"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Prediction failed")
            )

        db_data = {
            "type": "fingerprint",
            "file": unique_name,
            "blood_group": result["blood_group"],
            "confidence": result["confidence"],
            "warning": result.get("warning"),
            "top_2": result.get("top_2", [])
        }

        try:
            await prediction_collection.insert_one(db_data)
        except Exception as db_error:
            print("⚠️ MongoDB Error:", db_error)

        return {
            "success": True,
            "blood_group": result["blood_group"],
            "confidence": result["confidence"],
            "warning": result.get("warning"),
            "top_2": result.get("top_2", [])
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