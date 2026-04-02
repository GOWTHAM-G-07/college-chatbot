from fastapi import APIRouter, Depends, HTTPException
from backend.auth import verify_token
from backend.db import get_connection
import bcrypt

router = APIRouter(prefix="/admin")


@router.post("/add-user")
def add_user(data: dict, user=Depends(verify_token)):

    # 🔒 Only admin
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add users")

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing fields")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(email,password,role) VALUES(%s,%s,%s)",
        (email, hashed, role)
    )

    conn.commit()
    conn.close()

    return {"msg": "User added successfully"}