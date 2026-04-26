import os
import shutil
import uuid
from datetime import datetime
from fastapi import HTTPException, UploadFile

from app.database.mongodb import db
from app.modules.fingerprint.predictor import predict_blood_group

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ================= MAIN SERVICE =================
async def process_fingerprint_upload(file: UploadFile, user_id: str):

    # ---------------- VALIDATION ----------------
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    unique_name = f"{user_id}_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        # ---------------- SAVE FILE ----------------
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------- PREDICTION ----------------
        prediction = predict_blood_group(file_path, file.filename)

        # ✅ SAFE CHECK (IMPORTANT FIX)
        if not prediction or prediction.get("error"):
            raise HTTPException(
                status_code=400,
                detail=prediction.get("error", "Prediction failed")
            )

        # ---------------- DB PAYLOAD ----------------
        result_data = {
            "user_id": user_id,
            "type": "fingerprint",
            "file": unique_name,
            "blood_group": prediction.get("blood_group"),
            "confidence": prediction.get("confidence"),
            "warning": prediction.get("warning"),
            "top_2": prediction.get("top_2", []),
            "created_at": datetime.utcnow()
        }

        # ---------------- DB INSERT SAFE ----------------
        try:
            await db.fingerprint_predictions.insert_one(result_data)
        except Exception as db_error:
            print("⚠️ MongoDB Error (non-fatal):", db_error)

        return {
            "success": True,
            "blood_group": prediction.get("blood_group"),
            "confidence": prediction.get("confidence"),
            "warning": prediction.get("warning"),
            "top_2": prediction.get("top_2", [])
        }

    # ---------------- ERROR HANDLING ----------------
    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ SERVICE ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # ---------------- CLEANUP SAFE ----------------
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)