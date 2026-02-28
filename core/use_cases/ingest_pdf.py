"""
Caso de uso: Ingestão de PDF no banco vetorial.

Este é o orquestrador central do pipeline de ingestão. Coordena o fluxo completo:
1. Extração do texto bruto do PDF
2. Divisão do texto em chunks menores
3. Geração de embeddings em lote para todos os chunks
4. Persistência de cada chunk (texto + embedding) no banco vetorial

Segue o princípio da Clean Architecture: depende apenas de Ports (interfaces),
nunca de implementações concretas (psycopg2, openai, etc.).
"""

import logging
from pathlib import Path
from uuid import uuid4

from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort
from domain.entities.document import DocumentChunk
from infra.loaders.text_chunker import TextChunker


logger = logging.getLogger(__name__)

class IngestPDFUseCase:
    """
    Caso de uso responsável por ingerir um PDF no banco vetorial.
    Coordena o pipeline completo: load → chunk → embed → save.
    """

    def __init__(
        self,
        pdf_loader: PDFLoaderPort,       # Provedor de leitura de PDF (injetado via DI)
        embedding: EmbeddingPort,         # Provedor de embeddings (OpenAI ou Gemini)
        vector_store: VectorStorePort,    # Banco vetorial (PgVector ou outro)
    ):
        self.pdf_loader = pdf_loader
        self.embedding = embedding
        self.vector_store = vector_store
        # Chunker com tamanho de 1000 caracteres e sobreposição de 200 para preservar contexto
        self.chunker = TextChunker(chunk_size=1000, overlap=200)

    def execute(self, path: str) -> None:
        """
        Executa o pipeline completo de ingestão para o PDF no caminho informado.
        """

        logger.info("Iniciando ingestão do arquivo: %s", path)

        # Passo 1: Extrai o texto completo do PDF
        text = self.pdf_loader.load(path)

        # Passo 2: Divide o texto em chunks menores com sobreposição
        chunks = self.chunker.chunk(text)

        logger.info("Total de chunks gerados: %d", len(chunks))

        # Usa o nome do arquivo como identificador do documento
        document_name = Path(path).name

        if not chunks:
            logger.warning("Nenhum texto extraído do PDF.")
            return

        logger.info("Gerando embeddings em lote para %d chunks", len(chunks))

        # Passo 3: Gera todos os embeddings em uma única chamada em lote (mais eficiente)
        vectors = self.embedding.embed_batch(chunks)

        logger.info("Salvando chunks no banco vetorial...")

        # Passo 4: Persiste cada par (chunk, embedding) como um DocumentChunk no banco
        for chunk_text, vector in zip(chunks, vectors):
            chunk = DocumentChunk(
                id=uuid4(),
                document_name=document_name,
                content=chunk_text,
                embedding=vector,
                metadata={"source": document_name, "type": "pdf_ingestion"}
            )

            self.vector_store.save(chunk)

        logger.info("Ingestão concluída com sucesso.")