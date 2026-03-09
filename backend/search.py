import re
from backend.db import get_connection


def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())


def search_docs(question):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT content FROM documents")
    docs = cursor.fetchall()

    if not docs:
        return "No documents uploaded."

    question_tokens = tokenize(question)

    results = []

    for doc in docs:

        content = doc["content"]

        paragraphs = content.split("\n")

        for para in paragraphs:

            tokens = tokenize(para)

            score = sum(tokens.count(word) for word in question_tokens)

            if score > 0 and len(para) > 40:
                results.append((score, para))

    cursor.close()
    conn.close()

    if not results:
        return "Answer not found in uploaded documents."

    # sort by relevance
    results.sort(reverse=True)

    # take top 5 relevant paragraphs
    best_paragraphs = [para for score, para in results[:5]]

    return "\n\n".join(best_paragraphs)