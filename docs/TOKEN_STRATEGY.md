# Token Optimization Strategy

## Goals
- Reduce unnecessary context
- Improve cost efficiency
- Maintain answer quality

## Strategies

- Dynamic top-k retrieval
- Similarity score threshold
- Context trimming based on token budget
- Sliding window for conversation history
- Output token reservation

## Design Rule

Every LLM call must pass through:
Token Budget Estimator → Context Builder → Prompt Builder