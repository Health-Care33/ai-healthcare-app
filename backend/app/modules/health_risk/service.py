from datetime import datetime
from app.database.mongodb import db

collection = db["health_risk_predictions"]


async def save_prediction(user_id, input_data, result):

    document = {
        "user_id": user_id,
        "type": "health_risk",
        "input_data": input_data,
        "prediction": result,
        "created_at": datetime.utcnow()
    }

    try:
        await collection.insert_one(document)
    except Exception as e:
        print("⚠️ MongoDB Error:", e)

    return document