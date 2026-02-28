"""
Adaptador de armazenamento vetorial usando PostgreSQL + pgVector.

Implementação concreta de VectorStorePort que conecta ao PostgreSQL com a extensão pgVector.
Responsável por:
- Criar automaticamente a tabela `documents` e o índice HNSW na inicialização
- Persistir chunks (texto + embedding) no banco
- Buscar chunks por similaridade de cosseno usando o operador HNSW

O índice HNSW (Hierarchical Navigable Small World) oferece buscas de vizinhos
mais próximos aproximados de forma muito eficiente, mesmo com grandes volumes de dados.

"""

from typing import List, Optional
import psycopg2
from pgvector.psycopg2 import register_vector
from domain.ports.vector_store_port import VectorStorePort
from domain.entities.document import DocumentChunk
from infra.config.settings import Settings


class PgVectorStore(VectorStorePort):
    """
    Implementação do VectorStorePort usando PostgreSQL + pgVector.
    Responsável APENAS por persistência — sem lógica de negócio.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        # Abre a conexão com o banco usando a URL configurada no Settings
        self.conn = psycopg2.connect(settings.database_url)
        # Registra o tipo `vector` do pgVector na conexão para operações com embeddings
        register_vector(self.conn)
        # Garante que a tabela e o índice existem antes de qualquer operação
        self._ensure_table()

    def _ensure_table(self) -> None:
        """
        Cria a tabela `documents` e o índice HNSW se ainda não existirem.
        A dimensão do vetor é definida dinamicamente pelo Settings.
        """
        with self.conn.cursor() as cur:
            # Garante que a extensão pgVector está habilitada no banco
            cur.execute(
                """
                CREATE EXTENSION IF NOT EXISTS vector;
                """
            )

            # Cria a tabela de documentos com coluna de embedding vetorial
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id UUID PRIMARY KEY,
                    document_name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({self.settings.embedding_dimension}),
                    metadata JSONB DEFAULT '{{}}'::jsonb
                );
                """
            )

            # Cria o índice HNSW para buscas por similaridade de cosseno de alta performance
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx
                ON documents
                USING hnsw (embedding vector_cosine_ops);
                """
            )

            self.conn.commit()

    def save(self, chunk: DocumentChunk) -> None:
        """
        Persiste um DocumentChunk no banco. Usa ON CONFLICT DO NOTHING para
        evitar duplicatas caso o mesmo chunk seja inserido mais de uma vez.
        """
        import json
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (id, document_name, content, embedding, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (str(chunk.id), chunk.document_name, chunk.content, chunk.embedding, json.dumps(chunk.metadata)),
            )
            self.conn.commit()

    def similarity_search(
        self,
        embedding: List[float],
        k: int,
        threshold: Optional[float] = None,
    ) -> List[DocumentChunk]:
        """
        Busca os k chunks mais similares ao embedding fornecido usando distância coseno.
        O operador `<->` do pgVector calcula a distância — ordem ascendente = mais similar primeiro.
        Converte as linhas retornadas do banco em entidades de domínio (DocumentChunk).
        """
        with self.conn.cursor() as cur:
            if threshold is None:
                cur.execute(
                    """
                    SELECT id, document_name, content, embedding, metadata
                    FROM documents
                    ORDER BY embedding <-> %s::vector
                    LIMIT %s;
                    """,
                    (embedding, k),
                )
            else:
                # Para cosine distance: similaridade mínima (0..1) vira distância máxima (1 - similarity).
                max_distance = max(0.0, min(1.0, 1.0 - threshold))
                cur.execute(
                    """
                    SELECT id, document_name, content, embedding, metadata
                    FROM documents
                    WHERE embedding <-> %s::vector <= %s
                    ORDER BY embedding <-> %s::vector
                    LIMIT %s;
                    """,
                    (embedding, max_distance, embedding, k),
                )

            rows = cur.fetchall()

        # Converte cada linha do banco em uma entidade de domínio DocumentChunk
        return [
            DocumentChunk(
                id=row[0],
                document_name=row[1],
                content=row[2],
                embedding=row[3],
                metadata=row[4] if row[4] else {}
            )
            for row in rows
        ]