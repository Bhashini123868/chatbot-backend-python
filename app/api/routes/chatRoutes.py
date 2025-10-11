from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.agent import get_answer
from app.db.connection import get_db

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_question(q: Question, db=Depends(get_db)):
    answer = get_answer(q.question)
    return {"answer": answer}