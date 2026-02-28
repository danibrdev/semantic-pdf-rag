"""
Adaptador de embeddings para a API da OpenAI.

Implementação concreta de EmbeddingPort usando o SDK oficial da OpenAI.
Comunica-se diretamente com a API de embeddings da OpenAI para vetorizar textos.


"""

from openai import OpenAI
from domain.ports.embedding_port import EmbeddingPort

class OpenAIEmbedding(EmbeddingPort):

    def __init__(self, api_key: str, model: str):
        # Inicializa o cliente oficial da OpenAI com a chave de API fornecida
        self.client = OpenAI(api_key=api_key)
        # Modelo de embedding a ser utilizado (ex: "text-embedding-3-small")
        self.model = model

    def embed(self, text: str):
        """Gera o embedding para um único texto chamando a API da OpenAI."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Gera embeddings para múltiplos textos em uma única chamada à API.
        Mais eficiente que chamar embed() individualmente para cada chunk.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [data.embedding for data in response.data]