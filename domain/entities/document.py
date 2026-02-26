from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Dict, Any

class DocumentChunk(BaseModel):
    id: UUID
    document_name: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = {}