from unittest.mock import patch

from infra.factory import build_dependencies, build_embedding_provider


class FakeSettings:
    provider = "openai"
    openai_api_key = "test-openai-key"
    google_api_key = "test-google-key"
    openai_embedding_model = "text-embedding-3-small"
    gemini_embedding_model = "models/text-embedding-004"

    @property
    def current_embedding_model(self):
        if self.provider == "openai":
            return self.openai_embedding_model
        return self.gemini_embedding_model


@patch("infra.factory.OpenAIEmbedding")
def test_build_embedding_provider_openai(mock_openai_embedding):
    settings = FakeSettings()
    settings.provider = "openai"

    build_embedding_provider(settings)

    mock_openai_embedding.assert_called_once_with(
        api_key="test-openai-key",
        model="text-embedding-3-small",
    )


@patch("infra.factory.GeminiEmbedding")
def test_build_embedding_provider_gemini(mock_gemini_embedding):
    settings = FakeSettings()
    settings.provider = "gemini"

    build_embedding_provider(settings)

    mock_gemini_embedding.assert_called_once_with(
        api_key="test-google-key",
        model="models/text-embedding-004",
    )


@patch("infra.factory.PgVectorStore")
@patch("infra.factory.PDFLoader")
@patch("infra.factory.build_embedding_provider")
def test_build_dependencies_returns_expected_container(
    mock_build_embedding_provider,
    mock_pdf_loader,
    mock_pgvector_store,
):
    settings = FakeSettings()

    mock_build_embedding_provider.return_value = "embedding_instance"
    mock_pdf_loader.return_value = "pdf_loader_instance"
    mock_pgvector_store.return_value = "vector_store_instance"

    container = build_dependencies(settings)

    assert container == {
        "pdf_loader": "pdf_loader_instance",
        "embedding": "embedding_instance",
        "vector_store": "vector_store_instance",
    }
