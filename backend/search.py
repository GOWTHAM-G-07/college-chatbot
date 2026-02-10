import re
from backend.db import get_connection

def tokenize(text):
    return set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))

def search_docs(question: str):
    q_tokens = tokenize(question)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, content FROM documents")
    docs = cursor.fetchall()
    conn.close()

    best_score = 0
    best_answer = "Sorry, I couldn't find an answer."

    for doc in docs:
        content = doc["content"] or ""
        c_tokens = tokenize(content)

        score = len(q_tokens & c_tokens)
        if score > best_score:
            best_score = score
            best_answer = content[:800]  # return first part

    return best_answer
