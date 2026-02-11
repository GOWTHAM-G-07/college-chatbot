from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import backend modules (backend folder must be inside api/)
from backend.documents import upload_document
from backend.search import search_docs
from backend.admin import list_documents, delete_document
from backend.auth import authenticate

app = FastAPI()

# ------------------- CORS -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- STATIC FILES -------------------
# Serves frontend files if needed
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ------------------- ROOT -------------------
@app.get("/")
def root():
    return {"status": "College Chatbot API running"}

# ------------------- LOGIN -------------------
@app.post("/login")
def login(data: dict):
    if "email" not in data or "password" not in data:
        raise HTTPException(status_code=400, detail="Missing email or password")

    result = authenticate(data["email"], data["password"])

    if not result:
        raise HTTPException(status_code=401, detail="Invalid login")

    return result


# ------------------- ADMIN ROUTES -------------------
@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        return upload_document(title, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/docs")
def get_docs():
    try:
        return list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/admin/delete/{doc_id}")
def remove_doc(doc_id: int):
    try:
        delete_document(doc_id)
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------- CHAT -------------------
@app.post("/chat")
async def chat(data: dict):
    question = data.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        answer = search_docs(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
