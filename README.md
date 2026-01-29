# RAG-Based Question Answering System

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** based Question Answering system that allows users to upload documents and ask questions grounded strictly in the uploaded content. The system combines semantic search using vector embeddings with large language model (LLM) generation to produce accurate, context-aware answers.

The application is built as a RESTful API using **FastAPI**, supports asynchronous document ingestion, and is optimized for low-latency inference using **Groq-hosted LLMs**.

---

## Key Features
- Upload documents in **PDF** and **TXT** formats
- Asynchronous document ingestion using background tasks
- Text chunking with overlap for improved retrieval accuracy
- Embedding generation using **Sentence Transformers**
- Vector similarity search using **FAISS**
- Retrieval-Augmented Generation with **Groq (Llama 3)**
- Request validation using **Pydantic**
- Basic API rate limiting
- Low-latency, production-style API design

---

## System Architecture
The system follows a standard RAG pipeline:

1. Documents are uploaded via an API endpoint
2. Background tasks extract text, chunk documents, and generate embeddings
3. Embeddings are stored in a FAISS vector store
4. User queries are embedded and matched against stored vectors
5. Top-k relevant chunks are retrieved and provided as context to an LLM
6. The LLM generates a grounded answer based on retrieved context

An architecture diagram is provided in the `diagrams/` directory.

---

## Tech Stack
- **Backend:** FastAPI
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store:** FAISS
- **LLM:** Groq (Llama 3)
- **Rate Limiting:** slowapi
- **Document Parsing:** PyPDF2

---
```
## Project Structure
rag-qa-system/
│
├── app/
│ ├── main.py
│ ├── api.py
│ ├── schemas.py
│ ├── ingest.py
│ ├── rag.py
│ ├── vectorstore.py
│ └── rate_limiter.py
│
├── data/
│ ├── uploads/
│ └── faiss_index/
│
├── diagrams/
│ └── architecture.png
│
├── explanation.md
├── requirements.txt
└── README.md ```
