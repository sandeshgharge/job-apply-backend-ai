"""
Jobs API router.

Proxies Supabase operations for the `jobs` table.
"""

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from typing import List, Optional

from entities.cover_letter_model import CoverLetterDocInfo
from entities.cv_model import CvData
from entities.job_details import JobDetails, JobDetailsUpdate
import services.jobs_service as jobs_service

jobs_router = APIRouter(prefix="/jobs", tags=["Jobs"])

# ---------------------------------------------------------------------------
# POST /jobs
# ---------------------------------------------------------------------------

@jobs_router.post("", response_model=JobDetails)
async def create_job(
    request: Request,
    jd: JobDetails,
    cv_data: Optional[CvData]   ,
    cover_letter_data: Optional[CoverLetterDocInfo]):
    token = getattr(request.state, "token", None)
    return await jobs_service.add_job(jd, token, cv_data, cover_letter_data)

@jobs_router.post("/upsert", response_model=JobDetails)
async def upsertJob(
    request: Request,
    jd: JobDetails
):
    token = getattr(request.state, "token", None)
    return await jobs_service.add_job(jd, token)

# ---------------------------------------------------------------------------
# PUT /jobs/{id}
# ---------------------------------------------------------------------------

@jobs_router.patch("/{id}")
def update_job(id: str, request_data: JobDetailsUpdate, request: Request):
    token = getattr(request.state, "token", None)
    return jobs_service.update_job(id, request_data, token)


# ---------------------------------------------------------------------------
# GET /jobs/user/{user_id}
# ---------------------------------------------------------------------------

@jobs_router.get("/user/{user_id}", response_model=List[JobDetails])
def get_jobs_by_user(user_id: str, request: Request):
    token = getattr(request.state, "token", None)
    return jobs_service.get_jobs_by_user(user_id, token)


# ---------------------------------------------------------------------------
# DELETE /jobs/{job_id}
# ---------------------------------------------------------------------------

@jobs_router.delete("/{job_id}")
def delete_job(job_id: str, request: Request):
    token = getattr(request.state, "token", None)
    return jobs_service.delete_job(job_id, token)
