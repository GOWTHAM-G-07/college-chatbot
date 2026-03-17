from fastapi import APIRouter, Depends
from backend.auth import verify_token, require_role
from backend.db import get_connection

router = APIRouter()

@router.get("/leader/analytics")
def analytics(user=Depends(verify_token)):

    require_role(user,["leader","subleader"])

    conn=get_connection()
    cursor=conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM users")
    users=cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as chats FROM chat_history")
    chats=cursor.fetchone()

    cursor.execute("SELECT user_email,COUNT(*) as queries FROM chat_history GROUP BY user_email")
    usage=cursor.fetchall()

    conn.close()

    return {
        "total_users":users["total"],
        "total_queries":chats["chats"],
        "usage":usage
    }