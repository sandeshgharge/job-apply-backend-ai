"""
Profile API router.

Proxies Supabase reads/writes for the `user_details` table
and generates signed URLs from Supabase Storage.
"""

from fastapi import APIRouter, Query, Request
from typing import Optional

import services.profile_service as profile_service
from entities.profile_info import ProfileInfo

profile_router = APIRouter(prefix="/profile", tags=["Profile"])


# ---------------------------------------------------------------------------
# GET /profile/{user_id}
# ---------------------------------------------------------------------------

@profile_router.get("/{user_id}", response_model=ProfileInfo)
def get_profile(user_id: str, request: Request):
    token = getattr(request.state, "token", None)
    return profile_service.get_profile(user_id, token)


# ---------------------------------------------------------------------------
# PUT /profile/{user_id}
# ---------------------------------------------------------------------------

@profile_router.put("/{user_id}")
def update_profile(
    user_id: str, 
    profile_data: ProfileInfo, 
    request: Request
):
    token = getattr(request.state, "token", None)
        
    return profile_service.update_profile(user_id, profile_data, token)


# ---------------------------------------------------------------------------
# GET /profile/{user_id}/image-url
# ---------------------------------------------------------------------------

@profile_router.get("/{user_id}/image-url")
def get_image_url(
    user_id: str,
    request: Request,
    fileName: str = Query(..., description="File name/path inside the bucket"),
    bucket: str = Query(..., description="Supabase storage bucket name"),
    expiresIn: int = Query(3600, description="Signed URL expiry in seconds"),
):
    token = getattr(request.state, "token", None)
    return profile_service.get_image_url(user_id, fileName, bucket, expiresIn, token)
