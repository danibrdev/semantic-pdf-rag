"""
Ponto de entrada da aplicação via CLI.

Este módulo define os comandos disponíveis no terminal usando o framework Typer.
Atualmente suporta o comando `ingest`, responsável por inserir PDFs no banco vetorial.
"""

import logging
import typer

from infra.bootstrap.container import create_container
from core.use_cases.ingest_pdf import IngestPDFUseCase

# Configura o sistema de logging com nível INFO.
# Todos os módulos que usarem logging.getLogger() herdarão este formato.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# typer.Typer() cria o aplicativo CLI. Cada função decorada com @app.command()
# vira um subcomando disponível no terminal.
app = typer.Typer()

@app.command()
def ingest(file_path: str) -> None:
    """
    Ingere um arquivo PDF no banco vetorial.

    Fluxo:
    1. Cria o container de dependências lendo as configurações do .env
    2. Extrai os componentes concretos (loader, embedding, vector store)
    3. Instancia e executa o IngestPDFUseCase com esses componentes
    """
    # create_container() lê o .env via Settings e instancia todas as dependências concretas
    container = create_container()

    # Extrai os componentes do container pelo nome da chave
    pdf_loader = container["pdf_loader"]
    embedding_provider = container["embedding"]
    vector_store = container["vector_store"]

    # O caso de uso recebe as dependências prontas — não sabe quais provedores estão por baixo
    use_case = IngestPDFUseCase(
        pdf_loader=pdf_loader,
        embedding=embedding_provider,
        vector_store=vector_store,
    )
    use_case.execute(file_path)


# app() só é chamado quando o arquivo é executado diretamente no terminal.
# Quando o arquivo é importado por outro módulo, este bloco é ignorado.
if __name__ == "__main__":
    app()