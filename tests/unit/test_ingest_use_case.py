"""
Testes unitários para o IngestPDFUseCase.

Verifica que o pipeline de ingestão orquestra corretamente os três componentes:
PDF Loader, Embedding Provider e Vector Store.

Utiliza implementações falsas (Fakes) em vez de mocks para simular o comportamento
dos adaptadores sem depender de infraestrutura real (banco de dados, API de IA).
"""

from core.use_cases.ingest_pdf import IngestPDFUseCase

# Importamos os Ports para que os Fakes implementem os mesmos contratos das classes reais
from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort


class FakePDFLoader(PDFLoaderPort):
    """Leitor de PDF falso — retorna texto simulado sem ler nenhum arquivo real."""
    def load(self, path: str) -> str:
        # Texto repetido para garantir que o chunker gere múltiplos chunks
        return "conteudo extraido do pdf " * 200


class FakeEmptyPDFLoader(PDFLoaderPort):
    def load(self, path: str) -> str:
        return "   "


class FakeEmbedding(EmbeddingPort):
    """Provedor de embeddings falso — retorna vetores de zeros sem chamar a API."""
    def embed(self, text: str) -> list:
        return [0.1] * 10  # Vetor com 10 dimensões, todos iguais a 0.1

    def embed_batch(self, texts: list) -> list:
        # List comprehension: cria um vetor fake para cada texto na lista recebida
        return [[0.1] * 10 for _ in texts]


class FakeVectorStore(VectorStorePort):
    """Vector store falso — armazena chunks em uma lista em memória para verificação no teste."""
    def __init__(self):
        self.saved_chunks = []  # Lista que acumula os chunks salvos durante o teste

    def save(self, chunk) -> None:
        self.saved_chunks.append(chunk)  # Simula a persistência salvando na lista

    def similarity_search(self, embedding, k, threshold=None) -> list:
        return []  # Não utilizado neste teste


def test_ingest_generates_and_saves_chunks() -> None:
    """
    Verifica que o IngestPDFUseCase executa o pipeline completo e salva ao menos um chunk.
    """
    # Instancia os fakes no lugar das implementações reais
    pdf_loader = FakePDFLoader()
    embedding = FakeEmbedding()
    vector_store = FakeVectorStore()

    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding,
        vector_store=vector_store,
    )

    # O FakePDFLoader ignora o caminho e retorna o texto fixo configurado acima
    use_case.execute("fake.pdf")

    # Verifica que ao menos um chunk foi salvo no vector store
    assert len(vector_store.saved_chunks) > 0


def test_ingest_with_empty_text_saves_nothing() -> None:
    pdf_loader = FakeEmptyPDFLoader()
    embedding = FakeEmbedding()
    vector_store = FakeVectorStore()

    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding,
        vector_store=vector_store,
    )

    use_case.execute("empty.pdf")

    assert vector_store.saved_chunks == []