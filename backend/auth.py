from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import bcrypt
import jwt
import re
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "college_chatbot_secret"
ALGORITHM = "HS256"

# temporary database (replace with MySQL later)
users_db = {}

class User(BaseModel):
    email: str
    password: str


# Email validation
def validate_email(email: str):

    pattern = r'^[a-zA-Z0-9._%+-]+aids@dgct\.ac\.in$'

    if not re.match(pattern, email):
        raise HTTPException(
            status_code=403,
            detail="Only AIDS department emails are allowed"
        )


# Register user
@router.post("/register")
def register(user: User):

    validate_email(user.email)

    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    users_db[user.email] = hashed

    return {"message": "User registered successfully"}


# Login user
@router.post("/login")
def login(user: User):

    validate_email(user.email)

    if user.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = users_db[user.email]

    if not bcrypt.checkpw(user.password.encode(), stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    payload = {
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "message": "Login successful",
        "token": token
    }


# Token verification
def verify_token(authorization: str = Header(...)):

    try:
        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload["email"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Protected route
@router.get("/dashboard")
def dashboard(email: str = Depends(verify_token)):

    return {
        "message": f"Welcome {email}",
        "access": "AIDS Department Portal"
    }