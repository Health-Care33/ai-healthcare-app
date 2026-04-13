import os
import shutil
import uuid
from datetime import datetime
from fastapi import HTTPException

from app.database.mongodb import db
from app.modules.fingerprint.predictor import predict_blood_group

# ✅ Absolute path (Render safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def process_fingerprint_upload(file, user_id: str):
    # ✅ validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    # ✅ safe filename
    unique_name = f"{user_id}_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        # ✅ save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 prediction
        prediction = predict_blood_group(file_path)

        if "error" in prediction:
            raise HTTPException(status_code=400, detail=prediction["error"])

        result_data = {
            "user_id": user_id,
            "type": "fingerprint",
            "blood_group": prediction["blood_group"],
            "confidence": prediction["confidence"],
            "file": unique_name,
            "created_at": datetime.utcnow()
        }

        # 🔥 DB save (safe)
        try:
            await db.fingerprint_predictions.insert_one(result_data)
        except Exception as db_error:
            print("⚠️ MongoDB Error:", db_error)

        return prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # ✅ cleanup (Render storage safe)
        if os.path.exists(file_path):
            os.remove(file_path)