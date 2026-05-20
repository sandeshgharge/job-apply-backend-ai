import logging
from functools import lru_cache
from typing import Optional
from urllib import response
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




import time
import jwt
import requests
from jwt.algorithms import RSAAlgorithm, ECAlgorithm  # EC is likely for Supabase ES256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

ISSUER = settings.AUTH_ISSUER
JWKS_URL = settings.AUTH_JWKS_URL

_jwks_cache = {"fetched_at": 0, "jwks": None}
JWKS_TTL_SECONDS = 20 * 60  # safe-ish; adjust if you want fresher keys sooner

def get_jwks():
    now = time.time()
    if _jwks_cache["jwks"] is None or now - _jwks_cache["fetched_at"] > JWKS_TTL_SECONDS:
        resp = requests.get(JWKS_URL, timeout=10)
        resp.raise_for_status()
        _jwks_cache["jwks"] = resp.json()
        _jwks_cache["fetched_at"] = now
    return _jwks_cache["jwks"]

def find_signing_key(jwks, kid):
    for k in jwks["keys"]:
        if k.get("kid") == kid:
            return k
    return None

def jwk_to_pyjwt_key(jwk):
    # PyJWT can work with an RSA/EC public key if you build it.
    # Supabase signing keys are commonly EC (ES256 / P-256).
    kty = jwk["kty"]
    if kty == "EC":
        # Build EC public key from JWK using cryptography
        public_numbers = ec.EllipticCurvePublicNumbers(
            int.from_bytes(jwt.utils.base64url_decode(jwk["x"]), "big"),
            int.from_bytes(jwt.utils.base64url_decode(jwk["y"]), "big"),
            ec.SECP256R1()
        )
        return public_numbers.public_key()
    elif kty == "RSA":
        return jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
    else:
        raise ValueError(f"Unsupported JWK kty: {kty}")

def verify_supabase_jwt(access_token: str):
    unverified_header = jwt.get_unverified_header(access_token)
    kid = unverified_header.get("kid")
    alg = unverified_header.get("alg")

    jwks = get_jwks()
    jwk = find_signing_key(jwks, kid)
    if not jwk:
        raise jwt.InvalidTokenError("No matching JWK found for kid")

    public_key = jwk_to_pyjwt_key(jwk)

    # IMPORTANT: set issuer and algorithms
    payload = jwt.decode(
        access_token,
        key=public_key,
        algorithms=[alg],          # or hardcode ["ES256"] if you only use that
        issuer=ISSUER,
        options={"verify_aud": False},  # Supabase access tokens usually don't use aud the same way
    )
    return payload




bearer_scheme = HTTPBearer(auto_error=False)


def _decode_supabase_token(token: str) -> dict:
    """
    Validate and decode a Supabase-issued JWT.
    Raises jwt.PyJWTError on any validation failure.
    """
    return jwt.decode(
        token,
        SUPABASE_JWT_SECRET.encode("utf-8"),
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
        
        if request.method == "OPTIONS":
            return await call_next(request)
        
        body_bytes = await request.body()
        
        try:
            body_str = body_bytes.decode("utf-8")
        except UnicodeDecodeError:
            body_str = "<binary data>"
        
        logger.warning(
            f"Incoming {request.method} {request.url.path} | "
            f"Body: {body_str}"
        )

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
            payload = verify_supabase_jwt(token)
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has expired"},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError as exc:
            logger.warning("JWT validation failed : %s", exc)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or malformed token."},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Attach user to request state for use in route handlers
        request.state.user = payload
        return await call_next(request)