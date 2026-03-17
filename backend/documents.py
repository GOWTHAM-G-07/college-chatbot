import os
import pdfplumber
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from backend.db import get_connection

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Upload Document
# -----------------------------
@router.post("/upload")
async def upload_document(title: str, file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = ""

    with pdfplumber.open(file_location) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO documents (title,file_path,content)
        VALUES (%s,%s,%s)
        """,
        (title, file_location, text),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Document uploaded successfully"}


# -----------------------------
# List Documents
# -----------------------------
@router.get("/admin/docs")
def list_documents():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
        id,
        title,
        file_path,
        SUBSTRING_INDEX(file_path,'/',-1) AS filename
        FROM documents
        ORDER BY id DESC
        """
    )

    docs = cursor.fetchall()

    cursor.close()
    conn.close()

    return docs


# -----------------------------
# Delete Document
# -----------------------------
@router.delete("/delete/{doc_id}")
def delete_document(doc_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT file_path FROM documents WHERE id=%s",
        (doc_id,),
    )

    doc = cursor.fetchone()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = doc[0]

    if os.path.exists(file_path):
        os.remove(file_path)

    cursor.execute(
        "DELETE FROM documents WHERE id=%s",
        (doc_id,),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Document deleted successfully"}


# -----------------------------
# Download Document
# -----------------------------
@router.get("/download/{doc_id}")
def download_document(doc_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT file_path FROM documents WHERE id=%s",
        (doc_id,),
    )

    doc = cursor.fetchone()

    cursor.close()
    conn.close()

    if not doc:
        raise HTTPException(status_code=404)

    return FileResponse(doc["file_path"])


# -----------------------------
# Preview Document
# -----------------------------
@router.get("/preview/{doc_id}")
def preview_document(doc_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT file_path FROM documents WHERE id=%s",
        (doc_id,),
    )

    doc = cursor.fetchone()

    cursor.close()
    conn.close()

    if not doc:
        raise HTTPException(status_code=404)

    return FileResponse(doc["file_path"])