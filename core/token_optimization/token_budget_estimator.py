"""
Estimador e controlador de orçamento de tokens.

Centraliza todos os cálculos relacionados ao orçamento de tokens da janela de contexto do LLM.
Responsável por:
- Estimar quantos tokens um texto consome
- Retornar o orçamento disponível para o contexto
- Filtrar textos que excedem o limite de tokens

Complementa o TokenOptimizer: enquanto o Optimizer trabalha com DocumentChunks,
o BudgetEstimator trabalha com textos brutos (strings).
"""


class TokenBudgetEstimator:
    """
    Gerencia e aplica as regras de orçamento de tokens para a janela de contexto do LLM.
    """

    def __init__(self, max_context_tokens: int):
        # Número máximo de tokens disponíveis para o contexto após reservas de saída
        self.max_context_tokens = max_context_tokens

    def estimate_text_tokens(self, text: str) -> int:
        """
        Estima o número de tokens de um texto usando a heurística: 1 token ≈ 4 caracteres.
        Barato e determinístico — não depende de tokenizers externos como tiktoken.
        """
        return len(text) // 4

    def available_context_budget(self) -> int:
        """
        Retorna a quantidade de tokens disponíveis para o contexto (chunks recuperados).
        O valor já está pré-calculado pelo Settings (descontada a reserva para a resposta do LLM).
        """
        return self.max_context_tokens

    def enforce_budget(self, texts: list[str]) -> list[str]:
        """
        Recebe uma lista de textos e retorna apenas aqueles que cabem dentro do orçamento.
        Aplica truncagem sequencial: para quando o próximo texto ultrapassaria o limite.
        """

        max_tokens = self.available_context_budget()

        selected = []
        current_tokens = 0

        for text in texts:
            tokens = self.estimate_text_tokens(text)

            # Se o próximo texto ultrapassar o orçamento, descarta e encerra
            if current_tokens + tokens > max_tokens:
                break

            selected.append(text)
            current_tokens += tokens

        return selected
