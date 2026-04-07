from backend.db import get_connection
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
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
    name: str = None   # ✅ ADD THIS LINE
    email: str
    password: str
    role: str = "user"
class UserCreate(BaseModel):
    name: str | None = None
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
# -----------------------------
# Role Permission Helper
# -----------------------------
def require_role(user, allowed_roles):

    role = user.get("role")

    # 🔥 Leader inherits admin permissions
    if role == "leader" and "admin" in allowed_roles:
        return

    if role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )


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
    "access_token": token,
    "token": token,
    "role": role,
    "email": user.email   # 🔥 ADD THIS LINE
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
# LIST USERS (FROM DATABASE)
# -----------------------------
@router.get("/admin/users")
def get_users(user=Depends(verify_token)):

    role = user.get("role")

    if role not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, email, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return users

@router.post("/admin/add-user")
def add_user(new_user: UserCreate, user=Depends(verify_token)):

    role = user.get("role")

    # 👑 LEADER → FULL CONTROL
    if role == "leader":
        pass

    # 👨‍💼 ADMIN → ONLY USER
    elif role == "admin":
        if new_user.role != "user":
            raise HTTPException(
                status_code=403,
                detail="Admin can only create users"
            )

    else:
        raise HTTPException(status_code=403, detail="Not allowed")

    # -----------------------------
    # NAME GENERATION
    # -----------------------------
    name = new_user.name
    if not name:
        import re
        prefix = new_user.email.split("@")[0]
        prefix = re.sub(r'\d+', '', prefix)
        prefix = re.sub(r'[^a-zA-Z]', '', prefix)
        name = prefix if prefix else "user"

    # -----------------------------
    # HASH PASSWORD
    # -----------------------------
    hashed = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

    # -----------------------------
    # INSERT INTO DB (🔥 FIXED)
    # -----------------------------
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s,%s,%s,%s)",
            (name, new_user.email, hashed, new_user.role)   # ✅ FIX
        )
        conn.commit()

    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))

    conn.close()

    return {"msg": "User added successfully"}


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

    role = user.get("role")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT role FROM users WHERE email=%s", (email,))
    target = cursor.fetchone()

    if not target:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    target_role = target["role"]

    # 👨‍💼 ADMIN RULES
    if role == "admin":
        if target_role in ["admin", "leader"]:
            conn.close()
            raise HTTPException(
                status_code=403,
                detail="Admin cannot delete admin or leader"
            )

    # 👑 LEADER RULES
    elif role == "leader":
        if target_role == "leader":
            conn.close()
            raise HTTPException(
                status_code=403,
                detail="Leader cannot delete another leader"
            )

    else:
        conn.close()
        raise HTTPException(status_code=403, detail="Not allowed")

    # ❗ SELF DELETE BLOCK
    if email == user["email"]:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )

    cursor.execute("DELETE FROM users WHERE email=%s", (email,))
    conn.commit()
    conn.close()

    return {"msg": "User deleted successfully"}
#------------------------------------------------------
#-------------------------------------------------------
@router.get("/leader/stats")
def get_stats(user=Depends(verify_token)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔢 TOTAL MEMBERS (all roles)
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total = cursor.fetchone()["total"]

    # 👤 USERS (students)
    cursor.execute("SELECT COUNT(*) AS users FROM users WHERE role='user'")
    users = cursor.fetchone()["users"]

    # 🛡️ ADMINS
    cursor.execute("SELECT COUNT(*) AS admins FROM users WHERE role='admin'")
    admins = cursor.fetchone()["admins"]

    # 👑 LEADERS
    cursor.execute("SELECT COUNT(*) AS leaders FROM users WHERE role='leader'")
    leaders = cursor.fetchone()["leaders"]

    cursor.close()
    conn.close()

    return {
        "total": total,
        "users": users,
        "admins": admins,
        "leaders": leaders
    }
@router.put("/leader/update-role")
def update_role(data: dict, user=Depends(verify_token)):

    # 🔐 Only leader allowed
    if user["role"] != "leader":
        raise HTTPException(status_code=403, detail="Only leader can change roles")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET role=%s WHERE email=%s",
        (data["role"], data["email"])
    )

    conn.commit()   # 🔥 VERY IMPORTANT

    cursor.close()
    conn.close()

    return {"message": "Role updated"}