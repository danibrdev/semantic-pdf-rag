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

---

## Phase 3 – Semantic Search & CLI

**Status:** `In Progress`

### Objectives
- Implement retrieval pipeline
- Enable user querying

### Key Tasks
- Implement query embedding
- Implement similarity_search logic
- Implement CLI command: chat
- Connect retrieval to basic RAG pipeline

### Deliverables
- End-to-end retrieval working
- Relevant chunks returned

### Exit Criteria
- User can query ingested documents successfully

### Validation Checkpoint
- `semantic-rag chat`
- Query returns retrieved chunks and final response without runtime errors

---

## Phase 4 – Prompt Layer

**Status:** `Not Started`

### Objectives
- Standardize LLM interaction
- Structure prompts deterministically

### Key Tasks
- Implement PromptBuilder
- Separate system and user prompts
- Implement structured context formatting
- Ensure provider-agnostic prompt structure

### Deliverables
- Structured prompt object
- Deterministic LLM invocation flow

### Exit Criteria
- LLM receives well-structured and consistent prompts

### Validation Checkpoint
- Prompt object includes deterministic sections (`system`, `context`, `user`)
- Same input produces same prompt structure

---

## Phase 5 – Token Optimization Strategy Layer

**Status:** `Not Started`

### Objectives
- Improve cost-efficiency
- Optimize retrieval precision

### Key Tasks
- Implement dynamic top-k adjustment
- Implement similarity threshold filtering
- Implement context trimming
- Implement conversation history window control

### Deliverables
- TokenOptimizationStrategy component
- Measurable token reduction

### Exit Criteria
- Reduced token usage without significant quality loss

### Validation Checkpoint
- Compare baseline vs optimized token counts on same query set
- Optimization does not drop all relevant chunks

---

## Phase 6 – Token Budget Estimator

**Status:** `Not Started`

### Objectives
- Prevent token overflow
- Enforce safe LLM calls

### Key Tasks
- Implement token counting mechanism
- Reserve output tokens
- Enforce maximum context size
- Implement fallback reduction strategy

### Deliverables
- TokenBudgetEstimator component
- Safe LLM invocation wrapper

### Exit Criteria
- No token limit runtime errors

### Validation Checkpoint
- Calls near context limit execute safely
- Overflow scenario triggers fallback reduction strategy

---

## Phase 7 – Professional Polish & Production Mindset

**Status:** `Not Started`

### Objectives
- Elevate system to portfolio-level quality

### Key Tasks
- Add structured logging
- Add metrics collection
- Implement Economic and Deep execution modes
- Increase pytest coverage (core prioritized)
- Add benchmarking script
- Improve README documentation

### Deliverables
- Test coverage > 70% in core layer
- Benchmark results documented
- Clean and documented repository

### Exit Criteria
- Architecture consistent with ARCHITECTURE.md
- Project ready for portfolio publication

### Validation Checkpoint
- Core-focused test coverage target reached
- README and ADRs aligned with implemented structure (`cli/core/domain/infra`)

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