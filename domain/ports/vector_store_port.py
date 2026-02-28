"""
Port (contrato) para o armazenamento vetorial.

Define a interface abstrata que qualquer implementação de banco vetorial deve seguir
(ex: PgVector, Pinecone, ChromaDB). O domínio nunca importa o banco diretamente —
ele apenas depende deste contrato, preservando a independência de infraestrutura.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.document import DocumentChunk

class VectorStorePort(ABC):

    @abstractmethod
    def save(self, chunk: DocumentChunk) -> None:
        """Persiste um DocumentChunk (texto + embedding) no banco vetorial."""
        pass

    @abstractmethod
    def similarity_search(
        self,
        embedding: List[float],
        k: int,
        threshold: Optional[float] = None
    ) -> List[DocumentChunk]:
        """
        Busca os k chunks mais similares ao embedding fornecido.
        O parâmetro threshold (opcional) filtra resultados abaixo de um score mínimo de similaridade.
        """
        pass