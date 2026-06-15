import asyncio
from fastapi import HTTPException
from typing import Optional, List
from entities.cover_letter_model import CoverLetterDocInfo
from entities.cv_model import CvData
from entities.job_details import JobDetails, JobDetailsUpdate
from services.storage_service import upload_file_to_storage
from services import storage_service
from services.supabase_db_connection.supabase_client import get_supabase
from services import cv_service, cover_letter_service

async def add_job(jd: JobDetails, token: Optional[str] = None, cv_data: Optional[CvData] = None, cl_data: Optional[CoverLetterDocInfo] = None) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        data = jd.model_dump(exclude_none=True)
        response = supabase.table("jobs").insert(data).execute()
        job_id = response.data[0].get('id')
        jd.id = job_id  # Update the JobDetails with the generated ID for later use
        if response.data and len(response.data) > 0:
            print(f"Job created successfully with ID: {job_id}")
        else:
            raise HTTPException(status_code=500, detail="Failed to create job")
        
        if cv_data is not None and cl_data is not None:
            user_id = jd.user_id
            file_path = f"{job_id}"

            # Render HTML (sync, fast) for both documents
            cv_html = storage_service.render_html(cv_data)
            cl_html = storage_service.render_html(cl_data)

            # Helper to generate PDF and upload in one coroutine
            async def _generate_and_upload(html: str, bucket: str, filename: str) -> dict:
                pdf_bytes = await storage_service.generate_pdf(html)
                return await upload_file_to_storage(
                    user_id=user_id,
                    bucket=bucket,
                    file_path=f"{file_path}/{filename}",
                    file_bytes=pdf_bytes,
                    content_type="application/pdf",
                    token=token,
                )

            # Run both pipelines concurrently
            cv_public_url, cl_public_url = await asyncio.gather(
                _generate_and_upload(cv_html, "apply-docs", "cv.pdf"),
                _generate_and_upload(cl_html, "apply-docs", "cl.pdf"),
            )

            # Update DB with the actual uploaded URLs
            supabase.table("jobs").update({
                "cv_pdf_url": cv_public_url.get("public_url"),
                "cover_letter_pdf_url": cl_public_url.get("public_url"),
            }).eq("id", job_id).execute()

        return jd
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_job(id: str, request_data: JobDetailsUpdate, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        data = request_data.model_dump(exclude_none=True)
        data["id"] = id

        response = (
            supabase.table("jobs")
            .update(data)
            .eq("id", id)
            .execute()
        )

        row_id = id
        if response.data and len(response.data) > 0:
            row_id = response.data[0].get("id", id)

        return {"message": "Job saved successfully", "id": row_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_jobs_by_user(user_id: str, token: Optional[str]) -> List[JobDetails]:
    supabase = get_supabase(access_token=token)
    try:
        response = (
            supabase.table("jobs")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return [JobDetails.model_validate(job) for job in response.data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_job(job_id: str, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        response = (
            supabase.table("jobs")
            .delete()
            .eq("id", job_id)
            .execute()
        )
        return {"message": "Job deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
