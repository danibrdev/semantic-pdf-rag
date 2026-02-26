# 6. Adopt LangChain for Orchestration and Token Governance

Date: 2023-11-20

## Status

Accepted

## Context

The project's foundational architecture (`ARCHITECTURE.md`) established strict requirements for explicit **Token Governance** (Token Optimization Strategy Layer, Token Budget Estimator, and Context Window Constraints), but the requirements also mandate the use of **LangChain** alongside generic embeddings and LLMs (OpenAI or Gemini)

Initially, the project leaned toward custom-built adapters and loops to manually track tokens, enforce context limits, and inject prompts to maintain Clean Architecture purity without framework lock-in. 

We must implement the mandatory LangChain framework while strictly preserving the project's unique selling proposition: enterprise-grade token cost-awareness.

## Decision

We will adopt **LangChain** as the core orchestrator and infrastructure framework for the project, but we will wire its advanced internal components to fulfill our explicit Token Governance requirements.

1. **Token Budget Estimator:** We will utilize LangChain's `ConversationTokenBufferMemory` to handle automatic token counting and context window trimming.
2. **Token Optimization:** We will replace naive custom database queries with LangChain's `ContextualCompressionRetriever` and Embeddings Filters to drop irrelevant chunks (saving tokens) *before* prompt assembly.
3. **Infrastructure Adapters:** We will pivot custom PgVector implementation and generic Embedding Ports to use official `langchain-postgres` and `langchain-openai` / `langchain-google-genai` libraries respectively.

## Consequences

### Positive
- **Maintainability:** Relies on heavily tested, community-backed token counting and memory buffer abstractions instead of custom, fragile loops.
- **Speed of Delivery:** Allows faster implementation of the RAG pipeline by composing existing LangChain chains.

### Negative
- **Framework Coupling:** The `core` layer becomes tightly coupled to LangChain abstractions (`PromptTemplate`, `Chains`, `Memory`). If LangChain introduces breaking changes, the core orchestration logic will need to be refactored.
- **Learning Curve:** Developers must understand advanced LangChain retrieval (Contextual Compression) rather than simple SQL operations.
