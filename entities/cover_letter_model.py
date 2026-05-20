from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone


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
    id: Optional[str] = None
    title: str
    userId: str
    cldata: CoverLetterInfo
    version: int = 1

    model_config = {
        "populate_by_name": True  # ✅ add here, inside CVDocument only
    }