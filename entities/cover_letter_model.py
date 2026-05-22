from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import List, Optional
from pydantic.alias_generators import to_camel
from datetime import datetime, timezone


# Shared config for all models
camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class CoverLetterSection(BaseModel):
    model_config = camel_config

    id: str
    title: str
    content: str
    section_prompt: str
    loading: bool


class CoverLetterInfo(BaseModel):
    model_config = camel_config

    common_prompt: str
    section_prompts: List[CoverLetterSection]


class CoverLetterDocument(BaseModel):
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
    title: str
    cl_data: CoverLetterInfo
    version: int = 1
