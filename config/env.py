from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

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

    # Application
    DEBUG: bool = Field(False, description="Enable debug mode")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignore extra env vars not defined here
    )

settings = Settings()