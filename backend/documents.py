import os
import pdfplumber
from backend.db import get_connection
from backend.utils.text_chunker import clean_text, chunk_text
from backend.services.embedding_service import create_embeddings
from backend.vector_store import add_vectors


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_document(title, file):

    # Save uploaded file
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Extract text from PDF
    text = ""

    with pdfplumber.open(file_location) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Clean text
    text = clean_text(text)

    # Split into chunks
    chunks = chunk_text(text, chunk_size=400)

    # Generate embeddings
    embeddings = create_embeddings(chunks)

    # Store in database
    conn = get_connection()
    cursor = conn.cursor()

    # Insert document
    doc_query = """
    INSERT INTO documents
    (filename, title, subject, file_path, uploaded_by, content)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(doc_query, (
        file.filename,
        title,
        "general",
        file_location,
        1,
        text
    ))

    document_id = cursor.lastrowid

    # Store chunks
    chunk_query = """
    INSERT INTO document_chunks
    (document_id, chunk_text)
    VALUES (%s,%s)
    """

    for chunk in chunks:
        cursor.execute(chunk_query, (document_id, chunk))

    conn.commit()

    cursor.close()
    conn.close()

    # Add vectors to FAISS index
    add_vectors(embeddings, chunks)

    return {
        "message": "Document uploaded successfully",
        "chunks_created": len(chunks)
    }