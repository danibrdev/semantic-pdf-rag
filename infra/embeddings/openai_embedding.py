# Implementação concreta para geração de embeddings. Se comunica diretamente com a API da OpenAI
from openai import OpenAI
from domain.ports.embedding_port import EmbeddingPort

class OpenAIEmbedding(EmbeddingPort):

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed(self, text: str):
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding