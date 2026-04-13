from fastapi import APIRouter, Depends, HTTPException
from backend.db import get_connection
from backend.auth import verify_token
from datetime import date

router = APIRouter(prefix="/api")


# =========================
# CREATE ANNOUNCEMENT
# =========================
@router.post("/announcements/create")
def create_announcement(data: dict, user=Depends(verify_token)):

    role = user.get("role")

    if role not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Leader → auto approve
    # Admin → pending
    status = "approved" if role == "leader" else "pending"

    title = data.get("title", "").upper()
    content = data.get("content", "")
    category = data.get("category", "General")

    if not title or not content:
        raise HTTPException(status_code=400, detail="Missing fields")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO announcements (title, content, category, date, created_by, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            title,
            content,
            category,
            date.today(),
            user.get("email"),
            status
        ))

        conn.commit()

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail="Insert failed")

    finally:
        cursor.close()
        conn.close()

    return {
        "message": "Announcement created",
        "status": status
    }


# =========================
# GET ANNOUNCEMENTS
# =========================
@router.get("/announcements")
def get_announcements(user=Depends(verify_token)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, title, content, date, status
        FROM announcements
        ORDER BY date DESC
    """)

    data = cursor.fetchall()

    # 👉 AUTO CATEGORY LOGIC (NO DB CHANGE)
    for a in data:
        text = (a["title"] + " " + a["content"]).lower()

        if "exam" in text:
            a["category"] = "exam"
        elif "event" in text:
            a["category"] = "event"
        elif "urgent" in text:
            a["category"] = "urgent"
        elif "admin" in text:
            a["category"] = "admin"
        else:
            a["category"] = "general"

    return data

# =========================
# APPROVE ANNOUNCEMENT
# =========================
@router.put("/announcements/approve/{id}")
def approve_announcement(id: int, user=Depends(verify_token)):

    if user.get("role") != "leader":
        raise HTTPException(status_code=403, detail="Only leader can approve")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE announcements SET status='approved' WHERE id=%s",
            (id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not found")

        conn.commit()

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail="Update failed")

    finally:
        cursor.close()
        conn.close()

    return {"message": "Approved successfully"}


# =========================
# DELETE (OPTIONAL)
# =========================
@router.delete("/announcements/{id}")
def delete_announcement(id: int, user=Depends(verify_token)):

    if user.get("role") not in ["admin", "leader"]:
        raise HTTPException(status_code=403)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM announcements WHERE id=%s",
            (id,)
        )
        conn.commit()

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500)

    finally:
        cursor.close()
        conn.close()

    return {"message": "Deleted"}