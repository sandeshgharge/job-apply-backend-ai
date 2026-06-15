from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class JobDetails(BaseModel):
    model_config = camel_config

    id: Optional[str] = None
    user_id: str
    company_name: str
    role: str
    company_location: str
    applied_date: Optional[str] = None
    status: str
    salary: Optional[str] = None
    contact_name: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None
    job_description: Optional[str] = None
    cover_letter_pdf_url: Optional[str] = None
    cv_pdf_url: Optional[str] = None


class JobDetailsUpdate(BaseModel):
    """All-optional version of JobDetails for partial / PATCH updates."""
    model_config = camel_config

    user_id: Optional[str] = None
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
