from typing import Optional
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class ApiAgentInfo(BaseModel):
    model_config = camel_config

    id: Optional[str] = None
    user_id: Optional[str] = None
    name: str
    agent_api_url: Optional[str] = None
    agent_api_key: Optional[str] = None
    model_name: Optional[str] = None
    is_public: bool = False
