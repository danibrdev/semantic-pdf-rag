class TokenBudgetEstimator:
    """
    Responsible for estimating and enforcing token budget rules.
    This layer centralizes all token-related calculations.
    """

    def __init__(self, max_context_tokens: int):
        self.max_context_tokens = max_context_tokens

    def estimate_text_tokens(self, text: str) -> int:
        """
        Rough token estimation.
        Rule of thumb: 1 token ≈ 4 characters.
        Cheap and deterministic.
        """
        return len(text) // 4

    def available_context_budget(self) -> int:
        """
        Returns how many tokens are available
        for context after reserving response tokens.
        """
        return self.max_context_tokens

    def enforce_budget(self, texts: list[str]) -> list[str]:
        """
        Given a list of text blocks, returns only those
        that fit within the available token budget.
        """

        max_tokens = self.available_context_budget()

        selected = []
        current_tokens = 0

        for text in texts:
            tokens = self.estimate_text_tokens(text)

            if current_tokens + tokens > max_tokens:
                break

            selected.append(text)
            current_tokens += tokens

        return selected
