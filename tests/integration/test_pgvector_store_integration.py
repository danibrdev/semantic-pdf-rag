import uuid
import pytest
import psycopg2

from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore
from infra.config.settings import Settings


def _cleanup_collection(database_url: str, collection_name: str) -> None:
    """
    Remove dados da coleção de testes no schema padrão do `langchain-postgres`.
    Se as tabelas não existirem ainda (primeira execução), ignora silenciosamente.
    """
    conn = psycopg2.connect(database_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM langchain_pg_embedding
                WHERE collection_id IN (
                    SELECT uuid FROM langchain_pg_collection WHERE name = %s
                );
                """,
                (collection_name,),
            )
            cur.execute(
                """
                DELETE FROM langchain_pg_collection
                WHERE name = %s;
                """,
                (collection_name,),
            )
        conn.commit()
    except psycopg2.errors.UndefinedTable:
        # Tabelas ainda não existem (primeira execução), não há nada para limpar
        conn.rollback()
    finally:
        conn.close()


@pytest.fixture(scope="module")
def vector_store():
    settings = Settings(
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )
    _cleanup_collection(settings.database_url, "documents")
    store = PgVectorStore(settings)

    yield store

    _cleanup_collection(settings.database_url, "documents")


def test_integration_pgvector_save_and_search(vector_store):
    settings = vector_store.settings
    emb_dim = settings.embedding_dimension

    chunk_1 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc1.pdf",
        content="Apple is a tech company.",
        embedding=[0.9, 0.1, 0.0] * (emb_dim // 3),
        metadata={"category": "tech", "author": "Steve"}
    )

    chunk_2 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc2.pdf",
        content="Bananas are a great fruit.",
        embedding=[0.0, 0.9, 0.1] * (emb_dim // 3),
        metadata={"category": "food", "author": "Dani"}
    )

    vector_store.save(chunk_1)
    vector_store.save(chunk_2)

    search_vector = [0.8, 0.2, 0.0] * (emb_dim // 3)
    results = vector_store.similarity_search(embedding=search_vector, k=1)

    assert len(results) == 1
    assert results[0].id == chunk_1.id
    assert results[0].content == chunk_1.content
    assert results[0].metadata == {"category": "tech", "author": "Steve"}
