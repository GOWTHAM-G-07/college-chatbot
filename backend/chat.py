from fastapi import APIRouter, Depends, HTTPException
from backend.auth import verify_token
from backend.db import get_connection

router = APIRouter()

# -----------------------------
# CHAT API
# -----------------------------
@router.post("/chat")
def chat(data:dict, user=Depends(verify_token)):

    question = data.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    # Dummy AI answer (replace with your AI / vector search)
    answer = f"Answer for: {question}"

    # Save chat history
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO chat_history(user_email,query,response)
    VALUES(%s,%s,%s)
    """,
    (user["email"],question,answer)
    )

    conn.commit()
    conn.close()

    return {"answer":answer}
#-----------------------------------
#---chat history
#-----------------------------------
@router.get("/admin/chat-history")
def get_chat_history(user=Depends(verify_token)):

    if user["role"] not in ["admin","leader"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    "SELECT * FROM chat_history ORDER BY created_at DESC"
    )

    history = cursor.fetchall()

    conn.close()

    return history