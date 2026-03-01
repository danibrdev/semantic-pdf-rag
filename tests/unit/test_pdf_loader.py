"""
Testes unitários para o adaptador PDFLoader.

Verifica que o loader concatena corretamente o texto de todas as páginas
e lida com situações em que uma página não retorna texto (None).

POR QUÊ mockar o PdfReader:
- Evita precisar de um arquivo PDF real nos testes
- Permite controlar exatamente o conteúdo de cada página
- Torna o teste rápido e determinístico (sem I/O de disco)
"""

# MagicMock: cria objetos falsos que aceitam qualquer chamada de método.
# patch: substitui temporariamente um objeto real por um Mock durante o teste.
from unittest.mock import MagicMock, patch

from infra.loaders.pdf_loader import PDFLoader


@patch("infra.loaders.pdf_loader.PdfReader")
def test_pdf_loader_load_concatenates_page_text(mock_pdf_reader) -> None:
    """
    Verifica que load() concatena o texto de múltiplas páginas em uma única string,
    separando cada página com uma quebra de linha (\\n).
    """
    # Cria páginas falsas com MagicMock — cada uma simula um objeto de página do pypdf
    page_1 = MagicMock()
    page_1.extract_text.return_value = "Primeira página"  # Texto que a página "retorna"

    page_2 = MagicMock()
    page_2.extract_text.return_value = "Segunda página"

    # Monta o reader falso com as duas páginas controladas
    reader = MagicMock()
    reader.pages = [page_1, page_2]

    # Configura o patch: quando PdfReader(path) for chamado, retorna o reader falso
    mock_pdf_reader.return_value = reader

    loader = PDFLoader()
    result = loader.load("/tmp/fake.pdf")

    # Verifica o texto concatenado com \n entre as páginas
    assert result == "Primeira página\nSegunda página\n"

    # Verifica que PdfReader foi chamado com o caminho correto
    mock_pdf_reader.assert_called_once_with("/tmp/fake.pdf")


@patch("infra.loaders.pdf_loader.PdfReader")
def test_pdf_loader_load_handles_none_text(mock_pdf_reader) -> None:
    """
    Verifica que load() não quebra quando extract_text() retorna None.

    Isso pode acontecer com páginas que contêm apenas imagens (sem texto selecionável).
    O loader deve tratar None como string vazia e continuar normalmente.
    """
    page_1 = MagicMock()
    page_1.extract_text.return_value = None  # Simula página sem texto (ex: imagem)

    page_2 = MagicMock()
    page_2.extract_text.return_value = "Texto"

    reader = MagicMock()
    reader.pages = [page_1, page_2]
    mock_pdf_reader.return_value = reader

    loader = PDFLoader()
    result = loader.load("/tmp/fake.pdf")

    # None vira "" pelo `or ""` no loader, resultando em \n para a primeira página
    assert result == "\nTexto\n"
