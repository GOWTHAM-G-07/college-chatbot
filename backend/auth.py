import bcrypt
from backend.db import cursor

def login_user(email, password):
    cursor.execute(
        "SELECT id,name,email,password_hash,role FROM users WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        return None

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return None

    return user
