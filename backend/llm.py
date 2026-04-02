from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful college assistant.

Answer the question using ONLY the context below.
If answer is not found, say "Not available in documents".

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
