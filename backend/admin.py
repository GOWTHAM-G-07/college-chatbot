from db import get_connection

import os

def list_documents():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title FROM documents")
    data = cursor.fetchall()
    conn.close()
    return data

def delete_document(doc_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT file_path FROM documents WHERE id=%s", (doc_id,))
    row = cursor.fetchone()

    if row and os.path.exists(row["file_path"]):
        os.remove(row["file_path"])

    cursor.execute("DELETE FROM documents WHERE id=%s", (doc_id,))
    conn.commit()
    conn.close()
