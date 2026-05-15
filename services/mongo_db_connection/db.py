from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

db = client["job_apply_db"]

cv_collection = db["cv_documents"]
cover_letter_collection = db["cover_letter_documents"]