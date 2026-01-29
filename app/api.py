from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.ingest import ingest_document
from app.schema import QuestionRequest, QuestionResponse
from app.rag import answer_question
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    os.makedirs("data/uploads", exist_ok=True)
    file_path = f"data/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(ingest_document, file_path)

    return {"message": "Document ingestion started in background"}

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest):
    answer = answer_question(payload.question)
    return {"answer": answer}
