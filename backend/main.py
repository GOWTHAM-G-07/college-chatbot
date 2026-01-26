from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import login_user
from backend.ai_search import add_text, search_docs, delete_doc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "College Chatbot API is running"}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = login_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.post("/admin/upload")
async def upload(file: UploadFile = File(...)):
    content = (await file.read()).decode(errors="ignore")
    add_text(file.filename, content)
    return {"message": "Uploaded"}

@app.post("/admin/delete")
def delete(document_id: int = Form(...)):
    delete_doc(document_id)
    return {"message": "Deleted"}

@app.post("/search")
def search(query: str = Form(...)):
    return search_docs(query)
