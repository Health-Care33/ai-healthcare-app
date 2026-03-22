from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

db = client[settings.DATABASE_NAME]

# collections

user_collection = db["users"]

prediction_collection = db["predictions"]

donor_collection = db["donors"]

medical_report_collection = db["medical_reports"]

blood_check_collection = db["blood_checks"]