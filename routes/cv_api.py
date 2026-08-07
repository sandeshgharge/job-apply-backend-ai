from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from entities.cv_model import CVDocument, CvData
import services.cv_service as cv_service
from services import storage_service
from io import BytesIO
from config.env import settings
from services.profile_service import get_image_url

cv_router = APIRouter(prefix="/cv", tags=["CV"])


# -----------------------------------
# CREATE CV
# -----------------------------------

@cv_router.post("")
async def create_cv(cv: CVDocument):
    return await cv_service.create_cv(cv)


# -----------------------------------
# GET ALL CVS FOR USER
# -----------------------------------

@cv_router.get("/user/{user_id}")
async def get_user_cvs(user_id: str):
    return await cv_service.get_user_cvs(user_id)


# -----------------------------------
# GET SINGLE CV
# -----------------------------------

@cv_router.get("/{cv_id}")
async def get_cv(cv_id: str):
    return await cv_service.get_cv(cv_id)


# -----------------------------------
# UPDATE CV
# -----------------------------------

@cv_router.put("/{cv_id}")
async def update_cv(cv_id: str, cv_info: dict):
    return await cv_service.update_cv(cv_id, cv_info)


# -----------------------------------
# DELETE CV
# -----------------------------------

@cv_router.delete("/{cv_id}")
async def delete_cv(cv_id: str):
    return await cv_service.delete_cv(cv_id)


# -----------------------------------
# PREVIEW (HTML)
# -----------------------------------

from bson import ObjectId
from services.mongo_db_connection.db import cv_templates_collection

@cv_router.post("/preview/{user_id}")
async def render_cv(request: Request, cv_data: CvData, user_id: str, template_id: str = None):
    token = getattr(request.state, "token", None)
    image_url = get_image_url(user_id, settings.PROFILE_IMAGE_NAME, settings.PROFILE_STORAGE_BUCKET, 2000, token)
    
    custom_html = None
    if template_id:
        template = await cv_templates_collection.find_one({"_id": ObjectId(template_id)})
        if template:
            custom_html = template.get("html_template")
            
    return storage_service.render_html(cv_data, image_url, custom_html)


# -----------------------------------
# PDF
# -----------------------------------

class HtmlToPdfRequest(BaseModel):
    html: str

@cv_router.post("/pdf")
async def generate_cv_pdf(request: HtmlToPdfRequest):
    pdf_bytes = await storage_service.generate_pdf(request.html)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=cv.pdf"
        }
    )


