# RAG Flow

User question
→ Generate query embedding (via LangChain Embeddings)
→ Similarity search in pgVector (via `langchain-postgres`)
→ Retrieve top-k chunks
→ Apply threshold filter (via `ContextualCompressionRetriever`)
→ Apply token optimization (via `ConversationTokenBufferMemory`)
→ Build prompt (via LangChain `PromptTemplate`)
→ Call LLM (via LangChain Chat Models)
→ Return response