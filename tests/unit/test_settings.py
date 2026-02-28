import pytest

from infra.config.settings import Settings


def test_settings_openai_current_embedding_model_and_dimension():
    settings = Settings(
        provider="openai",
        openai_api_key="key",
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )

    assert settings.current_embedding_model == "text-embedding-3-small"
    assert settings.embedding_dimension == 1536


def test_settings_max_context_tokens_calculation():
    settings = Settings(
        provider="gemini",
        google_api_key="key",
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
        llm_max_tokens=4096,
        response_token_reserve=512,
    )

    assert settings.max_context_tokens == 3584


def test_settings_raises_for_unmapped_embedding_model_dimension():
    settings = Settings(
        provider="openai",
        openai_api_key="key",
        openai_embedding_model="custom-unknown-model",
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )

    with pytest.raises(ValueError, match="Embedding dimension not configured"):
        _ = settings.embedding_dimension


def test_settings_raises_when_openai_provider_has_no_key():
    with pytest.raises(ValueError, match="openai_api_key"):
        Settings(
            provider="openai",
            openai_api_key="",
            database_url="postgresql://rag:rag@localhost:5435/ragdb",
        )


def test_settings_raises_when_gemini_provider_has_no_key():
    with pytest.raises(ValueError, match="google_api_key"):
        Settings(
            provider="gemini",
            google_api_key="",
            database_url="postgresql://rag:rag@localhost:5435/ragdb",
        )
