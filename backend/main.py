import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.auth import router as auth_router, verify_token
from backend.chat import router as chat_router
from backend.documents import router as documents_router
from backend.dashboard import router as dashboard_router
from backend.users import router as users_router
from backend.vector_store import rebuild_index
from backend.search import search_docs
from dotenv import load_dotenv
from backend.llm import generate_answer
from backend.vector_store import semantic_search
load_dotenv()

app = FastAPI()

# -----------------------------
# Startup: Load FAISS index
# -----------------------------
#@app.on_event("startup")
#def startup_event():
 #   rebuild_index()


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
# Routers
# -----------------------------
app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router)
app.include_router(documents_router)   # 🔥 contains upload/docs/delete
app.include_router(dashboard_router)
app.include_router(users_router)

# -----------------------------
# Static Files
# -----------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 🔥 SERVE UPLOADED FILES
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"status": "College Chatbot Backend Running"}


# -----------------------------
# Chat (AI + Document Mode)
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