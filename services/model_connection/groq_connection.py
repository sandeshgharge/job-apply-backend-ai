import openai
from config.env import settings
from .base_connection import BaseModelConnection

class GroqConnection(BaseModelConnection):
    def call_model(self, prompt: str) -> str:
        client = openai.OpenAI(
            base_url=settings.GROQ_API_URL,
            api_key=settings.GROQ_API_KEY
        )

        try:
            # Send the POST request with a JSON body
            response = client.responses.create(
                input=prompt,
                model=settings.GROQ_MODEL
            )
            text = ""
            for item in response.output:
                if item.type == "message":
                    for content in item.content:
                        if content.type == "output_text":
                            text += content.text

            # Check if the response was successful
            if response.status == "completed":
                # Parse the JSON response
                return text
            else:
                print(f"Error: {response.status}")
                return 
        except Exception as e:
            print(f"Error: {e}")
            return ""