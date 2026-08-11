from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from entities.cover_letter_model import CoverLetterDocInfo, CoverLetterDocument
from services import cover_letter_service
from services import storage_service
from io import BytesIO
from config.env import settings
from services.profile_service import get_image_url

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
    return await cover_letter_service.insert_cover_letter(cover_letter)


# -----------------------------------
# GET ALL FOR USER
# -----------------------------------

@cl_router.get("/user/{user_id}")
async def get_user_cover_letters(
    user_id: str
):
    return await cover_letter_service.fetch_user_cover_letters(user_id)


# -----------------------------------
# GET SINGLE
# -----------------------------------

@cl_router.get("/{cover_letter_id}")
async def get_cover_letter(
    cover_letter_id: str
):
    return await cover_letter_service.fetch_cover_letter(cover_letter_id)
    


# -----------------------------------
# UPDATE
# -----------------------------------

@cl_router.put("/{cover_letter_id}")
async def edit_cover_letter(
    cover_letter_id: str,
    cover_letter_info: dict
):
    return await cover_letter_service.update_cover_letter(cover_letter_id, cover_letter_info)


# -----------------------------------
# DELETE
# -----------------------------------

@cl_router.delete("/{cover_letter_id}")
async def delete_cover_letter(
    cover_letter_id: str
):
    return await cover_letter_service.delete_cover_letter(cover_letter_id)


from bson import ObjectId
from services.mongo_db_connection.db import cl_templates_collection

@cl_router.post("/preview/{user_id}")
async def render_doc(
    request: Request,
    user_id,
    cover_letter_doc_info : CoverLetterDocInfo,
    template_id: str = None
):
    token = getattr(request.state, "token", None)
    image_url = get_image_url(user_id, settings.PROFILE_SIGN_IMAGE, settings.PROFILE_STORAGE_BUCKET, 2000, token)
    
    custom_html = None
    if template_id:
        template = await cl_templates_collection.find_one({"_id": ObjectId(template_id)})
        if template:
            custom_html = template.get("html_template")
            
    return storage_service.render_html(cover_letter_doc_info, image_url, custom_html)

class HtmlToPdfRequest(BaseModel):
    html: str
    
@cl_router.post("/pdf")
async def generate_cover_letter_pdf(
    request: HtmlToPdfRequest
):
    pdf_bytes = await storage_service.generate_pdf(request.html)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=cover-letter.pdf"
        }
    )
