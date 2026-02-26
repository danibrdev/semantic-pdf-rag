# ADR 002 – Adopt Clean Architecture

## Status
Accepted

---

## Context

The Semantic PDF RAG CLI aims to be a portfolio-level system that demonstrates architectural maturity, extensibility, testability, and production-readiness.

The system includes:

- PDF ingestion
- Vector storage with pgVector
- RAG orchestration
- Token optimization logic
- Multiple LLM and embedding providers

Given this level of complexity, a simple layered or script-based architecture would introduce tight coupling between business logic, infrastructure, and external providers.

Key architectural requirements:

- Clear separation of concerns
- High testability of business logic
- Replaceable infrastructure components
- Provider-agnostic LLM integration
- Long-term maintainability

---

## Decision

We adopt Clean Architecture with Ports & Adapters (Hexagonal Architecture).

### Structural Model

- **Domain Layer**: Contains business models, entities, value objects, and Ports (interfaces).
- **Core Layer**: Orchestrates RAG flow, token optimization, and application logic.
- **Infrastructure Layer**: Implements external dependencies (PostgreSQL, pgVector, LLM providers, PDF parsing, CLI).
- **App/CLI Layer**: Entry point that depends only on Core.

### Dependency Rule

All dependencies must point inward:

- Domain does not depend on Core or Infrastructure
- Core depends only on Domain
- Infrastructure implements Domain-defined Ports
- CLI depends on Core only

No business logic is allowed inside Infrastructure.

---

## Alternatives Considered

### 1. Simple Layered Architecture
- Easier initial setup
- Higher coupling between database, LLM, and business logic
- Harder to replace providers

### 2. Monolithic Script-Based Design
- Fast prototyping
- Poor scalability
- Difficult testing
- Not suitable for portfolio-level engineering

### 3. Framework-Driven Architecture (Heavy LangChain Abstraction)
- Faster integration
- Risk of framework lock-in
- Reduced architectural transparency

---

## Consequences

### Positive
- Strong separation of concerns
- Infrastructure components easily replaceable
- High unit test coverage potential
- Clear architectural boundaries
- Better long-term maintainability
- Professional engineering perception

### Negative
- Increased upfront complexity
- More boilerplate code
- Requires discipline to maintain dependency rules

---

## Notes

This ADR is foundational.

All subsequent implementation phases must comply with the Clean Architecture dependency rule.

Any future structural changes must reference this ADR and explicitly state whether it is being superseded or extended.