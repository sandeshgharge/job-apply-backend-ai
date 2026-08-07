from pydantic import BaseModel, Field
from typing import Optional

class TemplateModel(BaseModel):
    name: str
    html_template: str
    isPublic: bool = False
    userId: str

class TemplateCreate(BaseModel):
    name: str
    html_template: str
    isPublic: bool = False
    userId: str

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    html_template: Optional[str] = None
    isPublic: Optional[bool] = None
    userId: str

class TemplatePreviewRequest(BaseModel):
    docType: str
    html_template: str
    userId: str
