# ADR 001 – Use pgVector for Vector Storage

## Status
Accepted

## Context
We need a vector database for storing embeddings and performing similarity search.

## Decision
We will use PostgreSQL with pgVector extension.

## Alternatives Considered
- Pinecone
- Weaviate
- FAISS (local)

## Consequences

### Positive
- Local-first architecture
- No external service dependency
- Cost-efficient

### Negative
- Manual index management
- Requires PostgreSQL setup