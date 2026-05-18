from bson import ObjectId
from fastapi import HTTPException
from pydantic import Field
from entities.cv_model import CVDocument
from services.mongo_db_connection import cv_collection
from datetime import datetime, timezone


async def create_cv(cv: CVDocument):

    version = get_next_version(cv.user_id)
    cv.version = version
    cv._id = None
    cv.created_at = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload = cv.model_dump(exclude_none=True)
    result = await cv_collection.insert_one(payload)
    return result


async def get_user_cvs(user_id: str):
    cursor = cv_collection.find({
        "user_id": user_id
    }).sort("updated_at", -1)

    cvs = []
    async for cv in cursor:
        cv["_id"] = str(cv["_id"])
        cvs.append(cv)

    return cvs


async def get_cv(cv_id: str):
    cv = await cv_collection.find_one({
        "_id": ObjectId(cv_id)
    })

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    cv["_id"] = str(cv["_id"])
    return cv


async def update_cv(cv_id: str, cv_info: dict):
    existing = await cv_collection.find_one({
        "_id": ObjectId(cv_id)
    })

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    await cv_collection.update_one(
        {"_id": ObjectId(cv_id)},
        {
            "$set": {
                "cv_info": cv_info,
                "updated_at": Field(default_factory=lambda: datetime.now(timezone.utc))
            }
        }
    )

    return {"message": "CV updated"}


async def delete_cv(cv_id: str):
    result = await cv_collection.delete_one({
        "_id": ObjectId(cv_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    return {"message": "CV deleted"}

async def get_next_version(user_id: str) -> int:
    result = await cv_collection.find_one(
        {"user_id": user_id},
        sort=[("version", -1)]
    )
    return (result["version"] + 1) if result else 1