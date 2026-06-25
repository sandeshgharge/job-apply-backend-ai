import asyncio

from fastapi import HTTPException
from typing import Optional, Union
from config.env import settings
from services.supabase_db_connection.supabase_client import get_supabase
from services.doc_service.template_management import template_env
from services.doc_service.html_to_pdf.playwright import PdfService
from entities.cv_model import CvData
from entities.cover_letter_model import CoverLetterDocInfo
from services.supabase_db_connection.supabase_client import get_supabase
from services.profile_service import get_image_url

async def upload_file_to_storage(
    user_id: str,
    bucket: str,
    file_path: str,
    file_bytes: bytes,
    content_type: str,
    token: Optional[str]
) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        print(f"Uploading file to bucket '{bucket}' at path '{user_id}/{file_path}' with content type '{content_type}'")
        supabase.storage.from_(bucket).upload(
            user_id + "/" + file_path,
            file_bytes,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        public_url = supabase.storage.from_(bucket).get_public_url(user_id + "/" + file_path)
        return {"public_url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def remove_file_from_storage(
    bucket: str,
    file_path: str,
    token: Optional[str]
) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        supabase.storage.from_(bucket).remove([file_path])
        return {"message": "File removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# DOCUMENT RENDERING & PDF GENERATION
# -----------------------------------

def render_html(data: Union[CvData, CoverLetterDocInfo], image_url: Optional[str] = None) -> str:
    if isinstance(data, CvData):
        template_name = "cv_default.html"
    elif isinstance(data, CoverLetterDocInfo):
        template_name = "cover_letter_default.html"
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")

    template = template_env.get_template(template_name)
    return template.render(**data.model_dump(), image_url=image_url)


async def generate_pdf(html: str) -> bytes:
    pdf_bytes = await asyncio.get_event_loop().run_in_executor(
        None, PdfService.html_to_pdf, html
    )
    return pdf_bytes

