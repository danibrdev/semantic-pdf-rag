import uuid
from unittest.mock import MagicMock, patch
from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore


class MockSettings:
    database_url = "postgresql://user:pass@localhost:5432/db"
    embedding_dimension = 1536


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_initialization(mock_register_vector, mock_psycopg2):
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    settings = MockSettings()
    store = PgVectorStore(settings)

    mock_psycopg2.connect.assert_called_once_with(settings.database_url)
    mock_register_vector.assert_called_once_with(mock_conn)

    # Ensure table creation logic was executed
    mock_conn.cursor.assert_called()
    mock_conn.commit.assert_called()


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_save(mock_register_vector, mock_psycopg2):
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    settings = MockSettings()
    store = PgVectorStore(settings)

    # Reset calls made during init
    mock_conn.cursor.reset_mock()
    mock_conn.commit.reset_mock()

    chunk = DocumentChunk(
        id=uuid.uuid4(),
        document_name="test.pdf",
        content="Test content",
        embedding=[0.1, 0.2, 0.3]
    )

    store.save(chunk)

    mock_conn.cursor.assert_called()
    mock_conn.commit.assert_called_once()


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_similarity_search(mock_register_vector, mock_psycopg2):
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    mock_cursor = MagicMock()
    # Mocking rows returned by fetchall: (id, document_name, content, embedding)
    mock_id_1 = uuid.uuid4()
    mock_id_2 = uuid.uuid4()
    mock_cursor.fetchall.return_value = [
        (mock_id_1, "doc-a.pdf", "Result 1", [0.1, 0.2, 0.3]),
        (mock_id_2, "doc-b.pdf", "Result 2", [0.4, 0.5, 0.6]),
    ]

    # cursor context manager
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    settings = MockSettings()
    store = PgVectorStore(settings)

    search_embedding = [0.1, 0.2, 0.3]
    results = store.similarity_search(embedding=search_embedding, k=2)

    assert len(results) == 2
    assert results[0].id == mock_id_1
    assert results[0].document_name == "doc-a.pdf"
    assert results[0].content == "Result 1"
    assert results[0].embedding == [0.1, 0.2, 0.3]

    assert results[1].id == mock_id_2
    assert results[1].document_name == "doc-b.pdf"
    assert results[1].content == "Result 2"
    assert results[1].embedding == [0.4, 0.5, 0.6]
