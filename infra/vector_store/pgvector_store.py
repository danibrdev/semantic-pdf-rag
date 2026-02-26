

from typing import List
import psycopg2
from pgvector.psycopg2 import register_vector
from domain.ports.vector_store_port import VectorStorePort
from domain.entities.document import DocumentChunk
from infra.config.settings import Settings


class PgVectorStore(VectorStorePort):
    """
    PostgreSQL + pgVector implementation of VectorStorePort.
    Responsible ONLY for persistence concerns.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.conn = psycopg2.connect(settings.database_url)
        register_vector(self.conn)
        self._ensure_table()

    def _ensure_table(self) -> None:
        """
        Creates table if it does not exist.
        Embedding dimension is dynamically defined by Settings.
        Also ensures pgvector extension and HNSW index exist.
        """
        with self.conn.cursor() as cur:
            # Ensure pgvector extension exists
            cur.execute(
                """
                CREATE EXTENSION IF NOT EXISTS vector;
                """
            )

            # Create table
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id UUID PRIMARY KEY,
                    document_name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({self.settings.embedding_dimension})
                );
                """
            )

            # Create HNSW index for cosine similarity
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
        Persists a document chunk.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (id, document_name, content, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (str(chunk.id), chunk.document_name, chunk.content, chunk.embedding),
            )
            self.conn.commit()

    def similarity_search(
        self,
        embedding: List[float],
        k: int,
    ) -> List[DocumentChunk]:
        """
        Returns the k most similar chunks as domain entities.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, document_name, content, embedding
                FROM documents
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
                """,
                (embedding, k),
            )

            rows = cur.fetchall()

        # Convert raw DB rows into domain entities
        return [
            DocumentChunk(
                id=row[0],
                document_name=row[1],
                content=row[2],
                embedding=row[3],
            )
            for row in rows
        ]