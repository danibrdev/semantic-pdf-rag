import uuid
from domain.entities.document import DocumentChunk
from core.token_optimization.token_optimizer import TokenOptimizer


def create_chunk(content: str) -> DocumentChunk:
    return DocumentChunk(
        id=uuid.uuid4(),
        document_name="test.pdf",
        content=content,
        embedding=[0.0] * 10
    )


def test_token_optimizer_no_trimming_needed():
    optimizer = TokenOptimizer(max_context_tokens=100)
    # Each chunk has 40 chars -> 10 tokens. 3 chunks = 30 tokens. 30 < 100 max. All should be kept.
    chunks = [
        create_chunk("A" * 40),
        create_chunk("B" * 40),
        create_chunk("C" * 40),
    ]

    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 3


def test_token_optimizer_trims_excess_chunks():
    optimizer = TokenOptimizer(max_context_tokens=25)
    # Each chunk has 40 chars = 10 tokens.
    # Chunk 1: 10 tokens (Total: 10)
    # Chunk 2: 10 tokens (Total: 20)
    # Chunk 3: 10 tokens (Total: 30) - Should drop this one because 30 > 25.
    chunks = [
        create_chunk("A" * 40),
        create_chunk("B" * 40),
        create_chunk("C" * 40),
    ]

    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 2
    assert optimized[0].content == "A" * 40
    assert optimized[1].content == "B" * 40


def test_token_optimizer_empty_chunks():
    optimizer = TokenOptimizer(max_context_tokens=10)
    optimized = optimizer.optimize([])
    assert len(optimized) == 0


def test_token_optimizer_large_first_chunk():
    optimizer = TokenOptimizer(max_context_tokens=5)
    # First chunk is 40 chars = 10 tokens. Exceeds limit immediately.
    chunks = [
        create_chunk("A" * 40)
    ]
    optimized = optimizer.optimize(chunks)
    assert len(optimized) == 0
