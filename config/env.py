from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import json
from typing import Any


class Settings(BaseSettings):
    # MongoDB
    MONGO_URI: str = Field(..., description="MongoDB connection string")

    # Supabase
    SUPABASE_URL: str = Field(..., description="Supabase project URL")
    SUPABASE_ANON_KEY: str = Field(..., description="Supabase anonymous API key")

    # Agentic API
    AGENTIC_API_URL: str = Field(..., description="Agentic API URL")
    AGENTIC_API_KEY: str = Field(..., description="Agentic API key")
    MODEL_NAME: str = Field("mistral", description="LLM model name for the Agentic API")

    # Groq API
    GROQ_API_URL: str = Field(..., description="Groq API base URL")
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    GROQ_MODEL: str = Field("llama-3.1-8b-instant", description="Groq LLM model name")

    FRONTEND_URL: str = Field(..., description="Front end url")
    ALLOWED_ORIGINS: Any = Field(default=[], description="Allowed origins for CORS and origin validation")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [origin.rstrip("/") for origin in parsed]
                except json.JSONDecodeError:
                    pass
            # Replace semicolons with commas and split by comma to support both separators
            normalized_v = v.replace(";", ",")
            return [origin.strip().rstrip("/") for origin in normalized_v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return [origin.rstrip("/") for origin in v]
        return v

    APP_URL: str = Field(..., description="Application URL")
    PROFILE_STORAGE_BUCKET: str = Field(..., description="Storage bucket name profile files.")
    PROFILE_IMAGE_NAME: str = Field(..., description="Profile image url filename")

    PROFILE_SIGN_IMAGE: str = Field(..., description="Profile signature image url filename")

    # Application
    DEBUG: bool = Field(False, description="Enable debug mode")
    APP_ENV: str = Field("local", description="Environment (local or production)")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignore extra env vars not defined here
    )

settings = Settings()