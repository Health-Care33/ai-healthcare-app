from datetime import datetime
from app.database.mongodb import prediction_collection


async def save_prediction(data):

    prediction_data = {
        "blood_group": data["blood_group"],
        "confidence": data["confidence"],
        "image_path": data["image_path"],
        "created_at": datetime.utcnow()
    }

    result = await prediction_collection.insert_one(prediction_data)

    return str(result.inserted_id)