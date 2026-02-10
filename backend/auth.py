import bcrypt
import jwt
from backend.db import get_connection

SECRET = "college_secret"

def authenticate(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, email, password_hash, role FROM users WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return None

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return None

    # ✅ Create JWT token (KEEPING YOUR FEATURE)
    token = jwt.encode(
        {"id": user["id"], "email": user["email"], "role": user["role"]},
        SECRET,
        algorithm="HS256"
    )

    return {
        "token": token,
        "role": user["role"]
    }
