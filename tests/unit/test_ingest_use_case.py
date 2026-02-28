"""
Testes unitários para o IngestPDFUseCase.

Verifica que o pipeline de ingestão orquestra corretamente os três componentes:
PDF Loader, Embedding Provider e Vector Store.

Utiliza implementações falsas (Fakes) em vez de mocks para simular o comportamento
dos adaptadores sem depender de infraestrutura real (banco, API).
"""

from core.use_cases.ingest_pdf import IngestPDFUseCase
from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort


class FakePDFLoader(PDFLoaderPort):
    """Implementação falsa de PDFLoaderPort — retorna texto simulado sem ler arquivo real."""
    def load(self, path: str) -> str:
        return "conteudo extraido do pdf " * 200  # Texto grande o suficiente para gerar múltiplos chunks


class FakeEmbedding(EmbeddingPort):
    """Implementação falsa de EmbeddingPort — retorna vetores de zeros sem chamar API real."""
    def embed(self, text: str):
        return [0.1] * 10  # Embedding fake com dimensão 10

    def embed_batch(self, texts: list[str]):
        return [[0.1] * 10 for _ in texts]  # Retorna um embedding fake para cada texto


class FakeVectorStore(VectorStorePort):
    """Implementação falsa de VectorStorePort — armazena chunks em memória para asserções."""
    def __init__(self):
        self.saved_chunks = []  # Lista que captura todos os chunks salvos durante o teste

    def save(self, chunk):
        self.saved_chunks.append(chunk)  # Simula a persistência armazenando em memória

    def similarity_search(self, embedding, k, threshold=None):
        return []  # Não utilizado neste teste


def test_ingest_generates_and_saves_chunks():
    """
    Verifica que o IngestPDFUseCase executa o pipeline completo e salva ao menos um chunk.
    Garante que o caso de uso orquestra corretamente todos os adaptadores injetados.
    """

    pdf_loader = FakePDFLoader()
    embedding = FakeEmbedding()
    vector_store = FakeVectorStore()

    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding,
        vector_store=vector_store,
    )

    use_case.execute("fake.pdf")

    # Verifica que ao menos um chunk foi salvo no vector store após a ingestão
    assert len(vector_store.saved_chunks) > 0