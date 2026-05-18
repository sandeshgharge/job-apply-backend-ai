import logging
from functools import lru_cache
from typing import Optional
from config.env import settings

import jwt  # pip install PyJWT
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUPABASE_JWT_SECRET = settings.SUPABASE_JWT_SECRET

# Routes that skip authentication (add more as needed)
PUBLIC_PATHS: set[str] = {
    "/",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
}

# ---------------------------------------------------------------------------
# Token validation
# ---------------------------------------------------------------------------

bearer_scheme = HTTPBearer(auto_error=False)


def _decode_supabase_token(token: str) -> dict:
    """
    Validate and decode a Supabase-issued JWT.
    Raises jwt.PyJWTError on any validation failure.
    """
    return jwt.decode(
        token,
        SUPABASE_JWT_SECRET,
        algorithms=["HS256"],
        audience="authenticated",          # Supabase sets aud = "authenticated"
        options={"require": ["exp", "sub", "role"]},
    )


# ---------------------------------------------------------------------------
# FastAPI dependency  (use on individual routes if you prefer opt-in security)
# ---------------------------------------------------------------------------

async def require_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    """
    Dependency that returns the decoded JWT payload (the current user).

    Example:
        @app.get("/me")
        async def me(user: dict = Depends(require_user)):
            return {"user_id": user["sub"]}
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = _decode_supabase_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError as exc:
        logger.warning("JWT validation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# ---------------------------------------------------------------------------
# Global middleware  (protects ALL routes automatically)
# ---------------------------------------------------------------------------

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse


class SupabaseAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that validates Supabase JWTs on every request.
    Requests to PUBLIC_PATHS are allowed through without a token.
    On success, the decoded payload is stored as request.state.user.
    """

    async def dispatch(self, request: StarletteRequest, call_next):
        # Allow public / unauthenticated paths
        if request.url.path in PUBLIC_PATHS:
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

        try:
            payload = _decode_supabase_token(token)
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has expired"},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError as exc:
            logger.warning("JWT validation failed: %s", exc)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or malformed token"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Attach user to request state for use in route handlers
        request.state.user = payload
        return await call_next(request)