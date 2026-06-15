import requests
from config.env import settings

AGENTIC_URL = settings.AGENTIC_API_URL
AGENTIC_API_KEY = settings.AGENTIC_API_KEY
MODEL_NAME = settings.MODEL_NAME


def call_model(prompt: str) -> str:
    response = requests.post(
        AGENTIC_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception(f"Agentic AI error: {response.text}")

    return response.json()["response"]