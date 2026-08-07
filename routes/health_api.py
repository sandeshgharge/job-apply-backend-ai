from fastapi import APIRouter

health_router = APIRouter(prefix="/api", tags=["Health"])

@health_router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Backend is running successfully!"
    }
