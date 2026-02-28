# Token Optimization Strategy

## Goals
- Reduce unnecessary context
- Improve cost efficiency
- Maintain answer quality

## Strategies

- Dynamic top-k retrieval (via LangChain Retrievers)
- Similarity score threshold (via `ContextualCompressionRetriever`)
- Context trimming based on token budget
- Sliding window for conversation history (via `ConversationTokenBufferMemory`)
- Output token reservation
- LCEL transformation stages (via `RunnableLambda`) for deterministic context shaping
- Optional summarization of oversized retrieved context before final prompt assembly

## Summarization Gate Policy (Future Implementation)

- Summarization is optional and only activated under budget pressure
- Effective budget formula:
	- `budget = context_window - prompt_fixed - output_reserve(20%) - safety_margin(10%)`
- Activation threshold:
	- summarize only when `retrieved_tokens > 1.2 * budget`
- Compression target:
	- summarized context should fit within `70–80%` of `budget`
- Fidelity guardrail:
	- keep top-1/top-2 most similar chunks in original form for answer grounding

## Design Rule

Every LLM call must pass through LangChain constructs incorporating:
Contextual Compression → LCEL Transformations (`RunnableLambda`) → Token Buffer Memory → Prompt Template