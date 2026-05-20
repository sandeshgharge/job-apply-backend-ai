from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str
    SUPABASE_JWT_SECRET:str
    AGENTIC_API_URL: str
    AGENTIC_API_KEY: str
    AUTH_ISSUER:str
    AUTH_JWKS_URL:str

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()