Overview

Semantic PDF RAG CLI is a clean-architecture Python application designed to:
	•	Ingest PDF documents
	•	Chunk and embed content
	•	Store vectors in PostgreSQL + pgVector
	•	Perform semantic search
	•	Execute Retrieval-Augmented Generation (RAG)
	•	Apply structured Prompt Engineering
	•	Enforce Token Optimization and Budget Control
	•	Operate in a provider-agnostic manner (OpenAI / Gemini)

This project was built as a professional-grade portfolio system, following modern AI architecture practices.

Key Architectural Principles
	•	Clean Architecture
	•	Ports & Adapters
	•	Provider-agnostic LLM integration
	•	Token Optimization Strategy Layer
	•	Explicit Token Budget Estimation
	•	Structured Prompt Layer
	•	Testable and extensible design
	•	CLI-first workflow

Architecture

app/
    use_cases/
    prompting/
    token_optimization/
    services/

core/
    ports/

domain/
    entities/
    value_objects/

infrastructure/
    database/
    vector_store/
    embeddings/
    llm/

RAG Flow 
User Query
   ↓
Embedding
   ↓
Vector Search (pgVector + HNSW)
   ↓
Token Optimization Layer
   - dynamic top_k
   - similarity threshold
   - context compression
   - history control
   - token budget enforcement
   ↓
Prompt Architecture Layer
   - structured prompt sections
   - guardrails
   - minimal verbosity
   ↓
LLM (provider-agnostic)
   ↓
Response

Token Governance

This system includes an explicit Token Optimization Strategy Layer responsible for:
	•	Context pruning
	•	Dynamic top-k retrieval
	•	Redundancy removal
	•	Context compression
	•	Sliding window history
	•	Prompt minimalism

Token Budget Estimation

Before every LLM call:
	•	Token usage is estimated
	•	Maximum budget is enforced
	•	Context is dynamically reduced if necessary
	•	Reserved response tokens are guaranteed

This ensures:
	•	Predictable cost
	•	Reduced latency
	•	Production readiness

⸻

Prompt Architecture
Prompt structure is explicitly layered:
[ SYSTEM ]
[ INSTRUCTION ]
[ CONTEXT ]
[ USER QUERY ]

Techniques applied:
	•	Structured prompting
	•	Instruction anchoring
	•	Context isolation
	•	Anti-hallucination guidance
	•	Minimal verbosity control
	•	Optional ReAct-style reasoning

Tech Stack
	•	Python 3.11+
	•	PostgreSQL
	•	pgVector
	•	HNSW index
	•	LangChain (optional abstraction)
	•	Pydantic (configuration + models)
	•	pytest
	•	Docker
	•	OpenAI or Gemini embeddings
	•	Provider-agnostic LLM interface

CLI Commands (Planned)
semantic-rag ingest path/to/file.pdf
semantic-rag chat
semantic-rag reindex
semantic-rag stats

Differentiators
	•	Explicit token governance
	•	Clean architecture with ports
	•	Production-like design
	•	Cost-aware RAG
	•	Extensible strategy layers
	•	Enterprise-ready structure

Project Goals
	•	Demonstrate applied AI architecture knowledge
	•	Showcase scalable RAG design
	•	Exhibit cost-awareness and token control
	•	Build a portfolio-ready AI engineering system