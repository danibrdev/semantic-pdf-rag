"""
Testes unitários para infra/config/settings.py.

Verifica o comportamento das propriedades calculadas e das validações do Pydantic Settings:
- Seleção correta do modelo de embedding por provedor
- Cálculo do orçamento de tokens disponível
- Erro para modelo de embedding sem dimensão mapeada
- Erro para provedor sem chave de API configurada
"""

import pytest
from infra.config.settings import Settings


def test_settings_openai_current_embedding_model_and_dimension() -> None:
    """
    Verifica que, ao configurar o provider como 'openai',
    o modelo e a dimensão de embedding retornados são os corretos.

    O Pydantic permite instanciar Settings passando os valores diretamente,
    sem precisar de um arquivo .env.
    """
    settings = Settings(
        provider="openai",
        openai_api_key="key",
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )

    # current_embedding_model é uma @property que retorna o modelo do provedor ativo
    assert settings.current_embedding_model == "text-embedding-3-small"

    # embedding_dimension é uma @property que consulta o dicionário EMBEDDING_DIMENSIONS
    assert settings.embedding_dimension == 1536


def test_settings_max_context_tokens_calculation() -> None:
    """
    Verifica que o orçamento de tokens para o contexto é calculado corretamente.
    Fórmula: max_context_tokens = llm_max_tokens - response_token_reserve
    Esperado: 4096 - 512 = 3584 tokens disponíveis para os chunks do contexto.
    """
    settings = Settings(
        provider="gemini",
        google_api_key="key",
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
        llm_max_tokens=4096,
        response_token_reserve=512,
    )

    assert settings.max_context_tokens == 3584


def test_settings_raises_for_unmapped_embedding_model_dimension() -> None:
    """
    Verifica que Settings lança ValueError ao tentar obter a dimensão
    de um modelo que não está mapeado em EMBEDDING_DIMENSIONS.
    """
    settings = Settings(
        provider="openai",
        openai_api_key="key",
        openai_embedding_model="custom-unknown-model",  # Modelo fora do mapa
        database_url="postgresql://rag:rag@localhost:5435/ragdb",
    )

    # O erro é lançado ao acessar a @property, não na criação do objeto Settings
    with pytest.raises(ValueError, match="Embedding dimension not configured"):
        _ = settings.embedding_dimension


def test_settings_raises_when_openai_provider_has_no_key() -> None:
    """
    Verifica que o @model_validator do Pydantic rejeita a configuração
    quando o provider 'openai' é selecionado sem a chave de API.
    O validator é executado automaticamente após a criação do objeto.
    """
    with pytest.raises(ValueError, match="openai_api_key"):
        Settings(
            provider="openai",
            openai_api_key="",  # Chave vazia — rejeitada pelo validator
            database_url="postgresql://rag:rag@localhost:5435/ragdb",
        )


def test_settings_raises_when_gemini_provider_has_no_key() -> None:
    """
    Verifica que o @model_validator rejeita a configuração
    quando o provider 'gemini' é selecionado sem a chave do Google.
    """
    with pytest.raises(ValueError, match="google_api_key"):
        Settings(
            provider="gemini",
            google_api_key="",  # Chave vazia — rejeitada pelo validator
            database_url="postgresql://rag:rag@localhost:5435/ragdb",
        )
