from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.documents import upload_document
from backend.search import search_docs
from backend.admin import list_documents, delete_document
from backend.auth import authenticate

app = FastAPI()

# ---------- LOGIN ----------
@app.post("/login")
def login(data: dict):
    result = authenticate(data["email"], data["password"])
    if not result:
        return {"error": "Invalid login"}

    return result  # returns token + role

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------- STATIC ----------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ---------- ROOT ----------
@app.get("/")
def root():
    return {"status": "College Chatbot API running"}

# ---------- ADMIN ----------
@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    return upload_document(title, file)

@app.get("/admin/docs")
def get_docs():
    return list_documents()

@app.delete("/admin/delete/{doc_id}")
def remove_doc(doc_id: int):
    delete_document(doc_id)
    return {"message": "Deleted successfully"}

# ---------- CHAT ----------
@app.post("/chat")
async def chat(data: dict):
    question = data.get("question")
    answer = search_docs(question)
    return {"answer": answer}
if __name__ == "__main__":
    uvicorn.run(app, ...)
