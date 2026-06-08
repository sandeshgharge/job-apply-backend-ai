"""
Storage API router.

Proxies Supabase Storage operations: upload and remove files.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from services.supabase_db_connection.supabase_client import get_supabase

storage_router = APIRouter(prefix="/storage", tags=["Storage"])


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class RemoveFileRequest(BaseModel):
    bucket: str
    file_path: str


# ---------------------------------------------------------------------------
# POST /storage/upload
# ---------------------------------------------------------------------------

@storage_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    bucket: str = Form(...),
    file_path: str = Form(...),
):
    supabase = get_supabase()
    try:
        file_bytes = await file.read()
        content_type = file.content_type or "application/octet-stream"

        supabase.storage.from_(bucket).upload(
            file_path,
            file_bytes,
            file_options={"content-type": content_type, "upsert": "true"},
        )

        public_url = supabase.storage.from_(bucket).get_public_url(file_path)
        return {"public_url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# DELETE /storage/remove
# ---------------------------------------------------------------------------

@storage_router.delete("/remove")
def remove_file(request: RemoveFileRequest):
    supabase = get_supabase()
    try:
        supabase.storage.from_(request.bucket).remove([request.file_path])
        return {"message": "File removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
