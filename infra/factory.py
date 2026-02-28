"""
Composition Root — Factory de dependências da aplicação.

Este módulo é o único lugar do sistema onde implementações concretas são instanciadas.
Decide em runtime qual provedor usar (OpenAI ou Gemini) e cria todas as dependências
necessárias para o funcionamento do sistema, entregando-as via dicionário.

Seguindo o princípio da Clean Architecture, o restante do sistema (core, cli)
nunca instancia dependências diretamente — recebe-as prontas deste factory.
"""

from infra.config.settings import Settings
from infra.embeddings.openai_embedding import OpenAIEmbedding
from infra.embeddings.gemini_embedding import GeminiEmbedding
from infra.loaders.pdf_loader import PDFLoader
from infra.vector_store.pgvector_store import PgVectorStore


def build_embedding_provider(settings: Settings):
    """
    Cria e retorna o provedor de embeddings correto com base no `provider` configurado no .env.
    Suporta: "openai" → OpenAIEmbedding | "gemini" → GeminiEmbedding.
    """

    model = settings.current_embedding_model

    if settings.provider == "openai":
        return OpenAIEmbedding(
            api_key=settings.openai_api_key,
            model=model,
        )

    if settings.provider == "gemini":
        return GeminiEmbedding(
            api_key=settings.google_api_key,
            model=model,
        )

    raise ValueError(f"Unsupported provider: {settings.provider}")


def build_dependencies(settings: Settings):
    """
    Monta e retorna todas as dependências concretas da aplicação em um dicionário.
    Ponto central de injeção de dependências (Dependency Injection Manual).
    """

    embedding = build_embedding_provider(settings)
    pdf_loader = PDFLoader()
    vector_store = PgVectorStore(settings)

    return {
        "pdf_loader": pdf_loader,
        "embedding": embedding,
        "vector_store": vector_store,
    }