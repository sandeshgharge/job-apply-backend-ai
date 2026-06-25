from token import OP

from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import List, Optional
from pydantic.alias_generators import to_camel


# Shared config for all models
camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# -----------------------------
# PERSONAL INFO
# -----------------------------

class CvLinks(BaseModel):
    model_config = camel_config

    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    website: Optional[str] = None

class CvLanguage(BaseModel):
    model_config = camel_config
    language: str
    proficiency: str

class CvPersonalInfo(BaseModel):
    model_config = camel_config

    first_name: str
    last_name: str
    headline: Optional[str] = None
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    links: Optional[CvLinks] = None
    languages: Optional[List[CvLanguage]] = []


# -----------------------------
# SKILLS
# -----------------------------

class CvSkills(BaseModel):
    model_config = camel_config

    frontend: List[str] = []
    backend: List[str] = []
    devops: List[str] = []


# -----------------------------
# EXPERIENCE
# -----------------------------

class CvResponsibility(BaseModel):
    model_config = camel_config

    id: str
    text: str
    include: bool = True


class CvExperience(BaseModel):
    model_config = camel_config

    id: str
    job_title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    responsibilities: List[CvResponsibility] = []
    include: bool = True


# -----------------------------
# EDUCATION
# -----------------------------

class CvEducation(BaseModel):
    model_config = camel_config

    id: str
    degree: str
    field_of_study: Optional[str] = None
    institution: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include: bool = True


# -----------------------------
# PROJECTS
# -----------------------------

class CvProject(BaseModel):
    model_config = camel_config

    id: str
    title: str
    description: Optional[str] = None
    technologies: List[str] = []
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    link: Optional[str] = None
    include: bool = True


# -----------------------------
# CERTIFICATIONS
# -----------------------------

class CvCertification(BaseModel):
    model_config = camel_config

    id: str
    name: str
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    include: bool = True


# -----------------------------
# AWARDS
# -----------------------------

class CvAward(BaseModel):
    model_config = camel_config

    id: str
    title: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    include: bool = True


# -----------------------------
# PUBLICATIONS
# -----------------------------

class CvPublication(BaseModel):
    model_config = camel_config

    id: str
    title: str
    publisher: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    include: bool = True


# -----------------------------
# VOLUNTEER
# -----------------------------

class CvVolunteer(BaseModel):
    model_config = camel_config

    id: str
    role: str
    organization: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    include: bool = True


# -----------------------------
# REFERENCES
# -----------------------------

class CvReference(BaseModel):
    model_config = camel_config

    id: str
    name: str
    position: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    include: bool = True


# -----------------------------
# CUSTOM SECTIONS
# -----------------------------

class CvCustomItem(BaseModel):
    model_config = camel_config

    id: str
    text: str
    include: bool = True


class CvCustomSection(BaseModel):
    model_config = camel_config

    id: str
    section_title: str
    include: bool = True
    items: List[CvCustomItem] = []


# -----------------------------
# MAIN DATA
# -----------------------------

class CvData(BaseModel):
    model_config = camel_config

    personal_info: CvPersonalInfo
    summary: Optional[str] = None
    skills: Optional[CvSkills] = None
    experience: List[CvExperience] = []
    education: List[CvEducation] = []
    projects: List[CvProject] = []
    certifications: List[CvCertification] = []
    awards: List[CvAward] = []
    publications: List[CvPublication] = []
    volunteer_experience: List[CvVolunteer] = []
    interests: List[str] = []
    references: List[CvReference] = []
    custom_sections: List[CvCustomSection] = []



# -----------------------------
# DOCUMENT
# -----------------------------

class CVDocument(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("_id"),   # reads _id from MongoDB
        serialization_alias="id"                # writes as _id to MongoDB
    )
    user_id: str
    title: Optional[str] = None
    cv_data: CvData
    version: int = 1