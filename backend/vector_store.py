import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.db import get_connection
import PyPDF2

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

index = faiss.IndexFlatL2(dimension)

documents = []


def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def rebuild_index():
    global documents, index

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔥 read from uploaded files
    cursor.execute("SELECT id, file_path FROM documents")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    documents = []
    index.reset()

    all_chunks = []

    for doc in rows:
        text = read_pdf(doc["file_path"])

        # simple chunking
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        for chunk in chunks:
            documents.append({"content": chunk})
            all_chunks.append(chunk)

    if all_chunks:
        embeddings = model.encode(all_chunks)
        embeddings = np.array(embeddings).astype("float32")
        index.add(embeddings)


def semantic_search(query, k=3):
    D, I = index.search(query_embedding, k)

    results = []
    for i in I[0]:
        results.append(chunks[i])

    return results
def add_vectors(vectors, texts):
    """Add new document vectors dynamically"""
    global documents, index

    import numpy as np

    vectors = np.array(vectors).astype("float32")

    index.add(vectors)

    for text in texts:
        documents.append({"content": text})