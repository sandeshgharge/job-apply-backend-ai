from fastapi import HTTPException
from typing import Optional, List, Union
from pydantic import BaseModel
from entities.cover_letter_model import CoverLetterDocInfo
from entities.cv_model import CvData
from entities.job_details import JobDetails, JobDetailsUpdate
from services.supabase_db_connection.supabase_client import get_supabase
from services.mongo_db_connection.db import applied_job_details_collection

async def add_job(
    jd: JobDetails,
    token: Optional[str] = None,
    cv_data: Optional[Union[CvData, dict]] = None,
    cl_data: Optional[Union[CoverLetterDocInfo, dict]] = None
) -> JobDetails:
    supabase = get_supabase(access_token=token)
    try:
        data = jd.model_dump(mode='json', exclude_none=True)
        response = supabase.table("jobs").insert(data).execute()
        if response.data and len(response.data) > 0:
            job_id = response.data[0].get('id')
            jd.id = job_id  # Update the JobDetails with the generated ID for later use
            print(f"Job created successfully with ID: {job_id}")
        else:
            raise HTTPException(status_code=500, detail="Failed to create job")

        jd_dict = jd.model_dump(mode='json', exclude_none=True)
        cv_data_dict = (
            cv_data.model_dump(mode='json', exclude_none=True)
            if isinstance(cv_data, BaseModel)
            else cv_data
        )
        cl_data_dict = (
            cl_data.model_dump(mode='json', exclude_none=True)
            if isinstance(cl_data, BaseModel)
            else cl_data
        )

        doc = {
            "job_id": job_id,
            "user_id": jd.user_id,
            "job_details": jd_dict,
            "cv_data": cv_data_dict,
            "cl_data": cl_data_dict,
        }

        await applied_job_details_collection.insert_one(doc)

        return jd

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_job(id: str, request_data: JobDetailsUpdate, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        data = request_data.model_dump(mode='json', exclude_none=True)
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
