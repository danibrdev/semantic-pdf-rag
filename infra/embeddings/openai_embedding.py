"""
Adaptador de embeddings para OpenAI via LangChain.

Implementação concreta de EmbeddingPort usando `langchain-openai`.
Padroniza o acesso ao provedor dentro do ecossistema LangChain,
mantendo o contrato de domínio inalterado.
"""

from typing import List

# OpenAIEmbeddings é o wrapper do LangChain para a API de embeddings da OpenAI
from langchain_openai import OpenAIEmbeddings

from domain.ports.embedding_port import EmbeddingPort


class OpenAIEmbedding(EmbeddingPort):
    """
    Adaptador que implementa o EmbeddingPort usando o modelo de embeddings da OpenAI.
    Traduz as chamadas do domínio para chamadas da integração LangChain com a OpenAI.
    """

    def __init__(self, api_key: str, model: str):
        # Encapsula o cliente LangChain — o restante do sistema nunca o acessa diretamente
        self.client = OpenAIEmbeddings(
            api_key=api_key,
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