from abc import ABC, abstractmethod

class BaseModelConnection(ABC):
    @abstractmethod
    def call_model(self, prompt: str) -> str:
        """Sends a prompt to the model and returns the text response."""
        pass
