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
async def process_fingerprint_upload(file: UploadFile, user_id: str = None):

    file_path = None
    unique_name = None

    try:

        # 1️⃣ FILE TYPE CHECK
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files allowed")

        # 2️⃣ SAVE FILE
        unique_name = f"{user_id or 'guest'}_{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        file.file.seek(0)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3️⃣ DIRECT PREDICTION (filename check inside predictor)
        result = predict_blood_group(file_path, file.filename)

        if not result or not result.get("success"):
            return {
                "success": False,
                "blood_group": "Unknown",
                "confidence": 0.0,
                "error": result.get("error", "Prediction failed")
            }

        # 4️⃣ DB SAVE
        try:
            await db.fingerprint_predictions.insert_one({
                "user_id": user_id,
                "type": "fingerprint",
                "file": unique_name,
                "blood_group": result.get("blood_group"),
                "confidence": result.get("confidence"),
                "top_2": result.get("top_2", []),
                "created_at": datetime.utcnow()
            })
        except Exception as db_error:
            print("⚠️ DB Error (ignored):", db_error)

        # 5️⃣ FINAL RESPONSE
        return {
            "success": True,
            "blood_group": result.get("blood_group"),
            "confidence": result.get("confidence"),
            "top_2": result.get("top_2", []),
            "error": None
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ Service Error:", e)

        return {
            "success": False,
            "blood_group": "Unknown",
            "confidence": 0.0,
            "error": "Internal Server Error"
        }

    finally:
        # 6️⃣ CLEANUP FILE
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)
