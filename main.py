import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from middleware.supabase_middleware import SupabaseAuthMiddleware
from services.model_connection import send_prompt
from services.model_connection import groq_connection
from services.scraper_service import extract_job
from services.ai_service import extract_job_data
from routes.cover_letter_api import cl_router
from routes.cv_api import cv_router
from routes.auth_api import auth_router
from routes.profile_api import profile_router
from routes.storage_api import storage_router
from routes.jobs_api import jobs_router

# Configure global logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class ExtractRequest(BaseModel):
    url: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SupabaseAuthMiddleware)
app.include_router(cl_router)
app.include_router(cv_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(storage_router)
app.include_router(jobs_router)


@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    #data = send_prompt.call_model(body.get("prompt"))
    data = groq_connection.call_model(body.get("prompt"))
    return {"output": data}

@app.post("/extract-job-data")
async def extract_job_data_endpoint(request: Request):
    body = await request.json()
    job_description = body.get("job_description")

    return extract_job_data(job_description)

@app.post("/extract-job-description")
def extract(req: ExtractRequest):
    return extract_job(req.url)

@app.get("/hello")
async def read_root():
    return {"Hello": "World"}