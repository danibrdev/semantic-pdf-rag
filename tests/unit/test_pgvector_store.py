"""
Testes unitários para o PgVectorStore.

Verifica a inicialização, persistência e busca por similaridade
sem depender de um banco de dados PostgreSQL real.

POR QUÊ usar @patch aqui:
- PGVector faz conexão com o banco no construtor — sem mock, o teste quebraria
- O mock intercepta a chamada e retorna um objeto controlado (MagicMock)
"""

import uuid

# MagicMock: cria um objeto falso que aceita qualquer chamada de método sem erros.
# Útil para simular dependências externas como clientes de banco de dados.
from unittest.mock import MagicMock, patch

from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore, _NoopEmbeddings


class MockSettings:
    """Simula o Settings com os campos mínimos usados pelo PgVectorStore."""
    database_url = "postgresql://user:pass@localhost:5432/db"
    embedding_dimension = 1536


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_initialization(mock_pgvector) -> None:
    """
    Verifica que o PgVectorStore inicializa o PGVector com os parâmetros corretos:
    - connection: URL do banco de dados
    - collection_name: nome da tabela de vetores
    - use_jsonb: armazetodosna metadados como JSONB (mais eficiente no PostgreSQL)
    """
    settings = MockSettings()
    PgVectorStore(settings)

    # Verifica que PGVector foi instanciado exatamente uma vez
    mock_pgvector.assert_called_once()

    # call_args.kwargs captura os argumentos nomeados (keyword args) passados ao Mock
    assert mock_pgvector.call_args.kwargs["connection"] == settings.database_url
    assert mock_pgvector.call_args.kwargs["collection_name"] == "documents"
    assert mock_pgvector.call_args.kwargs["use_jsonb"] is True


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_save(mock_pgvector) -> None:
    """
    Verifica que save() chama add_embeddings com os parâmetros corretos.
    Garante que o chunk é persistido com id, texto, embedding e metadados corretamente.
    """
    # MagicMock() como instância do store — todos os métodos chamados nele são recordados
    store_impl = MagicMock()
    # Configura o mock para retornar store_impl quando PGVector() for chamado
    mock_pgvector.return_value = store_impl

    settings = MockSettings()
    store = PgVectorStore(settings)

    chunk_id = uuid.uuid4()
    chunk = DocumentChunk(
        id=chunk_id,
        document_name="test.pdf",
        content="Test content",
        embedding=[0.1, 0.2, 0.3],
        metadata={"source": "unit-test"},
    )

    store.save(chunk)

    # Verifica que add_embeddings foi chamado exatamente uma vez
    store_impl.add_embeddings.assert_called_once()

    # Inspeciona os argumentos com os quais add_embeddings foi chamado
    call_kwargs = store_impl.add_embeddings.call_args.kwargs
    assert call_kwargs["ids"] == [str(chunk_id)]
    assert call_kwargs["texts"] == ["Test content"]
    assert call_kwargs["embeddings"] == [[0.1, 0.2, 0.3]]
    assert call_kwargs["metadatas"][0]["document_name"] == "test.pdf"
    assert call_kwargs["metadatas"][0]["id"] == str(chunk_id)
    assert call_kwargs["metadatas"][0]["source"] == "unit-test"


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_similarity_search(mock_pgvector) -> None:
    """
    Verifica que similarity_search() reconstrói DocumentChunks corretamente
    a partir dos documentos retornados pelo PGVector.
    """
    store_impl = MagicMock()
    mock_pgvector.return_value = store_impl

    # Cria dois documentos falsos com metadados que simulam o que o banco retornaria
    mock_id_1 = uuid.uuid4()
    mock_id_2 = uuid.uuid4()
    doc_1 = MagicMock()
    doc_1.page_content = "Result 1"
    doc_1.metadata = {
        "id": str(mock_id_1),
        "document_name": "doc-a.pdf",
        "author": "Dani",
        "_embedding": [0.1, 0.2, 0.3],  # Embedding armazenado nos metadados
    }
    doc_2 = MagicMock()
    doc_2.page_content = "Result 2"
    doc_2.metadata = {
        "id": str(mock_id_2),
        "document_name": "doc-b.pdf",
        "author": "Steve",
        "_embedding": [0.4, 0.5, 0.6],
    }

    # Simula o retorno do banco: lista de tuplas (documento, score de distância)
    # Score 0.1 = distância baixa = alta similaridade
    store_impl.similarity_search_with_score_by_vector.return_value = [
        (doc_1, 0.1),
        (doc_2, 0.2),
    ]

    settings = MockSettings()
    store = PgVectorStore(settings)

    results = store.similarity_search(embedding=[0.1, 0.2, 0.3], k=2)

    assert len(results) == 2

    # Verifica que os campos do DocumentChunk foram reconstruídos corretamente
    assert results[0].id == mock_id_1
    assert results[0].document_name == "doc-a.pdf"
    assert results[0].content == "Result 1"
    assert results[0].embedding == [0.1, 0.2, 0.3]
    # Apenas "author" deve restar nos metadados — os campos internos são removidos
    assert results[0].metadata == {"author": "Dani"}

    assert results[1].id == mock_id_2
    assert results[1].document_name == "doc-b.pdf"
    assert results[1].content == "Result 2"
    assert results[1].embedding == [0.4, 0.5, 0.6]
    assert results[1].metadata == {"author": "Steve"}


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_similarity_search_with_threshold(mock_pgvector) -> None:
    """
    Verifica que o filtro de threshold descarta resultados com baixa similaridade.

    Score de distância: 0.9 → similaridade: 1 - 0.9 = 0.1
    Threshold configurado: 0.8 → 0.1 < 0.8, chunk deve ser descartado.
    """
    store_impl = MagicMock()
    mock_pgvector.return_value = store_impl

    doc = MagicMock()
    doc.page_content = "low confidence"
    doc.metadata = {
        "id": str(uuid.uuid4()),
        "document_name": "doc-threshold.pdf",
        "_embedding": [0.1, 0.1, 0.1],
    }
    # Score 0.9 = alta distância = baixa similaridade
    store_impl.similarity_search_with_score_by_vector.return_value = [(doc, 0.9)]

    settings = MockSettings()
    store = PgVectorStore(settings)

    # threshold=0.8 deve filtrar o resultado com similaridade 0.1
    results = store.similarity_search(embedding=[0.1, 0.2, 0.3], k=2, threshold=0.8)

    # Nenhum resultado deve ser retornado — todos abaixo do threshold
    assert results == []


