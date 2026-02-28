# RAG Flow

User question
→ Generate query embedding (via LangChain Embeddings)
→ Similarity search in pgVector (via `langchain-postgres`)
→ Retrieve top-k chunks
→ Apply threshold filter (via `ContextualCompressionRetriever`)
→ Apply LCEL transformation stages (via `RunnableLambda`)
→ Apply token optimization (via `ConversationTokenBufferMemory`)
→ Estimate effective token budget
→ Evaluate summarization gate (`retrieved_tokens > 1.2 * budget`)
→ (Optional) Summarize compressed context to `70–80%` of budget and preserve top-1/top-2 raw chunks
→ Build prompt (via LangChain `PromptTemplate`)
→ Call LLM (via LangChain Chat Models)
→ Return response