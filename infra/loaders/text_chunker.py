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

class TextChunker:

    def __init__(self, chunk_size=1000, overlap=200):
        # Número de caracteres por chunk (não tokens)
        self.chunk_size = chunk_size
        # Número de caracteres que se repetem entre chunks consecutivos para preservar contexto
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Divide o texto em uma lista de chunks com tamanho e sobreposição configurados.
        Retorna lista vazia se o texto estiver vazio.
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            # Avança pela diferença entre chunk_size e overlap para criar a janela deslizante
            start += self.chunk_size - self.overlap

        return chunks