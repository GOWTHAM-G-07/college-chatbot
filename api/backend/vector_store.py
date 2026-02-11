import faiss
from sentence_transformers import SentenceTransformer
from backend.db import cursor

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
documents = []

def rebuild_index():
    global documents, index
    cursor.execute("SELECT id, content FROM documents")
    rows = cursor.fetchall()
    documents = rows
    index.reset()

    if rows:
        embeddings = model.encode([r["content"] for r in rows])
        index.add(embeddings)

def semantic_search(query):
    if not documents:
        return None

    q_vec = model.encode([query])
    D, I = index.search(q_vec, 1)
    return documents[I[0][0]]["content"]
