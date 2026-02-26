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

## Design Rule

Every LLM call must pass through LangChain constructs incorporating:
Contextual Compression → Token Buffer Memory → Prompt Template