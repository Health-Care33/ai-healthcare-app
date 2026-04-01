from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = None
db = None

try:
    print("🔄 Connecting to MongoDB...")

    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DATABASE_NAME]

    print("✅ MongoDB connected successfully")

except Exception as e:
    print("❌ MongoDB connection failed:", e)


# collections

user_collection = db["users"] if db else None
prediction_collection = db["predictions"] if db else None
donor_collection = db["donors"] if db else None
medical_report_collection = db["medical_reports"] if db else None
blood_check_collection = db["blood_checks"] if db else None
