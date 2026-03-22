from datetime import datetime
from app.database.mongodb import blood_check_collection
from app.modules.blood_donation.compatibility_engine import BloodCompatibilityEngine


async def process_blood_compatibility(blood_group: str):

    result = BloodCompatibilityEngine.check_compatibility(blood_group)

    data = {
        "blood_group": result["blood_group"],
        "can_donate_to": result["can_donate_to"],
        "can_receive_from": result["can_receive_from"],
        "created_at": datetime.utcnow()
    }

    await blood_check_collection.insert_one(data)

    return result