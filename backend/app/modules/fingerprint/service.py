import os
import shutil
from datetime import datetime
from app.database.mongodb import db
from app.modules.fingerprint.predictor import predict_blood_group

UPLOAD_DIR = "uploads/fingerprints"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def process_fingerprint_upload(file, user_id: str):

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    filename = f"{user_id}_{timestamp}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    prediction = predict_blood_group(file_path)

    result_data = {
        "user_id": user_id,
        "blood_group": prediction["blood_group"],
        "confidence": prediction["confidence"],
        "image_path": file_path,
        "created_at": datetime.utcnow()
    }

    await db.fingerprint_predictions.insert_one(result_data)

    return prediction