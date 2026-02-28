"""
Testes unitários para o TokenOptimizer.

Verifica o comportamento da lógica de truncagem dinâmica de chunks
baseada no orçamento de tokens disponível.

Cenários cobertos:
- Todos os chunks cabem no orçamento (sem truncagem)
- Orçamento esgotado no terceiro chunk (truncagem parcial)
- Lista de chunks vazia
- Primeiro chunk já excede o orçamento (nenhum chunk retornado)
"""

import uuid
from domain.entities.document import DocumentChunk
from core.token_optimization.token_optimizer import TokenOptimizer


def create_chunk(content: str) -> DocumentChunk:
    """Factory helper para criar um DocumentChunk de teste com embedding fake."""
    return DocumentChunk(
        id=uuid.uuid4(),
        document_name="test.pdf",
        content=content,
        embedding=[0.0] * 10  # Embedding fake — não relevante para este teste
    )


def test_token_optimizer_no_trimming_needed():
    """
    Cenário: todos os chunks cabem dentro do orçamento.
    Cada chunk tem 40 chars → 10 tokens. 3 chunks = 30 tokens. 30 < 100 → nenhum é descartado.
    """
    optimizer = TokenOptimizer(max_context_tokens=100)
    chunks = [
        create_chunk("A" * 40),
        create_chunk("B" * 40),
        create_chunk("C" * 40),
    ]

    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 3  # Todos os chunks devem ser retornados


def test_token_optimizer_trims_excess_chunks():
    """
    Cenário: o terceiro chunk ultrapassa o orçamento e deve ser descartado.
    - Chunk 1: 10 tokens (acumulado: 10)
    - Chunk 2: 10 tokens (acumulado: 20)
    - Chunk 3: 10 tokens (acumulado: 30) → excede o limite de 25 → descartado
    """
    optimizer = TokenOptimizer(max_context_tokens=25)
    chunks = [
        create_chunk("A" * 40),
        create_chunk("B" * 40),
        create_chunk("C" * 40),
    ]

    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 2                     # Apenas os dois primeiros devem ser retornados
    assert optimized[0].content == "A" * 40
    assert optimized[1].content == "B" * 40


def test_token_optimizer_empty_chunks():
    """
    Cenário: lista de entrada vazia — deve retornar lista vazia sem erros.
    """
    optimizer = TokenOptimizer(max_context_tokens=10)
    optimized = optimizer.optimize([])
    assert len(optimized) == 0


def test_token_optimizer_large_first_chunk():
    """
    Cenário: o primeiro chunk já excede o orçamento — nenhum chunk deve ser retornado.
    Chunk 1: 40 chars → 10 tokens. Orçamento: 5 tokens. 10 > 5 → descartado imediatamente.
    """
    optimizer = TokenOptimizer(max_context_tokens=5)
    chunks = [
        create_chunk("A" * 40)
    ]
    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 0  # Nenhum chunk cabe no orçamento
