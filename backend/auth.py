import bcrypt
from backend.db import cursor


def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return None

    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user
    return None
