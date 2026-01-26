import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from backend.db import cursor, conn

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)
texts = []


def add_text(text: str, email: str):
    """
    Store document text + embed into FAISS + save metadata in MySQL
    """
    embedding = model.encode([text])
    index.add(np.array(embedding))
    texts.append(text)

    cursor.execute(
        "INSERT INTO documents (email, content) VALUES (%s, %s)",
        (email, text)
    )
    conn.commit()


def search(query: str):
    """
    Semantic search over stored documents
    """
    if len(texts) == 0:
        return []

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=3)

    results = []
    for i in indices[0]:
        if i < len(texts):
            results.append(texts[i])

    return results
