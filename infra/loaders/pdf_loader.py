"""
Adaptador de leitura de arquivos PDF.

Implementação concreta de PDFLoaderPort usando a biblioteca `pypdf`.
Responsável por abrir o arquivo PDF, iterar sobre todas as suas páginas
e concatenar o texto extraído em uma única string.

Esta implementação é simples e direta — futuramente pode ser substituída
por um LangChain Document Loader (ex: PyPDFLoader) sem afetar o restante do sistema,
graças ao Port (interface) que ela implementa.
"""

from pypdf import PdfReader
from domain.ports.pdf_loader_port import PDFLoaderPort


class PDFLoader(PDFLoaderPort):

    def load(self, path: str) -> str:
        """
        Carrega o PDF no caminho fornecido e retorna o texto completo como uma string.
        Itera sobre todas as páginas e concatena o conteúdo extraído.
        """
        reader = PdfReader(path)
        text = ""

        
        #O loop itera sobre cada página do PDF usando `reader.pages`. Para cada página, ele chama `extract_text()`, que tenta extrair o texto da página. Se a página não contiver texto (por exemplo, se for uma imagem), `extract_text()` pode retornar `None`, então usamos `or ""` para garantir que `page_text` seja sempre uma string. Em seguida, concatenamos o texto extraído de cada página em uma única string `text`, separando as páginas com uma nova linha (`\n`). No final do loop, `text` conterá o conteúdo completo do PDF.
        for page in reader.pages:
            # O método `extract_text()` retorna uma string contendo o texto extraído da página PDF. 
            # Ele analisa o conteúdo da página e tenta reconstrui-lo, levando em consideração a formatação, os espaços e a ordem dos elementos. 
            # No entanto, a qualidade da extração pode variar dependendo do layout do PDF, da presença de imagens ou de como o texto foi codificado no arquivo. 
            # Se a página não contiver texto ou se o método não conseguir extrair o texto por algum motivo (por exemplo, se a página for composta principalmente por imagens), ele pode retornar `None`. 
            # Por isso, no código, usamos `or ""` para garantir que `page_text` seja sempre uma string, mesmo que `extract_text()` retorne `None`.
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        return text