"""
Testes unitários para os adaptadores de embedding da OpenAI.

Verifica que o adaptador chama os métodos corretos da integração LangChain
para vetorizar textos individuais e em lote.
"""

from unittest.mock import MagicMock, patch

from infra.embeddings.openai_embedding import OpenAIEmbedding


@patch("infra.embeddings.openai_embedding.OpenAIEmbeddings")
def test_openai_embedding_embed(mock_openai_embeddings) -> None:
    """
    Verifica que embed() chama embed_query() no cliente LangChain
    e retorna o vetor produzido pela API da OpenAI.
    """
    # Cria um cliente falso e configura o valor de retorno de embed_query
    client = MagicMock()
    client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_openai_embeddings.return_value = client

    adapter = OpenAIEmbedding(api_key="key", model="text-embedding-3-small")
    result = adapter.embed("hello")

    assert result == [0.1, 0.2, 0.3]
    # Confirma que embed_query foi chamado com o texto correto
    client.embed_query.assert_called_once_with("hello")


@patch("infra.embeddings.openai_embedding.OpenAIEmbeddings")
def test_openai_embedding_embed_batch_empty(mock_openai_embeddings) -> None:
    """
    Verifica que embed_batch() retorna lista vazia sem chamar a API
    quando recebe uma lista de textos vazia.
    """
    client = MagicMock()
    mock_openai_embeddings.return_value = client

    adapter = OpenAIEmbedding(api_key="key", model="text-embedding-3-small")
    result = adapter.embed_batch([])

    assert result == []
    # embed_documents não deve ser chamado quando não há textos para processar
    client.embed_documents.assert_not_called()


@patch("infra.embeddings.openai_embedding.OpenAIEmbeddings")
def test_openai_embedding_embed_batch(mock_openai_embeddings) -> None:
    """
    Verifica que embed_batch() chama embed_documents() com a lista de textos
    e retorna os vetores correspondentes para cada texto.
    """
    client = MagicMock()
    client.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]
    mock_openai_embeddings.return_value = client

    adapter = OpenAIEmbedding(api_key="key", model="text-embedding-3-small")
    result = adapter.embed_batch(["a", "b"])

    assert result == [[0.1, 0.2], [0.3, 0.4]]
    client.embed_documents.assert_called_once_with(["a", "b"])
