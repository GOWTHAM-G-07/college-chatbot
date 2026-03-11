import faiss
import numpy as np
import os
import pickle

dimension = 384

INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_metadata.pkl"


# Load or create index
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else:
    index = faiss.IndexFlatL2(dimension)


# Load metadata
if os.path.exists(META_FILE):
    with open(META_FILE, "rb") as f:
        metadata = pickle.load(f)
else:
    metadata = []


def save_index():
    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)


def add_vectors(vectors, texts):

    global metadata

    vectors = np.array(vectors).astype("float32")

    index.add(vectors)

    metadata.extend(texts)

    save_index()


def search_vectors(query_vector, top_k=5):

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for i in indices[0]:
        if i < len(metadata):
            results.append(metadata[i])

    return results