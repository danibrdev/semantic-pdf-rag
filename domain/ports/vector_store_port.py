from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.document import DocumentChunk

class VectorStorePort(ABC):

    @abstractmethod
    def save(self, chunk: DocumentChunk) -> None:
        pass

    @abstractmethod
    def similarity_search(
        self,
        embedding: List[float],
        k: int,
        threshold: Optional[float] = None
    ) -> List[DocumentChunk]:
        pass