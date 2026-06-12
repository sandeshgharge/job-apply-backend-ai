"""
Storage API router.

Proxies Supabase Storage operations: upload and remove files.
"""

from fastapi import APIRouter, UploadFile, File, Form, Request
from pydantic import BaseModel

from services.storage_service import upload_file_to_storage, remove_file_from_storage

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
    request: Request,
    file: UploadFile = File(...),
    bucket: str = Form(...),
    file_path: str = Form(...),
):
    token = getattr(request.state, "token", None)
    user_id = request.state.user.get("id")
    file_bytes = await file.read()
    content_type = file.content_type or "application/octet-stream"

    return await upload_file_to_storage(
        user_id=user_id,
        bucket=bucket,
        file_path=file_path,
        file_bytes=file_bytes,
        content_type=content_type,
        token=token
    )


# ---------------------------------------------------------------------------
# DELETE /storage/remove
# ---------------------------------------------------------------------------

@storage_router.delete("/remove")
def remove_file(request: Request, body: RemoveFileRequest):
    token = getattr(request.state, "token", None)
    return remove_file_from_storage(
        bucket=body.bucket,
        file_path=body.file_path,
        token=token
    )
