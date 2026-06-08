"""
Jobs API router.

Proxies Supabase upsert operations for the `jobs` table.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.supabase_db_connection.supabase_client import get_supabase

jobs_router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class JobUpsertRequest(BaseModel):
    id: str
    user_id: str
    company_name: Optional[str] = None
    role: Optional[str] = None
    company_location: Optional[str] = None
    applied_date: Optional[str] = None
    status: Optional[str] = None
    salary: Optional[str] = None
    contact_name: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None
    job_description: Optional[str] = None
    cover_letter_pdf_url: Optional[str] = None
    cv_pdf_url: Optional[str] = None


# ---------------------------------------------------------------------------
# POST /jobs/upsert
# ---------------------------------------------------------------------------

@jobs_router.post("/upsert")
def upsert_job(request: JobUpsertRequest):
    supabase = get_supabase()
    try:
        data = request.model_dump(exclude_none=True)

        response = (
            supabase.table("jobs")
            .upsert(data)
            .execute()
        )

        # Return the id from the upserted row
        row_id = request.id
        if response.data and len(response.data) > 0:
            row_id = response.data[0].get("id", request.id)

        return {"message": "Job saved successfully", "id": row_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
