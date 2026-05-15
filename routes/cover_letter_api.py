from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.cover_letter import CoverLetterDocument
from db import cover_letter_collection
from datetime import datetime

router = APIRouter(
    prefix="/cover-letter",
    tags=["Cover Letter"]
)


# -----------------------------------
# CREATE
# -----------------------------------

@router.post("/")
async def create_cover_letter(
    cover_letter: CoverLetterDocument
):

    payload = cover_letter.dict()

    result = await cover_letter_collection.insert_one(
        payload
    )

    return {
        "message": "Cover letter created",
        "id": str(result.inserted_id)
    }


# -----------------------------------
# GET ALL FOR USER
# -----------------------------------

@router.get("/user/{user_id}")
async def get_user_cover_letters(
    user_id: str
):

    cursor = cover_letter_collection.find({
        "user_id": user_id
    }).sort("updated_at", -1)

    documents = []

    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        documents.append(doc)

    return documents


# -----------------------------------
# GET SINGLE
# -----------------------------------

@router.get("/{cover_letter_id}")
async def get_cover_letter(
    cover_letter_id: str
):

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


# -----------------------------------
# UPDATE
# -----------------------------------

@router.put("/{cover_letter_id}")
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
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "message": "Cover letter updated"
    }


# -----------------------------------
# DELETE
# -----------------------------------

@router.delete("/{cover_letter_id}")
async def delete_cover_letter(
    cover_letter_id: str
):

    result = await cover_letter_collection.delete_one({
        "_id": ObjectId(cover_letter_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Cover letter not found"
        )

    return {
        "message": "Cover letter deleted"
    }