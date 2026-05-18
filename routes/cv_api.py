from fastapi import APIRouter
from entities.cv_model import CVDocument
import services.cv_service as cv_service

router = APIRouter(prefix="/cv", tags=["CV"])


# -----------------------------------
# CREATE CV
# -----------------------------------

@router.post("/")
async def create_cv(cv: CVDocument):
    return await cv_service.create_cv(cv)


# -----------------------------------
# GET ALL CVS FOR USER
# -----------------------------------

@router.get("/user/{user_id}")
async def get_user_cvs(user_id: str):
    return await cv_service.get_user_cvs(user_id)


# -----------------------------------
# GET SINGLE CV
# -----------------------------------

@router.get("/{cv_id}")
async def get_cv(cv_id: str):
    return await cv_service.get_cv(cv_id)


# -----------------------------------
# UPDATE CV
# -----------------------------------

@router.put("/{cv_id}")
async def update_cv(cv_id: str, cv_info: dict):
    return await cv_service.update_cv(cv_id, cv_info)


# -----------------------------------
# DELETE CV
# -----------------------------------

@router.delete("/{cv_id}")
async def delete_cv(cv_id: str):
    return await cv_service.delete_cv(cv_id)