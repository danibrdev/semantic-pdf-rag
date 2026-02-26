import logging
from pathlib import Path
from uuid import uuid4

from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort
from domain.entities.document import DocumentChunk


logger = logging.getLogger(__name__)


class IngestPDFUseCase:
    """
    Application use case responsible for:
    1. Extracting text (placeholder for now)
    2. Chunking (1000 / 200 overlap)
    3. Generating embeddings
    4. Persisting into vector store
    """

    def __init__(
        self,
        pdf_loader: PDFLoaderPort,
        embedding: EmbeddingPort,
        vector_store: VectorStorePort,
    ):
        self.pdf_loader = pdf_loader
        self.embedding = embedding
        self.vector_store = vector_store

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    def execute(self, path: str) -> None:

        logger.info("Iniciando ingestão do arquivo: %s", path)

        text = self.pdf_loader.load(path)

        chunks = self._chunk_text(text)

        logger.info("Total de chunks gerados: %d", len(chunks))

        document_name = Path(path).name

        if not chunks:
            logger.warning("Nenhum texto extraído do PDF.")
            return

        logger.info("Gerando embeddings em lote para %d chunks", len(chunks))
        
        # Call batch embedding
        vectors = self.embedding.embed_batch(chunks)

        logger.info("Salvando chunks no banco vetorial...")
        
        for chunk_text, vector in zip(chunks, vectors):
            chunk = DocumentChunk(
                id=uuid4(),
                document_name=document_name,
                content=chunk_text,
                embedding=vector,
            )

            self.vector_store.save(chunk)

        logger.info("Ingestão concluída com sucesso.")