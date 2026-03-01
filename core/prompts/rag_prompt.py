"""
Prompt templates centrais do pipeline RAG usando LangChain.

Os prompts são centralizados aqui para que mudanças no comportamento do LLM
sejam feitas em um único lugar, sem tocar na lógica de negócio.
"""

# PromptTemplate cria templates de texto com variáveis ({context}, {question})
# que são substituídas pelos valores reais em tempo de execução.
from langchain_core.prompts import PromptTemplate


def build_rag_prompt_template() -> PromptTemplate:
    """
    Cria e retorna o template padrão para perguntas sobre contexto recuperado.

    O template instrui o LLM a responder apenas com base no contexto fornecido,
    evitando que ele invente informações não presentes no documento.
    """
    # from_template() analisa a string e extrai automaticamente as variáveis {context} e {question}
    # .strip() remove espaços em branco desnecessários nas extremidades da string
    return PromptTemplate.from_template(
        """
Você é um assistente técnico e deve responder somente com base no contexto fornecido.

Contexto:
{context}

Pergunta:
{question}

Instruções:
- Seja objetivo e claro.
- Se a resposta não estiver no contexto, diga explicitamente que não encontrou evidências suficientes.
- Não invente informações.

Resposta:
""".strip()
    )


def format_rag_prompt(context: str, question: str) -> str:
    """
    Preenche o template com o contexto e a pergunta fornecidos,
    retornando o prompt final pronto para ser enviado ao LLM.
    """
    template = build_rag_prompt_template()
    # .format() substitui os placeholders {context} e {question} pelos valores reais
    return template.format(context=context, question=question)