def test_noop_embeddings_methods_raise_not_implemented_error() -> None:
    embeddings = _NoopEmbeddings()

    try:
        embeddings.embed_documents(["a"])
        assert False, "embed_documents deveria lançar NotImplementedError"
    except NotImplementedError:
        pass

    try:
        embeddings.embed_query("a")
        assert False, "embed_query deveria lançar NotImplementedError"
    except NotImplementedError:
        pass


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_similarity_search_fallback_without_score_method(mock_pgvector) -> None:
    class FakeStoreWithoutScore:
        def add_embeddings(self, **kwargs):
            return None

        def similarity_search_by_vector(self, embedding, k):
            doc = MagicMock()
            doc.page_content = "fallback-result"
            doc.metadata = {
                "id": str(uuid.uuid4()),
                "document_name": "fallback.pdf",
                "_embedding": [0.1, 0.2],
                "tag": "fallback",
            }
            return [doc]

    mock_pgvector.return_value = FakeStoreWithoutScore()

    store = PgVectorStore(MockSettings())
    results = store.similarity_search(embedding=[0.1, 0.2], k=1)

    assert len(results) == 1
    assert results[0].content == "fallback-result"
    assert results[0].metadata == {"tag": "fallback"}


@patch("infra.vector_store.pgvector_store.PGVector")
def test_pgvector_store_similarity_search_skips_documents_without_id(mock_pgvector) -> None:
    store_impl = MagicMock()
    mock_pgvector.return_value = store_impl

    doc = MagicMock()
    doc.page_content = "missing-id"
    doc.metadata = {
        "document_name": "doc.pdf",
        "_embedding": [0.1, 0.2],
    }

    store_impl.similarity_search_with_score_by_vector.return_value = [(doc, 0.1)]

    store = PgVectorStore(MockSettings())
    results = store.similarity_search(embedding=[0.1, 0.2], k=1)

    assert results == []
