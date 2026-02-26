# ADR 004 – Provider-Agnostic LLM Design

## Status
Accepted

---

## Context

The system requires integration with:

- Embedding providers
- Large Language Model (LLM) providers

Examples include:

- OpenAI
- Gemini
- Future providers

Directly coupling business logic to a specific provider (e.g., OpenAI SDK calls inside application logic) would introduce:

- Vendor lock-in
- Tight coupling
- Difficult provider replacement
- Reduced testability
- Limited flexibility for cost optimization

The project aims to demonstrate architectural maturity and long-term maintainability.

Therefore, direct provider dependency inside business logic is not acceptable.

---

## Decision

We adopt a **Provider-Agnostic Design** using Ports & Adapters.

### Domain Layer

The Domain defines abstract interfaces (Ports):

- `EmbeddingProviderPort`
- `LLMProviderPort`

These interfaces define the required behavior without referencing any external SDK.

### Infrastructure Layer

Concrete adapters implement the ports:

- `OpenAIEmbeddingProvider`
- `GeminiEmbeddingProvider`
- `OpenAILLMProvider`
- `GeminiLLMProvider`

The Core layer interacts only with the Ports.

Provider selection must be handled via:

- Factory Pattern
- Configuration-based injection

No provider-specific SDK logic is allowed outside Infrastructure.

---

## Architectural Flow

Core Layer  
→ Calls LLMProviderPort  
→ Infrastructure Adapter executes provider SDK  
→ Returns normalized response  

This guarantees isolation of external dependencies.

---

## Alternatives Considered

### 1. Direct SDK Usage in Core

- Faster implementation
- High coupling
- Hard to test
- Strong vendor lock-in

### 2. Framework-Abstraction Only (e.g., heavy LangChain reliance)

- Reduced boilerplate
- Reduced architectural control
- Hidden provider coupling

---

## Consequences

### Positive

- Easy provider replacement
- Lower vendor lock-in risk
- Improved testability (mock providers)
- Cost optimization flexibility
- Cleaner separation of concerns
- Strong architectural maturity signal

### Negative

- Additional abstraction layer
- Slight increase in boilerplate code
- Requires disciplined dependency management

---

## Notes

Provider-agnostic design is a foundational architectural principle of this project.

All embedding and LLM calls must go through their respective Ports.

Any direct SDK usage outside Infrastructure is considered a violation of architectural rules.