import os
from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.documents import upload_document
from backend.search import search_docs
from backend.admin import list_documents, delete_document
from backend.auth import router as auth_router
from backend.auth import verify_token
from backend.vector_store import rebuild_index

app = FastAPI()

# -----------------------------
# Load FAISS index on startup
# -----------------------------
@app.on_event("startup")
def startup_event():
    rebuild_index()


# -----------------------------
# Auth Router
# -----------------------------
app.include_router(auth_router, prefix="/auth")


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# Upload Document (Admin only)
# -----------------------------
@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...),
    user=Depends(verify_token)
):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return upload_document(title, file)


# -----------------------------
# List Documents
# -----------------------------
@app.get("/admin/docs")
def get_docs(user=Depends(verify_token)):

    if user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403)

    return list_documents()


# -----------------------------
# Delete Document
# -----------------------------
@app.delete("/admin/delete/{doc_id}")
def remove_doc(doc_id: int, user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    delete_document(doc_id)

    return {"message": "Deleted successfully"}


# -----------------------------
# Chat
# -----------------------------
@app.post("/chat")
def chat(data: dict, user=Depends(verify_token)):

    question = data.get("question")
    mode = data.get("mode", "doc")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    if mode == "doc":
        answer = search_docs(question)

    elif mode == "ai":
        from backend.ai_mode import ai_answer
        answer = ai_answer(question)

    else:
        answer = "Invalid mode"

    return {
        "answer": answer,
        "user": user["email"]
    }


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