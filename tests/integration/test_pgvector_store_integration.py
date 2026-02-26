import os
import uuid
import pytest
from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore
from infra.config.settings import Settings


@pytest.fixture(scope="module")
def vector_store():
    settings = Settings(
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )
    
    # Drop table cleanly to prevent dimension mismatch from dirty docker volumes
    import psycopg2
    conn = psycopg2.connect(settings.database_url)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS documents;")
    conn.commit()
    conn.close()
    
    store = PgVectorStore(settings)
    
    yield store

    # Teardown logic
    with store.conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS documents;")
    store.conn.commit()
    store.conn.close()


def test_integration_pgvector_save_and_search(vector_store):
    # 1. Provide an embedding and a chunk
    # Dynamically inject the appropriate dimension based on settings dynamically loaded
    settings = vector_store.settings # Access settings from the store
    emb_dim = settings.embedding_dimension
    
    chunk_1 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc1.pdf",
        content="Apple is a tech company.",
        embedding=[0.9, 0.1, 0.0] * (emb_dim // 3)
    )
    chunk_2 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc2.pdf",
        content="Bananas are a great fruit.",
        embedding=[0.0, 0.9, 0.1] * (emb_dim // 3)
    )
    
    # 2. Save
    vector_store.save(chunk_1)
    vector_store.save(chunk_2)
    
    # 3. Search for a vector close to chunk_1
    search_vector = [0.8, 0.2, 0.0] * (emb_dim // 3)
    results = vector_store.similarity_search(embedding=search_vector, k=1)
    
    assert len(results) == 1
    assert results[0].id == chunk_1.id
    assert results[0].content == chunk_1.content
