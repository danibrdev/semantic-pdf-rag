"""
Port (contrato) para carregadores de PDF.

Define a interface abstrata que qualquer leitor de PDF deve implementar
(ex: PyPDF, PDFMiner, LangChain Document Loaders). Garante que o core
nunca dependa de uma biblioteca específica de leitura de arquivos.
"""

from abc import ABC, abstractmethod

class PDFLoaderPort(ABC):

    @abstractmethod
    def load(self, path: str) -> str:
        """Carrega o arquivo PDF no caminho informado e retorna todo o seu conteúdo como texto bruto."""
        pass
