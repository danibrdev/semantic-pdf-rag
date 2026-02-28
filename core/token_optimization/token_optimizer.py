"""
Otimizador de tokens para o contexto RAG.

Responsável por garantir que apenas os chunks que cabem dentro do orçamento de tokens
sejam enviados ao LLM. Aplica truncagem dinâmica (Dynamic Top-K): itera sobre os chunks
por ordem de relevância e para quando o limite de tokens é atingido.

Utiliza uma estimativa heurística simples: 1 token ≈ 4 caracteres.
Esta estimativa é intencional — é determinística, barata e não requer tokenizer externo.
"""

from typing import List
from domain.entities.document import DocumentChunk


class TokenOptimizer:
    """
    Otimiza a lista de chunks recuperados para respeitar o orçamento de tokens.
    Deve ser aplicado ANTES de montar o prompt e chamar o LLM.
    """

    def __init__(self, max_context_tokens: int):
        # Limite máximo de tokens que podem ser usados pelo contexto (chunks recuperados)
        self.max_context_tokens = max_context_tokens

    def optimize(
        self,
        chunks: List[DocumentChunk],
    ) -> List[DocumentChunk]:
        """
        Filtra e retorna apenas os chunks que cabem dentro do orçamento de tokens.
        Chunks excedentes (que ultrapassariam o limite) são descartados.
        """

        max_tokens = self.max_context_tokens

        optimized_chunks = []
        current_tokens = 0  # Acumulador de tokens consumidos

        for chunk in chunks:
            chunk_tokens = self._estimate_tokens(chunk.content)

            # Se adicionar este chunk ultrapassar o limite, para imediatamente
            if current_tokens + chunk_tokens > max_tokens:
                break

            optimized_chunks.append(chunk)
            current_tokens += chunk_tokens

        return optimized_chunks

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimativa heurística de tokens: 1 token ≈ 4 caracteres.
        Determinística e sem dependência externa (não usa tiktoken ou equivalente).
        """
        return len(text) // 4