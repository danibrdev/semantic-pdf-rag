from abc import ABC, abstractmethod

class LLMPort(ABC):

    # Abstração para definir a interface para geração do texto RAG
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass