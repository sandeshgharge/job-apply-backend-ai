from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.cv import CVDocument
from db import cv_collection
from datetime import datetime

router = APIRouter(prefix="/cv", tags=["CV"])


# -----------------------------------
# CREATE CV
# -----------------------------------

@router.post("/")
async def create_cv(cv: CVDocument):

    payload = cv.dict()

    result = await cv_collection.insert_one(payload)

    return {
        "message": "CV created",
        "id": str(result.inserted_id)
    }


# -----------------------------------
# GET ALL CVS FOR USER
# -----------------------------------

@router.get("/user/{user_id}")
async def get_user_cvs(user_id: str):

    cursor = cv_collection.find({
        "user_id": user_id
    }).sort("updated_at", -1)

    cvs = []

    async for cv in cursor:
        cv["_id"] = str(cv["_id"])
        cvs.append(cv)

    return cvs


# -----------------------------------
# GET SINGLE CV
# -----------------------------------

@router.get("/{cv_id}")
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


# -----------------------------------
# UPDATE CV
# -----------------------------------

@router.put("/{cv_id}")
async def update_cv(
    cv_id: str,
    cv_info: dict
):

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
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "message": "CV updated"
    }


# -----------------------------------
# DELETE CV
# -----------------------------------

@router.delete("/{cv_id}")
async def delete_cv(cv_id: str):

    result = await cv_collection.delete_one({
        "_id": ObjectId(cv_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    return {
        "message": "CV deleted"
    }