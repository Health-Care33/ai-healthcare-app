import os
import shutil
import uuid
from datetime import datetime
from fastapi import HTTPException, UploadFile

from app.database.mongodb import db
from app.modules.fingerprint.predictor import predict_blood_group
from app.modules.fingerprint.model.fingerprint_validation import is_fingerprint

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ================= MAIN SERVICE =================
async def process_fingerprint_upload(file: UploadFile, user_id: str):

    # ---------------- FILE TYPE CHECK ----------------
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    unique_name = f"{user_id}_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        # ---------------- SAVE FILE ----------------
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------- VALIDATION ----------------
        try:
            is_valid = is_fingerprint(file_path)
        except Exception as e:
            print("⚠️ Validation error:", e)

            return {
                "success": False,
                "blood_group": "Unknown",
                "confidence": 0.0,
                "warning": None,
                "top_2": [],
                "error": "Validation failed",
                "details": str(e)
            }

        if not is_valid:
            return {
                "success": False,
                "blood_group": "Unknown",
                "confidence": 0.0,
                "warning": None,
                "top_2": [],
                "error": "Invalid fingerprint image"
            }

        # ---------------- PREDICTION ----------------
        result = predict_blood_group(file_path, file.filename)

        if not result:
            result = {
                "success": False,
                "blood_group": "Unknown",
                "confidence": 0.0,
                "warning": None,
                "top_2": [],
                "error": "Prediction returned empty result"
            }

        confidence = result.get("confidence", 0.0)

        # ---------------- DB SAVE ----------------
        db_data = {
            "user_id": user_id,
            "type": "fingerprint",
            "file": unique_name,
            "blood_group": result.get("blood_group", "Unknown"),
            "confidence": confidence,
            "warning": result.get("warning"),
            "top_2": result.get("top_2", []),
            "created_at": datetime.utcnow()
        }

        try:
            await db.fingerprint_predictions.insert_one(db_data)
        except Exception as db_error:
            print("⚠️ MongoDB Error (non-fatal):", db_error)

        # ---------------- FINAL RESPONSE ----------------
        return {
            "success": result.get("success", False),
            "blood_group": result.get("blood_group", "Unknown"),
            "confidence": confidence,
            "warning": result.get("warning"),
            "top_2": result.get("top_2", []),
            "error": result.get("error"),
            "details": result.get("details")
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ SERVICE ERROR:", e)

        return {
            "success": False,
            "blood_group": "Unknown",
            "confidence": 0.0,
            "warning": None,
            "top_2": [],
            "error": "Internal Server Error",
            "details": str(e)
        }

    finally:
        # ---------------- CLEANUP ----------------
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)