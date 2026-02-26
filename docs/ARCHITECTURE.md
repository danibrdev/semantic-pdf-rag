# Semantic PDF RAG CLI – Architecture

## 1. Vision

Semantic PDF RAG CLI is a production-grade, portfolio-level system designed to:

- Ingest PDF documents
- Perform semantic chunking (1000 size / 200 overlap)
- Generate embeddings using a provider-agnostic interface
- Store vectors in PostgreSQL with pgVector
- Execute high-performance similarity search (HNSW index)
- Apply Retrieval-Augmented Generation (RAG)
- Optimize token usage through a dedicated Token Optimization Strategy Layer
- Expose functionality via a professional CLI interface

The system prioritizes architectural clarity, extensibility, and token efficiency.

---

## 2. Architectural Style

The project follows:

- Clean Architecture
- Ports & Adapters (Hexagonal Architecture)
- SOLID Principles
- Provider-Agnostic Design
- Token-Efficient RAG Design

### Core Architectural Rule (Dependency Rule)

All dependencies must point inward.

- Domain does not depend on Core or Infrastructure
- Core depends only on Domain
- Infrastructure implements Domain-defined ports
- CLI depends on Core

---

## 3. Layers Definition

### 3.1 Domain Layer (Pure Business Logic)

Responsibilities:
- Core business models
- Domain entities
- Value objects
- Interfaces (Ports)
- Custom domain exceptions

Constraints:
- No external libraries
- No database logic
- No LLM provider logic
- Fully testable in isolation

Examples:
- DocumentChunk
- QueryRequest
- VectorRepositoryPort
- EmbeddingProviderPort
- LLMProviderPort

---

### 3.2 Core Layer (Application Logic)

Responsibilities:
- RAG orchestration
- Token Optimization Strategy Layer
- Token Budget Estimator
- Context builder
- Prompt builder
- Dynamic retrieval logic (dynamic top-k, threshold filtering)

This layer coordinates the system but does not implement infrastructure.

Subcomponents:

#### Token Optimization Strategy Layer (Mandatory)
- Dynamic top-k adjustment via LangChain Retrievers
- Similarity threshold filtering via `ContextualCompressionRetriever`
- Context trimming via LangChain Document Compressors
- Conversation window control via `ConversationTokenBufferMemory`

#### Token Budget Estimator (Mandatory)
- Pre-LLM token estimation via LangChain generic tokenizers (e.g. tiktoken integration)
- Output token reservation
- Context reduction when limits exceeded natively via Memory constraints

---

### 3.3 Infrastructure Layer (Adapters)

Responsibilities:
- PostgreSQL + pgVector implementation
- HNSW index configuration
- Embedding provider adapters (OpenAI / Gemini)
- LLM provider adapters
- PDF loader implementation
- CLI implementation (Typer)
- Logging and metrics integration

This layer implements the ports defined in Domain.

Patterns used:
- Adapter Pattern (external services)
- Factory Pattern (provider selection)
- Repository Pattern (vector storage)

---

## 4. RAG Execution Flow

User Question
→ Generate query embedding
→ Similarity search (pgVector + HNSW)
→ Retrieve top-k chunks
→ Apply similarity threshold
→ Apply token optimization
→ Estimate token budget
→ Build structured prompt
→ Call LLM
→ Return response

All LLM calls must pass through:
Token Budget Estimator → Context Builder → Prompt Builder

---

## 5. Design Patterns Applied

- Ports & Adapters (Hexagonal)
- Repository Pattern (Vector storage)
- Strategy Pattern (Token Optimization)
- Factory Pattern (Provider selection)
- Dependency Injection via constructor
- Provider-Agnostic abstraction

---

## 6. Non-Functional Requirements

- Token efficiency prioritized
- Provider-agnostic LLM integration
- Modular and testable
- Replaceable embedding and LLM providers
- Clean code and SOLID compliance
- Structured logging (no print statements)
- High cohesion and low coupling
- Small, single-responsibility classes

---

## 7. Technical Stack

- Python 3.11+
- PostgreSQL
- pgVector (with HNSW index)
- SQLAlchemy
- Pydantic
- Typer (CLI)
- pytest
- Docker
- LangChain (Core Orchestrator / Mandatory)

---

## 8. Operational Modes (Future Extension)

The architecture must support multiple execution modes:

- Economic Mode (strict token limits, aggressive trimming)
- Deep Mode (higher context allowance)
- Benchmark Mode (metrics collection)

Modes must be configurable without modifying domain logic.

---

## 9. Architectural Goals

- Portfolio-level engineering quality
- Clear separation of concerns
- Replaceable infrastructure components
- Explicit token optimization strategy
- Production-readiness mindset
- Clean extensible design

This document serves as the architectural contract for the project.