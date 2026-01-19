from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Interview

router = APIRouter()

QUESTIONS = [
    "Introduce yourself",
    "Explain your last project",
    "What is Python used for?",
    "Explain SQL joins",
    "What is REST API?",
    "Explain Docker",
    "Explain system design",
    "Any questions for us?"
]

index = 0

@router.get("/next")
def next_question():
    global index
    if index >= len(QUESTIONS):
        return {"done": True}

    q = QUESTIONS[index]
    index += 1
    return {"text": q, "audio": ""}
