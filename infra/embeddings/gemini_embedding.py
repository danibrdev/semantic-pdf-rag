"""
Adaptador de embeddings para a API do Google Gemini.

Implementação concreta de EmbeddingPort usando o SDK oficial do Google Generative AI.
Comunica-se diretamente com a API de embeddings do Gemini para vetorizar textos.
Suporta tanto a geração de embeddings para um único texto quanto em lote (lista de textos).

"""

import google.generativeai as genai
from domain.ports.embedding_port import EmbeddingPort

class GeminiEmbedding(EmbeddingPort):

    def __init__(self, api_key: str, model: str):
        # Configura a chave de API globalmente no SDK do Google Generative AI
        genai.configure(api_key=api_key)
        # Modelo de embedding a ser utilizado (ex: "models/text-embedding-004")
        self.model = model

    def embed(self, text: str):
        """Gera o embedding para um único texto chamando a API do Gemini."""
        response = genai.embed_content(
            model=self.model,
            content=text
        )
        return response["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Gera embeddings para múltiplos textos em uma única chamada à API do Gemini.
        Quando o input é uma lista, a API retorna um dicionário onde "embedding" é uma lista de listas.
        """
        response = genai.embed_content(
            model=self.model,
            content=texts
        )
        # Quando enviamos uma lista de textos, genai retorna "embedding" como lista de listas
        return response["embedding"]