from bson import ObjectId
from fastapi import HTTPException
from pydantic import Field
from entities.cover_letter_model import CoverLetterDocInfo, CoverLetterDocument
from services.mongo_db_connection.db import cover_letter_collection


async def insert_cover_letter(cl_doc: CoverLetterDocument) -> CoverLetterDocument:
    version = await get_next_version(cl_doc.user_id)
    cl_doc.id = None
    cl_doc.version = version
    payload = cl_doc.model_dump(by_alias=False, exclude_none=True)
    result = await cover_letter_collection.insert_one(
        payload
    )
    # fetch and return the full inserted document
    created = await cover_letter_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])  # convert ObjectId to string
    return CoverLetterDocument.model_validate(created)


async def fetch_user_cover_letters(user_id) -> list[CoverLetterDocument]:
    cursor = cover_letter_collection.find({
        "user_id": user_id
    }).sort("updated_at", -1)

    documents = []

    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        documents.append(CoverLetterDocument.model_validate(doc))

    return documents


async def fetch_cover_letter(cover_letter_id) -> dict:
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
) -> CoverLetterDocument:
    cl_update = CoverLetterDocument.model_validate(cover_letter_info)
    updated_doc = await cover_letter_collection.find_one_and_update(
        {"_id": ObjectId(cover_letter_id)},
        {
            "$set": {
                "cl_data": cl_update.cl_data.model_dump(),
                "title": cl_update.title
            }
        },
        return_document=True
    )

    if updated_doc is None:
        raise HTTPException(
            status_code=404,
            detail="Cover letter not found"
        )
    
    updated_doc["_id"] = str(updated_doc["_id"])

    return CoverLetterDocument.model_validate(updated_doc)


async def delete_cover_letter(cover_letter_id: str) -> dict:
    result = await cover_letter_collection.delete_one({
        "_id": ObjectId(cover_letter_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Cover letter not found"
        )

    return {"message": "Cover letter deleted"}


async def get_next_version(user_id: str) -> int:
    result = await cover_letter_collection.find_one(
        {"user_id": user_id},
        sort=[("version", -1)]
    )
    return (result["version"] + 1) if result else 1