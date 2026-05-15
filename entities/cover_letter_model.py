from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CoverLetterSection(BaseModel):
    id: str
    title: str
    content: str
    sectionPrompt: str
    loading: bool


class CoverLetterInfo(BaseModel):
    commonPrompt: str
    sectionPrompts: List[CoverLetterSection]

class CoverLetterDocument(BaseModel):
    user_id: str
    cover_letter_info: CoverLetterInfo
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)