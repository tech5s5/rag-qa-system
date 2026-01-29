from sentence_transformers import SentenceTransformer
from app.vectorstore import load_index
from groq import Groq
import os

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Groq client (API key via env variable)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def answer_question(question: str):
    index, metadata = load_index()
    if index is None or len(metadata) == 0:
        return "No documents uploaded yet."

    # Embed user query
    query_emb = model.encode([question])

    # Similarity search
    distances, indices = index.search(query_emb, k=3)

    # Build context from retrieved chunks
    context = "\n".join([metadata[i] for i in indices[0]])

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below minimum 50 words.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""

    # Groq LLM call
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return completion.choices[0].message.content.strip()
