import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from rag_engine import load_document, query_rag

load_dotenv()

app = FastAPI(title="RAG Q&A API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "RAG Q&A API is running!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or TXT file to be indexed"""
    allowed = [".pdf", ".txt"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files allowed")

    # Save uploaded file temporarily
    save_path = f"./uploaded_{file.filename}"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Load into vector DB
    num_chunks = load_document(save_path)
    os.remove(save_path)  # clean up

    return {
        "message": f"Document indexed successfully",
        "filename": file.filename,
        "chunks_created": num_chunks
    }

@app.post("/ask")
def ask_question(body: QuestionRequest):
    """Ask a question about the uploaded document"""
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer = query_rag(body.question)
    return {
        "question": body.question,
        "answer": answer
    }