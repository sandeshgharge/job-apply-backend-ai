from fastapi import HTTPException
from typing import Optional
from services.supabase_db_connection.supabase_client import get_supabase

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
