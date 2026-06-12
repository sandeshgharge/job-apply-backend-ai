"""
Authentication API router.

Proxies Supabase Auth calls: login, signup, logout, session, and password update.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from services.supabase_db_connection.supabase_client import get_supabase

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str


class SetPasswordRequest(BaseModel):
    new_password: str


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

@auth_router.post("/login")
def login(request: LoginRequest):
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })

        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user.model_dump() if hasattr(response.user, "model_dump") else response.user,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ---------------------------------------------------------------------------
# POST /auth/signup
# ---------------------------------------------------------------------------

@auth_router.post("/signup")
def signup(request: SignupRequest):
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })

        user_data = None
        if response.user:
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
            }

        session_data = None
        if response.session:
            session_data = {
                "access_token": response.session.access_token,
            }

        return {"user": user_data, "session": session_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------------------------
# POST /auth/logout
# ---------------------------------------------------------------------------

@auth_router.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        
    supabase = get_supabase(token)
    try:
        supabase.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# GET /auth/session
# ---------------------------------------------------------------------------

@auth_router.get("/session")
def get_session(authorization: Optional[str] = Header(None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        
    supabase = get_supabase()
    try:
        # get_user() is generally safer/better to validate the token on the backend
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            return {"session": None}

        return {
            "session": {
                "access_token": token,
                "user": response.user.model_dump() if hasattr(response.user, "model_dump") else response.user,
            }
        }
    except Exception:
        return {"session": None}


# ---------------------------------------------------------------------------
# POST /auth/set-password
# ---------------------------------------------------------------------------

@auth_router.post("/set-password")
def set_password(
    request: SetPasswordRequest,
    authorization: Optional[str] = Header(None),
):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        
    supabase = get_supabase()
    try:
        supabase.auth.update_user({"password": request.new_password})
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
