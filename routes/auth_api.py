"""
Authentication API router.

Proxies Supabase Auth calls: login, signup, logout, session, and password update.
"""

from os import access

from fastapi import APIRouter, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from config.env import settings
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
        
    supabase = get_supabase(access_token=token)
    try:
        supabase.auth.update_user({"password": request.new_password})
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.get("/callback")
def handle_callback(request: Request):
    return HTMLResponse("""
    <script>
      const params = new URLSearchParams(window.location.hash.substring(1));
      const access_token = params.get('access_token');
      const refresh_token = params.get('refresh_token');
      
      window.location.href = 
        `/auth/set-password/page?access_token=${access_token}&refresh_token=${refresh_token}`;
    </script>
    """)

@auth_router.get("/set-password/page")
def set_password_page(access_token: str, refresh_token: str):
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Set Password</title>
        <style>
            body {{ font-family: Arial, sans-serif; display: flex; 
                    justify-content: center; align-items: center; 
                    height: 100vh; margin: 0; background: #f5f5f5; }}
            .card {{ background: white; padding: 2rem; border-radius: 8px; 
                     box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 360px; }}
            input {{ width: 100%; padding: 0.6rem; margin: 0.5rem 0 1rem; 
                     box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px; }}
            button {{ width: 100%; padding: 0.75rem; background: #4f46e5; 
                      color: white; border: none; border-radius: 4px; cursor: pointer; }}
            .error {{ color: red; font-size: 0.85rem; display: none; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Set Your Password</h2>
            <label>New Password</label>
            <input type="password" id="password" placeholder="Min 8 characters" />
            <label>Confirm Password</label>
            <input type="password" id="confirm" placeholder="Repeat password" />
            <p class="error" id="error"></p>
            <button onclick="submit()">Set Password</button>
        </div>

        <script>
            async function submit() {{
                const password = document.getElementById('password').value;
                const confirm = document.getElementById('confirm').value;
                const error = document.getElementById('error');

                if (!password) {{
                    error.style.display = 'block';
                    error.textContent = 'Password is required';
                    return;
                }}

                if (password.length < 8) {{
                    error.style.display = 'block';
                    error.textContent = 'Password must be at least 8 characters';
                    return;
                }}

                if (!/[A-Z]/.test(password)) {{
                    error.style.display = 'block';
                    error.textContent = 'Password must contain at least one uppercase letter';
                    return;
                }}

                if (!/[0-9]/.test(password)) {{
                    error.style.display = 'block';
                    error.textContent = 'Password must contain at least one number';
                    return;
                }}

                if (!confirm) {{
                    error.style.display = 'block';
                    error.textContent = 'Confirm password is required';
                    return;
                }}

                if (password !== confirm) {{
                    error.style.display = 'block';
                    error.textContent = 'Passwords do not match';
                    return;
                }}

                const res = await fetch('/auth/set-first-time-password', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        new_password: password,
                        repeat_password: confirm,
                        access_token: '{access_token}',
                        refresh_token: '{refresh_token}'
                    }})
                }});

                if (res.ok) {{
                    window.location.href = '{settings.FRONTEND_URL}/login?onboarded=true';
                }} else {{
                    const data = await res.json();
                    error.style.display = 'block';
                    error.textContent = data.detail || 'Something went wrong';
                }}
            }}
        </script>
    </body>
    </html>
    """)

class SetPasswordRequest(BaseModel):
    new_password: str
    access_token: str
    refresh_token: str

@auth_router.post("/set-first-time-password")
def set_password(request: SetPasswordRequest):
    print(request.access_token)
    print(request.refresh_token)
    supabase = get_supabase(
        access_token=request.access_token,
        refresh_token=request.refresh_token
    )
    try:
        supabase.auth.update_user({"password": request.new_password})
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))