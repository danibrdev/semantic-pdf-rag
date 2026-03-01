"""
Testes unitários para os adaptadores de embedding do Gemini.

Verifica que o adaptador chama os métodos corretos da integração LangChain
para vetorizar textos individuais e em lote.
"""

from unittest.mock import MagicMock, patch

from infra.embeddings.gemini_embedding import GeminiEmbedding


@patch("infra.embeddings.gemini_embedding.GoogleGenerativeAIEmbeddings")
def test_gemini_embedding_embed(mock_gemini_embeddings) -> None:
    """
    Verifica que embed() chama embed_query() no cliente LangChain
    e retorna o vetor produzido pela API do Gemini.
    """
    # Cria um cliente falso e configura o valor de retorno de embed_query
    client = MagicMock()
    client.embed_query.return_value = [0.5, 0.6, 0.7]
    mock_gemini_embeddings.return_value = client

    adapter = GeminiEmbedding(api_key="key", model="models/text-embedding-004")
    result = adapter.embed("hello")

    assert result == [0.5, 0.6, 0.7]
    # Confirma que embed_query foi chamado com o texto correto
    client.embed_query.assert_called_once_with("hello")


@patch("infra.embeddings.gemini_embedding.GoogleGenerativeAIEmbeddings")
def test_gemini_embedding_embed_batch_empty(mock_gemini_embeddings) -> None:
    """
    Verifica que embed_batch() retorna lista vazia sem chamar a API
    quando recebe uma lista de textos vazia.
    """
    client = MagicMock()
    mock_gemini_embeddings.return_value = client

    adapter = GeminiEmbedding(api_key="key", model="models/text-embedding-004")
    result = adapter.embed_batch([])

    assert result == []
    # embed_documents não deve ser chamado quando não há textos para processar
    client.embed_documents.assert_not_called()


@patch("infra.embeddings.gemini_embedding.GoogleGenerativeAIEmbeddings")
def test_gemini_embedding_embed_batch(mock_gemini_embeddings) -> None:
    """
    Verifica que embed_batch() chama embed_documents() com a lista de textos
    e retorna os vetores correspondentes para cada texto.
    """
    client = MagicMock()
    client.embed_documents.return_value = [[0.9, 0.8], [0.7, 0.6]]
    mock_gemini_embeddings.return_value = client

    adapter = GeminiEmbedding(api_key="key", model="models/text-embedding-004")
    result = adapter.embed_batch(["a", "b"])

    assert result == [[0.9, 0.8], [0.7, 0.6]]
    client.embed_documents.assert_called_once_with(["a", "b"])
