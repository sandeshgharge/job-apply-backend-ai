from config.env import settings
from .local_connection import LocalConnection
from .groq_connection import GroqConnection
from .base_connection import BaseModelConnection

def get_model_connection() -> BaseModelConnection:
    if settings.APP_ENV == "production":
        return GroqConnection()
    return LocalConnection()
