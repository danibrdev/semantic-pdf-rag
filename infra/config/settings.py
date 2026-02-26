from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic import ConfigDict
from typing import Literal, Optional, ClassVar, Dict
from pydantic import model_validator

class Settings(BaseSettings):

    # decidir qual provider usar
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    # Provider Selection
    provider: Literal["openai", "gemini"] = Field(
        default="gemini",
        description="Embedding and LLM provider"
    )

    # Keys
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Modelos específicos para geração de embeddings e LLMs
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"

    gemini_embedding_model: str = "models/text-embedding-004"
    gemini_llm_model: str = "gemini-1.5-flash"

    # Database
    database_url: str

    # Gestão de tokens e similaridade
    llm_max_tokens: int = 8192
    response_token_reserve: int = 1024
    default_top_k: int = 4
    similarity_threshold: float = 0.75

    # Calcula dinamicamente a dimensão do embedding baseado no provider
    EMBEDDING_DIMENSIONS: ClassVar[Dict[str, int]] = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "models/text-embedding-004": 768,
    }
    
    @property
    def current_embedding_model(self) -> str:
        if self.provider == "openai":
            return self.openai_embedding_model
        return self.gemini_embedding_model
    
    def current_llm_model(self) -> str:
        if self.provider == "openai":
            return self.openai_llm_model
        return self.gemini_llm_model

    @property
    def embedding_dimension(self) -> int:
        model_name = self.current_embedding_model
        if model_name not in self.EMBEDDING_DIMENSIONS:
            raise ValueError(f"Embedding dimension not configured for model: {model_name}")
        return self.EMBEDDING_DIMENSIONS[model_name]

    @property
    def max_context_tokens(self) -> int:
        return self.llm_max_tokens - self.response_token_reserve
    
    @model_validator(mode="after")
    def validate_provider_keys(self):
        if self.provider == "openai" and not self.openai_api_key:
            raise ValueError("Provider 'openai' selected but openai_api_key not provided.")
        if self.provider == "gemini" and not self.google_api_key:
            raise ValueError("Provider 'gemini' selected but google_api_key not provided.")
        return self

settings = Settings()