from fastapi import HTTPException
from typing import Optional
from entities.profile_info import ProfileInfo
from services.supabase_db_connection.supabase_client import get_supabase


def get_profile(user_id: str, token: Optional[str]) -> ProfileInfo:
    supabase = get_supabase(access_token=token)
    try:
        response = (
            supabase.table("user_details")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return ProfileInfo.model_validate(response.data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_profile(user_id: str, profile_data: ProfileInfo, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        profile_data.id = user_id
        supabase.table("user_details").update(profile_data.model_dump()).eq("id", user_id).execute()
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_image_url(user_id: str, file_name: str, bucket: str, expires_in: int, token: Optional[str] = None) -> dict:
    supabase = get_supabase(access_token=token)
    try:    
        response = supabase.storage.from_(bucket).create_signed_url(
            user_id + "/" + file_name, expires_in
        )

        signed_url = response.get("signedURL") or response.get("signedUrl")
        if not signed_url:
            raise HTTPException(status_code=500, detail="Failed to create signed URL")

        return {"signed_url": signed_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
