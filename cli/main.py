"""
Ponto de entrada da aplicação via CLI.

Este módulo define os comandos disponíveis no terminal usando o framework Typer.
Atualmente suporta apenas o comando `ingest`, responsável por inserir PDFs no banco vetorial.
"""

import logging
import typer

from infra.bootstrap.container import create_container
from core.use_cases.ingest_pdf import IngestPDFUseCase

# Configura o sistema de logs da aplicação para exibir mensagens com timestamp, nível e origem
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Instância principal do aplicativo Typer — registra todos os comandos do CLI
app = typer.Typer()

@app.command()
def ingest(file_path: str):
    """
    Ingere um arquivo PDF no banco vetorial.

    Fluxo:
    1. Cria o container de dependências via composition root
    2. Resolve dependências concretas (embedding, loader, vector store)
    3. Instancia e executa o IngestPDFUseCase
    """

    # Composition Root oficial: centraliza bootstrap e validação das configurações
    container = create_container()

    pdf_loader = container["pdf_loader"]
    embedding_provider = container["embedding"]
    vector_store = container["vector_store"]

    # Instancia o caso de uso de ingestão e executa o pipeline completo
    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding_provider,
        vector_store=vector_store,
    )
    use_case.execute(file_path)


if __name__ == "__main__":
    app()