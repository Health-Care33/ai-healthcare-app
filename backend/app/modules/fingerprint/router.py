import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.fingerprint.predictor import predict_blood_group
from app.database.mongodb import prediction_collection

router = APIRouter(tags=["Fingerprint"])

# ✅ Absolute path (Render safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predict-blood-group")
async def predict_fingerprint(file: UploadFile = File(...)):

    # ✅ validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    # ✅ unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        # ✅ save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 prediction
        result = predict_blood_group(file_path)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        blood_group = result["blood_group"]
        confidence = result["confidence"]

        # 🔥 Mongo save (safe)
        try:
            await prediction_collection.insert_one({
                "type": "fingerprint",
                "file": unique_name,
                "blood_group": blood_group,
                "confidence": confidence
            })
        except Exception as db_error:
            print("⚠️ MongoDB Error:", db_error)

        return {
            "success": True,
            "blood_group": blood_group,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # ✅ cleanup (VERY IMPORTANT for Render)
        if os.path.exists(file_path):
            os.remove(file_path)