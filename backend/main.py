from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.db import conn, cursor
from backend.auth import login_user
from backend.ai_search import add_text, search
from fastapi import Form, HTTPException
import os
from backend.db import cursor, conn

import os
from pypdf import PdfReader

app = FastAPI()
# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.get("/")
def home():
    return {"status": "College Chatbot API is running"}

# LOGIN
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = login_user(email, password)
    if not user:
        return {"error": "Invalid credentials"}
    return {
        "name": user["name"],
        "role": user["role"]
    }

# ADMIN UPLOAD
@app.post("/admin/upload")
def upload(title: str = Form(...), file: UploadFile = Form(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())

    reader = PdfReader(path)
    for page in reader.pages:
        add_text(page.extract_text())

    cursor.execute(
        "INSERT INTO documents (title, subject, file_path, uploaded_by) VALUES (%s,%s,%s,%s)",
        (title, "General", path, 1)
    )
    conn.commit()

    return {"status": "uploaded"}

# SEARCH (STUDENT)
@app.post("/search")
def search_docs(query: str = Form(...)):
    results = search(query)
    return {"results": results}
@app.get("/admin/docs")
def list_docs():
    cursor.execute("SELECT id, title FROM documents")
    return cursor.fetchall()
@app.post("/admin/delete")
def delete_doc(doc_id: int = Form(...)):
    cursor.execute("SELECT filename FROM documents WHERE id=%s", (doc_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = f"backend/uploads/{row[0]}"
    if os.path.exists(file_path):
        os.remove(file_path)

    cursor.execute("DELETE FROM documents WHERE id=%s", (doc_id,))
    conn.commit()

    return {"status": "deleted"}
