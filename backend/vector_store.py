import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.db import get_connection

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Vector dimension
dimension = 384

# FAISS index
index = faiss.IndexFlatL2(dimension)

# store texts linked to vectors
documents = []


def rebuild_index():
    """Rebuild FAISS index from database on startup"""
    global documents, index

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, content FROM documents")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    documents = rows
    index.reset()

    if rows:
        texts = [r["content"] for r in rows]

        embeddings = model.encode(texts)

        embeddings = np.array(embeddings).astype("float32")

        index.add(embeddings)


def add_vectors(vectors, texts):
    """Add vectors dynamically when new documents are uploaded"""
    global documents, index

    vectors = np.array(vectors).astype("float32")

    index.add(vectors)

    for text in texts:
        documents.append({"content": text})


def semantic_search(query):
    """Search FAISS index"""
    if not documents:
        return None

    q_vec = model.encode([query])
    q_vec = np.array(q_vec).astype("float32")

    distances, indices = index.search(q_vec, 1)

    return documents[indices[0][0]]["content"]