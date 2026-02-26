# ADR 003 – Introduce Token Optimization Strategy Layer

## Status
Accepted

---

## Context

Large Language Models (LLMs) operate under token limits and cost constraints.

In a Retrieval-Augmented Generation (RAG) system, the naive approach is:

- Retrieve top-k chunks
- Concatenate them
- Send everything to the LLM

This approach introduces several issues:

- Token overflow errors
- High operational costs
- Context noise
- Decreased answer quality
- Lack of control over retrieval precision

The project goal includes:

- Token efficiency
- Cost-awareness
- Production-ready design
- Explicit control over LLM context

Therefore, a simple retrieval pipeline is insufficient.

---

## Decision

We introduce a dedicated **Token Optimization Strategy Layer** inside the Core layer.

This layer is mandatory for all LLM calls.

### Responsibilities

The Token Optimization Strategy Layer must:

- Dynamically adjust top-k retrieval
- Apply similarity score threshold filtering
- Trim context based on token budget
- Control conversation history window
- Reduce redundant or low-relevance chunks

No LLM call is allowed without passing through this layer.

---

## Architectural Placement

The Token Optimization Strategy Layer resides in the **Core Layer**, not in Infrastructure.

Flow:

User Query  
→ Embedding  
→ Similarity Search  
→ Token Optimization Strategy  
→ Token Budget Estimator  
→ Prompt Builder  
→ LLM

This ensures separation between retrieval mechanics and token governance.

---

## Alternatives Considered

### 1. Static top-k Retrieval

- Simple implementation
- No adaptive behavior
- Higher risk of token overflow
- Poor cost control

### 2. Rely on LLM Truncation

- Delegate trimming to model
- No explicit control
- Non-deterministic behavior
- Reduced engineering transparency

### 3. Framework-Managed Context (LangChain Default)

- Faster setup
- Reduced architectural visibility
- Harder to customize deeply

---

## Consequences

### Positive

- Explicit cost control
- Improved retrieval precision
- Reduced token waste
- Better scalability
- Clear engineering responsibility
- Differentiated portfolio-level architecture

### Negative

- Increased implementation complexity
- Additional abstraction layer
- Requires testing and tuning

---

## Notes

This ADR formalizes token efficiency as a first-class architectural concern.

The Token Optimization Strategy Layer is a structural component of the system, not an optional enhancement.

Any future changes to retrieval or prompt construction must respect this architectural constraint.