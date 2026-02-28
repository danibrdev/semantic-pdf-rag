"""
Port (contrato) para provedores de LLM.

Define a interface abstrata para geração de texto (respostas) a partir de prompts.
Mantém a camada de domínio desacoplada de SDKs específicos (OpenAI, Gemini, etc.).
"""

from abc import ABC, abstractmethod


class LLMPort(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Gera e retorna uma resposta textual para o prompt informado."""
        pass
