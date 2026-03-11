import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.documents import upload_document
from backend.search import search_docs
from backend.admin import list_documents, delete_document
from fastapi import FastAPI
from backend.auth import router as auth_router
app = FastAPI()
app.include_router(auth_router, prefix="/auth")
# -----------------------------
# CORS FIX (Important)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Serve frontend
# -----------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"status": "College Chatbot Backend Running"}

# -----------------------------
# Login
# -----------------------------
@app.post("/login")
def login(data: dict):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    result = authenticate(email, password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid login")

    return result


# -----------------------------
# Upload Document
# -----------------------------
@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        return upload_document(title, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# List Documents
# -----------------------------
@app.get("/admin/docs")
def get_docs():
    try:
        return list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Delete Document
# -----------------------------
@app.delete("/admin/delete/{doc_id}")
def remove_doc(doc_id: int):
    try:
        delete_document(doc_id)
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Chat
# -----------------------------
@app.post("/chat")
def chat(data: dict):

    question = data.get("question")
    mode = data.get("mode", "doc")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    # DOCUMENT MODE
    if mode == "doc":
        answer = search_docs(question)

    # AI MODE
    elif mode == "ai":
        from backend.ai_mode import ai_answer
        answer = ai_answer(question)

    else:
        answer = "Invalid mode"

    return {"answer": answer}
# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )