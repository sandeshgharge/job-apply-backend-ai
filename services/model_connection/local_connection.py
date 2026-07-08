import requests
from config.env import settings
from .base_connection import BaseModelConnection

class LocalConnection(BaseModelConnection):
    def __init__(self):
        self.agentic_url = settings.AGENTIC_API_URL
        self.agentic_api_key = settings.AGENTIC_API_KEY
        self.model_name = settings.MODEL_NAME

    def call_model(self, prompt: str) -> str:
        response = requests.post(
            self.agentic_url,
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            raise Exception(f"Agentic AI error: {response.text}")

        return response.json()["response"]