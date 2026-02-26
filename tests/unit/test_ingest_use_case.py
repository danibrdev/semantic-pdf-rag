from core.use_cases.ingest_pdf import IngestPDFUseCase
from domain.ports.embedding_port import EmbeddingPort
from domain.ports.pdf_loader_port import PDFLoaderPort
from domain.ports.vector_store_port import VectorStorePort


class FakePDFLoader(PDFLoaderPort):
    def load(self, path: str) -> str:
        return "conteudo extraido do pdf " * 200


class FakeEmbedding(EmbeddingPort):
    def embed(self, text: str):
        return [0.1] * 10  # embedding fake

    def embed_batch(self, texts: list[str]):
        return [[0.1] * 10 for _ in texts]  # batch fake


class FakeVectorStore(VectorStorePort):
    def __init__(self):
        self.saved_chunks = []

    def save(self, chunk):
        self.saved_chunks.append(chunk)

    def similarity_search(self, embedding, k):
        return []


def test_ingest_generates_and_saves_chunks():

    pdf_loader = FakePDFLoader()
    embedding = FakeEmbedding()
    vector_store = FakeVectorStore()

    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding,
        vector_store=vector_store,
    )

    use_case.execute("fake.pdf")

    assert len(vector_store.saved_chunks) > 0