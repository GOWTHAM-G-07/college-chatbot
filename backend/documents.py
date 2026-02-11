from fastapi import UploadFile, HTTPException
import os
import PyPDF2
from db import get_connection


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_document(title: str, file: UploadFile, uploaded_by: int = 1):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    reader = PyPDF2.PdfReader(path)
    content = ""
    for page in reader.pages:
        content += page.extract_text() or ""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (filename, title, subject, file_path, uploaded_by, content)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        file.filename,
        title,
        title,
        path,
        uploaded_by,
        content
    ))

    conn.commit()
    conn.close()

    return {"message": "Uploaded successfully"}
