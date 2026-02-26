# Semantic PDF RAG CLI

> Aplicativo CLI em Python com Clean Architecture para Geração Aumentada de Recuperação (RAG) de documentos PDF, focado em alta performance e conscientização de custos (tokens).

O **Semantic PDF RAG CLI** foi construído como um sistema de nível profissional para portfólio, demonstrando práticas modernas de arquitetura de IA, governança explícita de tokens e separação de responsabilidades.

---

## Principais Princípios Arquiteturais

- **Arquitetura Limpa & Ports/Adapters**: Lógica de domínio (Core) isolada da infraestrutura (bancos de dados, provedores LLM).
- **Design Agnóstico de Provedor**: Facilidade para alternar entre OpenAI, Gemini ou modelos locais.
- **Governança Explícita de Tokens**: Inclui uma Camada de Estratégia de Otimização de Tokens para aplicar controle de orçamento e limpeza de contexto antes de qualquer chamada ao LLM.
- **Focado em CLI**: Projetado para processamento de alta velocidade baseado no terminal.
- **Pronto para Produção**: Testável, extensível, e estruturado com tipagem (Type Hints) e logs claros.

---

## Estrutura do Projeto

O projeto segue uma regra de Dependência, onde as dependências apontam apenas para dentro, em direção à camada de domínio (`domain`):

```text
semantic-pdf-rag/
├── cli/                 # Camada de apresentação CLI baseada no Typer
├── core/                # Orquestração RAG e Casos de Uso (Otimização de tokens, Prompts)
├── domain/              # Lógica de negócio pura (Entidades, Ports/Interfaces, Objetos de Valor)
├── infra/               # Adaptadores de infraestrutura (PostgreSQL, pgVector, LLMs, Leitores PDF)
└── tests/               # Testes Unitários e de Integração
```

---

## Fluxo de Execução (RAG Flow)

```mermaid
flowchart TD
    Q[Pergunta do Usuário] --> E[Provedor de Embeddings]
    E --> VS[(pgVector + HNSW)]
    VS --> R[Recuperar Top-K Chunks]
    R --> TO[Camada de Otimização de Tokens]
    TO --> TB[Estimador de Orçamento de Tokens]
    TB --> PB[Construtor de Prompts]
    PB --> LLM[LLM Agnóstico]
    LLM --> A[Resposta Final]
```

### Governança e Estratégia de Tokens
Antes de cada chamada ao LLM, o sistema garante eficiência de tokens através de:
1. Ajuste dinâmico de recuperação (Top-K) e filtragem por limite de similaridade.
2. Compressão da janela de contexto e remoção de redundância.
3. Reserva de tokens para a saída e aplicação rígida de limites máximos (Context window limits).

---

## Stack Tecnológico

- **Linguagem**: Python 3.11+
- **Banco de Dados**: PostgreSQL com `pgVector`
- **Indexação**: Índice HNSW para busca de similaridade de cossenos
- **CLI**: Typer
- **Validação**: Pydantic
- **Testes**: Pytest
- **Infraestrutura**: Docker & Docker Compose

---

## Guia de Início Rápido (Planejado)

```bash
# Inserir um documento PDF no banco de vetores
semantic-rag ingest caminho/para/o/arquivo.pdf

# Iniciar uma sessão de chat usando os documentos indexados
semantic-rag chat

# Visualizar estatísticas de indexação
semantic-rag stats
```

---

## Objetivos do Projeto

- **Demonstrar conhecimento aplicado em arquitetura de IA** utilizando padrões de Arquitetura Limpa em um contexto de LLMs.
- **Apresentar um design escalável para RAG** usando PostgreSQL e pgVector para recuperação a nível empresarial.
- **Exibir conscientização de custos** através de rigoroso controle de tokens e isolamento de orçamentos.
- **Fornecer um sistema pronto para portfólio** expondo práticas robustas de engenharia de software corporativa.

---

## 📝 Licença

Este projeto está sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.