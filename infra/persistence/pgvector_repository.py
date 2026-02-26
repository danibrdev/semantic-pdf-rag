import psycopg2
from domain.entities.document import DocumentChunk
import os

class PGVectorRepository:

    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    def save(self, chunk: DocumentChunk):
        with self.conn.cursor() as cur:
            cur.execute(
            """
                INSERT INTO document_chunks (id, document_name, content, embedding)
                VALUES (%s, %s, %s, %s)
            """, (
                str(chunk.id),
                chunk.document_name,
                chunk.content,
                chunk.embedding
            ))
        self.conn.commit()