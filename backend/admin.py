from backend.db import get_connection


def list_documents():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, filename FROM documents")

    docs = cursor.fetchall()

    cursor.close()
    conn.close()

    return docs


def delete_document(doc_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM documents WHERE id=%s",
        (doc_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()