"""
Caso de uso: Ingestão de PDF no banco vetorial.

Este é o orquestrador central do pipeline de ingestão. Coordena o fluxo completo:
1. Extração do texto bruto do PDF
2. Divisão do texto em chunks menores
3. Geração de embeddings em lote para todos os chunks
4. Persistência de cada chunk (texto + embedding) no banco vetorial

Segue o princípio da Clean Architecture: depende apenas de Ports (interfaces abstratas),
nunca de implementações concretas como psycopg2, openai, etc.
"""

import logging
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

# RunnableLambda transforma uma função comum do Python em um passo de pipeline do LangChain.
# O operador `|` encadeia esses passos: a saída de um vira entrada do próximo.
from langchain_core.runnables import RunnableLambda

# Importamos os Ports (interfaces abstratas), nunca as implementações concretas.
# Isso significa que este caso de uso não sabe se está usando OpenAI ou Gemini —
# ele apenas chama os métodos definidos na interface.
from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort
from domain.entities.document import DocumentChunk
from infra.loaders.text_chunker import TextChunker


# Logger nomeado com o módulo atual — registra mensagens identificando de onde elas vieram
logger = logging.getLogger(__name__)

class IngestPDFUseCase:
    """
    Caso de uso responsável por ingerir um PDF no banco vetorial.
    Coordena o pipeline completo: load → chunk → embed → save.
    """

    def __init__(
        self,
        pdf_loader: PDFLoaderPort,       # Leitor de PDF (injetado de fora)
        embedding: EmbeddingPort,         # Gerador de embeddings (OpenAI ou Gemini)
        vector_store: VectorStorePort,    # Banco vetorial onde os chunks serão salvos
    ):
        # As dependências são recebidas prontas — padrão de Injeção de Dependência.
        # Este caso de uso não cria nenhuma instância de provedor diretamente.
        self.pdf_loader = pdf_loader
        self.embedding = embedding
        self.vector_store = vector_store

        # O TextChunker divide o texto em pedaços de 1000 caracteres.
        # O overlap de 200 repete os últimos 200 caracteres no início do próximo chunk,
        # para que o contexto nas bordas não seja perdido.
        self.chunker = TextChunker(chunk_size=1000, overlap=200)

    def execute(self, path: str) -> None:
        """
        Executa o pipeline completo de ingestão para o PDF no caminho informado.
        """
        # O operador `|` do LangChain encadeia os passos sequencialmente.
        # Cada passo recebe como entrada a saída do passo anterior.
        ingestion_chain = (
            RunnableLambda(self._load_pdf)
            | RunnableLambda(self._chunk_text)
            | RunnableLambda(self._embed_chunks)
            | RunnableLambda(self._persist_chunks)
        )

        # Inicia o pipeline passando o caminho do arquivo como entrada do primeiro passo
        ingestion_chain.invoke(path)

    def _load_pdf(self, path: str) -> Dict[str, Any]:
        """Carrega o texto bruto do PDF e monta o dicionário que vai trafegar pelo pipeline."""
        logger.info("Iniciando ingestão do arquivo: %s", path)
        text = self.pdf_loader.load(path)

        return {
            "path": path,
            "document_name": Path(path).name,  # Extrai apenas o nome do arquivo, sem o diretório
            "text": text,
        }

    def _chunk_text(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Divide o texto em chunks menores e adiciona a lista ao dicionário do pipeline."""
        chunks = self.chunker.chunk(payload["text"])
        logger.info("Total de chunks gerados: %d", len(chunks))

        if not chunks:
            logger.warning("Nenhum texto extraído do PDF.")

        payload["chunks"] = chunks
        return payload

    def _embed_chunks(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Gera os vetores de embedding para todos os chunks em um único request em lote."""
        chunks = payload.get("chunks", [])
        if not chunks:
            payload["vectors"] = []
            return payload

        logger.info("Gerando embeddings em lote para %d chunks", len(chunks))

        # embed_batch processa todos os textos de uma vez, reduzindo o número de chamadas à API
        payload["vectors"] = self.embedding.embed_batch(chunks)
        return payload

    def _persist_chunks(self, payload: Dict[str, Any]) -> None:
        """Salva cada chunk com seu embedding correspondente no banco vetorial."""
        chunks = payload.get("chunks", [])
        vectors = payload.get("vectors", [])
        document_name = payload["document_name"]

        if not chunks:
            return

        logger.info("Salvando chunks no banco vetorial...")

        # zip() emparelha cada chunk com seu vetor pelo mesmo índice
        for chunk_text, vector in zip(chunks, vectors):
            chunk = DocumentChunk(
                id=uuid4(),               # Gera um identificador único e aleatório para o chunk
                document_name=document_name,
                content=chunk_text,
                embedding=vector,
                metadata={"source": document_name, "type": "pdf_ingestion"},
            )
            self.vector_store.save(chunk)

        logger.info("Ingestão concluída com sucesso.")