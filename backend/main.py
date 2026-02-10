from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.documents import upload_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root():
    return {"status": "College Chatbot API running"}

@app.post("/admin/upload")
async def admin_upload(
    title: str = Form(...),
    file: UploadFile = Form(...)
):
    return upload_document(title, file)
