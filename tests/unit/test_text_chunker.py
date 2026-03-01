from infra.loaders.text_chunker import TextChunker


def test_text_chunker_returns_empty_for_blank_input() -> None:
    chunker = TextChunker(chunk_size=10, overlap=2)

    assert chunker.chunk("") == []
    assert chunker.chunk("   ") == []


def test_text_chunker_splits_text_into_non_empty_chunks() -> None:
    chunker = TextChunker(chunk_size=20, overlap=5)
    text = "Este é um texto de teste para validar chunking com LangChain."

    chunks = chunker.chunk(text)

    assert len(chunks) > 0
    assert all(chunk.strip() for chunk in chunks)
