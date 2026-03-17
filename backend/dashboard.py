from fastapi import APIRouter, Depends, HTTPException
from backend.auth import verify_token
from backend.db import get_connection

router = APIRouter()

# -----------------------------
# ADD EXAM (Leader/Subleader)
# -----------------------------
@router.post("/leader/add-exam")
def add_exam(data:dict, user=Depends(verify_token)):

    if user["role"] not in ["leader","subleader"]:
        raise HTTPException(status_code=403, detail="Access denied")

    subject = data.get("subject")
    exam_date = data.get("exam_date")
    description = data.get("description")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO exam_schedule(subject,exam_date,description)
    VALUES(%s,%s,%s)
    """,
    (subject,exam_date,description)
    )

    conn.commit()
    conn.close()

    return {"message":"Exam schedule added"}
#---------------------------------------
#----------------exam-------------------------
#----------------------------------------
@router.get("/exams")
def get_exams():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    "SELECT * FROM exam_schedule ORDER BY exam_date"
    )

    exams = cursor.fetchall()

    conn.close()

    return exams