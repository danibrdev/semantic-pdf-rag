"""
Configurações centrais da aplicação.

Carrega e valida todas as variáveis de ambiente a partir do arquivo `.env`
usando Pydantic Settings. É a única fonte de verdade para:
- Qual provedor de IA usar (OpenAI ou Gemini)
- Chaves de API e modelos configurados
- URL de conexão com o banco de dados
- Parâmetros de controle de tokens e similaridade

Propriedades calculadas automaticamente (embedding_dimension, max_context_tokens)
evitam erros manuais de configuração.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic import ConfigDict
from typing import Literal, Optional, ClassVar, Dict
from pydantic import model_validator

class Settings(BaseSettings):

    # Configura o Pydantic para ler o arquivo .env e ignorar variáveis desconhecidas
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    # Seleção do provedor de IA ativo: "openai" ou "gemini"
    provider: Literal["openai", "gemini"] = Field(
        default="gemini",
        description="Embedding and LLM provider"
    )

    # Chaves de API — apenas a chave do provedor selecionado é obrigatória
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Modelos padrão para embedding e geração de texto por provedor
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"

    gemini_embedding_model: str = "models/text-embedding-004"
    gemini_llm_model: str = "gemini-1.5-flash"

    # URL de conexão com o PostgreSQL (obrigatória)
    database_url: str

    # Parâmetros de controle de orçamento de tokens e qualidade de recuperação
    llm_max_tokens: int = 8192           # Janela de contexto máxima do modelo LLM
    response_token_reserve: int = 1024   # Tokens reservados para a resposta do LLM
    default_top_k: int = 4               # Número padrão de chunks recuperados por busca
    similarity_threshold: float = 0.75   # Score mínimo de similaridade aceito

    # Mapa estático de dimensões de embedding por modelo (usado para criar a tabela no banco)
    EMBEDDING_DIMENSIONS: ClassVar[Dict[str, int]] = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "models/text-embedding-004": 768,
    }

    @property
    def current_embedding_model(self) -> str:
        """Retorna o modelo de embedding do provedor ativo."""
        if self.provider == "openai":
            return self.openai_embedding_model
        return self.gemini_embedding_model

    @property
    def embedding_dimension(self) -> int:
        """
        Retorna a dimensão do vetor de embedding com base no modelo configurado.
        Lança erro se o modelo não estiver mapeado em EMBEDDING_DIMENSIONS.
        """
        model_name = self.current_embedding_model
        if model_name not in self.EMBEDDING_DIMENSIONS:
            raise ValueError(f"Embedding dimension not configured for model: {model_name}")
        return self.EMBEDDING_DIMENSIONS[model_name]

    @property
    def max_context_tokens(self) -> int:
        """Calcula o orçamento disponível para contexto: janela total menos reserva de resposta."""
        return self.llm_max_tokens - self.response_token_reserve

    @model_validator(mode="after")
    def validate_provider_keys(self):
        """
        Valida que a chave de API do provedor selecionado foi fornecida.
        Lança erro descritivo caso a chave esteja ausente.
        """
        if self.provider == "openai" and not self.openai_api_key:
            raise ValueError("Provider 'openai' selected but openai_api_key not provided.")
        if self.provider == "gemini" and not self.google_api_key:
            raise ValueError("Provider 'gemini' selected but google_api_key not provided.")
        return self

settings = Settings()