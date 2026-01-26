from backend.db import cursor
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
doc_ids = []
index = None


def load_documents():
    global documents, doc_ids, index

    cursor.execute("""
        SELECT id, title, subject, file_path
        FROM documents
    """)
    rows = cursor.fetchall()

    documents = []
    doc_ids = []

    for row in rows:
        doc_id, title, subject, file_path = row
        text = f"Title: {title}\nSubject: {subject}\nPath: {file_path}"
        documents.append(text)
        doc_ids.append(doc_id)

    if documents:
        embeddings = model.encode(documents)
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings))
    else:
        index = None


def add_text(doc_id, title, subject, file_path):
    global index

    text = f"Title: {title}\nSubject: {subject}\nPath: {file_path}"
    embedding = model.encode([text])

    documents.append(text)
    doc_ids.append(doc_id)

    if index is None:
        index = faiss.IndexFlatL2(len(embedding[0]))
    index.add(np.array(embedding))


def search_docs(query):
    if not index:
        return []

    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding), 5)

    results = []
    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results


def delete_doc(doc_id):
    cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
    load_documents()


# Load documents at startup
load_documents()
