import logging
import typer

from infra.config.settings import Settings
from infra.factory import build_dependencies
from core.use_cases.ingest_pdf import IngestPDFUseCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = typer.Typer()

@app.command()
def ingest(file_path: str):
    """
    Ingest a PDF file into the vector store.
    """

    # Load and validate settings
    settings = Settings()

    # Build dependencies via composition root
    container = build_dependencies(settings)

    pdf_loader = container["pdf_loader"]
    embedding_provider = container["embedding"]
    vector_store = container["vector_store"]

    # Instantiate and execute use case
    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding_provider,
        vector_store=vector_store,
    )
    use_case.execute(file_path)


if __name__ == "__main__":
    app()