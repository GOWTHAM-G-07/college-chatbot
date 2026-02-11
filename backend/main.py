import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import your modules
from documents import upload_document
from search import search_docs
from admin import list_documents, delete_document
from auth import authenticate

app = FastAPI()

# ----------------------------------------------------
# CORS (IMPORTANT – allow Vercel frontend)
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://college-chatbot.vercel.app",  # Replace with your Vercel URL
        "http://localhost:3000"  # for local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# ROOT
# ----------------------------------------------------
@app.get("/")
def root():
    return {"status": "College Chatbot Backend Running on Render"}

# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------
@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    result = authenticate(email, password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return result


# ----------------------------------------------------
# ADMIN: Upload Document
# ----------------------------------------------------
@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        return upload_document(title, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
# ADMIN: List Documents
# ----------------------------------------------------
@app.get("/admin/docs")
def get_docs():
    try:
        return list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
# ADMIN: Delete Document
# ----------------------------------------------------
@app.delete("/admin/delete/{doc_id}")
def remove_doc(doc_id: int):
    try:
        delete_document(doc_id)
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
# CHAT
# ----------------------------------------------------
@app.post("/chat")
def chat(data: dict):
    question = data.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        answer = search_docs(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
# Render requires PORT binding
# ----------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )
