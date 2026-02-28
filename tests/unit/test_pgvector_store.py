"""
Testes unitários para o PgVectorStore.

Verifica o comportamento do adaptador de banco vetorial sem depender de uma
instância real do PostgreSQL. Usa `unittest.mock.patch` e `MagicMock` para
simular a conexão com o banco (`psycopg2`) e verificar as chamadas realizadas.

Cobre:
- Inicialização e criação de tabela/índice
- Persistência de chunks (save)
- Busca por similaridade (similarity_search)
"""

import uuid
from unittest.mock import MagicMock, patch
from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore


class MockSettings:
    """Settings falso para isolar os testes das variáveis de ambiente reais."""
    database_url = "postgresql://user:pass@localhost:5432/db"
    embedding_dimension = 1536


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_initialization(mock_register_vector, mock_psycopg2):
    """
    Verifica que na inicialização do PgVectorStore:
    - A conexão com o banco é aberta com a URL correta
    - O tipo vector é registrado na conexão
    - A lógica de criação de tabela (cursor + commit) é executada
    """
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    settings = MockSettings()
    store = PgVectorStore(settings)

    mock_psycopg2.connect.assert_called_once_with(settings.database_url)
    mock_register_vector.assert_called_once_with(mock_conn)

    # Garante que a lógica de criação de tabela foi executada (cursor aberto e commit chamado)
    mock_conn.cursor.assert_called()
    mock_conn.commit.assert_called()


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_save(mock_register_vector, mock_psycopg2):
    """
    Verifica que o método save() abre um cursor e faz commit ao persistir um chunk.
    """
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    settings = MockSettings()
    store = PgVectorStore(settings)

    # Reseta os mocks para ignorar as chamadas feitas durante a inicialização (_ensure_table)
    mock_conn.cursor.reset_mock()
    mock_conn.commit.reset_mock()

    # Cria um chunk de teste com dados mínimos
    chunk = DocumentChunk(
        id=uuid.uuid4(),
        document_name="test.pdf",
        content="Test content",
        embedding=[0.1, 0.2, 0.3]
    )

    store.save(chunk)

    # Verifica que um cursor foi aberto e o commit foi chamado exatamente uma vez
    mock_conn.cursor.assert_called()
    mock_conn.commit.assert_called_once()


@patch("infra.vector_store.pgvector_store.psycopg2")
@patch("infra.vector_store.pgvector_store.register_vector")
def test_pgvector_store_similarity_search(mock_register_vector, mock_psycopg2):
    """
    Verifica que o método similarity_search() converte corretamente as linhas
    retornadas pelo banco em entidades de domínio (DocumentChunk).
    """
    mock_conn = MagicMock()
    mock_psycopg2.connect.return_value = mock_conn

    mock_cursor = MagicMock()
    # Simula as linhas retornadas pelo cursor do banco: (id, document_name, content, embedding, metadata)
    mock_id_1 = uuid.uuid4()
    mock_id_2 = uuid.uuid4()
    mock_cursor.fetchall.return_value = [
        (mock_id_1, "doc-a.pdf", "Result 1", [0.1, 0.2, 0.3], {"author": "Dani"}),
        (mock_id_2, "doc-b.pdf", "Result 2", [0.4, 0.5, 0.6], {"author": "Steve"}),
    ]

    # Configura o context manager do cursor para retornar o cursor mockado
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    settings = MockSettings()
    store = PgVectorStore(settings)

    search_embedding = [0.1, 0.2, 0.3]
    results = store.similarity_search(embedding=search_embedding, k=2)

    # Verifica que retornou exatamente 2 resultados como DocumentChunk
    assert len(results) == 2
    assert results[0].id == mock_id_1
    assert results[0].document_name == "doc-a.pdf"
    assert results[0].content == "Result 1"
    assert results[0].embedding == [0.1, 0.2, 0.3]
    assert results[0].metadata == {"author": "Dani"}

    assert results[1].id == mock_id_2
    assert results[1].document_name == "doc-b.pdf"
    assert results[1].content == "Result 2"
    assert results[1].embedding == [0.4, 0.5, 0.6]
    assert results[1].metadata == {"author": "Steve"}
