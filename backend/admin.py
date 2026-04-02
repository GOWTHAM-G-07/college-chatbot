from backend.db import get_connection


def list_documents():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, file_path FROM documents")

    docs = cursor.fetchall()

    cursor.close()
    conn.close()

    return docs