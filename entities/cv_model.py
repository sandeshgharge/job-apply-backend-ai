from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


# -----------------------------
# PERSONAL INFO
# -----------------------------

class CvLinks(BaseModel):
    linkedin: str
    github: str
    portfolio: str
    website: str


class CvPersonalInfo(BaseModel):
    firstName: str
    lastName: str
    headline: str
    email: str
    phone: str
    address: str
    links: CvLinks


# -----------------------------
# SKILLS
# -----------------------------

class CvLanguage(BaseModel):
    id: str
    language: str
    proficiency: str


class CvSkills(BaseModel):
    technical: List[str]
    soft: List[str]
    tools: List[str]
    frameworks: List[str]
    languages: List[CvLanguage]


# -----------------------------
# EXPERIENCE
# -----------------------------

class CvResponsibility(BaseModel):
    id: str
    text: str
    include: bool


class CvExperience(BaseModel):
    id: str
    jobTitle: str
    company: str
    location: str
    startDate: str
    endDate: str
    current: bool
    responsibilities: List[CvResponsibility]
    include: bool


# -----------------------------
# EDUCATION
# -----------------------------

class CvEducation(BaseModel):
    id: str
    degree: str
    fieldOfStudy: str
    institution: str
    location: str
    startDate: str
    endDate: str
    include: bool


# -----------------------------
# PROJECTS
# -----------------------------

class CvProject(BaseModel):
    id: str
    title: str
    description: str
    technologies: List[str]
    role: str
    startDate: str
    endDate: str
    link: str
    include: bool


# -----------------------------
# CERTIFICATIONS
# -----------------------------

class CvCertification(BaseModel):
    id: str
    name: str
    issuer: str
    issueDate: str
    expiryDate: str
    credentialId: str
    credentialUrl: str
    include: bool


# -----------------------------
# AWARDS
# -----------------------------

class CvAward(BaseModel):
    id: str
    title: str
    issuer: str
    date: str
    description: str
    include: bool


# -----------------------------
# PUBLICATIONS
# -----------------------------

class CvPublication(BaseModel):
    id: str
    title: str
    publisher: str
    date: str
    link: str
    description: str
    include: bool


# -----------------------------
# VOLUNTEER
# -----------------------------

class CvVolunteer(BaseModel):
    id: str
    role: str
    organization: str
    location: str
    startDate: str
    endDate: str
    description: str
    include: bool


# -----------------------------
# REFERENCES
# -----------------------------

class CvReference(BaseModel):
    id: str
    name: str
    position: str
    company: str
    email: str
    phone: str
    include: bool


# -----------------------------
# CUSTOM SECTIONS
# -----------------------------

class CvCustomItem(BaseModel):
    id: str
    text: str
    include: bool


class CvCustomSection(BaseModel):
    id: str
    sectionTitle: str
    include: bool
    items: List[CvCustomItem]


# -----------------------------
# METADATA
# -----------------------------

class CvMetadata(BaseModel):
    createdAt: str
    updatedAt: str
    version: str
    source: str


# -----------------------------
# MAIN DATA
# -----------------------------

class CvData(BaseModel):
    personalInfo: CvPersonalInfo
    summary: str
    skills: CvSkills
    experience: List[CvExperience]
    education: List[CvEducation]
    projects: List[CvProject]
    certifications: List[CvCertification]
    awards: List[CvAward]
    publications: List[CvPublication]
    volunteerExperience: List[CvVolunteer]
    interests: List[str]
    references: List[CvReference]
    customSections: List[CvCustomSection]
    metadata: CvMetadata

# -----------------------------
# DOCUMENT
# -----------------------------

class CVDocument(BaseModel):
    user_id: str
    cv_info: CvData
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)