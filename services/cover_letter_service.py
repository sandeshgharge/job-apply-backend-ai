from pydantic import Field

from entities.cover_letter_model import CoverLetterDocument
from services.mongo_db_connection import cover_letter_collection
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timezone

async def insert_cover_letter(cl_doc : CoverLetterDocument) : 

    version = await get_next_version(cl_doc.user_id)
    cl_doc._id = None
    cl_doc.version = version
    cl_doc.created_at = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload = cl_doc.model_dump(exclude_none=True)
    result = await cover_letter_collection.insert_one(
        payload
    )
    return result

async def fetch_user_cover_letters(user_id):

    cursor = cover_letter_collection.find({
        "user_id": user_id
    }).sort("updated_at", -1)

    documents = []

    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        documents.append(doc)

    return documents

async def fetch_cover_letter(cover_letter_id):
    doc = await cover_letter_collection.find_one({
        "_id": ObjectId(cover_letter_id)
    })

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Cover letter not found"
        )

    doc["_id"] = str(doc["_id"])

    return doc

async def update_cover_letter(
    cover_letter_id: str,
    cover_letter_info: dict
):
    existing = await cover_letter_collection.find_one({
        "_id": ObjectId(cover_letter_id)
    })

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Cover letter not found"
        )

    await cover_letter_collection.update_one(
        {"_id": ObjectId(cover_letter_id)},
        {
            "$set": {
                "cover_letter_info": cover_letter_info,
                "updated_at": Field(default_factory=lambda: datetime.now(timezone.utc))
            }
        }
    )

    return {
        "message": "Cover letter updated"
    }

async def get_next_version(user_id: str) -> int:
    result = await cover_letter_collection.find_one(
        {"user_id": user_id},
        sort=[("version", -1)]
    )
    return (result["version"] + 1) if result else 1