from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.env import settings

class ValidateOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        origin = request.headers.get("origin")
        if origin:
            clean_origin = origin.lower().rstrip("/")
            allowed_origins = [o.lower().rstrip("/") for o in settings.ALLOWED_ORIGINS]
            if "*" not in allowed_origins and clean_origin not in allowed_origins:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": f"Origin '{origin}' is not allowed."}
                )

        return await call_next(request)
