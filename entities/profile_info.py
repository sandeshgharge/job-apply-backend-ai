from typing import Optional
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict, Field

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ProfileInfo(BaseModel):
    model_config = camel_config

    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    agent_api_url: Optional[str] = None
    agent_api_key: Optional[str] = None
    model_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    signature_image_url: Optional[str] = None
    role: str = None
    use_default_api: bool = Field(default=True, description="Whether to use the default API or not")