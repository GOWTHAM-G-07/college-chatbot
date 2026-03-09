import os
import pdfplumber
from backend.db import get_connection


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_document(title, file):

    # save file
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # extract text
    text = ""

    with pdfplumber.open(file_location) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # connect database
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO documents
    (filename, title, subject, file_path, uploaded_by, content)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        file.filename,
        title,
        "general",
        file_location,
        1,
        text
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Document uploaded successfully"}