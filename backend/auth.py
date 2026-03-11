from fastapi import APIRouter, HTTPException, Depends, Header
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
users_db = {}
chat_logs = []
user_activity = []

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
# Token Verification
# -----------------------------
def verify_token(authorization: str = Header(...)):

    try:

        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


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
# Login
# -----------------------------
@router.post("/login")
def login(user: User):

    validate_email(user.email)

    if user.email not in users_db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    stored_password = users_db[user.email]["password"]

    if not bcrypt.checkpw(
        user.password.encode(),
        stored_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    role = users_db[user.email]["role"]

    payload = {
        "email": user.email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    users_db[user.email]["last_login"] = datetime.utcnow()

    user_activity.append({
        "email": user.email,
        "action": "login",
        "time": datetime.utcnow()
    })

    return {
        "message": "Login successful",
        "token": token,
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

    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403)

    total_users = len(users_db)
    total_queries = len(chat_logs)

    active_users = 0

    for u in users_db.values():
        if u["last_login"]:
            active_users += 1

    inactive_users = total_users - active_users

    user_search_count = {}

    for log in chat_logs:
        email = log["email"]
        user_search_count[email] = user_search_count.get(email, 0) + 1

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "total_queries": total_queries,
        "search_activity": user_search_count
    }


# -----------------------------
# Chat History
# -----------------------------
@router.get("/admin/chat-history")
def chat_history(user=Depends(verify_token)):

    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403)

    return chat_logs


# -----------------------------
# List Users
# -----------------------------
@router.get("/admin/users")
def list_users(user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    users_list = []

    for email, data in users_db.items():

        users_list.append({
            "email": email,
            "role": data["role"],
            "last_login": data["last_login"]
        })

    return users_list


# -----------------------------
# Add User (Admin Only)
# -----------------------------
@router.post("/admin/add-user")
def add_user(new_user: User, user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    validate_email(new_user.email)

    hashed = bcrypt.hashpw(
        new_user.password.encode(),
        bcrypt.gensalt()
    )

    users_db[new_user.email] = {
        "password": hashed,
        "role": new_user.role,
        "created_at": datetime.utcnow(),
        "last_login": None
    }

    return {"message": "User added successfully"}


# -----------------------------
# Remove User
# -----------------------------
@router.delete("/admin/remove-user/{email}")
def remove_user(email: str, user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    if email not in users_db:
        raise HTTPException(status_code=404)

    del users_db[email]

    return {"message": "User removed successfully"}