from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from backend.auth import verify_token
from backend.db import get_connection
from backend.vector_store import add_vectors, model
import os
import shutil
from PyPDF2 import PdfReader

router = APIRouter(prefix="/admin")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# UPLOAD DOCUMENT
# -----------------------------
@router.post("/upload")
async def upload_doc(
    file: UploadFile = File(...),
    title: str = Form(...),
    user=Depends(verify_token)
):

    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="Access denied")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    # ✅ SAVE FILE
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ SAVE TO DATABASE
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents(title, file_path) VALUES(%s,%s)",
        (title, filepath)
    )

    conn.commit()
    conn.close()

    # ✅ FAST VECTOR ADD (NO REBUILD)
    try:
        reader = PdfReader(filepath)

        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        if chunks:
            embeddings = model.encode(chunks)
            add_vectors(embeddings, chunks)

    except Exception as e:
        print("Vector error:", e)

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