import os
from fastapi import APIRouter, Depends, HTTPException
from backend.auth import verify_token
from backend.db import get_connection
from groq import Groq

router = APIRouter()

# ✅ Secure API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# CHAT API
# -----------------------------
@router.post("/chat")
def chat(data: dict, user=Depends(verify_token)):

    question = data.get("question")
    mode = data.get("mode", "doc")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # 🧠 AI MODE
    # =========================
    if mode == "ai":

        # 🔒 LIMIT ONLY AI USAGE
        cursor.execute(
            "SELECT COUNT(*) FROM chat_history WHERE user_email=%s AND mode='ai'",
            (user["email"],)
        )
        usage = cursor.fetchone()[0]

        if usage >= 50:
            conn.close()
            return {"answer": "⚠️ AI usage limit reached. Try later."}

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful college assistant."},
                    {"role": "user", "content": question}
                ]
            )

            answer = response.choices[0].message.content

        except Exception as e:
            print("AI ERROR:", e)
            answer = "⚠️ AI service temporarily unavailable"

    # =========================
    # 📄 DOCUMENT MODE
    # =========================
    else:
        answer = f"Answer for: {question}"


    # =========================
    # SAVE CHAT HISTORY
    # =========================
    cursor.execute(
        """
        INSERT INTO chat_history(user_email, query, response, mode)
        VALUES(%s, %s, %s, %s)
        """,
        (user["email"], question, answer, mode)
    )

    conn.commit()
    conn.close()

    return {"answer": answer}


# -----------------------------------
# CHAT HISTORY
# -----------------------------------
@router.get("/admin/chat-history")
def get_chat_history(user=Depends(verify_token)):

    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM chat_history ORDER BY created_at DESC"
    )

    history = cursor.fetchall()

    conn.close()

    return history