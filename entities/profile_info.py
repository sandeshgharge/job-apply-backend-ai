from typing import Optional
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict, Field

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ProfileInfo(BaseModel):
    model_config = camel_config

    id: str
    first_name: str
    last_name: str
    location: str
    email: str
    agent_api_url: str
    agent_api_key: str
    model_name: str
    profile_image_url: Optional[str]
    signature_image_url: Optional[str]