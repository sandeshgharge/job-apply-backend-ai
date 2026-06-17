import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse

import sys
from services.supabase_db_connection.supabase_client import get_supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Routes that skip authentication (add more as needed)
PUBLIC_PATHS: set[str] = {
    "/hello",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/auth/login",
    "/auth/signup",
}

bearer_scheme = HTTPBearer(auto_error=False)

# ---------------------------------------------------------------------------
# FastAPI dependency (use on individual routes if you prefer opt-in security)
# ---------------------------------------------------------------------------

async def require_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    """
    Dependency that returns the user dict from Supabase.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    supabase = get_supabase(credentials.credentials)
    try:
        user_response = supabase.auth.get_user(credentials.credentials)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or malformed token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Return user as dictionary
        return user_response.user.model_dump()
    except Exception as exc:
        logger.warning("Supabase validation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------
# Global middleware (protects ALL routes automatically)
# ---------------------------------------------------------------------------

class SupabaseAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that validates Supabase JWTs on every request using the client library.
    Requests to PUBLIC_PATHS are allowed through without a token.
    On success, the user payload is stored as request.state.user.
    """

    async def dispatch(self, request: StarletteRequest, call_next):
        # Allow public / unauthenticated paths
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)
        
        # Extract Bearer token
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid Authorization header"},
                headers={"WWW-Authenticate": "Bearer"},
            )


        token = auth_header.removeprefix("Bearer ").strip()
        supabase = get_supabase(token)

        try:
            user_response = supabase.auth.get_user(token)
            if not user_response or not user_response.user:
                raise ValueError("No user found for token")
                
            # Attach user and token to request state for use in route handlers
            request.state.user = user_response.user.model_dump()
            request.state.token = token
        except Exception as exc:
            logger.warning("Supabase JWT validation failed: %s", exc)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid, expired, or revoked token."},
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await call_next(request)