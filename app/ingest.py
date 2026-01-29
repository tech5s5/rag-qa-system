from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from app.vectorstore import save_index, load_index
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([p.extract_text() for p in reader.pages])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def ingest_document(file_path):
    text = extract_text(file_path)
    chunks = chunk_text(text)

    embeddings = model.encode(chunks)

    index, metadata = load_index()
    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)
    metadata.extend(chunks)

    save_index(index, metadata)
