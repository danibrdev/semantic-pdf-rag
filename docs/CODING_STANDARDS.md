# Coding Standards

- Type hints mandatory (public APIs, ports, adapters, use cases)
- Pydantic models for DTOs and settings validation
- Small, single-responsibility classes
- No business logic inside infrastructure
- Test every core component
- Avoid hard-coded values
- Prefer composition root for dependency wiring (single bootstrap point)
- Keep provider-agnostic contracts in domain/core

## Python Quality Baseline

- Follow PEP 8 and keep naming explicit and consistent
- Favor pure functions for deterministic business rules when possible
- Avoid mutable default arguments and hidden side effects
- Raise domain-meaningful exceptions (never swallow infrastructure errors silently)
- Prefer explicit imports and avoid wildcard imports
- Keep modules cohesive (one clear responsibility per module)
- Use context managers for external resources (files, DB cursors, network clients)
- Avoid import-time side effects that execute I/O or load secrets eagerly

## Clean Architecture Rules (Mandatory)

- Dependency rule must be respected: dependencies point inward only
- `domain` must not import `core`, `infra`, or CLI modules
- `core` must depend only on `domain` abstractions
- `infra` implements ports and can depend on external libraries
- CLI/presentation layer orchestrates use cases, never domain rules
- Ports and adapters signatures must remain contract-compatible

## LangChain & AI Standards

- Use LangChain primitives through adapters, not directly inside domain
- Prefer LCEL composition for pipelines (`RunnableSequence` / pipe syntax)
- Use focused `RunnableLambda` transformations (single concern per step)
- Prompt templates must be centralized and versionable
- Keep retrieval and generation concerns separated (retriever vs prompt/LLM)
- Chunking strategy must be standardized via LangChain Text Splitters (1000/200 unless explicitly changed)
- Any summarization must be conditional and budget-driven (not always-on)

## Token Governance Standards

- Every LLM invocation must pass through token budget checks
- Apply optimization before generation: top-k, threshold, trimming, then optional summarization
- Keep deterministic gating rules for summarization activation
- Reserve output tokens explicitly and track effective context budget
- Log token metrics before and after optimization
  
# Clean Code Guidelines

## Naming
- Clear and descriptive names
- Avoid abbreviations

## Functions
- Small and focused
- Max 30 lines recommended
- Public functions should have precise docstrings when behavior is non-trivial
- Avoid boolean-flag overloads; prefer small composable functions

## Classes
- Single responsibility
- Inject dependencies via constructor
- Avoid service god-classes; split orchestration from transformation logic

## Errors
- Use custom exceptions in domain
- Do not expose infrastructure errors directly
- Fail fast on invalid configuration (`Settings`) during startup
- Preserve error context with actionable messages

## Testing
- Core logic must be unit tested
- Infrastructure must be integration tested
- Add contract tests for ports/adapters compatibility
- For AI flows, test deterministic parts (prompt/context assembly, gating decisions)
- Mock external providers in unit tests; keep provider calls for integration/e2e only
- New features must include at least one test covering success path and one edge case

## Logging
- No print statements
- Use structured logging
- Include correlation context when possible (command/use-case/document)
- Never log secrets, API keys, or full sensitive payloads

## Configuration & Secrets

- All runtime config must come from `Settings` / environment variables
- No direct access to `.env` outside settings layer
- Never hardcode credentials, model keys, or database passwords
- Keep safe defaults explicit and documented
- Validate config bounds/invariants (e.g., token reserves, thresholds, top-k limits)
- Never instantiate global settings objects that fail at import time

## Persistence & Vector Store

- Schema/index initialization must be idempotent
- Keep vector dimension consistent with active embedding model
- Use migrations/controlled DDL changes for production evolution
- Similarity semantics (distance vs score) must be explicit in code and docs
- Enforce DB connection timeout and statement timeout
- Prefer SSL/TLS DB connections outside local development
- Always rollback on DB exceptions before retrying/propagating

## Input Validation & Ingestion Safety

- Validate file path existence and extension before parsing
- Enforce maximum file size/page limits for PDF ingestion
- Handle parser failures gracefully with actionable errors
- Reject suspicious or unsupported payloads without crashing the process

## Dependency & Supply Chain Security

- Pin dependency versions for reproducible and safer builds
- Run periodic vulnerability scanning (`pip-audit` or equivalent)
- Upgrade dependencies with changelog review and targeted regression tests

## Documentation Standards

- Keep docs aligned with implementation status (Done/In Progress/Not Started)
- When architecture changes, update at least: `ARCHITECTURE`, `DEVELOPMENT_PLAN`, `RAG_FLOW`
- Document formulas/thresholds used for token or summarization gates
- Avoid stale examples in README and CLI docs

## Git & Version Control
- All commits MUST follow the [Semantic Commits](https://www.conventionalcommits.org/) convention.
- **Format**: `<type>(<scope>): <subject>`
- **Types**:
  - `feat`: A new feature (e.g., `feat(ingest): add pdf chunking`)
  - `fix`: A bug fix (e.g., `fix(vector-store): resolve connection timeout`)
  - `docs`: Documentation changes (e.g., `docs: translate readme to pt-br`)
  - `style`: Formatting, missing semicolons, etc.
  - `refactor`: Refactoring production code (e.g., `refactor(domain): extract interface`)
  - `test`: Adding missing tests, refactoring tests
  - `chore`: Updating dependencies, build tasks, gitignore, etc.
  - `perf`: A code change that improves performance
- Include a clear description of *why* the change was made in the commit body when necessary.

## Pull Request Checklist (Mandatory)

- Architecture boundaries respected (no forbidden imports between layers)
- Contracts preserved (ports and adapters remain compatible)
- Tests added/updated and passing for impacted areas
- Docs updated when behavior, flow, or formulas changed
- No secrets or sensitive payloads introduced in code/logs