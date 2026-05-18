from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str
    SUPABASE_JWT_SECRET:str
    JWT_SECRET: str
    AGENTIC_URL: str
    AGENTIC_API_KEY: str

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()