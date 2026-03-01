"""
Divisor de texto em chunks (pedaços menores).

Responsável por dividir um texto longo em partes menores com tamanho controlado,
usando uma janela deslizante com sobreposição (overlap). A sobreposição garante
que o contexto semântico nas bordas dos chunks não seja perdido.

Exemplo com chunk_size=1000 e overlap=200:
- Chunk 1: caracteres 0–1000
- Chunk 2: caracteres 800–1800  (200 chars de sobreposição com o chunk anterior)
- Chunk 3: caracteres 1600–2600 ...e assim por diante
"""

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        # Número de caracteres por chunk (não tokens)
        self.chunk_size = chunk_size
        # Número de caracteres que se repetem entre chunks consecutivos para preservar contexto
        self.overlap = overlap

        # Usa o splitter oficial do LangChain para padronizar o chunking
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap,
            separators=["\n\n", "\n", " ", ""],  # Quebra hierárquica (parágrafo -> linha -> palavra)
        )

    def chunk(self, text: str) -> List[str]:
        """
        Divide o texto em chunks usando o splitter do LangChain.
        :param text: O texto completo a ser dividido.
        :return: Lista de chunks resultantes.
        """

        # Proteção contra texto vazio/nulo
        if not text or not text.strip():
            return []

        # Gera os chunks via LangChain
        chunks = self._splitter.split_text(text)

        # Remove blocos vazios do inicio e do fim da string por segurança
        # Isso é importante porque o processo de chunking pode, em alguns casos, gerar chunks vazios, especialmente se o texto tiver muitas quebras de linha ou espaços. 
        # Ao usar essa expressão, garantimos que a lista final de chunks contenha apenas pedaços de texto significativos.
        return [chunk for chunk in chunks if chunk.strip()]