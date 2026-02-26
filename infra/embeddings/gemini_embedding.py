# Implementação concreta para geração de embeddings. Se comunica diretamente com a API do Gemini
import google.generativeai as genai
from domain.ports.embedding_port import EmbeddingPort

class GeminiEmbedding(EmbeddingPort):

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = model

    def embed(self, text: str):
        response = genai.embed_content(
            model=self.model,
            content=text
        )
        return response["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = genai.embed_content(
            model=self.model,
            content=texts
        )
        # When sending a list of texts, genai returns a dictionary where "embedding" is a list of lists.
        return response["embedding"]