# Implementação de factory para criação de embeddings. Lê as configurações do arquivo .env e cria a implementação concreta de acordo com o provider selecionado
from infra.config.settings import Settings
from infra.embeddings.openai_embedding import OpenAIEmbedding
from infra.embeddings.gemini_embedding import GeminiEmbedding
from infra.loaders.pdf_loader import PDFLoader
from infra.vector_store.pgvector_store import PgVectorStore


def get_embedding_provider():

    if Settings.provider == "openai":
        if not Settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        return OpenAIEmbedding(
            api_key=Settings.openai_api_key,
            model=Settings.openai_embedding_model
        )

    if Settings.provider == "gemini":
        if not Settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not configured")

        return GeminiEmbedding(
            api_key=Settings.google_api_key,
            model=Settings.gemini_embedding_model
        )

    raise ValueError("Invalid provider")

# Composition Root / Dependency Builder
# Responsible for instantiating concrete implementations
# based on validated Settings

def build_embedding_provider(settings: Settings):
    """
    Builds the embedding provider based on the configured provider.
    Assumes Settings validation has already been executed.
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
    Centralized dependency builder.
    Future-proof for adding LLM, VectorStore, TokenOptimizer, etc.
    """

    embedding = build_embedding_provider(settings)
    pdf_loader = PDFLoader()
    vector_store = PgVectorStore(settings)

    return {
        "pdf_loader": pdf_loader,
        "embedding": embedding,
        "vector_store": vector_store,
    }