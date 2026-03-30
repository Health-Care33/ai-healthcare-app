from datetime import datetime
from app.database.mongodb import db

collection = db["health_risk_predictions"]


async def save_prediction(user_id, input_data, result):
    try:
        document = {
            "user_id": user_id,
            "input_data": input_data,
            "prediction": result,
            "created_at": datetime.utcnow()
        }

        await collection.insert_one(document)
        return document

    except Exception as e:
        print(f"❌ DB Save Error: {e}")
        return None