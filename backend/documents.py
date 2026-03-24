from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from backend.auth import verify_token
from backend.db import get_connection
import os
import bcrypt

router = APIRouter(prefix="/admin")


# -----------------------------
# UPLOAD DOCUMENT
# -----------------------------
@router.post("/upload")
def upload_doc(
    file: UploadFile = File(...),
    title: str = Form(...),
    user=Depends(verify_token)
):

    # 🔒 Only admin / leader
    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="Access denied")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    # ✅ Ensure folder exists
    os.makedirs("uploads", exist_ok=True)

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents(title, file_path) VALUES(%s,%s)",
        (title, filepath)
    )

    conn.commit()
    conn.close()

    return {"msg": "Uploaded successfully"}


# -----------------------------
# GET DOCUMENTS
# -----------------------------
@router.get("/docs")
def get_docs(user=Depends(verify_token)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM documents ORDER BY id DESC")

    docs = cursor.fetchall()

    conn.close()

    return docs


# -----------------------------
# ADD USER
# -----------------------------
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

    # 🔐 Hash password
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