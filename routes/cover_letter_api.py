from fastapi import APIRouter, HTTPException
from entities.cover_letter_model import CoverLetterDocument
from services.cover_letter_service import insert_cover_letter, fetch_user_cover_letters, fetch_cover_letter, update_cover_letter

cl_router = APIRouter(
    prefix="/cover-letter",
    tags=["Cover Letter"]
)


# -----------------------------------
# CREATE
# -----------------------------------

@cl_router.post("/")
async def create_cover_letter(
    cover_letter: CoverLetterDocument
):
    return await insert_cover_letter(cover_letter)


# -----------------------------------
# GET ALL FOR USER
# -----------------------------------

@cl_router.get("/user/{user_id}")
async def get_user_cover_letters(
    user_id: str
):
    return await fetch_user_cover_letters(user_id)


# -----------------------------------
# GET SINGLE
# -----------------------------------

@cl_router.get("/{cover_letter_id}")
async def get_cover_letter(
    cover_letter_id: str
):
    return await fetch_cover_letter(cover_letter_id)
    


# -----------------------------------
# UPDATE
# -----------------------------------

@cl_router.put("/{cover_letter_id}")
async def edit_cover_letter(
    cover_letter_id: str,
    cover_letter_info: dict
):
    return await update_cover_letter(cover_letter_id, cover_letter_info)