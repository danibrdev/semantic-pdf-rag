"""
Composition Root — Factory de dependências da aplicação.

Este módulo é o único lugar do sistema onde as implementações concretas são instanciadas.
Decide em tempo de execução qual provedor usar (OpenAI ou Gemini) e cria todas
as dependências necessárias, entregando-as como um dicionário para o restante do sistema.
"""

from infra.config.settings import Settings
from infra.embeddings.openai_embedding import OpenAIEmbedding
from infra.embeddings.gemini_embedding import GeminiEmbedding
from infra.loaders.pdf_loader import PDFLoader
from infra.vector_store.pgvector_store import PgVectorStore


def build_embedding_provider(settings: Settings):
    """
    Cria e retorna o provedor de embeddings correto com base no campo `provider` do .env.
    Suporta "openai" e "gemini".
    """
    # current_embedding_model é uma @property do Settings que retorna o modelo do provedor ativo
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

    # Se o provider configurado não for reconhecido, o sistema falha imediatamente
    # com uma mensagem clara identificando o valor inválido
    raise ValueError(f"Unsupported provider: {settings.provider}")


def build_dependencies(settings: Settings) -> dict:
    """
    Cria todas as dependências concretas da aplicação e as retorna em um dicionário.
    O dicionário funciona como um container de dependências para a CLI e os casos de uso.
    """
    embedding = build_embedding_provider(settings)
    pdf_loader = PDFLoader()
    vector_store = PgVectorStore(settings)

    return {
        "pdf_loader": pdf_loader,
        "embedding": embedding,
        "vector_store": vector_store,
    }