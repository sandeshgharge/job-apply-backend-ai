from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str
    DATABASE_NAME: str

    JWT_SECRET: str

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()