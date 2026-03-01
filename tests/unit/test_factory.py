"""
Testes unitários para o infra/factory.py (Composition Root).

Verifica que a factory cria os provedores corretos com base na configuração de `provider`,
e que o container de dependências retorna os componentes esperados.
"""

import pytest

# `patch` substitui temporariamente uma classe ou função por um objeto controlado (Mock)
# durante a execução do teste, isolando o código de dependências externas.
from unittest.mock import patch

from infra.factory import build_dependencies, build_embedding_provider


class FakeSettings:
    """
    Simula o comportamento da classe Settings real.
    Evita que o teste precise de um arquivo .env ou de uma conexão com banco de dados.
    """
    provider = "openai"
    openai_api_key = "test-openai-key"
    google_api_key = "test-google-key"
    openai_embedding_model = "text-embedding-3-small"
    gemini_embedding_model = "models/text-embedding-004"

    @property
    def current_embedding_model(self) -> str:
        """Retorna o modelo do provedor configurado, replicando o comportamento do Settings real."""
        if self.provider == "openai":
            return self.openai_embedding_model
        return self.gemini_embedding_model


@patch("infra.factory.OpenAIEmbedding")
def test_build_embedding_provider_openai(mock_openai_embedding) -> None:
    """
    Verifica que a factory instancia OpenAIEmbedding com a chave e o modelo corretos.
    O @patch substitui OpenAIEmbedding por um Mock durante o teste.
    """
    settings = FakeSettings()
    settings.provider = "openai"

    build_embedding_provider(settings)

    # assert_called_once_with confirma que o Mock foi instanciado exatamente uma vez,
    # com os argumentos esperados
    mock_openai_embedding.assert_called_once_with(
        api_key="test-openai-key",
        model="text-embedding-3-small",
    )


@patch("infra.factory.GeminiEmbedding")
def test_build_embedding_provider_gemini(mock_gemini_embedding) -> None:
    """Verifica que a factory instancia GeminiEmbedding com a chave e o modelo corretos."""
    settings = FakeSettings()
    settings.provider = "gemini"

    build_embedding_provider(settings)

    mock_gemini_embedding.assert_called_once_with(
        api_key="test-google-key",
        model="models/text-embedding-004",
    )


# Quando múltiplos @patch são empilhados, os argumentos aparecem na função
# na ordem inversa — o último @patch vira o primeiro argumento.
@patch("infra.factory.PgVectorStore")
@patch("infra.factory.PDFLoader")
@patch("infra.factory.build_embedding_provider")
def test_build_dependencies_returns_expected_container(
    mock_build_embedding_provider,
    mock_pdf_loader,
    mock_pgvector_store,
) -> None:
    """
    Verifica que build_dependencies retorna um dicionário com as três dependências esperadas.
    """
    settings = FakeSettings()

    # Configura cada Mock para retornar uma string identificável no lugar de uma instância real
    mock_build_embedding_provider.return_value = "embedding_instance"
    mock_pdf_loader.return_value = "pdf_loader_instance"
    mock_pgvector_store.return_value = "vector_store_instance"

    container = build_dependencies(settings)

    assert container == {
        "pdf_loader": "pdf_loader_instance",
        "embedding": "embedding_instance",
        "vector_store": "vector_store_instance",
    }


def test_build_embedding_provider_invalid_provider_raises_error() -> None:
    """
    Verifica que a factory lança ValueError quando o provider configurado é desconhecido.
    """
    settings = FakeSettings()
    settings.provider = "invalid-provider"

    # pytest.raises() verifica que o bloco `with` lança a exceção esperada.
    # match= usa regex para confirmar que a mensagem de erro contém o texto esperado.
    with pytest.raises(ValueError, match="Unsupported provider"):
        build_embedding_provider(settings)
