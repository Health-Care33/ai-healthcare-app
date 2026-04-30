import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.fingerprint.predictor import predict_blood_group
from app.database.mongodb import db

router = APIRouter(tags=["Fingerprint"])

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "fingerprints")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ================= ROUTE =================
@router.post("/predict-blood-group")
async def predict_fingerprint(file: UploadFile = File(...)):

    file_path = None

    try:
        # 1️⃣ FILE TYPE CHECK
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files allowed")

        # 2️⃣ SAVE FILE
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ensure file fully written (deploy safety)
        buffer.flush() if "buffer" in locals() else None

        # 3️⃣ PREDICTION
        result = predict_blood_group(file_path, file.filename)

        # if predictor returns error
        if not result or not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Prediction failed")
            }

        # 4️⃣ DB SAVE (non-blocking safe)
        try:
            await db.fingerprint_predictions.insert_one({
                "type": "fingerprint",
                "file": unique_name,
                "blood_group": result.get("blood_group"),
                "confidence": result.get("confidence"),
                "top_2": result.get("top_2", [])
            })
        except Exception as db_error:
            print("⚠️ DB Error (ignored):", db_error)

        # 5️⃣ FINAL RESPONSE
        return {
            "success": True,
            "blood_group": result.get("blood_group"),
            "confidence": result.get("confidence"),
            "top_2": result.get("top_2", [])
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ Router Error:", e)

        return {
            "success": False,
            "error": "Internal Server Error",
            "details": str(e)
        }

    finally:
        # 6️⃣ CLEANUP FILE
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print("⚠️ Cleanup Error:", cleanup_error)