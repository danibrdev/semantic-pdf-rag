"""
Testes unitários para o RAG prompt.

Verifica que o template é criado com as variáveis corretas
e que o prompt final contém os valores de contexto e pergunta.
"""

from core.prompts.rag_prompt import build_rag_prompt_template, format_rag_prompt


def test_build_rag_prompt_template_variables() -> None:
    """
    Verifica que o template declara exatamente as variáveis {context} e {question}.
    O LangChain extrai automaticamente essas variáveis da string do template.
    """
    template = build_rag_prompt_template()
    # input_variables é a lista de variáveis detectadas pelo PromptTemplate
    assert set(template.input_variables) == {"context", "question"}


def test_format_rag_prompt_includes_context_and_question() -> None:
    """
    Verifica que o prompt formatado contém o contexto e a pergunta fornecidos,
    além das instruções fixas do template.
    """
    context = "Chunk A: LangChain integra embeddings e retriever."
    question = "Como funciona o fluxo?"

    # format_rag_prompt preenche o template com os valores reais
    prompt = format_rag_prompt(context=context, question=question)

    # O texto do contexto, da pergunta e das instruções deve estar no prompt final
    assert context in prompt
    assert question in prompt
    assert "Não invente informações" in prompt
