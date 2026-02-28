"""
Port (contrato) para provedores de embeddings.

Define a interface abstrata que qualquer implementação de geração de embeddings
deve seguir (ex: OpenAI, Gemini). A camada core conhece apenas este contrato,
nunca a implementação concreta — garantindo o princípio de inversão de dependência.
"""

from abc import ABC, abstractmethod
from typing import List

class EmbeddingPort(ABC):

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Gera e retorna o embedding (vetor de floats) para um único texto."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera e retorna embeddings em lote para uma lista de textos de forma otimizada."""
        pass