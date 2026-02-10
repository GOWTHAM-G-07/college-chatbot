from PyPDF2 import PdfReader
from backend.db import cursor, conn
from backend.vector_store import rebuild_index

def upload_pdf(title, file):
    reader = PdfReader(file)
    text = "".join(p.extract_text() or "" for p in reader.pages)

    cursor.execute(
        "INSERT INTO documents (title, content) VALUES (%s,%s)",
        (title, text)
    )
    conn.commit()
    rebuild_index()

def delete_doc(doc_id):
    cursor.execute("DELETE FROM documents WHERE id=%s", (doc_id,))
    conn.commit()
    rebuild_index()
