from backend.db import get_connection

def search_docs(query: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, content FROM documents")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # simple keyword matching
    query_words = set(query.lower().split())
    results = []

    for row in rows:
        content_words = set(row["content"].lower().split())
        score = len(query_words & content_words)
        if score > 0:
            results.append({
                "id": row["id"],
                "title": row["title"],
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
