# Mandatory System Explanations

This document explains key design decisions, observed limitations, and metrics tracked during the development of the Retrieval-Augmented Generation (RAG) system.

---

## 1. Chunk Size Selection Rationale

We selected a chunk size of **500 characters with an overlap of 50 characters**.

### Reasoning:
- Smaller chunks (e.g., 100–200 characters) often lack sufficient semantic context, leading to incomplete or ambiguous retrieval results.
- Larger chunks (e.g., >1000 characters) reduce retrieval precision, as embeddings may represent multiple unrelated concepts.
- A 500-character chunk size provides a balance between semantic completeness and embedding specificity.
- The 50-character overlap ensures that important contextual information at chunk boundaries is preserved, reducing the risk of losing key sentences during splitting.

This strategy improved retrieval quality while keeping embedding and storage costs manageable.

---

## 2. Observed Retrieval Failure Case

### Failure Scenario:
A retrieval failure was observed when a user query required **cross-document or multi-chunk reasoning**.

### Example:
A question that depended on information split across multiple documents or distant sections of a single document sometimes returned only partially relevant chunks. Since similarity search ranks chunks independently, related but semantically weaker chunks were occasionally excluded from the top-k results.

### Root Cause:
- Vector similarity search optimizes for local semantic similarity rather than global document-level reasoning.
- The system does not currently perform chunk re-ranking or document-level aggregation.

### Mitigation (Future Improvement):
- Increase top-k retrieval size followed by re-ranking.
- Introduce hybrid search (semantic + keyword).
- Apply multi-step retrieval or chunk grouping by document source.

---

## 3. Metric Tracked: End-to-End Latency

We tracked **end-to-end query latency**, measured from the moment a question is received to the generation of the final answer.

### Observations:
- Average retrieval latency (FAISS similarity search): ~20–30 ms
- Average LLM inference latency (Groq Llama 3): ~250–350 ms
- Total average response time: ~300–400 ms

### Importance:
Latency is a critical metric for real-world API usability. Using Groq significantly reduced inference time compared to traditional hosted LLM APIs, making the system more responsive for interactive use cases.

---

## 4. Background Ingestion Justification

Document ingestion (chunking and embedding) is executed as a background task.

### Reasoning:
- Embedding generation is computationally expensive.
- Running ingestion synchronously would block API requests and degrade user experience.
- Background tasks allow the system to scale ingestion independently from query handling.

This design aligns with production-grade API practices.

---

## 5. LLM Selection Rationale (Groq)

We used **Groq-hosted Llama 3** models for answer generation.

### Reasons:
- Extremely low inference latency.
- Cost-effective and developer-friendly.
- Suitable context window (8k tokens) for RAG-based prompts.

This choice directly supports our latency optimization goals.

---

## Summary

The system demonstrates a practical and scalable implementation of Retrieval-Augmented Generation, with careful consideration given to chunking strategy, retrieval quality, performance metrics, and API design. While the current system handles single-hop retrieval effectively, future improvements can further enhance multi-document reasoning and retrieval robustness.
