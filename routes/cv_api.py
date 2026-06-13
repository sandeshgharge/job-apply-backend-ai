from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from entities.cv_model import CVDocument, CvData
import services.cv_service as cv_service
from services import storage_service
from io import BytesIO

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

@cv_router.post("/preview")
def render_cv(cv_data: CvData):
    return storage_service.render_html(cv_data)


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

