import asyncio
import sys

# Playwright requires ProactorEventLoop on Windows to spawn subprocesses.
# uvicorn defaults to SelectorEventLoop on Windows, which raises NotImplementedError
# when asyncio.create_subprocess_exec is called internally by Playwright.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.env import settings
from middleware.supabase_middleware import SupabaseAuthMiddleware
from middleware.origin_middleware import ValidateOriginMiddleware
from services.model_connection.factory import get_model_connection
from services.scraper_service import extract_job
from services.ai_service import extract_job_data
from routes.cover_letter_api import cl_router
from routes.cv_api import cv_router
from routes.auth_api import auth_router
from routes.profile_api import profile_router
from routes.storage_api import storage_router
from routes.jobs_api import jobs_router
from routes.agents_api import agents_router
from services.background_scheduler_service import ping_self

from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from services.browser_service import browser_manager


# Configure global logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown."""

    scheduler = BackgroundScheduler()

    try:
        # -------------------------
        # STARTUP
        # -------------------------

        # Start Playwright + Chromium
        await browser_manager.start()
        logger.info("Browser instance started!")

        # Start Scheduler
        scheduler.add_job(
            ping_self,
            "interval",
            minutes=14
        )
        scheduler.start()
        logger.info("Background scheduler started successfully.")


        # Application runs here
        yield

    finally:
        await browser_manager.stop()
        logger.info("Browser instance closed!")

        if scheduler.running:
            scheduler.shutdown(wait=False)
            logger.info("Background scheduler stopped.")



app = FastAPI(lifespan=lifespan)

class ExtractRequest(BaseModel):
    url: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SupabaseAuthMiddleware)
app.add_middleware(ValidateOriginMiddleware)

app.include_router(cl_router)
app.include_router(cv_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(storage_router)
app.include_router(jobs_router)
app.include_router(agents_router)


@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    connection = get_model_connection()
    data = connection.call_model(body.get("prompt"))
    return {"text": data}

@app.post("/extract-job-data")
async def extract_job_data_endpoint(request: Request):
    body = await request.json()
    job_description = body.get("jobDescription", body.get("jobDescription"))
    return extract_job_data(job_description)

@app.post("/extract-job-description")
async def extract(req: ExtractRequest):
    return await extract_job(req.url)

@app.get("/hello")
async def read_root():
    return {"Hello": "World"}