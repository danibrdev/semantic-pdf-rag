"""
Adaptador de embeddings para Gemini via LangChain.

Implementação concreta de EmbeddingPort usando `langchain-google-genai`.
Mantém o contrato de domínio e centraliza a integração no ecossistema LangChain.
"""

from typing import List

# GoogleGenerativeAIEmbeddings é o wrapper do LangChain para a API de embeddings do Google Gemini
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from domain.ports.embedding_port import EmbeddingPort


class GeminiEmbedding(EmbeddingPort):
    """
    Adaptador que implementa o EmbeddingPort usando o modelo de embeddings do Gemini.
    Traduz as chamadas do domínio para chamadas da integração LangChain com o Google.
    """

    def __init__(self, api_key: str, model: str):
        # Encapsula o cliente LangChain — o restante do sistema nunca o acessa diretamente
        self.client = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model=model,
        )

    def embed(self, text: str) -> List[float]:
        """Gera o embedding para um único texto e retorna o vetor resultante."""
        # embed_query é o método do LangChain para vetorizar textos de busca (queries)
        return self.client.embed_query(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings para múltiplos textos em um único request à API."""
        # Evita chamar a API quando não há textos para processar
        if not texts:
            return []

        # embed_documents processa todos os textos de uma vez em lote
        return self.client.embed_documents(texts)