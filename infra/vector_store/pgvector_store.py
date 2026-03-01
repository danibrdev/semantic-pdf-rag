"""
Adaptador de armazenamento vetorial usando `langchain-postgres`.

Implementa o `VectorStorePort` delegando persistência e busca vetorial para o `PGVector`,
evitando SQL manual e mantendo a integração dentro do ecossistema LangChain.
"""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

# Document representa um trecho de texto com metadados no LangChain
from langchain_core.documents import Document
# Embeddings é a interface base do LangChain para qualquer provedor de vetorização
from langchain_core.embeddings import Embeddings
# PGVector é a integração do LangChain com o PostgreSQL usando a extensão pgvector
from langchain_postgres import PGVector

from domain.entities.document import DocumentChunk
from domain.ports.vector_store_port import VectorStorePort
from infra.config.settings import Settings


class _NoopEmbeddings(Embeddings):
    """
    Implementação mínima de Embeddings exigida pela interface do PGVector.

    O PGVector do LangChain exige um objeto `Embeddings` no construtor, mas neste projeto
    os vetores já chegam calculados pelo EmbeddingPort antes de chegar ao store.
    As operações de escrita e busca usam vetores explícitos (`add_embeddings` e
    `similarity_search_by_vector`), então este objeto nunca é chamado de fato.

    O prefixo `_` indica que esta classe é interna ao módulo e não deve ser usada de fora.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError("Use add_embeddings com vetores já calculados.")

    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError("Use similarity_search com vetor já calculado.")


class PgVectorStore(VectorStorePort):
    """Implementação de store vetorial baseada em `PGVector` do LangChain."""

    def __init__(self, settings: Settings):
        self.settings = settings
        # Nome da coleção (tabela) onde os chunks serão armazenados no banco
        self.collection_name = "documents"

        # Inicializa o PGVector com a string de conexão e o nome da coleção.
        # use_jsonb=True armazena os metadados como JSONB no PostgreSQL,
        # o que permite buscas eficientes dentro dos campos de metadados.
        self.store = PGVector(
            embeddings=_NoopEmbeddings(),
            connection=settings.database_url,
            collection_name=self.collection_name,
            use_jsonb=True,
        )

    def save(self, chunk: DocumentChunk) -> None:
        """Persiste um chunk (texto + embedding) no banco vetorial."""

        # Cria uma cópia dos metadados para não modificar o objeto original
        metadata: Dict[str, Any] = dict(chunk.metadata)

        # Adiciona campos de identificação nos metadados para recuperação posterior
        metadata["id"] = str(chunk.id)
        metadata["document_name"] = chunk.document_name
        metadata["_embedding"] = chunk.embedding  # Armazena o vetor para reconstruir o chunk na leitura

        # add_embeddings recebe vetores já calculados (não chama o _NoopEmbeddings)
        self.store.add_embeddings(
            texts=[chunk.content],
            embeddings=[chunk.embedding],
            metadatas=[metadata],
            ids=[str(chunk.id)],
        )

    def similarity_search(
        self,
        embedding: List[float],
        k: int,
        threshold: Optional[float] = None,
    ) -> List[DocumentChunk]:
        """
        Busca os k chunks mais similares ao vetor fornecido e os retorna como entidades de domínio.
        Se threshold for informado, descarta resultados com similaridade abaixo do valor mínimo.
        """
        docs_with_scores: List[Tuple[Document, float]] = []

        # Algumas versões do langchain-postgres possuem o método com score, outras não.
        # Verificamos se ele existe antes de chamar para garantir compatibilidade.
        if hasattr(self.store, "similarity_search_with_score_by_vector"):
            docs_with_scores = self.store.similarity_search_with_score_by_vector(
                embedding=embedding,
                k=k,
            )
        else:
            # Fallback para versões sem suporte a score: atribui 0.0 como distância
            docs = self.store.similarity_search_by_vector(
                embedding=embedding,
                k=k,
            )
            docs_with_scores = [(doc, 0.0) for doc in docs]

        results: List[DocumentChunk] = []
        for doc, distance_score in docs_with_scores:
            # O PGVector retorna distância (0 = idêntico). Convertemos para similaridade (1 = idêntico):
            # similaridade = 1 - distância. max/min garantem o resultado entre 0.0 e 1.0.
            similarity_score = max(0.0, min(1.0, 1.0 - float(distance_score)))

            # Descarta o chunk se a similaridade for menor que o limiar configurado
            if threshold is not None and similarity_score < threshold:
                continue

            # Separa os campos internos dos metadados para montar o DocumentChunk
            metadata = dict(doc.metadata or {})
            chunk_id = metadata.pop("id", None)                     # Remove e captura o id
            document_name = metadata.pop("document_name", "unknown")  # Remove e captura o nome
            stored_embedding = metadata.pop("_embedding", [])        # Remove e captura o embedding

            # Chunk sem id não pode ser reconstruído — pula para o próximo
            if chunk_id is None:
                continue

            results.append(
                DocumentChunk(
                    id=UUID(str(chunk_id)),             # Converte string de volta para UUID
                    document_name=str(document_name),
                    content=doc.page_content,           # Texto principal do documento LangChain
                    embedding=stored_embedding,
                    metadata=metadata,                  # Metadados restantes (sem os campos internos)
                )
            )

        return results