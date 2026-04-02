from backend.db import get_connection
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi import Request
from pydantic import BaseModel
import bcrypt
import jwt
import re
from datetime import datetime, timedelta
router = APIRouter()

SECRET_KEY = "college_chatbot_secret"
ALGORITHM = "HS256"

# -----------------------------
# In-memory storage
# -----------------------------
users_db = {

"leader@aids.dgct.ac.in":{
"password":bcrypt.hashpw("123456".encode(),bcrypt.gensalt()),
"role":"leader",
"created_at":datetime.utcnow(),
"last_login":None
},

"subleader@aids.dgct.ac.in":{
"password":bcrypt.hashpw("123456".encode(),bcrypt.gensalt()),
"role":"subleader",
"created_at":datetime.utcnow(),
"last_login":None
},

"admin@aids.dgct.ac.in":{
"password":bcrypt.hashpw("123456".encode(),bcrypt.gensalt()),
"role":"admin",
"created_at":datetime.utcnow(),
"last_login":None
}

}

chat_logs = []
user_activity = []

# -----------------------------
# Default Leader & Subleader
# -----------------------------
leader_email = "gowthamgowtham59133@gmail.com"
leader_password = bcrypt.hashpw("123456789".encode(), bcrypt.gensalt())

users_db[leader_email] = {
    "password": leader_password,
    "role": "leader",
    "created_at": datetime.utcnow(),
    "last_login": None
}

subleader_email = "gowthamstudy59133@gmail.com"
subleader_password = bcrypt.hashpw("123456789".encode(), bcrypt.gensalt())

users_db[subleader_email] = {
    "password": subleader_password,
    "role": "subleader",
    "created_at": datetime.utcnow(),
    "last_login": None
}

# -----------------------------
# Models
# -----------------------------
class User(BaseModel):
    email: str
    password: str
    role: str = "user"


class ChatQuery(BaseModel):
    query: str


# -----------------------------
# Email Validation
# -----------------------------
def validate_email(email: str):

    pattern = r'^[a-zA-Z0-9._%+-]+@aids\.dgct\.ac\.in$'

    if not re.match(pattern, email):
        raise HTTPException(
            status_code=403,
            detail="Only AIDS department emails allowed"
        )


# -----------------------------
# Token Verification (🔥 FIXED SAFE VERSION)
# -------------------------

from fastapi import Request

def verify_token(request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
# -----------------------------
# Role Permission Helper
# -----------------------------
def require_role(user, allowed_roles):
    if user["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")


# -----------------------------
# Register
# -----------------------------
@router.post("/register")
def register(user: User):

    validate_email(user.email)

    if user.role in ["admin", "leader"]:
        raise HTTPException(
            status_code=403,
            detail="Cannot assign privileged role"
        )

    if user.email in users_db:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    )

    users_db[user.email] = {
        "password": hashed,
        "role": "user",
        "created_at": datetime.utcnow(),
        "last_login": None
    }

    return {"message": "User registered successfully"}


# -----------------------------
# Login (🔥 ONLY FIX HERE)
# -----------------------------
@router.post("/login")
def login(user: User):

    validate_email(user.email)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT email,password_hash,role FROM users WHERE email=%s",
        (user.email,)
    )

    db_user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = db_user["password_hash"]

    if isinstance(stored_password, str):
        stored_password = stored_password.encode()

    if not bcrypt.checkpw(user.password.encode(), stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    role = db_user["role"]

    payload = {
        "email": user.email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "message": "Login successful",
        "access_token": token,   # 🔥 FIXED (IMPORTANT)
        "token": token,          # 🔥 KEEP OLD FOR COMPATIBILITY
        "role": role
    }


# -----------------------------
# Chat Endpoint
# -----------------------------
@router.post("/chat")
def chat(data: ChatQuery, user=Depends(verify_token)):

    email = user["email"]

    response = f"Answer for: {data.query}"

    chat_logs.append({
        "email": email,
        "query": data.query,
        "response": response,
        "time": datetime.utcnow()
    })

    user_activity.append({
        "email": email,
        "action": "chat",
        "query": data.query,
        "time": datetime.utcnow()
    })

    return {"response": response}


# -----------------------------
# Leader Dashboard
# -----------------------------
@router.get("/leader/dashboard")
def leader_dashboard(user=Depends(verify_token)):

    require_role(user, ["admin", "leader"])

    total_users = len(users_db)
    total_queries = len(chat_logs)

    active_users = sum(1 for u in users_db.values() if u["last_login"])

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "total_queries": total_queries
    }


# -----------------------------
# Chat History
# -----------------------------
@router.get("/admin/chat-history")
def chat_history(user=Depends(verify_token)):

    require_role(user, ["admin", "leader"])

    return chat_logs


# -----------------------------
# List Users
# -----------------------------
@router.get("/admin/users")
def list_users(user=Depends(verify_token)):

    require_role(user, ["admin"])

    return [
        {
            "email": email,
            "role": data["role"],
            "last_login": data["last_login"]
        }
        for email, data in users_db.items()
    ]


# -----------------------------
# Add User (Admin Only)
# -----------------------------
@router.post("/auth/admin/add-user")
def add_user(new_user: User, user=Depends(verify_token)):

    require_role(user, ["admin"])

    if new_user.role != "user":
        raise HTTPException(
            status_code=403,
            detail="Admin can only create normal users"
        )

    hashed = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

    users_db[new_user.email] = {
        "password": hashed,
        "role": "user",
        "created_at": datetime.utcnow(),
        "last_login": None
    }

    return {"message": "User added by admin"}


# -----------------------------
# Leader Add User
# -----------------------------
@router.post("/leader/add-user")
def leader_add_user(new_user: User, user=Depends(verify_token)):

    require_role(user, ["leader"])

    validate_email(new_user.email)

    if new_user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

    users_db[new_user.email] = {
        "password": hashed,
        "role": new_user.role,
        "created_at": datetime.utcnow(),
        "last_login": None
    }

    return {"message": "User added by leader successfully"}


# -----------------------------
# Assign Subleader
# -----------------------------
@router.post("/leader/assign-subleader/{email}")
def assign_subleader(email: str, user=Depends(verify_token)):

    require_role(user, ["leader"])

    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    users_db[email]["role"] = "subleader"

    return {"message": f"{email} promoted to subleader"}


# -----------------------------
# Remove User
# -----------------------------
@router.delete("/admin/remove-user/{email}")
def remove_user(email: str, user=Depends(verify_token)):

    require_role(user, ["admin"])

    if email not in users_db:
        raise HTTPException(status_code=404)

    if users_db[email]["role"] in ["leader", "subleader"]:
        raise HTTPException(
            status_code=403,
            detail="Admin cannot remove leader or subleader"
        )

    del users_db[email]

    return {"message": "User removed successfully"}