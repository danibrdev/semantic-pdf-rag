from typing import List
from domain.entities.document import DocumentChunk


class TokenOptimizer:
    """
    Responsible for optimizing retrieved chunks
    based on token budget constraints.
    """

    def __init__(self, max_context_tokens: int):
        self.max_context_tokens = max_context_tokens

    def optimize(
        self,
        chunks: List[DocumentChunk],
    ) -> List[DocumentChunk]:
        """
        Applies:
        - Dynamic Top-K
        - Context trimming
        - Token budget enforcement
        """

        max_tokens = self.max_context_tokens

        optimized_chunks = []
        current_tokens = 0

        for chunk in chunks:
            chunk_tokens = self._estimate_tokens(chunk.content)

            if current_tokens + chunk_tokens > max_tokens:
                break

            optimized_chunks.append(chunk)
            current_tokens += chunk_tokens

        return optimized_chunks

    def _estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (1 token ≈ 4 chars).
        Deterministic and cheap.
        """
        return len(text) // 4