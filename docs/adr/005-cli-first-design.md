# ADR 005 – Adopt CLI-First Interface Strategy

## Status
Accepted

---

## Context

The project aims to demonstrate architectural maturity in:

- RAG system design
- Token optimization strategies
- Provider-agnostic LLM integration
- Clean Architecture implementation

The primary goal is to showcase backend engineering quality rather than build a user-facing SaaS application.

Possible interface options included:

- REST API (FastAPI)
- Web Interface
- CLI (Command Line Interface)
- Hybrid approach

Introducing a web or REST layer would increase:

- Infrastructure complexity
- Deployment requirements
- Authentication concerns
- Operational overhead

This complexity does not directly contribute to the architectural goals of the project.

---

## Decision

We adopt a CLI-first interface strategy using Typer.

The CLI will provide commands such as:

- `ingest <file>`
- `chat`
- `benchmark`

The CLI will depend only on the Core layer.

The architecture must allow future introduction of a REST API without modifying Domain or Core layers.

---

## Alternatives Considered

### 1. REST API (FastAPI)

- More production-like
- Increased infrastructure complexity
- Diverts focus from RAG core logic

### 2. Web Interface

- Improves usability
- Adds UI complexity
- Not aligned with portfolio technical focus

### 3. Hybrid CLI + API

- Flexible
- Over-engineered for initial scope

---

## Consequences

### Positive

- Simpler deployment
- Focus on backend architecture
- Lower operational overhead
- Clear demonstration of system internals
- Faster iteration cycle

### Negative

- Not immediately accessible via browser
- Not multi-user
- Less product-oriented presentation

---

## Notes

This decision prioritizes architectural clarity over interface complexity.

Future expansion to a REST API or web interface must reuse the existing Core and Domain layers without architectural changes.