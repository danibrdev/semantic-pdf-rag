# RAG Flow

User question
→ Generate query embedding
→ Similarity search in pgVector
→ Retrieve top-k chunks
→ Apply threshold filter
→ Apply token optimization
→ Build prompt
→ Call LLM
→ Return response