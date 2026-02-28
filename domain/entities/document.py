"""
Entidade de domínio: DocumentChunk.

Representa a unidade central de dados do sistema RAG.
Um DocumentChunk é um pedaço (chunk) de um PDF processado, contendo
o texto original, seu embedding vetorial e metadados associados.

Esta entidade é agnóstica a qualquer infraestrutura — não conhece banco,
API ou framework. É pura lógica de domínio.
"""

from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict, Any

class DocumentChunk(BaseModel):
    id: UUID                        # Identificador único do chunk (UUID gerado automaticamente)
    document_name: str              # Nome do arquivo PDF de origem
    content: str                    # Texto bruto do chunk extraído do PDF
    embedding: List[float]          # Vetor de embedding gerado pelo provedor (OpenAI ou Gemini)
    metadata: Dict[str, Any] = {}   # Metadados adicionais (ex: autor, fonte, tipo)