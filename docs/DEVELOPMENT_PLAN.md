# Development Plan

## Planning Conventions

- Status values for phases: `Not Started`, `In Progress`, `Done`
- Primary dependency source: `requirements.txt`
- Optional modernization: `pyproject.toml` (without changing current workflow)

## Phase 1 – Foundation (Architecture & Environment)

**Status:** `Done`

### Objectives
- Establish Clean Architecture structure
- Configure development environment
- Define domain contracts (Ports)

### Key Tasks
- Create folder structure: domain, core, infra, cli, tests
- Configure Docker (PostgreSQL + pgVector)
- Configure environment variables (.env)
- Setup dependency management with requirements.txt (pyproject.toml optional)
- Define base Pydantic models
- Define Domain Ports:
  - VectorStorePort
  - EmbeddingPort
  - LLMPort

### Deliverables
- Running PostgreSQL container
- Project boots without runtime errors
- Domain layer independent from infrastructure
- CLI entrypoint operational for initial commands

### Exit Criteria
- No infrastructure imports inside domain
- Docker environment fully operational

### Validation Checkpoint
- `docker compose up -d`
- `python -m pytest -q`

---

## Phase 2 – PDF Ingestion & Vector Storage

**Status:** `Done`

### Objectives
- Implement ingestion pipeline
- Store embeddings in pgVector

### Key Tasks
- Implement PDF loader adapter
- Implement chunking (1000 size / 200 overlap)
- Implement embedding provider adapter
- Implement PgVectorRepository
- Configure HNSW index

### Deliverables
- CLI command: ingest <file>
- Embeddings stored in PostgreSQL
- HNSW index active

### Exit Criteria
- Stored content retrievable via similarity search

### Validation Checkpoint
- `semantic-rag ingest <file>` (or equivalent Typer command)
- Verify rows in `documents` table with non-null embeddings

## Phase 3 – LangChain Integration (Framework Transition)

**Status:** `In Progress`

### Objectives
- Pivot custom infrastructure to LangChain ecosystem
- Satisfy mandatory technical challenge requirement

### Key Tasks
- Refactor `OpenAIEmbedding` to `langchain-openai` embeddings
- Refactor `PgVectorStore` to utilize `langchain-postgres`
- Implement LangChain PromptTemplates
- Establish LangChain as the core orchestrator interface

### Deliverables
- Fully operational LangChain document ingestion
- Re-architected infrastructure adapters

### Exit Criteria
- System operates using LangChain mechanics natively without custom SQL vectors

### Validation Checkpoint
- `semantic-rag ingest` successfully uses `langchain-postgres`
- Pytest integration tests pass with LangChain mock objects

---

## Phase 4 – Semantic Search & CLI

**Status:** `Not Started`

### Objectives
- Implement retrieval pipeline via LangChain
- Enable user querying

### Key Tasks
- Implement Query embedding via LangChain
- Implement VectorStore retrieval logic
- Implement CLI command: chat
- Connect retrieval to basic LangChain RAG pipeline

### Deliverables
- End-to-end retrieval working via CLI
- Relevant chunks dynamically retrieved

### Exit Criteria
- User can query ingested documents via Terminal chat successfully

### Validation Checkpoint
- `semantic-rag chat`
- Query returns LangChain retrieved chunks and final LLM response

---

## Phase 5 – Prompt Layer

**Status:** `Not Started`

### Objectives
- Standardize LLM interaction
- Structure prompts deterministically

### Key Tasks
- Configure robust LangChain `PromptTemplate`
- Separate system and user prompts
- Implement structured context formatting

### Deliverables
- Deterministic LLM invocation flow

### Exit Criteria
- LLM receives well-structured and consistent formatting

### Validation Checkpoint
- Inspect LangChain tracer / logs for consistent prompt formats
- Same input produces same prompt structure

---

## Phase 6 – Token Optimization Strategy Layer

**Status:** `Not Started`

### Objectives
- Improve cost-efficiency
- Optimize retrieval precision before calling LLM

### Key Tasks
- Implement dynamic top-k adjustment
- Implement similarity threshold filtering
- Implement context trimming

### Deliverables
- TokenOptimizationStrategy Component
- Measurable token reduction

### Exit Criteria
- Reduced token payload compared to naive RAG

### Validation Checkpoint
- Log pre-optimization and post-optimization token counts

---

## Phase 7 – Token Budget Estimator

**Status:** `Not Started`

### Objectives
- Prevent Token Limit Overflow issues
- Enforce strict adherence to Context Window Limits

### Key Tasks
- Reserve output tokens dynamically
- Enforce maximum input token bounds
- Implement fallback reduction strategy (truncation)

### Deliverables
- Safe LLM invocation wrapper over LangChain chain

### Exit Criteria
- Application never crashes due to Context Window limits

### Validation Checkpoint
- Provide a massive query and verify correct token rejection or reduction

---

## Phase 8 – Professional Polish & Production Mindset

**Status:** `Not Started`

### Objectives
- Elevate system to portfolio-level quality

### Key Tasks
- Add structured logging
- Increase test coverage
- Final check of Clean Architecture boundaries

### Deliverables
- Clean, documented, production-ready project

### Exit Criteria
- Project ready for portfolio presentation

### Validation Checkpoint
- Typer CLI flows beautifully without generic exceptions

---

## Continuous Practices (All Phases)

- Respect Clean Architecture dependency rule
- Keep classes small and single-responsibility
- Write tests for core logic
- Avoid business logic inside infrastructure
- Maintain provider-agnostic design
- Optimize tokens consciously before every LLM call

---

## Final Goal

Deliver a professional, extensible, token-efficient RAG system demonstrating:

- Architectural thinking
- LLM systems understanding
- Cost awareness
- Production-ready mindset

This document is the official execution roadmap for the project.