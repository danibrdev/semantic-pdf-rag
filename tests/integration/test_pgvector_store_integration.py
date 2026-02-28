"""
Teste de integração para o PgVectorStore.

Diferente dos testes unitários, este teste se conecta a uma instância REAL do PostgreSQL
com a extensão pgVector instalada (disponível via Docker Compose).

O que é testado:
- Criação automática da tabela `documents` e do índice HNSW
- Persistência de dois DocumentChunks com embeddings distintos
- Busca por similaridade de cosseno: verifica que o chunk mais próximo ao vetor de busca é retornado

ATENÇÃO: Este teste requer que o Docker Compose esteja em execução.
Execute `docker compose up -d` antes de rodar este teste.
"""

import os
import uuid
import pytest
from domain.entities.document import DocumentChunk
from infra.vector_store.pgvector_store import PgVectorStore
from infra.config.settings import Settings


@pytest.fixture(scope="module")
def vector_store():
    """
    Fixture de integração: cria uma instância real do PgVectorStore conectando ao banco Docker.
    Antes de criar o store, dropa a tabela `documents` para garantir ambiente limpo
    e evitar erros de incompatibilidade de dimensão de vetores de volumes anteriores.
    Após todos os testes do módulo, dropa a tabela novamente e fecha a conexão (teardown).
    """
    settings = Settings(
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )

    # Limpa o banco antes de cada sessão de testes para evitar conflito de dimensões
    import psycopg2
    conn = psycopg2.connect(settings.database_url)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS documents;")
    conn.commit()
    conn.close()

    # Cria o store real — isso vai recriar a tabela e o índice HNSW automaticamente
    store = PgVectorStore(settings)

    yield store  # Entrega o store para os testes

    # Teardown: limpa a tabela e fecha a conexão após todos os testes do módulo
    with store.conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS documents;")
    store.conn.commit()
    store.conn.close()


def test_integration_pgvector_save_and_search(vector_store):
    """
    Verifica o ciclo completo de ingestão e busca no banco real:
    1. Salva dois chunks com embeddings distintos
    2. Realiza busca com vetor próximo ao chunk_1
    3. Verifica que o resultado retornado é o chunk_1 com metadados corretos
    """
    # Obtém a dimensão de embedding do model configurado para criar vetores válidos
    settings = vector_store.settings
    emb_dim = settings.embedding_dimension

    # Chunk 1: representa um documento de tecnologia (vetor próximo de [0.9, 0.1, 0.0])
    chunk_1 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc1.pdf",
        content="Apple is a tech company.",
        embedding=[0.9, 0.1, 0.0] * (emb_dim // 3),
        metadata={"category": "tech", "author": "Steve"}
    )

    # Chunk 2: representa um documento de alimentação (vetor próximo de [0.0, 0.9, 0.1])
    chunk_2 = DocumentChunk(
        id=uuid.uuid4(),
        document_name="doc2.pdf",
        content="Bananas are a great fruit.",
        embedding=[0.0, 0.9, 0.1] * (emb_dim // 3),
        metadata={"category": "food", "author": "Dani"}
    )

    # Salva ambos os chunks no banco real
    vector_store.save(chunk_1)
    vector_store.save(chunk_2)

    # Busca com vetor próximo ao chunk_1 (tecnologia) — deve retornar chunk_1
    search_vector = [0.8, 0.2, 0.0] * (emb_dim // 3)
    results = vector_store.similarity_search(embedding=search_vector, k=1)

    # Verifica que apenas um resultado foi retornado e que é o chunk correto
    assert len(results) == 1
    assert results[0].id == chunk_1.id
    assert results[0].content == chunk_1.content
    assert results[0].metadata == {"category": "tech", "author": "Steve"}
