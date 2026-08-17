from motor.motor_asyncio import AsyncIOMotorClient
from config.env import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

db = client["job_apply_db"]

cv_collection = db["cv_documents"]
cover_letter_collection = db["cover_letter_documents"]
cv_templates_collection = db["cv_html_templates"]
cl_templates_collection = db["cl_html_templates"]
applied_job_details_collection = db["applied_job_details"]